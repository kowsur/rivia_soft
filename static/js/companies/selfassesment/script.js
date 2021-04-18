// collect urls
let all_url = document.querySelector('input[name="all_url"]').value;
let search_url = document.querySelector('input[name="search_url_without_argument"]').value;
let update_url = document.querySelector('input[name="update_url_without_argument"]').value;
let delete_url = document.querySelector('input[name="delete_url_without_argument"]').value;
let template_querySelector_string = 'template#data-template';
let template = document.querySelector(template_querySelector_string);

export let DATA = {
  all_url,
  search_url,
  update_url,
  delete_url
};
export default DATA;

export function get_tr_for_table(data, template=template, update_url=DATA.update_url, delete_url=DATA.delete_url) {
  // prepare table row for table using template and data
  let instance = template.content.cloneNode(true)
  let update_link = `${update_url}${data.pk}/`
  let delete_link = `${delete_url}${data.pk}/`
  instance.getElementById('edit').href = `${update_link}`
  instance.getElementById('delete').href = `${delete_link}`
  instance.getElementById('client_file_number').textContent = data.fields['client_file_number']
  instance.getElementById('client_name').textContent = data.fields['client_name']
  instance.getElementById('client_phone_number').textContent = data.fields['client_phone_number']
  instance.getElementById('date_of_registration').textContent = data.fields['date_of_registration']
  instance.getElementById('UTR').textContent = data.fields['UTR']
  instance.getElementById('HMRC_referance').textContent = data.fields['HMRC_referance']
  instance.getElementById('NINO').textContent = data.fields['NINO']
  instance.getElementById('gateway_id').textContent = data.fields['gateway_id']
  instance.getElementById('gateway_password').textContent = data.fields['gateway_password']
  instance.getElementById('address').textContent = data.fields['address']
  instance.getElementById('post_code').textContent = data.fields['post_code']
  instance.getElementById('email').textContent = data.fields['email']
  instance.getElementById('bank_name').textContent = data.fields['bank_name']
  instance.getElementById('bank_account_number').textContent = data.fields['bank_account_number']
  instance.getElementById('bank_sort_code').textContent = data.fields['bank_sort_code']
  instance.getElementById('bank_account_holder_name').textContent = data.fields['bank_account_holder_name']
  instance.getElementById('is_active').textContent = data.fields['is_active']
  return instance
}
