import { fetch_url, db_all_records, db_search_records, db_search_records_client_id } from './fetch_data.js'
import { populate_with_data } from './table.js'
import { removeAllEventListeners } from './utilities.js'
import DATA from './parse_data.js'


const Limited = DATA.Limited
const limited_template_query_string = 'template#limited_tracker_template'
const Selfassesment = DATA.Selfassesment
const selfassesment_template_query_string = 'template#selfassesment_tracker_template'

// // Merged tracker Create Options
// const create_btn = document.querySelector('#merged_tracker_create')
// const create_options = document.querySelector('#create_options_container')
// const create_options_close_btn = document.querySelector('#merged_tracker_create_options_close')

// create_btn.addEventListener('click', (event) => {
//   event.preventDefault()
//   create_options.style.display = 'flex'
// })

// create_options_close_btn.addEventListener('click', (event)=>{
//   event.preventDefault()
//   create_options.style.display = 'none'
// })

//table cell compare attribute name = "data-cmp"

// clear messsage after 10 seconds
let delete_message_after = 10000 //milisecond
setTimeout(function(){
  let messages = document.querySelectorAll('.message')
  if (messages){
    for (let element of messages){
      element.remove()
    }
  };
}, delete_message_after);

// ================================================================================================
// Handle reload
document.querySelector('.action-reload').addEventListener('click', async (event) => {
  loadAllTrackers()
})

// Search functionality
//setup before functions
let typingTimer;                  //timer identifier
//                miliseconds * seconds
let doneTypingInterval = 1000;//time in ms (4/5 seconds)
//on keyup, start the countdown
// document.getElementById('element-id').addEventListener('keyup', () => {
//     clearTimeout(typingTimer);
//     if (myInput.value) {
//         typingTimer = setTimeout(search_function, doneTypingInterval);
//     }
// });
const search_bar = document.querySelector('input[name="search"]');
if (search_bar){
  let limited_search_url = Limited.search_url
  let selfassesment_search_url = Selfassesment.search_url
  
  search_bar.addEventListener('input', (event)=>{  
    let search_text = search_bar.value.trim()

    // reset timer to prevent extra search
    clearTimeout(typingTimer);
    // set the timer again to call api after doneTypingInterval
    if (search_text===''){
      typingTimer = setTimeout( async () => {
        loadAllTrackers()
      }, doneTypingInterval); // Get all the records
    }else{
     searchTrackers(doneTypingInterval, search_text, limited_search_url, selfassesment_search_url)
    }
  })

  // OpenSearch
  let current_url = window.location.href
  let url = new URL(current_url)
  let open_query = url.searchParams.get('q')
  if (open_query){open_query=open_query.trim()}

  if (open_query){
    searchTrackers(0, open_query, limited_search_url, selfassesment_search_url)
  }else{
    // when page loads load all the records
    loadAllTrackers();
  }
}

export function loadAllTrackers(){
  setTimeout(async ()=>{
    let all_records = await db_all_records(Limited.viewall_url)
    populate_with_data(all_records, limited_template_query_string, Limited.model_fields, Limited.update_url, Limited.delete_url, true)
    all_records = await db_all_records(Selfassesment.viewall_url)
    populate_with_data(all_records, selfassesment_template_query_string, Selfassesment.model_fields, Selfassesment.update_url, Selfassesment.delete_url, false)
  }, 10); // search with text
}

export function searchTrackers(doneTypingInterval, search_text, limited_search_url, selfassesment_search_url){
  typingTimer = setTimeout(async (search_text, limited_search_url, selfassesment_search_url)=>{
    let limited_search_records = await db_search_records(search_text, limited_search_url)
    populate_with_data(limited_search_records, limited_template_query_string, Limited.model_fields, Limited.update_url, Limited.delete_url, true)

    let selfassesment_search_records = await db_search_records(search_text, selfassesment_search_url)
    populate_with_data(selfassesment_search_records, selfassesment_template_query_string, Selfassesment.model_fields, Selfassesment.update_url, Selfassesment.delete_url, false)
  }, doneTypingInterval, search_text, limited_search_url, selfassesment_search_url); // search with text
}


let task_container = document.querySelector('.task-container')
let tasks = task_container.querySelectorAll('.task')
for (let task of tasks){
  task = removeAllEventListeners(task)
  task.addEventListener('click', async (event) => {
    let task = event.currentTarget
    let param = task.getAttribute('data-tasks')
  
    // prepare url to fetch
    let params = {tasks: param}
    // params['q'] = 'ifta'

    let search_param = new URLSearchParams(params).toString()

    let limited_data = await searchTrackersTasks(Limited.search_url, search_param)
    populate_with_data(limited_data, limited_template_query_string, Limited.model_fields, Limited.update_url, Limited.delete_url, true)
    
    let selfassesment_data = await searchTrackersTasks(Selfassesment.search_url, search_param)
    populate_with_data(selfassesment_data, selfassesment_template_query_string, Selfassesment.model_fields, Selfassesment.update_url, Selfassesment.delete_url, false)

    let counts = task.querySelector('#task-count')
    counts.innerHTML = limited_data.length + selfassesment_data.length
  })
}


async function searchTrackersTasks(
  search_url,
  search_param){
  let url = `${search_url}?${search_param}`
  
  let kwargs = {
    url: url,
    req_method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }
  let response = await fetch_url(kwargs)
  let data = await response.json()
  return data
}
