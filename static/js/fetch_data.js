import { deepCompare, catchErrorAndLog } from "./utilities.js"
import DATA from "./parse_data.js";


//====================================================================================================================================
// get data from backend
export async function db_all_records(all_url = DATA.all_url) {
  let kwargs = {
    url: all_url,
    req_method: 'GET'
  }
  const records = await fetch_url(kwargs)
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}

export async function db_search_records(search_text, search_url = DATA.search_url) {
  let params = {q:search_text}
  let search_param = new URLSearchParams(params).toString()
  let kwargs = {
    url: `${search_url}?${search_param}`,
    req_method: 'GET'
  }
  const records = await fetch_url(kwargs)
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}
export async function db_search_records_client_id(client_id, search_url = DATA.search_url) {
  let params = {client_id: client_id}
  let search_param = new URLSearchParams(params).toString()
  let kwargs = {
    url: `${search_url}?${search_param}`,
    req_method: 'GET'
  }
  const records = await fetch_url(kwargs)
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}


// =============================================================================================================================
// Api caller
export async function fetch_url({url, req_method, data_object={}, headers={'Content-Type': 'application/json'}, others={}}){
  catchErrorAndLog(showLoadingIndicator)
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
    catchErrorAndLog(hideLoadingIndicator)
    return response
  }else{
    // send other requests
    const response = await fetch( url, {
        method: req_method,
        headers: headers,
        body: data_object,
        ...others
      })
    catchErrorAndLog(hideLoadingIndicator())
    return response
  }
}

// =============================================================================================================================
// Show and hide loading indicator when data is loading
const loading_indicator_selector = '#loading-indicator'

export function showLoadingIndicator(){
  let loading_indicator = document.querySelector(loading_indicator_selector)
  if (!loading_indicator!==null) loading_indicator.classList.remove('hidden')
}

export function hideLoadingIndicator(){
  let loading_indicator = document.querySelector(loading_indicator_selector)
  if (loading_indicator!==null) loading_indicator.classList.add('hidden')
}
