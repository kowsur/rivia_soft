from django.urls import path
from django.urls.conf import re_path
from .views import home_selfassesment, view_selfassesment, create_selfassesment, update_selfassesment, delete_selfassesment, search_selfassesment, all_selfassesment
from .views import home_selfassesment_account_submission, create_selfassesment_account_submission
from .url_variables import *

app_name = application_name

urlpatterns = [
    path(route='', 
        view=view_selfassesment,
        name='home'),
    
    # =============================================================================================================
    # =============================================================================================================
    # Selfassesment
    path(route=f'{Selfassesment_path}/{home_suffix}/',
        view=home_selfassesment,
        name=f'{Selfassesment_name}_{home_suffix}'),

    path(route=f'{Selfassesment_path}/{create_suffix}/',
        view=create_selfassesment,
        name=f'{Selfassesment_name}_{create_suffix}'),

    path(route=f'{Selfassesment_path}/{update_suffix}/<int:client_id>/', 
        view=update_selfassesment, 
        name=f'{Selfassesment_name}_{update_suffix}'),

    path(route=f'{Selfassesment_path}/{delete_suffix}/<int:client_id>/', 
        view=delete_selfassesment, 
        name=f'{Selfassesment_name}_{delete_suffix}'),

    path(route=f'{Selfassesment_path}/{search_suffix}/<str:search_text>/', 
        view=search_selfassesment, 
        name=f'{Selfassesment_name}_{search_suffix}'), # fetch only

    path(route=f'{Selfassesment_path}/{viewall_suffix}/', 
        view=all_selfassesment, 
        name=f'{Selfassesment_name}_{viewall_suffix}'), # fetch only


    # SelfassesmentAccountSubmission
    path(route=f'{Selfassesment_Account_Submission_path}/{home_suffix}/', 
        view=home_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{home_suffix}'),

    path(route=f'{Selfassesment_Account_Submission_path}/{create_suffix}/', 
        view=create_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{create_suffix}'),

    # path(route=f'{Selfassesment_Account_Submission_path}/{update_suffix}/<int:client_id>/', 
    #     view=update_selfassesment_account_submission, 
    #     name=f'{Selfassesment_Account_Submission_name}_{update_suffix}'),

    # path(route=f'{Selfassesment_Account_Submission_path}/{delete_suffix}/<int:client_id>/', 
    #     view=delete_selfassesment_account_submission, 
    #     name=f'{Selfassesment_Account_Submission_name}_{delete_suffix}'),
    
    # path(route=f'{Selfassesment_Account_Submission_path}/{search_suffix}/<str:search_text>/', 
    #     view=search_selfassesment_account_submission, 
    #     name=f'{Selfassesment_Account_Submission_name}_{search_suffix}'),
    
    # path(route=f'{Selfassesment_Account_Submission_path}/{viewall_suffix}/', 
    #     view=all_selfassesment_account_submission, 
    #     name=f'{Selfassesment_Account_Submission_name}_{viewall_suffix}'),

    # # Add all Selfassesment to SelfassesmentAccountSubmission
    # path(route=f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/', 
    #     # view=add_all_Selfassesment_to_SelfassesmentAccountSubmission_w_submission_year, 
    #     name=f'add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'),
    

    # =============================================================================================================
    # =============================================================================================================
    # Limited
    # path(route=f'{Limited_path}/{home_suffix}/',
    #     # view=create_Limited,
    #     name=f'{Limited_name}_{home_suffix}'),

    # path(route=f'{Limited_path}/{create_suffix}/',
    #     # view=create_Limited,
    #     name=f'{Limited_name}_{create_suffix}'),

    # path(route=f'{Limited_path}/{update_suffix}/<int:client_id>/', 
    #     # view=update_Limited, 
    #     name=f'{Limited_name}_{update_suffix}'),

    # path(route=f'{Limited_path}/{delete_suffix}/<int:client_id>/', 
    #     # view=update_Limited, 
    #     name=f'{Limited_name}_{delete_suffix}'),

    # path(route=f'{Limited_path}/{search_suffix}/<str:search_text>/', 
    #     # view=search_Limited, 
    #     name=f'{Limited_name}_{search_suffix}'),

    # path(route=f'{Limited_path}/{viewall_suffix}/', 
    #     # view=all_Limited, 
    #     name=f'{Limited_name}_{viewall_suffix}'),
    

    # # LimitedAccountSubmission
    # path(route=f'{Limited_Account_Submission_path}/{home_suffix}/', 
    #     # view=home_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{home_suffix}'),

    # path(route=f'{Limited_Account_Submission_path}/{create_suffix}/', 
    #     # view=create_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{create_suffix}'),

    # path(route=f'{Limited_Account_Submission_path}/{update_suffix}/<int:client_id>/', 
    #     # view=create_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{update_suffix}'),

    # path(route=f'{Limited_Account_Submission_path}/{delete_suffix}/<int:client_id>/', 
    #     # view=create_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{delete_suffix}'),
    
    # path(route=f'{Limited_Account_Submission_path}/{search_suffix}/<str:search_text>/', 
    #     # view=create_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{search_suffix}'),
    
    # path(route=f'{Limited_Account_Submission_path}/{viewall_suffix}/', 
    #     # view=create_LimitedAccountSubmission, 
    #     name=f'{Limited_Account_Submission_name}_{viewall_suffix}'),

    # # Add all Limited to LimitedAccountSubmission
    # path(route=f'add_all/{Limited_path}/to/{Limited_Account_Submission_path}/', 
    #     # view=add_all_Limited_to_LimitedAccountSubmission_w_submission_year, 
    #     name=f'add_all_{Limited_name}_to_{Limited_Account_Submission_name}'),


    # # =============================================================================================================
    # # =============================================================================================================
    # # Tracker
    # path(route=f'{Tracker_path}/{home_suffix}/',
    #     # view=create_Tracker,
    #     name=f'{Tracker_name}_{home_suffix}'),

    # path(route=f'{Tracker_path}/{create_suffix}/',
    #     # view=create_Tracker,
    #     name=f'{Tracker_name}_{create_suffix}'),

    # path(route=f'{Tracker_path}/{update_suffix}/<int:client_id>/', 
    #     # view=update_Tracker, 
    #     name=f'{Tracker_name}_{update_suffix}'),

    # path(route=f'{Tracker_path}/{delete_suffix}/<int:client_id>/', 
    #     # view=update_Tracker, 
    #     name=f'{Tracker_name}_{delete_suffix}'),

    # path(route=f'{Tracker_path}/{search_suffix}/<str:search_text>/', 
    #     # view=search_Tracker, 
    #     name=f'{Tracker_name}_{search_suffix}'),

    # path(route=f'{Tracker_path}/{viewall_suffix}/', 
    #     # view=all_Tracker, 
    #     name=f'{Tracker_name}_{viewall_suffix}'),
]
