APPLICATION_NAME = 'companies'

# url paths 'companies/model_path/action/'
home_suffix = 'home'
create_suffix = 'create'
update_suffix = 'update'
delete_suffix = 'delete'
search_suffix = 'search'
viewall_suffix = 'all'


Selfassesment_path = 'SA'
Selfassesment_name = 'SA'

Selfassesment_Account_Submission_path = 'SAS'
Selfassesment_Account_Submission_name = 'SAS'

Selfassesment_Tracker_path = 'SATrc'
Selfassesment_Tracker_name = 'SATrc'


Limited_path = 'LTD'
Limited_name = 'LTD'

Limited_Account_Submission_path = 'LAS'
Limited_Account_Submission_name = 'LAS'

LimitedTracker_path = 'LTDTrc'
LimitedTracker_name = 'LTDTrc'


class Dict_Duck_type:
  def get_dict(self):
    attars = {}
    for attar in dir(self):
      if not callable(attar) and not (attar.startswith('__') or attar.endswith('__')):
        attars[attar] = getattr(self, attar)
    return attars
  
  def __getitem__(self, key:str) -> str:
    return getattr(self, key, '')
  
  def __setitem__(self, key:str, value) -> None:
    setattr(self, key, value)


# Only use in urls.py to set url routes
class URL_PATHS(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_url = f'{Selfassesment_path}/{home_suffix}/'
  Selfassesment_create_url = f'{Selfassesment_path}/{create_suffix}/'
  Selfassesment_update_url = f'{Selfassesment_path}/{update_suffix}/<int:client_id>/'
  Selfassesment_delete_url = f'{Selfassesment_path}/{delete_suffix}/<int:client_id>/'
  Selfassesment_search_url = f'{Selfassesment_path}/{search_suffix}/<str:search_text>/' # fetch only
  Selfassesment_viewall_url = f'{Selfassesment_path}/{viewall_suffix}/' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_url = f'{Selfassesment_Account_Submission_path}/{home_suffix}/'
  Selfassesment_Account_Submission_create_url = f'{Selfassesment_Account_Submission_path}/{create_suffix}/'
  Selfassesment_Account_Submission_update_url = f'{Selfassesment_Account_Submission_path}/{update_suffix}/<int:submission_id>/'
  Selfassesment_Account_Submission_delete_url = f'{Selfassesment_Account_Submission_path}/{delete_suffix}/<int:submission_id>/'
  Selfassesment_Account_Submission_search_url = f'{Selfassesment_Account_Submission_path}/{search_suffix}/<str:search_text>/' # fetch only
  Selfassesment_Account_Submission_viewall_url = f'{Selfassesment_Account_Submission_path}/{viewall_suffix}/' # fetch only
  add_all_Selfassesment_to_Selfassesment_Account_Submission_url = f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/'

  # Tracker
  Selfassesment_Tracker_home_url = f'{Selfassesment_Tracker_path}/{home_suffix}/'
  Selfassesment_Tracker_create_url = f'{Selfassesment_Tracker_path}/{create_suffix}/'
  Selfassesment_Tracker_update_url = f'{Selfassesment_Tracker_path}/{update_suffix}/<int:tracker_id>/'
  Selfassesment_Tracker_delete_url = f'{Selfassesment_Tracker_path}/{delete_suffix}/<int:tracker_id>/'
  Selfassesment_Tracker_search_url = f'{Selfassesment_Tracker_path}/{search_suffix}/<str:search_text>/' # fetch only
  Selfassesment_Tracker_viewall_url = f'{Selfassesment_Tracker_path}/{viewall_suffix}/' # fetch only


# Only use in urls.py to set url names
class URL_NAMES(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_name = f'{Selfassesment_name}_{home_suffix}'
  Selfassesment_create_name = f'{Selfassesment_name}_{create_suffix}'
  Selfassesment_update_name = f'{Selfassesment_name}_{update_suffix}'
  Selfassesment_delete_name = f'{Selfassesment_name}_{delete_suffix}'
  Selfassesment_search_name = f'{Selfassesment_name}_{search_suffix}' # fetch only
  Selfassesment_viewall_name = f'{Selfassesment_name}_{viewall_suffix}' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_name = f'{Selfassesment_Account_Submission_name}_{home_suffix}'
  Selfassesment_Account_Submission_create_name = f'{Selfassesment_Account_Submission_name}_{create_suffix}'
  Selfassesment_Account_Submission_update_name = f'{Selfassesment_Account_Submission_name}_{update_suffix}'
  Selfassesment_Account_Submission_delete_name = f'{Selfassesment_Account_Submission_name}_{delete_suffix}'
  Selfassesment_Account_Submission_search_name = f'{Selfassesment_Account_Submission_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_viewall_name = f'{Selfassesment_Account_Submission_name}_{viewall_suffix}' # fetch only
  add_all_Selfassesment_to_Selfassesment_Account_Submission_name = f'add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'

  # Tracker
  Selfassesment_Tracker_home_name = f'{Selfassesment_Tracker_name}_{home_suffix}'
  Selfassesment_Tracker_create_name = f'{Selfassesment_Tracker_name}_{create_suffix}'
  Selfassesment_Tracker_update_name = f'{Selfassesment_Tracker_name}_{update_suffix}'
  Selfassesment_Tracker_delete_name = f'{Selfassesment_Tracker_name}_{delete_suffix}'
  Selfassesment_Tracker_search_name = f'{Selfassesment_Tracker_name}_{search_suffix}' # fetch only
  Selfassesment_Tracker_viewall_name = f'{Selfassesment_Tracker_name}_{viewall_suffix}' # fetch only


# Should be passed in templates for JavaScript to fetch() api calls
class Full_URL_PATHS_WITHOUT_ARGUMENTS(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{home_suffix}/'
  Selfassesment_create_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{create_suffix}/'
  Selfassesment_update_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{update_suffix}/'
  Selfassesment_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{delete_suffix}/'
  Selfassesment_search_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{search_suffix}/' # fetch only
  Selfassesment_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_path}/{viewall_suffix}/' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{home_suffix}/'
  Selfassesment_Account_Submission_create_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{create_suffix}/'
  Selfassesment_Account_Submission_update_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{update_suffix}/'
  Selfassesment_Account_Submission_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{delete_suffix}/'
  Selfassesment_Account_Submission_search_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{search_suffix}/' # fetch only
  Selfassesment_Account_Submission_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_Account_Submission_path}/{viewall_suffix}/' # fetch only
  add_all_Selfassesment_to_Selfassesment_Account_Submission_url = f'add_all/{Selfassesment_path}/to/{Selfassesment_Account_Submission_path}/'

  # Tracker
  Selfassesment_Tracker_home_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{home_suffix}/'
  Selfassesment_Tracker_create_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{create_suffix}/'
  Selfassesment_Tracker_update_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{update_suffix}/'
  Selfassesment_Tracker_delete_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{delete_suffix}/'
  Selfassesment_Tracker_search_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{search_suffix}/' # fetch only
  Selfassesment_Tracker_viewall_url = f'/{APPLICATION_NAME}/{Selfassesment_Tracker_path}/{viewall_suffix}/' # fetch only


# Should be used in templates to reffer to links
class URL_NAMES_PREFIXED_WITH_APP_NAME(Dict_Duck_type):
  # Selfassesment
  Selfassesment_home_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{home_suffix}'
  Selfassesment_create_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{create_suffix}'
  Selfassesment_update_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{update_suffix}'
  Selfassesment_delete_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{delete_suffix}'
  Selfassesment_search_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{search_suffix}' # fetch only
  Selfassesment_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_name}_{viewall_suffix}' # fetch only

  # Selfassesment Account Submission
  Selfassesment_Account_Submission_home_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{home_suffix}'
  Selfassesment_Account_Submission_create_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{create_suffix}'
  Selfassesment_Account_Submission_update_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{update_suffix}'
  Selfassesment_Account_Submission_delete_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{delete_suffix}'
  Selfassesment_Account_Submission_search_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{search_suffix}' # fetch only
  Selfassesment_Account_Submission_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_Account_Submission_name}_{viewall_suffix}' # fetch only
  add_all_Selfassesment_to_Selfassesment_Account_Submission_name = f'{APPLICATION_NAME}:add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}'

  # Tracker
  Selfassesment_Tracker_home_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{home_suffix}'
  Selfassesment_Tracker_create_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{create_suffix}'
  Selfassesment_Tracker_update_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{update_suffix}'
  Selfassesment_Tracker_delete_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{delete_suffix}'
  Selfassesment_Tracker_search_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{search_suffix}' # fetch only
  Selfassesment_Tracker_viewall_name = f'{APPLICATION_NAME}:{Selfassesment_Tracker_name}_{viewall_suffix}' # fetch only


