import logging
from gettext import gettext as _

from contribution.models import Premium, PayTypeChoices
from core.models import Officer
from django.db import connection
from django.db.models import OuterRef, Sum, Q, Max
from insuree.models import Insuree
from location.apps import LocationConfig
from payment.apps import PaymentConfig
from payment.models import Payment, PaymentDetail
from policy.apps import PolicyConfig
from policy.models import Policy
from policy.services import update_insuree_policies
from policy.values import policy_values, set_start_date, set_expiry_date
from product.models import Product

logger = logging.getLogger(__file__)


def set_payment_deleted(payment):
    try:
        for pd in payment.payment_details.filter(validity_to__isnull=True):
            pd.delete_history()
        payment.delete_history()
        return []
    except Exception as exc:
        logger.debug("Exception when deleting payment %s", payment.uuid, exc_info=exc)
        return {
            'title': payment.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_delete_payment") % {'uuid': payment.uuid},
                'detail': payment.uuid}]
        }


def detach_payment_detail(payment_detail):
    try:
        payment_detail.save_history()
        payment_detail.premium = None
        payment_detail.save()
        return []
    except Exception as exc:
        return [{
            'title': payment_detail.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_detach_payment_detail") % {'payment_detail': str(payment_detail)},
                'detail': payment_detail.uuid}]
        }]


def reset_payment_before_update(payment):
    payment.expected_amount = None
    payment.received_amount = None
    payment.officer_code = None
    payment.phone_number = None
    payment.request_date = None
    payment.received_date = None
    payment.status = None
    payment.transaction_no = None
    payment.origin = None
    payment.matched_date = None
    payment.receipt_no = None
    payment.payment_date = None
    payment.rejected_reason = None
    payment.date_last_sms = None
    payment.language_name = None
    payment.type_of_payment = None
    payment.transfer_fee = None


def update_or_create_payment(data, user):
    if "client_mutation_id" in data:
        data.pop('client_mutation_id')
    if "client_mutation_label" in data:
        data.pop('client_mutation_label')
    from core import datetime
    now = datetime.datetime.now()
    # No audit here
    # data['audit_user_id'] = user.id_for_audit
    data.pop("rejected_reason", None)
    data['validity_from'] = now
    payment_uuid = data.pop("uuid") if "uuid" in data else None
    if payment_uuid:
        payment = Payment.objects.get(uuid=payment_uuid)
        payment.save_history()
        reset_payment_before_update(payment)
        [setattr(payment, k, v) for k, v in data.items()]
        payment.save()
    else:
        payment = Payment.objects.create(**data)
    return payment


def update_or_create_payment_detail(payment, premium_uuid, user):
    premium = Premium.filter_queryset()\
        .filter(uuid=premium_uuid)\
        .select_related("policy__family__head_insuree")\
        .select_related("policy__product")\
        .filter(policy__validity_to__isnull=True)\
        .filter(policy__product__validity_to__isnull=True)\
        .filter(policy__family__validity_to__isnull=True)\
        .filter(policy__family__head_insuree__validity_to__isnull=True)\
        .values("id",
                "amount",
                "policy__stage",
                "policy__enroll_date",
                "policy__family__head_insuree__chf_id",
                "policy__product__code")\
        .first()
    payment_detail, _ = PaymentDetail.objects.update_or_create(
        payment=payment, premium_id=premium["id"],
        defaults=dict(
            audit_user_id=user.id_for_audit,
            amount=payment.received_amount,
            product_code=premium["policy__product__code"],
            insurance_number=premium["policy__family__head_insuree__chf_id"],
            policy_stage=premium["policy__stage"],
            enrollment_date=premium["policy__enroll_date"],
            expected_amount=premium["amount"],
        )
    )
    return payment_detail


def legacy_match_payment(payment_id=None, audit_user_id=-1):
    with connection.cursor() as cur:
        sql = """
            SET NOCOUNT ON;
            DECLARE @ret int;
            EXEC @ret = [dbo].[uspMatchPayment] @PaymentID = %s, @AuditUserId = %s;
            SELECT @ret;
        """
        cur.execute(sql, (payment_id, audit_user_id,))

        if cur.description is None:  # 0 is considered as 'no result' by pyodbc
            res = None
        else:
            info = cur.fetchall()  # FETCH 'SELECT @ret' returned value
            logger.info("matchPayment result: %s", info)
        if cur.nextset() and cur.description:
            res = cur.fetchone()[0]
        if res:
            raise Exception(res)


