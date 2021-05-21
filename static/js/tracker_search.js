import * as methods from './script.js';

let search_url = document.querySelector('input[name="search_url_without_argument"]').value
let task_containser = document.querySelector('.task-container')
let tasks = task_containser.querySelectorAll('.task')
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
    let response = await methods.fetch_url(kwargs)
    let data = await response.json()
    
    methods.populate_with_data(data)

    let regex = /\s*\d+[\s]*/gm;
    console.log(task.innerHTML)
    task.innerHTML = task.innerHTML.replace(regex, data.length)
  })
}
