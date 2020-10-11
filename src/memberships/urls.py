from django.urls import path
from . import views
app_name = 'memberships'
urlpatterns = [
    path('membership_select/',views.MembershipSelectView.as_view(),name='membership_select'),
    path('payment/',views.PaymentView,name='payment'),
    path('update_transactions/<sub_id>/',views.UpdateTransactionView.as_view(),name='update_transactions'),
    path('cancel_subscription/',views.CancelSubscription.as_view(),name='cancel_subscription'),


]
