from django.utils.timezone import now

from apps.common.models import ActiveStatusChoices
from apps.subscription.models import UserSubscription
from apps.subscription.models.user_subscription_model import UserSubscriptionPaymentStatus


def get_active_subscription(user):
    current_time = now()
    return UserSubscription.objects.filter(
        user=user,
        active_status=ActiveStatusChoices.ACTIVE,
        payment_status=UserSubscriptionPaymentStatus.PAID,
        start_at__lte=current_time,
        end_at__gte=current_time,
    ).first()
