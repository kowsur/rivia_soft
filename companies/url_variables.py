APPLICATION_NAME = 'companies'

# url paths 'companies/model_path/action/'
home_suffix = 'home'
create_suffix = 'create'
update_suffix = 'update'
delete_suffix = 'delete'
search_suffix = 'search'
details_suffix = 'details'
export_suffix = 'export'
viewall_suffix = 'all'


Selfassesment_path = 'SA'
Selfassesment_name = 'SA'

Selfassesment_Account_Submission_Tax_Year_path = 'SASTY'
Selfassesment_Account_Submission_Tax_Year_name = 'SASTY'

Selfassesment_Account_Submission_path = 'SAS'
Selfassesment_Account_Submission_name = 'SAS'

Selfassesment_Tracker_path = 'SATrc'
Selfassesment_Tracker_name = 'SATrc'


Limited_path = 'LTD'
Limited_name = 'LTD'

Limited_Submission_Deadline_Tracker_path = 'LAS'
Limited_Submission_Deadline_Tracker_name = 'LAS'

Limited_VAT_Tracker_path = 'LVATTrc'
Limited_VAT_Tracker_name = 'LVATTrc'

Limited_Confirmation_Statement_Tracker_path = 'LCSTrc'
Limited_Confirmation_Statement_Tracker_name = 'LCSTrc'

Limited_Tracker_path = 'LTDTrc'
Limited_Tracker_name = 'LTDTrc'

Merged_Tracker = 'MTrc'


class Dict_Duck_type:
  @classmethod
  def get_dict(cls) -> dict:
    attars = {}
    for attar in dir(cls):
      if not callable(attar) and not (attar.startswith('__') or attar.endswith('__')):
        attars[attar] = getattr(cls, attar)
    return attars
  
  @classmethod
  def __getitem__(cls, key:str) -> str:
    return getattr(cls, key, '')
  
  @classmethod
  def __setitem__(cls, key:str, value) -> None:
    setattr(cls, key, value)


