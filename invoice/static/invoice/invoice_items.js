import { deepCompare } from '/static/js/utilities.js'
import { fetch_url, db_all_records, db_search_records } from '/static/js/fetch_data.js'
import { update_options, show_option, option_selected } from '/static/js/form_search.js'


let typingTimer;
let doneTypingInterval = 300;

// find all searchable select fields
let select_elements = document.querySelectorAll('div[class="search_field"] > div.select')

// add event listeners on searchable select fields
select_elements.forEach(element => {
  // add event listenner to each item
  element.addEventListener('change', (event) => {
    // get select tag from event
    let select = event.currentTarget
    // get previous sibling input tag
    let search_box = select.previousElementSibling

    // update placeholder to currently selected value
    let selected_option_text = select.options[select.selectedIndex].textContent
    // search_box.placeholder = selected_option_text
    // search_box.value = selected_option_text
  })
}); 

// Add event lister to query database on text input
let search_boxes = document.querySelectorAll('div[class="search_field"] > [name="search"]')
search_boxes.forEach((search_box) => {
  // break early if data-do-not-attach-form-search-event-listener is set
  let doNotAttachFormSearchEventListener = search_box.hasAttribute('data-do-not-attach-form-search-event-listener')
  if (doNotAttachFormSearchEventListener) return false

  let search_field = search_box.parentElement
  let options_container = search_field.querySelector('div.select')
  
  // Add event listeners to update selected option
  let option_elements = options_container?.children||[]
  for(let option of option_elements){
    option.addEventListener('click', option_selected)
  }

  search_box.addEventListener('input', (event) => {
    // collect fields containing input and urls
    let search_field = event.currentTarget.parentElement
    let search_url_input_tag = search_field.querySelector('[name="search_url"]')
    let all_url_input_tag = search_field.querySelector('[name="all_url"]')
    let repr_format_pre_tag = search_field.querySelector('[name="repr_format"]')

    // separate info to search
    let search_text = event.currentTarget.value.trim()
    let search_url = search_url_input_tag.value
    let all_url = all_url_input_tag.value
    let repr_format = repr_format_pre_tag.value
    
    let select_element = search_field.querySelector('select')
    let options_container = search_field.querySelector('div.select')
    
    clearTimeout(typingTimer)
    typingTimer =  setTimeout(async (search_text, search_url, all_url, repr_format, select_element, options_container)=>{
      if(!deepCompare(search_text, '')){
        let records = await db_search_records(search_text, search_url)
        update_options(records, repr_format, select_element, options_container)
      }else{
        let records = await db_all_records(all_url)
        update_options(records, repr_format, select_element, options_container)
      }
    }, doneTypingInterval, search_text, search_url, all_url, repr_format, select_element, options_container)
  })
})
