import { populate_with_data } from './table.js';
import { fetch_url } from './fetch_data.js';
import DATA from './parse_data.js';


let search_url = DATA['search_url']
let task_container = document.querySelector('.task-container')
let tasks = task_container.querySelectorAll('.task')

async function handleTaskClick(event){
  let task = event.currentTarget
  let param = task.getAttribute('data-tasks')

  // prepare url to fetch
  let url = search_url
  let params = {tasks: param, tax_year: DATA.tax_year}
  // params['q'] = 'ifta'

  let search_param = new URLSearchParams(params).toString()
  url = `${url}?${search_param}`

  let kwargs = {
    url: url,
    req_method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }
  let response = await fetch_url(kwargs)
  let data = await response.json()

  if(!event?.detail?.update_counters_only) populate_with_data(data)

  let counts = task.querySelector('#task-count')
  counts.innerText = data.length
}

for (let task of tasks){
  if(!task.hasAttribute('data-disabled')) task.addEventListener('click', handleTaskClick)
}
