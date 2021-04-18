from django.db import models

def get_field_names_from_model(django_model:models.Model):
  field_names = []
  for field in django_model._meta.fields:
    field_names.append(field.name)
  return field_names

def get_header_name_from_field_name(django_model, field_name):
  return django_model._meta.get_field(field_name).verbose_name


def generate_template_tag_for_model(django_model:models.Model, pk_filed='id', exclude_fields=('is_updated','created_by'),tag_name='data-template', tag_id='data-template'):
  model_fields = get_field_names_from_model(django_model)
  inner_template_tr = """
  <td class="data-cell data-id" >
    <a class="w-max" href="" id='edit'>
      <svg class="edit-icon" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
      <g>
        <g>
          <g>
            <path d="M352.459,220c0-11.046-8.954-20-20-20h-206c-11.046,0-20,8.954-20,20s8.954,20,20,20h206
              C343.505,240,352.459,231.046,352.459,220z"/>
            <path d="M126.459,280c-11.046,0-20,8.954-20,20c0,11.046,8.954,20,20,20H251.57c11.046,0,20-8.954,20-20c0-11.046-8.954-20-20-20
              H126.459z"/>
            <path d="M173.459,472H106.57c-22.056,0-40-17.944-40-40V80c0-22.056,17.944-40,40-40h245.889c22.056,0,40,17.944,40,40v123
              c0,11.046,8.954,20,20,20c11.046,0,20-8.954,20-20V80c0-44.112-35.888-80-80-80H106.57c-44.112,0-80,35.888-80,80v352
              c0,44.112,35.888,80,80,80h66.889c11.046,0,20-8.954,20-20C193.459,480.954,184.505,472,173.459,472z"/>
            <path d="M467.884,289.572c-23.394-23.394-61.458-23.395-84.837-0.016l-109.803,109.56c-2.332,2.327-4.052,5.193-5.01,8.345
              l-23.913,78.725c-2.12,6.98-0.273,14.559,4.821,19.78c3.816,3.911,9,6.034,14.317,6.034c1.779,0,3.575-0.238,5.338-0.727
              l80.725-22.361c3.322-0.92,6.35-2.683,8.79-5.119l109.573-109.367C491.279,351.032,491.279,312.968,467.884,289.572z
              M333.776,451.768l-40.612,11.25l11.885-39.129l74.089-73.925l28.29,28.29L333.776,451.768z M439.615,346.13l-3.875,3.867
              l-28.285-28.285l3.862-3.854c7.798-7.798,20.486-7.798,28.284,0C447.399,325.656,447.399,338.344,439.615,346.13z"/>
            <path d="M332.459,120h-206c-11.046,0-20,8.954-20,20s8.954,20,20,20h206c11.046,0,20-8.954,20-20S343.505,120,332.459,120z"/>
          </g>
        </g>
      </g>
      </svg>
    <a class="w-max" href="" id='delete'>
      <svg class="delete-icon" enable-background="new 0 0 512.016 512.016" height="512" viewBox="0 0 512.016 512.016" width="512" xmlns="http://www.w3.org/2000/svg">
        <g>
          <path d="m448.199 164.387h-236.813l106.048-106.048c5.858-5.858 5.858-15.356 0-21.215l-26.872-26.872c-13.669-13.669-35.831-13.669-49.501 0l-27.63 27.631-14.144-14.144c-15.596-15.597-40.975-15.596-56.572 0l-55.158 55.158c-15.597 15.597-15.597 40.976 0 56.573l14.143 14.144-27.63 27.63c-13.669 13.669-13.669 35.831 0 49.501l26.872 26.872c5.857 5.858 15.356 5.859 21.214 0l38.021-38.021v231.416c0 35.901 29.104 65.005 65.005 65.005h158.012c35.901 0 65.005-29.104 65.005-65.005zm-325.284-35.989-14.143-14.143c-3.899-3.899-3.899-10.244 0-14.144l55.158-55.158c3.9-3.9 10.245-3.899 14.143 0l14.143 14.144zm129.533 299.612c0 8.285-6.716 15.001-15.001 15.001s-15.001-6.716-15.001-15.001v-179.616c0-8.285 6.716-15.001 15.001-15.001s15.001 6.716 15.001 15.001zm66.741 0c0 8.285-6.716 15.001-15.001 15.001s-15.001-6.716-15.001-15.001v-179.616c0-8.285 6.716-15.001 15.001-15.001s15.001 6.716 15.001 15.001zm66.741 0c0 8.285-6.716 15.001-15.001 15.001s-15.001-6.716-15.001-15.001v-179.616c0-8.285 6.716-15.001 15.001-15.001s15.001 6.716 15.001 15.001z"/>
          <path d="m320.898 113.548c-9.151 3.19-15.571 11.361-16.631 20.842h143.932v-24.932c0-17.119-16.845-29.167-33.022-23.682l-93.968 27.672c-.101.029-.211.069-.311.1z"/>
        </g>
      </svg>
    </a>
  </td>
  """

  for field in model_fields:
    if not field == pk_filed and field not in exclude_fields:
      inner_template_tr += f'<td class="data-cell" id="{field}"></td>\n'
  
  template_tag = f"""
  <template id="{tag_id}" name="{tag_name}">
    <tr class="data-row">
    {inner_template_tr}
    </tr>
  </template>
  """
  return template_tag


def generate_data_container_table(django_model:models.Model, pk_filed='id', exclude_fields=('is_updated','created_by'),tag_name='data-template', tag_id='data-template'):
  model_fields = get_field_names_from_model(django_model)
  inner_header_tr = """
  <th class="data-cell stick-top data-id">#</th>
  """

  for field in model_fields:
    if not field == pk_filed and field not in exclude_fields:
      header_name = get_header_name_from_field_name(django_model, field)
      inner_header_tr += f'<th class="data-cell stick-top data-id">{header_name}</th>\n'
  
  header_tr = f"""
  <tr class="data-row data-head-row">
  {inner_header_tr}
  </tr>
  """

  table_tag = f"""
  <div class="data-wrapper">
    <table class="data-container">
      <thead class="data-head">
          {header_tr}
      </thead>
      <tbody id="data">
          
      </tbody>
    </table>
  </div>
  """
  return table_tag