# Only use in urls.py to set url routes
class URL_PATHS(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_url = f'{Selfassesment_path}/{home_suffix}/'
  Selfassesment_create_url = f'{Selfassesment_path}/{create_suffix}/'
  Selfassesment_details_url = f'{Selfassesment_path}/{details_suffix}/<int:client_id>/'
  Selfassesment_update_url = f'{Selfassesment_path}/{update_suffix}/<int:client_id>/'
  Selfassesment_delete_url = f'{Selfassesment_path}/{delete_suffix}/<int:client_id>/'
  Selfassesment_search_url = f'{Selfassesment_path}/{search_suffix}/' # fetch only
  Selfassesment_viewall_url = f'{Selfassesment_path}/{viewall_suffix}/' # fetch only
  Selfassesment_export_url = f'{Selfassesment_path}/{export_suffix}/'

  # Selfassesment Account Submission Tax Year
  Selfassesment_Account_Submission_Tax_Year_details_url = f'{Selfassesment_Account_Submission_Tax_Year_path}/{details_suffix}/<int:id>/'
  Selfassesment_Account_Submission_Tax_Year_search_url = f'{Selfassesment_Account_Submission_Tax_Year_path}/{search_suffix}/' # fetch only
  Selfassesment_Account_Submission_Tax_Year_viewall_url = f'{Selfassesment_Account_Submission_Tax_Year_path}/{viewall_suffix}/' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_url = f'{Selfassesment_Account_Submission_path}/{home_suffix}/'
  Selfassesment_Account_Submission_create_url = f'{Selfassesment_Account_Submission_path}/{create_suffix}/'
  Selfassesment_Account_Submission_update_url = f'{Selfassesment_Account_Submission_path}/{update_suffix}/<int:submission_id>/'
  Selfassesment_Account_Submission_delete_url = f'{Selfassesment_Account_Submission_path}/{delete_suffix}/<int:submission_id>/'
  Selfassesment_Account_Submission_search_url = f'{Selfassesment_Account_Submission_path}/{search_suffix}/' # fetch only
  Selfassesment_Account_Submission_viewall_url = f'{Selfassesment_Account_Submission_path}/{viewall_suffix}/' # fetch only
  Selfassesment_Account_Submission_export_url = f'{Selfassesment_Account_Submission_path}/{export_suffix}/'
  add_all_Selfassesment_to_Selfassesment_Account_Submission_url = f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/'

  # Tracker
  Selfassesment_Tracker_home_url = f'{Selfassesment_Tracker_path}/{home_suffix}/'
  Selfassesment_Tracker_create_url = f'{Selfassesment_Tracker_path}/{create_suffix}/'
  Selfassesment_Tracker_update_url = f'{Selfassesment_Tracker_path}/{update_suffix}/<int:tracker_id>/'
  Selfassesment_Tracker_delete_url = f'{Selfassesment_Tracker_path}/{delete_suffix}/<int:tracker_id>/'
  Selfassesment_Tracker_search_url = f'{Selfassesment_Tracker_path}/{search_suffix}/' # fetch only
  Selfassesment_Tracker_viewall_url = f'{Selfassesment_Tracker_path}/{viewall_suffix}/' # fetch only
  Selfassesment_Tracker_export_url = f'{Selfassesment_Tracker_path}/{export_suffix}/'


  # Limited
  Limited_home_url = f'{Limited_path}/{home_suffix}/'
  Limited_create_url = f'{Limited_path}/{create_suffix}/'
  Limited_details_url = f'{Limited_path}/{details_suffix}/<int:client_id>/'
  Limited_update_url = f'{Limited_path}/{update_suffix}/<int:client_id>/'
  Limited_delete_url = f'{Limited_path}/{delete_suffix}/<int:client_id>/'
  Limited_search_url = f'{Limited_path}/{search_suffix}/' # fetch only
  Limited_viewall_url = f'{Limited_path}/{viewall_suffix}/' # fetch only
  Limited_export_url = f'{Limited_path}/{export_suffix}/'

  # Limited Submission Deadline Tracker
  Limited_Submission_Deadline_Tracker_home_url = f'{Limited_Submission_Deadline_Tracker_path}/{home_suffix}/'
  Limited_Submission_Deadline_Tracker_create_url = f'{Limited_Submission_Deadline_Tracker_path}/{create_suffix}/'
  Limited_Submission_Deadline_Tracker_update_url = f'{Limited_Submission_Deadline_Tracker_path}/{update_suffix}/<int:submission_id>/'
  Limited_Submission_Deadline_Tracker_delete_url = f'{Limited_Submission_Deadline_Tracker_path}/{delete_suffix}/<int:submission_id>/'
  Limited_Submission_Deadline_Tracker_search_url = f'{Limited_Submission_Deadline_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Submission_Deadline_Tracker_viewall_url = f'{Limited_Submission_Deadline_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Submission_Deadline_Tracker_export_url = f'{Limited_Submission_Deadline_Tracker_path}/{export_suffix}/'
  
  # Limited VAT Tracker
  Limited_VAT_Tracker_home_url = f'{Limited_VAT_Tracker_path}/{home_suffix}/'
  Limited_VAT_Tracker_create_url = f'{Limited_VAT_Tracker_path}/{create_suffix}/'
  Limited_VAT_Tracker_update_url = f'{Limited_VAT_Tracker_path}/{update_suffix}/<int:vat_id>/'
  Limited_VAT_Tracker_delete_url = f'{Limited_VAT_Tracker_path}/{delete_suffix}/<int:vat_id>/'
  Limited_VAT_Tracker_search_url = f'{Limited_VAT_Tracker_path}/{search_suffix}/' # fetch only
  Limited_VAT_Tracker_viewall_url = f'{Limited_VAT_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_VAT_Tracker_export_url = f'{Limited_VAT_Tracker_path}/{export_suffix}/'

  # Limited Confirmation Statement Tracker
  Limited_Confirmation_Statement_Tracker_home_url = f'{Limited_Confirmation_Statement_Tracker_path}/{home_suffix}/'
  Limited_Confirmation_Statement_Tracker_create_url = f'{Limited_Confirmation_Statement_Tracker_path}/{create_suffix}/'
  Limited_Confirmation_Statement_Tracker_update_url = f'{Limited_Confirmation_Statement_Tracker_path}/{update_suffix}/<int:statement_id>/'
  Limited_Confirmation_Statement_Tracker_delete_url = f'{Limited_Confirmation_Statement_Tracker_path}/{delete_suffix}/<int:statement_id>/'
  Limited_Confirmation_Statement_Tracker_search_url = f'{Limited_Confirmation_Statement_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Confirmation_Statement_Tracker_viewall_url = f'{Limited_Confirmation_Statement_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Confirmation_Statement_Tracker_export_url = f'{Limited_Confirmation_Statement_Tracker_path}/{export_suffix}/'

  # Tracker
  Limited_Tracker_home_url = f'{Limited_Tracker_path}/{home_suffix}/'
  Limited_Tracker_create_url = f'{Limited_Tracker_path}/{create_suffix}/'
  Limited_Tracker_update_url = f'{Limited_Tracker_path}/{update_suffix}/<int:tracker_id>/'
  Limited_Tracker_delete_url = f'{Limited_Tracker_path}/{delete_suffix}/<int:tracker_id>/'
  Limited_Tracker_search_url = f'{Limited_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Tracker_viewall_url = f'{Limited_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Tracker_export_url = f'{Limited_Tracker_path}/{export_suffix}/'

  # Merged Tracker
  Merged_Tracker_home_url = f'{Merged_Tracker}/{home_suffix}/'
  Merged_Tracker_create_url = f'{Merged_Tracker}/{create_suffix}/'
  Merged_Tracker_export_url = f'{Merged_Tracker}/{export_suffix}/'


# Only use in urls.py to set url names
class URL_NAMES(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_name = f'{Selfassesment_name}_{home_suffix}'
  Selfassesment_create_name = f'{Selfassesment_name}_{create_suffix}'
  Selfassesment_details_name = f'{Selfassesment_path}_{details_suffix}'
  Selfassesment_update_name = f'{Selfassesment_name}_{update_suffix}'
  Selfassesment_delete_name = f'{Selfassesment_name}_{delete_suffix}'
  Selfassesment_search_name = f'{Selfassesment_name}_{search_suffix}' # fetch only
  Selfassesment_viewall_name = f'{Selfassesment_name}_{viewall_suffix}' # fetch only
  Selfassesment_export_name = f'{Selfassesment_name}_{export_suffix}'

  # Selfassesment Account Submission Tax 
  Selfassesment_Account_Submission_Tax_Year_details_name = f'{Selfassesment_Account_Submission_Tax_Year_path}_{details_suffix}'
  Selfassesment_Account_Submission_Tax_Year_search_name = f'{Selfassesment_Account_Submission_Tax_Year_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_Tax_Year_viewall_name = f'{Selfassesment_Account_Submission_Tax_Year_name}_{viewall_suffix}' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_name = f'{Selfassesment_Account_Submission_name}_{home_suffix}'
  Selfassesment_Account_Submission_create_name = f'{Selfassesment_Account_Submission_name}_{create_suffix}'
  Selfassesment_Account_Submission_update_name = f'{Selfassesment_Account_Submission_name}_{update_suffix}'
  Selfassesment_Account_Submission_delete_name = f'{Selfassesment_Account_Submission_name}_{delete_suffix}'
  Selfassesment_Account_Submission_search_name = f'{Selfassesment_Account_Submission_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_viewall_name = f'{Selfassesment_Account_Submission_name}_{viewall_suffix}' # fetch only
  Selfassesment_Account_Submission_export_name = f'{Selfassesment_Account_Submission_name}_{export_suffix}'
  add_all_Selfassesment_to_Selfassesment_Account_Submission_name = f'add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'

  # Tracker
  Selfassesment_Tracker_home_name = f'{Selfassesment_Tracker_name}_{home_suffix}'
  Selfassesment_Tracker_create_name = f'{Selfassesment_Tracker_name}_{create_suffix}'
  Selfassesment_Tracker_update_name = f'{Selfassesment_Tracker_name}_{update_suffix}'
  Selfassesment_Tracker_delete_name = f'{Selfassesment_Tracker_name}_{delete_suffix}'
  Selfassesment_Tracker_search_name = f'{Selfassesment_Tracker_name}_{search_suffix}' # fetch only
  Selfassesment_Tracker_viewall_name = f'{Selfassesment_Tracker_name}_{viewall_suffix}' # fetch only
  Selfassesment_Tracker_export_name = f'{Selfassesment_Tracker_name}_{export_suffix}'


  # Limited
  Limited_home_name = f'{Limited_name}_{home_suffix}'
  Limited_create_name = f'{Limited_name}_{create_suffix}'
  Limited_details_name = f'{Limited_path}_{details_suffix}'
  Limited_update_name = f'{Limited_name}_{update_suffix}'
  Limited_delete_name = f'{Limited_name}_{delete_suffix}'
  Limited_search_name = f'{Limited_name}_{search_suffix}' # fetch only
  Limited_viewall_name = f'{Limited_name}_{viewall_suffix}' # fetch only
  Limited_export_name = f'{Limited_name}_{export_suffix}'

  # Limited Submission Deadline Tracker
  Limited_Submission_Deadline_Tracker_home_name = f'{Limited_Submission_Deadline_Tracker_name}_{home_suffix}'
  Limited_Submission_Deadline_Tracker_create_name = f'{Limited_Submission_Deadline_Tracker_name}_{create_suffix}'
  Limited_Submission_Deadline_Tracker_update_name = f'{Limited_Submission_Deadline_Tracker_name}_{update_suffix}'
  Limited_Submission_Deadline_Tracker_delete_name = f'{Limited_Submission_Deadline_Tracker_name}_{delete_suffix}'
  Limited_Submission_Deadline_Tracker_search_name = f'{Limited_Submission_Deadline_Tracker_name}_{search_suffix}' # fetch only
  Limited_Submission_Deadline_Tracker_viewall_name = f'{Limited_Submission_Deadline_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Submission_Deadline_Tracker_export_name = f'{Limited_Submission_Deadline_Tracker_name}_{export_suffix}'
  
  # Limited VAT Tracker
  Limited_VAT_Tracker_home_name = f'{Limited_VAT_Tracker_name}_{home_suffix}'
  Limited_VAT_Tracker_create_name = f'{Limited_VAT_Tracker_name}_{create_suffix}'
  Limited_VAT_Tracker_update_name = f'{Limited_VAT_Tracker_name}_{update_suffix}'
  Limited_VAT_Tracker_delete_name = f'{Limited_VAT_Tracker_name}_{delete_suffix}'
  Limited_VAT_Tracker_search_name = f'{Limited_VAT_Tracker_name}_{search_suffix}' # fetch only
  Limited_VAT_Tracker_viewall_name = f'{Limited_VAT_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_VAT_Tracker_export_name = f'{Limited_VAT_Tracker_name}_{export_suffix}'
  
  # Limited Confirmation Statement Tracker
  Limited_Confirmation_Statement_Tracker_home_name = f'{Limited_Confirmation_Statement_Tracker_name}_{home_suffix}'
  Limited_Confirmation_Statement_Tracker_create_name = f'{Limited_Confirmation_Statement_Tracker_name}_{create_suffix}'
  Limited_Confirmation_Statement_Tracker_update_name = f'{Limited_Confirmation_Statement_Tracker_name}_{update_suffix}'
  Limited_Confirmation_Statement_Tracker_delete_name = f'{Limited_Confirmation_Statement_Tracker_name}_{delete_suffix}'
  Limited_Confirmation_Statement_Tracker_search_name = f'{Limited_Confirmation_Statement_Tracker_name}_{search_suffix}' # fetch only
  Limited_Confirmation_Statement_Tracker_viewall_name = f'{Limited_Confirmation_Statement_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Confirmation_Statement_Tracker_export_name = f'{Limited_Confirmation_Statement_Tracker_name}_{export_suffix}'

  # Tracker
  Limited_Tracker_home_name = f'{Limited_Tracker_name}_{home_suffix}'
  Limited_Tracker_create_name = f'{Limited_Tracker_name}_{create_suffix}'
  Limited_Tracker_update_name = f'{Limited_Tracker_name}_{update_suffix}'
  Limited_Tracker_delete_name = f'{Limited_Tracker_name}_{delete_suffix}'
  Limited_Tracker_search_name = f'{Limited_Tracker_name}_{search_suffix}' # fetch only
  Limited_Tracker_viewall_name = f'{Limited_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Tracker_export_name = f'{Limited_Tracker_name}_{export_suffix}'

  # Merged Tracker
  Merged_Tracker_home_name = f'{Merged_Tracker}_{home_suffix}'
  Merged_Tracker_create_name = f'{Merged_Tracker}_{create_suffix}'
  Merged_Tracker_export_name = f'{Merged_Tracker}_{export_suffix}'



# Should be passed in templates for JavaScript to fetch() api calls
class Full_URL_PATHS_WITHOUT_ARGUMENTS(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{home_suffix}/'
  Selfassesment_create_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{create_suffix}/'
  Selfassesment_details_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{details_suffix}/'
  Selfassesment_update_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{update_suffix}/'
  Selfassesment_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{delete_suffix}/'
  Selfassesment_search_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{search_suffix}/' # fetch only
  Selfassesment_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{viewall_suffix}/' # fetch only
  Selfassesment_export_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{export_suffix}/'

  # Selfassesment Account Submission Tax Year
  Selfassesment_Account_Submission_Tax_Year_details_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_Tax_Year_path}/{details_suffix}/'
  Selfassesment_Account_Submission_Tax_Year_search_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_Tax_Year_path}/{search_suffix}/' # fetch only
  Selfassesment_Account_Submission_Tax_Year_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_Tax_Year_path}/{viewall_suffix}/' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{home_suffix}/'
  Selfassesment_Account_Submission_create_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{create_suffix}/'
  Selfassesment_Account_Submission_update_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{update_suffix}/'
  Selfassesment_Account_Submission_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{delete_suffix}/'
  Selfassesment_Account_Submission_search_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{search_suffix}/' # fetch only
  Selfassesment_Account_Submission_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{viewall_suffix}/' # fetch only
  Selfassesment_Account_Submission_export_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{export_suffix}/'
  add_all_Selfassesment_to_Selfassesment_Account_Submission_url = f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/'

  # Tracker
  Selfassesment_Tracker_home_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{home_suffix}/'
  Selfassesment_Tracker_create_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{create_suffix}/'
  Selfassesment_Tracker_update_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{update_suffix}/'
  Selfassesment_Tracker_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{delete_suffix}/'
  Selfassesment_Tracker_search_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{search_suffix}/' # fetch only
  Selfassesment_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{viewall_suffix}/' # fetch only
  Selfassesment_Tracker_export_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{export_suffix}/'


  # Limited
  Limited_home_url = f'/{APPLICATION_NAME}/{Limited_path}/{home_suffix}/'
  Limited_create_url = f'/{APPLICATION_NAME}/{Limited_path}/{create_suffix}/'
  Limited_details_url = f'/{APPLICATION_NAME}/{Limited_path}/{details_suffix}/'
  Limited_update_url = f'/{APPLICATION_NAME}/{Limited_path}/{update_suffix}/'
  Limited_delete_url = f'/{APPLICATION_NAME}/{Limited_path}/{delete_suffix}/'
  Limited_search_url = f'/{APPLICATION_NAME}/{Limited_path}/{search_suffix}/' # fetch only
  Limited_viewall_url = f'/{APPLICATION_NAME}/{Limited_path}/{viewall_suffix}/' # fetch only
  Limited_export_url = f'/{APPLICATION_NAME}/{Limited_path}/{export_suffix}/'

  # Limited Submission Deadline Tracker
  Limited_Submission_Deadline_Tracker_home_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{home_suffix}/'
  Limited_Submission_Deadline_Tracker_create_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{create_suffix}/'
  Limited_Submission_Deadline_Tracker_update_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{update_suffix}/'
  Limited_Submission_Deadline_Tracker_delete_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{delete_suffix}/'
  Limited_Submission_Deadline_Tracker_search_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Submission_Deadline_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Submission_Deadline_Tracker_export_url = f'/{APPLICATION_NAME}/{Limited_Submission_Deadline_Tracker_path}/{export_suffix}/'

  # Limited VAT Tracker
  Limited_VAT_Tracker_home_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{home_suffix}/'
  Limited_VAT_Tracker_create_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{create_suffix}/'
  Limited_VAT_Tracker_update_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{update_suffix}/'
  Limited_VAT_Tracker_delete_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{delete_suffix}/'
  Limited_VAT_Tracker_search_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{search_suffix}/' # fetch only
  Limited_VAT_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_VAT_Tracker_export_url = f'/{APPLICATION_NAME}/{Limited_VAT_Tracker_path}/{export_suffix}/'

  # Limited Confirmation Statement Tracker
  Limited_Confirmation_Statement_Tracker_home_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{home_suffix}/'
  Limited_Confirmation_Statement_Tracker_create_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{create_suffix}/'
  Limited_Confirmation_Statement_Tracker_update_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{update_suffix}/'
  Limited_Confirmation_Statement_Tracker_delete_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{delete_suffix}/'
  Limited_Confirmation_Statement_Tracker_search_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Confirmation_Statement_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Confirmation_Statement_Tracker_export_url = f'/{APPLICATION_NAME}/{Limited_Confirmation_Statement_Tracker_path}/{export_suffix}/'

  # Tracker
  Limited_Tracker_home_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{home_suffix}/'
  Limited_Tracker_create_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{create_suffix}/'
  Limited_Tracker_update_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{update_suffix}/'
  Limited_Tracker_delete_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{delete_suffix}/'
  Limited_Tracker_search_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{search_suffix}/' # fetch only
  Limited_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{viewall_suffix}/' # fetch only
  Limited_Tracker_export_url = f'/{APPLICATION_NAME}/{Limited_Tracker_path}/{export_suffix}/'

  # Merged Tracker
  Merged_Tracker_home_url = f'/{APPLICATION_NAME}/{Merged_Tracker}/{home_suffix}/'
  Merged_Tracker_create_url = f'/{APPLICATION_NAME}/{Merged_Tracker}/{create_suffix}/'
  Merged_Tracker_export_url = f'/{APPLICATION_NAME}/{Merged_Tracker}/{export_suffix}'



# Should be used in templates to reffer to links
class URL_NAMES_PREFIXED_WITH_APP_NAME(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{home_suffix}'
  Selfassesment_create_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{create_suffix}'
  Selfassesment_details_name = f'{APPLICATION_NAME}:{Selfassesment_path}_{details_suffix}'
  Selfassesment_update_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{update_suffix}'
  Selfassesment_delete_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{delete_suffix}'
  Selfassesment_search_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{search_suffix}' # fetch only
  Selfassesment_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{viewall_suffix}' # fetch only
  Selfassesment_export_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{export_suffix}'

  # Selfassesment Account Submission Tax Year
  Selfassesment_Account_Submission_Tax_Year_details_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_Tax_Year_path}_{details_suffix}'
  Selfassesment_Account_Submission_Tax_Year_search_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_Tax_Year_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_Tax_Yearviewall_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_Tax_Year_name}_{viewall_suffix}' # fetch onl

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{home_suffix}'
  Selfassesment_Account_Submission_create_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{create_suffix}'
  Selfassesment_Account_Submission_update_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{update_suffix}'
  Selfassesment_Account_Submission_delete_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{delete_suffix}'
  Selfassesment_Account_Submission_search_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{viewall_suffix}' # fetch only
  Selfassesment_Account_Submission_export_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{export_suffix}'
  add_all_Selfassesment_to_Selfassesment_Account_Submission_name = f'{APPLICATION_NAME}:add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'

  # Tracker
  Selfassesment_Tracker_home_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{home_suffix}'
  Selfassesment_Tracker_create_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{create_suffix}'
  Selfassesment_Tracker_update_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{update_suffix}'
  Selfassesment_Tracker_delete_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{delete_suffix}'
  Selfassesment_Tracker_search_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{search_suffix}' # fetch only
  Selfassesment_Tracker_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{viewall_suffix}' # fetch only
  Selfassesment_Tracker_export_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{export_suffix}'


  # Limited
  Limited_home_name = f'{APPLICATION_NAME}:{Limited_name}_{home_suffix}'
  Limited_create_name = f'{APPLICATION_NAME}:{Limited_name}_{create_suffix}'
  Limited_details_name = f'{APPLICATION_NAME}:{Limited_path}_{details_suffix}'
  Limited_update_name = f'{APPLICATION_NAME}:{Limited_name}_{update_suffix}'
  Limited_delete_name = f'{APPLICATION_NAME}:{Limited_name}_{delete_suffix}'
  Limited_search_name = f'{APPLICATION_NAME}:{Limited_name}_{search_suffix}' # fetch only
  Limited_viewall_name = f'{APPLICATION_NAME}:{Limited_name}_{viewall_suffix}' # fetch only
  Limited_export_name = f'{APPLICATION_NAME}:{Limited_name}_{export_suffix}'

  # Limited Submission Deadline Tracker
  Limited_Submission_Deadline_Tracker_home_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{home_suffix}'
  Limited_Submission_Deadline_Tracker_create_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{create_suffix}'
  Limited_Submission_Deadline_Tracker_update_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{update_suffix}'
  Limited_Submission_Deadline_Tracker_delete_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{delete_suffix}'
  Limited_Submission_Deadline_Tracker_search_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{search_suffix}' # fetch only
  Limited_Submission_Deadline_Tracker_viewall_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Submission_Deadline_Tracker_export_name = f'{APPLICATION_NAME}:{Limited_Submission_Deadline_Tracker_name}_{export_suffix}'

  # Limited VAT Tracker
  Limited_VAT_Tracker_home_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{home_suffix}'
  Limited_VAT_Tracker_create_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{create_suffix}'
  Limited_VAT_Tracker_update_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{update_suffix}'
  Limited_VAT_Tracker_delete_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{delete_suffix}'
  Limited_VAT_Tracker_search_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{search_suffix}' # fetch only
  Limited_VAT_Tracker_viewall_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_VAT_Tracker_export_name = f'{APPLICATION_NAME}:{Limited_VAT_Tracker_name}_{export_suffix}'
  
  # Limited Confirmation Statement Tracker
  Limited_Confirmation_Statement_Tracker_home_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{home_suffix}'
  Limited_Confirmation_Statement_Tracker_create_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{create_suffix}'
  Limited_Confirmation_Statement_Tracker_update_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{update_suffix}'
  Limited_Confirmation_Statement_Tracker_delete_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{delete_suffix}'
  Limited_Confirmation_Statement_Tracker_search_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{search_suffix}' # fetch only
  Limited_Confirmation_Statement_Tracker_viewall_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Confirmation_Statement_Tracker_export_name = f'{APPLICATION_NAME}:{Limited_Confirmation_Statement_Tracker_name}_{export_suffix}'

  # Tracker
  Limited_Tracker_home_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{home_suffix}'
  Limited_Tracker_create_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{create_suffix}'
  Limited_Tracker_update_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{update_suffix}'
  Limited_Tracker_delete_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{delete_suffix}'
  Limited_Tracker_search_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{search_suffix}' # fetch only
  Limited_Tracker_viewall_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{viewall_suffix}' # fetch only
  Limited_Tracker_export_name = f'{APPLICATION_NAME}:{Limited_Tracker_name}_{export_suffix}'

  # Merged Tracker
  Merged_Tracker_home_name = f'{APPLICATION_NAME}:{Merged_Tracker}_{home_suffix}'
  Merged_Tracker_create_name = f'{APPLICATION_NAME}:{Merged_Tracker}_{create_suffix}'
  Merged_Tracker_export_name = f'{APPLICATION_NAME}:{Merged_Tracker}_{export_suffix}'
