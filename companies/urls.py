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


from .url_variables import APPLICATION_NAME, URL_PATHS, URL_NAMES
from .url_variables import *


app_name = APPLICATION_NAME
application_name = app_name

urlpatterns = [
    path(route='',
        view=home_selfassesment,
        name='home'),

    # =============================================================================================================
    # =============================================================================================================
    # Selfassesment
    path(route = URL_PATHS.Selfassesment_home_url,
        view = home_selfassesment,
        name = URL_NAMES.Selfassesment_home_name),

    path(route = URL_PATHS.Selfassesment_create_url,
        view = create_selfassesment,
        name = URL_NAMES.Selfassesment_create_name),

    path(route = URL_PATHS.Selfassesment_update_url,
        view = update_selfassesment,
        name = URL_NAMES.Selfassesment_update_name),

    path(route = URL_PATHS.Selfassesment_delete_url,
        view = delete_selfassesment,
        name= URL_NAMES.Selfassesment_delete_name),

    path(route = URL_PATHS.Selfassesment_search_url,
        view = search_selfassesment,
        name = URL_NAMES.Selfassesment_search_name), # fetch only

    path(route = URL_PATHS.Selfassesment_viewall_url,
        view = all_selfassesment,
        name = URL_NAMES.Selfassesment_viewall_name), # fetch only


    # SelfassesmentAccountSubmission
    path(route = URL_PATHS.Selfassesment_Account_Submission_home_url,
        view = home_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_home_name),

    path(route = URL_PATHS.Selfassesment_Account_Submission_create_url,
        view = create_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_create_name),

    path(route = URL_PATHS.Selfassesment_Account_Submission_update_url,
        view = update_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_update_name),

    path(route = URL_PATHS.Selfassesment_Account_Submission_delete_url,
        view = delete_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_delete_name),

    path(route = URL_PATHS.Selfassesment_Account_Submission_search_url,
        view = search_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_search_name),

    path(route = URL_PATHS.Selfassesment_Account_Submission_viewall_url,
        view = all_selfassesment_account_submission,
        name = URL_NAMES.Selfassesment_Account_Submission_viewall_name),

    # Add all Selfassesment to SelfassesmentAccountSubmission
    path(route = URL_PATHS.add_all_Selfassesment_to_Selfassesment_Account_Submission_url,
        view = add_all_selfassesment_to_selfassesment_account_submission_w_submission_year,
        name = URL_NAMES.add_all_Selfassesment_to_Selfassesment_Account_Submission_name),


    # =============================================================================================================
    # SelfassesmentTracker
    path(route = URL_PATHS.Selfassesment_Tracker_home_url,
        view = home_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_home_name),

    path(route = URL_PATHS.Selfassesment_Tracker_create_url,
        view = create_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_create_name),

    path(route = URL_PATHS.Selfassesment_Tracker_update_url,
        view = update_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_update_name),

    path(route = URL_PATHS.Selfassesment_Tracker_delete_url,
        view = delete_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_delete_name),

    path(route = URL_PATHS.Selfassesment_Tracker_search_url,
        view = search_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_search_name),

    path(route = URL_PATHS.Selfassesment_Tracker_viewall_url,
        view = all_selfassesment_tracker,
        name = URL_NAMES.Selfassesment_Tracker_viewall_name),
]