def match_payment(payment_id=None, payment=None, audit_user_id=None):
    if payment is None:
        payment = Payment.filter_queryset().get(id=payment_id)

    payment_details = payment.payment_details.filter(validity_to__isnull=True)

    valid_pd = []
    # validation
    for pd in payment_details:
        errors = validate_payment_detail(pd)
        if len(errors) > 0:
            continue
        valid_pd.append(pd)

        assign_payment_detail(pd, audit_user_id)

    # Only update the policy status for self payer renew (stage R, no officer)
    # contribution without payment (Stage N status READY with officer)
    # PolicyID and phone number required in both cases
    should_update_policy = any((
                (pd.policy_stage == Policy.STAGE_RENEWED and pd.payment.officer_code is None)
                or (pd.policy.status == Policy.STATUS_READY
                    and pd.policy_stage == Policy.STAGE_NEW
                    and pd.payment.officer_code is not None)
                and pd.payment.phone_number is not None
                and pd.policy is not None)
            for pd in valid_pd)

    if should_update_policy:
        processed = {}
        for pd in valid_pd:
            # recompute policy value for renewal
            new_policy, warnings = policy_values(pd.policy, pd.insuree.family, pd.policy)
            if len(warnings) > 0:
                logger.warning("Warning computing the new policy value %s", warnings)
            transaction_no = pd.payment.transaction_no if pd.payment.transaction_no else None

            if (
                    (pd.policy.status == Policy.STATUS_IDLE and pd.policy.stage == Policy.STAGE_RENEWED)
                    and (pd.policy.status == Policy.STATUS_READY
                         and PolicyConfig.activation_option == PolicyConfig.ACTIVATION_OPTION_READY
                         and pd.policy_stage == Policy.STAGE_NEW)
                    and pd.policy.id not in processed):
                if pd.premium.amount >= pd.policy.value:
                    new_policy.save_history()
                    new_policy.status = Policy.STATUS_ACTIVE
                    new_policy.effective_date = pd.policy.start_date
                    set_expiry_date(new_policy)
                    from core import datetime
                    new_policy.validity_from = datetime.datetime.now()
                    new_policy.audit_user_id = audit_user_id
                    new_policy.save()

                    for ip in new_policy.insuree_policies.filter(validity_to__isnull=True):
                        ip.save_history()
                        ip.effective_date = pd.policy.start_date
                        ip.validity_from = datetime.datetime.now()
                        ip.audit_user_id = audit_user_id
                        ip.save()

                    processed[pd.policy.id] = True
            else:
                if pd.policy.status not in [Policy.STATUS_IDLE, Policy.STATUS_READY] and pd.policy.id not in processed:
                    # insert new renewals if the policy is not IDLE
                    set_expiry_date(pd.policy)
                    if pd.amount >= pd.policy.value:
                        pd.policy.status = Policy.STATUS_ACTIVE
                        set_start_date(pd.policy)
                    else:
                        pd.policy.status = Policy.STATUS_IDLE

                    pd.policy.save_history()
                    pd.policy.save()

                    for insuree in pd.insuree.family.members.filter(validity_to__isnull=True):
                        update_insuree_policies(pd.policy, audit_user_id)
                    processed[pd.policy.id] = True
                else:
                    # increment matched payment ?
                    pass

            # insert premiums for individual renewals only
            if pd.premium is None:
                premium, premium_created = Premium.objects.filter(validity_to__isnull=True).update_or_create(
                    policy=pd.policy,
                    amount=pd.amount,
                    type=PayTypeChoices.CASH.value,
                    transaction_no=transaction_no,
                    defaults=dict(
                        audit_user_id=audit_user_id,
                        pay_date=datetime.datetime.now(),
                        validity_from=datetime.datetime.now(),
                    ),
                )
                pd.premium = premium
                pd.save()


def assign_payment_detail(pd, audit_user_id):
    # List premiums with the already paid amounts for each
    payment_details_subquery = PaymentDetail.filter_queryset()\
        .filter(premium_id=OuterRef("id")).values(amount_sum=Sum("amount"))
    premiums = Premium.filter_queryset().filter(policy=pd.policy).annotate(total_paid=payment_details_subquery)

    logger.debug("Assigning payment_detail %s with amount %s in policy %s", pd.id, pd.amount, pd.policy)
    available = 0
    for premium in premiums:
        # if the payments (including carried excess) equals or exceeds this premium, skip it and adjust available
        total_paid = premium.total_paid if premium.total_paid else 0
        if available + total_paid >= premium.amount:
            available += total_paid - premium.amount
            logger.debug("payment_detail %s, premium %s is already fulfilled (paid: %s, needed: %s, carrying over: %s)",
                         pd.id, premium.id, total_paid, premium.amount, available)
            continue
        # we'll assign payment to this premium
        logger.debug("Assigning payment_detail %s to premium %s", pd.id, premium.id)
        if pd.amount + available + total_paid >= premium.amount:
            logger.debug("Payment_detail %s is enough to cover the premium", pd.id)
        else:
            logger.debug("Payment_detail %s is NOT enough to cover the premium: %s+%s+%s/%s",
                         pd.id, pd.amount, available, total_paid, premium.amount)
        pd.premium = premium
        from core import datetime
        pd.validity_from = datetime.datetime.now()
        # pd.amount = premium.amount
        pd.audit_user_id = audit_user_id
        pd.save()

        pd.payment.status = Payment.STATUS_PAYMENTMATCHED
        pd.payment.matched_date = datetime.datetime.now()
        pd.payment.audit_user_id = audit_user_id
        pd.payment.validity_from = datetime.datetime.now()
        pd.payment.save()


