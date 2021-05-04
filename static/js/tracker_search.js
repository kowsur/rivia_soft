let search_url = document.querySelector('input[name="search_url_without_argument"]').value
let task_containser = document.querySelector('.task-container')
let tasks = task_containser.querySelectorAll('.task')
for (let task of tasks){
  task.addEventListener('click', (event) => {
    let task = event.currentTarget
    let param = task.getAttribute('data-query_param')
  
    // prepare url to fetch
    let url = search_url
    let params = {}
    params[param] = true

    let search_param = new URLSearchParams(params).toString();

    url = `${url}?${search_param}`
    console.log(url)
    fetch(url, {
      method:'GET', 
      headers: {'Content-Type': 'application/json'}
    }).then( response => console.log(response))
  })
}


// ============================================================================================================================================
// Api caller
async function fetch_url(url, req_method, data_object={'name': 'IFTAKHAR HUSAN'}, headers={ 'Content-Type': 'application/json', }, others={}){
  req_method = req_method.toUpperCase()
  if (deepCompare(others, {})){
    others = {
      credentials: 'same-origin',
      cache: 'no-cache',
      mode: 'cors', // no-cors, *cors, same-origin
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin,
                                    // same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    }
  }
  if (req_method==='GET'){
    // send GET request
    const response = await fetch( url, {
      method: req_method,
      headers: headers,
      ...others
    })
    return response
  }else{
    // send other requests
    const response = await fetch( url, {
        method: req_method,
        headers: headers,
        body: data_object,
        ...others
      })
    return response
  }
}