def gen_urls(
    prefixes=['Selfassesment', 'Selfassesment_Account_Submission', 'Selfassesment_Tracker'],
    paths=['home', 'create', 'viewall'],
    paths_w_args=['update', 'delete'],
    id_param='<int:client_id>',
    search='search',
    open='{',
    close='}'):
  for prefix in prefixes:
    for path in paths:
      print(f"{prefix}_{path}_url = f'{open}{prefix}_path{close}/{open}{path}_suffix{close}/'")
    for path in paths_w_args:
      print(f"{prefix}_{path}_url = f'{open}{prefix}_path{close}/{open}{path}_suffix{close}/{id_param}/'")
    print(f"{prefix}_search_url = f'{open}{prefix}_path{close}/{open}{search}_suffix{close}/<str:search_text>/'")
    print('')

def gen_names(
    prefixes=['Selfassesment', 'Selfassesment_Account_Submission', 'Selfassesment_Tracker'],
    paths=['home', 'create', 'update', 'delete', 'search', 'viewall'],
    open='{',
    close='}'):
  for prefix in prefixes:
    for path in paths:
      print(f"{prefix}_{path}_name = f'{open}{prefix}_name{close}_{open}{path}_suffix{close}'")
    print('')

def gen_names(
    prefixes=['Selfassesment', 'Selfassesment_Account_Submission', 'Selfassesment_Tracker'],
    paths=['home', 'create', 'update', 'delete', 'search', 'viewall'],
    open='{',
    close='}'):
  for prefix in prefixes:
    for path in paths:
      print(f"{prefix}_{path}_name = f'{open}APPLICATION_NAME{close}:{open}{prefix}_name{close}_{open}{path}_suffix{close}'")
    print('')