PAYMENT_DETAIL_REJECTION_INSURANCE_NB = 101
PAYMENT_DETAIL_REJECTION_PRODUCT_CODE = 102
PAYMENT_DETAIL_REJECTION_INSURANCE_NB_INVALID = 103
PAYMENT_DETAIL_REJECTION_POLICY_NOT_FOUND = 104
PAYMENT_DETAIL_REJECTION_PRODUCT_CODE_INVALID = 105
PAYMENT_DETAIL_REJECTION_PRODUCT_NOT_ALLOWED = 106
PAYMENT_DETAIL_REJECTION_OFFICER_NOT_FOUND = 107
PAYMENT_DETAIL_REJECTION_PRODUCT_LOCATION = 108
PAYMENT_DETAIL_REJECTION_NO_PREMIUM = 109


def validate_payment_detail(pd):
    if PaymentConfig.default_validations_disabled:
        return []

    errors = []
    if pd.insurance_number is None:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_INSURANCE_NB,
                    'message': _("payment.validation.detail.reject.insurance_nb") % {
                        'id': pd.id
                    },
                    'detail': pd.id}]

    if pd.product_code is None:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_PRODUCT_CODE,
                    'message': _("payment.validation.detail.reject.product_code") % {
                        'id': pd.id
                    },
                    'detail': pd.id}]

    if len(errors) > 0:
        return errors

    insuree = Insuree.filter_queryset().filter(chf_id=pd.insurance_number) \
        .first()
    if not insuree:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_INSURANCE_NB_INVALID,
                    'message': _("payment.validation.detail.reject.insurance_nb_invalid") % {
                        'id': pd.id,
                        'chf': pd.insurance_number
                    },
                    'detail': pd.id}]
        return errors

    policy = Policy.filter_queryset()\
        .filter(product__validity_to__isnull=True, product__code=pd.product_code)\
        .filter(family__validity_to__isnull=True)\
        .filter(family__members__validity_to__isnull=True, family__members__chf_id=pd.insurance_number)\
        .first()

    if not policy:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_POLICY_NOT_FOUND,
                    'message': _("payment.validation.detail.reject.policy_not_found") % {
                        'id': pd.id,
                        'chf': pd.insurance_number,
                        'product_code': pd.product_code,
                    },
                    'detail': pd.id}]
        return errors

    location_cursor = insuree.family.location
    family_location_ids = []
    if location_cursor:
        for loc in LocationConfig.location_types:
            family_location_ids.append(location_cursor.id)
            location_cursor = location_cursor.parent
            if location_cursor is None:
                break

    # Original code checked the product validity against current_date, I used the enroll_date instead
    product = Product.filter_queryset().filter(
        Q(location_id__isnull=True) | Q(location_id__in=family_location_ids),
        date_from__lte=policy.enroll_date,
        date_to__gte=policy.enroll_date,
        code=pd.product_code,
    ).first()
    if not product:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_PRODUCT_NOT_ALLOWED,
                    'message': _("payment.validation.detail.reject.product_not_allowed") % {
                        'id': pd.id,
                        'chf': pd.insurance_number,
                        'product_code': pd.product_code,
                    },
                    'detail': pd.id}]
        return errors

    # Check enrollment officer
    officer = Officer.filter_queryset().filter(
        code=pd.payment.officer_code
    ).first()
    if not product:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_OFFICER_NOT_FOUND,
                    'message': _("payment.validation.detail.reject.officer_not_found") % {
                        'id': pd.id,
                        'chf': pd.insurance_number,
                        'officer_code': pd.payment.officer_code,
                    },
                    'detail': pd.id}]
        return errors

    # Check officer district vs product location
    # TODO this checks district/region, should be more generic
    if not (
            officer.location is None
            or product is None
            or officer.location_id == product.location_id
            or (officer.location.parent is not None and officer.location.parent == product.location.parent)):
        errors += [{'code': PAYMENT_DETAIL_REJECTION_PRODUCT_LOCATION,
                    'message': _("payment.validation.detail.reject.product_location") % {
                        'id': pd.id,
                        'chf': pd.insurance_number,
                        'product_code': pd.product_code,
                    },
                    'detail': pd.id}]
        return errors

    # Check that there is a premium available for that policy
    # TODO avoid relying on max(id) as using uuids would ruin it
    latest_premium = policy.premiums.filter(validity_to__isnull=True).aggregate(Max("id"))
    if not latest_premium:
        errors += [{'code': PAYMENT_DETAIL_REJECTION_NO_PREMIUM,
                    'message': _("payment.validation.detail.reject.no_premium") % {
                        'id': pd.id,
                        'policy': policy.uuid,
                    },
                    'detail': pd.id}]
        return errors

    # TODO instead of returning those, we should update the payment_detail with actual foreign keys
    pd.policy = policy
    pd.insuree = insuree
    pd.latest_premium = latest_premium
    pd.product = product
    return errors

