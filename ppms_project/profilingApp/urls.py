from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login_registration, name='login_registration'),
    path('logout', views.logout_user, name='logout'),
    
    #privacy policy
    path('privacyPolicy', views.privacyPolicy, name='privacyPolicy'),

    # Parent
    path('home', views.parent_home, name='parent_home'),
    path('preschooler/<str:pk>/', views.parent_preschooler, name='parent_preschooler'),
    path('PG_password/<str:pk>/', views.change_pass, name='PG_pass'),

    

    # Admin
    path('ahome', views.admin_home, name='admin_home'),
    path('apreschoolers', views.admin_preschoolers, name='admin_home2'),
    path('apreschoolersbarangay/<str:brgy>/', views.admin_preschoolers_barangay, name='apreschoolersb'),
    path('avalidation', views.bhw_validation, name='bhw_validation'),
    path('validate_profile/<str:pk>/', views.unvalidated_profile, name='unvalidated_profile'),
    path('delete_profile/<str:pk>/', views.delete_profile, name='delete_profile'),
    path('abarangay', views.admin_barangay, name='admin_barangay'),
    path('set_password/<str:pk>/', views.set_pass, name='set_pass'),
    path('auseraccounts', views.admin_userAccounts, name='admin_userAccounts'),
    path('aHistoryLogs', views.admin_historyLogs, name='admin_historyLogs'),



    # Barangay Health Worker
    path('bhwhome', views.bhw_home, name='bhw_home'),
    path('preschooler_dashboard', views.preschooler_dashboard, name='preschooler_dashboard'),
    path('preschooler_profile/<str:pk>/', views.preschooler_profile, name='preschooler_profile'),
    path('update_preschooler', views.update_preschooler, name='update_preschooler'),
    path('preschooler_profile/immunization/<str:pk>/', views.immunization_schedule, name='immunization_schedule'),
    path('new_password/<str:pk>/', views.change_pass, name='new_pass'),
    
]