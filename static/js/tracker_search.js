import { populate_with_data } from './table.js';
import { fetch_url } from './fetch_data.js';
import DATA from './parse_data.js';


let search_url = DATA['search_url']
let task_container = document.querySelector('.task-container')
let tasks = task_container.querySelectorAll('.task')
for (let task of tasks){
  task.addEventListener('click', async (event) => {
    let task = event.currentTarget
    let param = task.getAttribute('data-tasks')
  
    // prepare url to fetch
    let url = search_url
    let params = {tasks: param}
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
    
    populate_with_data(data)

    let counts = task.querySelector('#task-count')
    counts.innerHTML = data.length
  })
}
