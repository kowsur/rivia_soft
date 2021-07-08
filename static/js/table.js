import DATA from './parse_data.js'
import { fetch_url } from './fetch_data.js';
import { makeSafeHTML, URL_HasQueryParams, dateFormat } from './utilities.js';
//Cache foriegn key fields
const CACHE = {}


let template_querySelector = 'template#data-template';
let template = document.querySelector(template_querySelector);
// Prepare row for data table
export async function get_tr_for_table(data, template=template, model_fields=DATA.model_fields, update_url=DATA.update_url, delete_url=DATA.delete_url) {
  // prepare table row for table using template and data
  let instance = template.content.cloneNode(true)
  let serial_num = instance.getElementById('pk')
  if (serial_num) serial_num.textContent = data.pk

  let update_link = `${update_url}${data.pk}/`
  let delete_link = `${delete_url}${data.pk}/`
  instance.getElementById('edit').href = `${update_link}`
  instance.getElementById('delete').href = `${delete_link}`

  // fill the template
  for (let field of model_fields){
    let field_data = data.fields[field]
    let formatted_text = document.createElement('pre')
    let td = instance.getElementById(field)
    if (!td) continue

    let data_field = td.getAttribute('data-field')
    if (data_field) {
      let field_data_format = `{${data_field}}`
      field_data = field_data_format.format(data)
    }
    if (field_data==null) continue

    formatted_text.innerHTML = makeSafeHTML(`${field_data}`)
    
    td.classList.add('whitespace-nowrap') // show text in one line
    
    // data to compare elements in table_sort.js
    td.setAttribute('data-cmp', field_data)

    
    // Foreign Data
    let data_url = td.getAttribute('data-url')
    let repr_format = td.getAttribute('data-repr-format')
    if (data_url && field_data){
      //this is a foreign key field. fetch the data and format it
      (!URL_HasQueryParams(data_url)) ? data_url = `${data_url}${field_data}/`: data_url = `${data_url}${field_data}`
      if (field_data=='null') continue

      let kwargs = {
        url: data_url,
        req_method: 'GET'
      }
      if (!CACHE[data_url]){
        fetch_url(kwargs).then(response => response.json()).then(resp => {
          CACHE[data_url] = resp
          let string = repr_format.format(CACHE[data_url])
          let len = parseInt(string)
        
          td.textContent = string
          td.removeAttribute('data-url')
          td.removeAttribute('data-repr-format')
          td.setAttribute('data-cmp', string)
          
          let hrefURL = td.getAttribute('data-href-url')
          if (hrefURL){
            td.innerHTML = `<a href="${hrefURL}${field_data}">${makeSafeHTML(string)}</a>`
          }

          if (field=='incomplete_tasks'){
            td.innerHTML = `<a href="/companies/SATrc/home/?client_id=${data.pk}">${string}</a>`
          }
          if (len>0) {
            td.style.color = 'red'
            td.style.fontWeight = 'bold'
          }
        })
      }else{
        let string = repr_format.format(CACHE[data_url])
        let len = parseInt(string)

        td.textContent = string
        td.removeAttribute('data-url')
        td.removeAttribute('data-repr-format')
        td.setAttribute('data-cmp', string)
        
        let hrefURL = td.getAttribute('data-href-url')
        if (hrefURL){
            td.innerHTML = `<a href="${hrefURL}${field_data}">${makeSafeHTML(string)}</a>`
          }
        if (field=='incomplete_tasks'){
          td.innerHTML = `<a href="/companies/SATrc/home/?client_id=${data.pk}">${string}</a>`
        }
        if (len>0) td.style.color = 'red'
      }
      continue
    }

    // Number data
    if (typeof field_data == 'number'){
      td.textContent = field_data
      continue
    }
    
    // Boolean data
    if(typeof field_data === "boolean"){
      //data is boolean so show it as checkbox
      let checked_checkbox = `<input type="checkbox" checked="" disabled>`
      let unchecked_checkbox = `<input type="checkbox" disabled>`
      if(field_data) {td.innerHTML=checked_checkbox} else{td.innerHTML=unchecked_checkbox}
      continue
    }

    // date/time data
    let date = dayjs(field_data)
    if (!isNaN(date) && typeof(field_data)==="string" && ((field_data[4]==='-' && field_data[7]==='-') || field_data[2]===':')){
      //this is date field so show it in local format 
      td.textContent = dateFormat(date, field_data)
      continue
    }

    // show preformatted text
    td.appendChild(formatted_text)

    // pretty-format text
    td.classList.add('whitespace-normal')
    td.style.textAlign = 'justify'
    td.style.minWidth = `${field_data.length+1}ch`
    if (field_data.length >= 37){
      td.classList.remove('whitespace-nowrap')
      td.style.minWidth = '37ch'
      formatted_text.style.maxWidth = '37ch'
      formatted_text.style.whiteSpace = 'pre-wrap'
    }

  }
  return instance;
}

// Update table date with the provided data
export async function populate_with_data(
  data_array,
  template_querySelector_string = template_querySelector,
  model_fields=DATA.model_fields,
  update_url=DATA.update_url,
  delete_url=DATA.delete_url,
  clear_table_before_insertion=true,

  ){
  let template = document.querySelector(template_querySelector_string) //find template
  
  let tbody = document.querySelector('tbody#data') // find data container
  if (clear_table_before_insertion) tbody.innerHTML='' // clear the container
  
  // Populate the table using the provided data
  for (let record of data_array){
    let table_row = await get_tr_for_table(record, template, model_fields, update_url, delete_url)
    tbody.appendChild(table_row)
  }
}
