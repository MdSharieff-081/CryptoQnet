"""
URL configuration for market_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from admins import views as admin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dj-admin/', admin.site.urls),  
    path('',user_views.home,name='home'),
    path('about/',user_views.about,name='about'),
    path('contact/',user_views.contact,name='contact'),
    path('admin_login/',admin_views.admin_login_page,name='admin-login'),
    path('user-login/',user_views.user_login_page,name='user-login'),

    path('user/check-login/', user_views.check_user_credentials),
    path('user/check-register/', user_views.check_register_fields),

    path('user/send-otp/', user_views.user_send_otp, name='user_send_otp'),
    path('user/verify-otp/', user_views.user_verify_otp, name='user_verify_otp'),
    path('user/login/', user_views.user_login, name='user_login_check'),
    path('user/register/', user_views.user_register, name='user_register'),
    path('user-dashboard/',user_views.user_dashboard,name='user-dashboard'),

    path('admin_dashboard/',admin_views.admin_dashboard,name='admin_dashboard'),
        path('approve-user/<int:user_id>/', admin_views.approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', admin_views.reject_user, name='reject_user'),

    path('admin/send-otp/', admin_views.send_otp, name='send_otp'),
    path('admin/verify-otp/', admin_views.verify_otp, name='verify_otp'),
    path('admin/login/', admin_views.admin_login, name='admin_login_check'),
    path('pending_users/',admin_views.pending_users,name='pending_users'),
    path('rejected_users/',admin_views.rejected_users,name='rejected_users'),
    path('all_users/',admin_views.all_users,name='all_users'),
    path('accepted_users/',admin_views.accepted_users, name='accepted_users'),
    path('upload_dataset/',admin_views.upload_dataset,name='upload_dataset'),
    path('view_dataset',admin_views.view_dataset,name='view_dataset'),
    path('open-dataset/<int:dataset_id>/', admin_views.open_dataset, name='open_dataset'),

    path('lstm/',admin_views.lstm,name='lstm'),
    path('gru/',admin_views.gru,name='gru'),
    path('rnn/',admin_views.rnn,name='rnn'),
    path('random_forest/',admin_views.random_forest,name='random_forest'),
    path('arima/',admin_views.arima,name='arima'),
    path('qml/',admin_views.qml_model,name='qml'),
    path('graph/',admin_views.graph,name='graph'),
    path('lstm_result/',admin_views.lstm_result,name='lstm_result'),
    path('gru_result',admin_views.gru_result,name='gru_result'),
    path('rnn_result',admin_views.rnn_result,name='rnn_result'),
    path('random_result',admin_views.random_result,name='random_result'),
    path('arima_result',admin_views.arima_result,name='arima_result'),
    path('qml_result',admin_views.qml_result,name='qml_result'),
    path('user_predict/',user_views.user_predict,name='user_predict'),
    path('result/',user_views.result_view,name='result'),
    path('user_profile/',user_views.user_profile,name='user_profile')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
