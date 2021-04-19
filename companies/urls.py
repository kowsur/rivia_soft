from django.urls import path
from django.urls.conf import re_path

# selfassesment view functions
from .views import home_selfassesment, create_selfassesment, update_selfassesment, \
    delete_selfassesment, search_selfassesment, all_selfassesment

# selfassesment account submission view function
from .views import home_selfassesment_account_submission, create_selfassesment_account_submission, \
    update_selfassesment_account_submission, delete_selfassesment_account_submission,               \
    search_selfassesment_account_submission, all_selfassesment_account_submission,                  \
    add_all_selfassesment_to_selfassesment_account_submission_w_submission_year

# selfassesment tracker
from .views import home_selfassesment_tracker, create_selfassesment_tracker, update_selfassesment_tracker, \
    delete_selfassesment_tracker, search_selfassesment_tracker, all_selfassesment_tracker
    
from .url_variables import *

app_name = application_name

urlpatterns = [
    path(route='', 
        view=home_selfassesment,
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

    path(route=f'{Selfassesment_Account_Submission_path}/{update_suffix}/<int:submission_id>/', 
        view=update_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{update_suffix}'),

    path(route=f'{Selfassesment_Account_Submission_path}/{delete_suffix}/<int:submission_id>/', 
        view=delete_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{delete_suffix}'),
    
    path(route=f'{Selfassesment_Account_Submission_path}/{search_suffix}/<str:search_text>/', 
        view=search_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{search_suffix}'),
    
    path(route=f'{Selfassesment_Account_Submission_path}/{viewall_suffix}/', 
        view=all_selfassesment_account_submission, 
        name=f'{Selfassesment_Account_Submission_name}_{viewall_suffix}'),

    # Add all Selfassesment to SelfassesmentAccountSubmission
    path(route=f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/', 
        view=add_all_selfassesment_to_selfassesment_account_submission_w_submission_year, 
        name=f'add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'),
    

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


    # =============================================================================================================
    # =============================================================================================================
    # SelfassesmentTracker
    path(route=f'{SelfassesmentTracker_path}/{home_suffix}/',
        view=home_selfassesment_tracker,
        name=f'{SelfassesmentTracker_name}_{home_suffix}'),

    path(route=f'{SelfassesmentTracker_path}/{create_suffix}/',
        view=create_selfassesment_tracker,
        name=f'{SelfassesmentTracker_name}_{create_suffix}'),

    path(route=f'{SelfassesmentTracker_path}/{update_suffix}/<int:tracker_id>/', 
        view=update_selfassesment_tracker, 
        name=f'{SelfassesmentTracker_name}_{update_suffix}'),

    path(route=f'{SelfassesmentTracker_path}/{delete_suffix}/<int:tracker_id>/', 
        view=delete_selfassesment_tracker, 
        name=f'{SelfassesmentTracker_name}_{delete_suffix}'),

    path(route=f'{SelfassesmentTracker_path}/{search_suffix}/<str:search_text>/', 
        view=search_selfassesment_tracker, 
        name=f'{SelfassesmentTracker_name}_{search_suffix}'),

    path(route=f'{SelfassesmentTracker_path}/{viewall_suffix}/', 
        view=all_selfassesment_tracker, 
        name=f'{SelfassesmentTracker_name}_{viewall_suffix}'),
]
