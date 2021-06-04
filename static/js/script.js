//table cell compare attribute name = "data-cmp"

dayjs.extend(window.dayjs_plugin_customParseFormat)

// datetime format
const time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone // get user timezone
const time_format = "HH:mm"
const date_format = "YYYY-MM-DD"
const datetime_format = `${date_format} ${time_format}`

const search_date_format = "YYYY-MM-DD"
const search_time_format = "HH:mm:ss:SSS"
const search_datetime_format = `${date_format} ${time_format}`

// let date = dayjs()
// console.log(date.format(datetime_format))
// console.log(date.format(date_format))

//Cache foriegn key fields
const CACHE = {}
const loading_indicator_selector = '#loading-indicator'

// clear messsage after 10 seconds
let delete_message_after = 10000 //milisecond
setTimeout(function(){
  let messages = document.getElementsByClassName('message')
  if (messages){
    for (let element of messages){
      element.remove()
    }
  };
}, delete_message_after);

let template_querySelector = 'template#data-template';

// collect urls
let all_url = document.querySelector('input[name="all_url"]').value;
let search_url = document.querySelector('input[name="search_url_without_argument"]').value;
let update_url = document.querySelector('input[name="update_url_without_argument"]').value;
let delete_url = document.querySelector('input[name="delete_url_without_argument"]').value;

// get fields
let fields = JSON.parse(document.querySelector('pre[name="model_fields"]').innerText.replaceAll("'",'"'))
let template_querySelector_string = 'template#data-template';
let template = document.querySelector(template_querySelector_string);
let DATA = {
  all_url,
  search_url,
  update_url,
  delete_url
};

// ================================================================================================
// Handle reload
document.querySelector('.action-reload').addEventListener('click', async (event) => {
  loadAllRecords()
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
  search_bar.addEventListener('input', (event)=>{
    let search_url = DATA.search_url
    let search_text = search_bar.value.trim()
    
    // reset timer to prevent extra search
    clearTimeout(typingTimer);
    // set the timer again to call api after doneTypingInterval
    if (search_text===''){
      typingTimer = setTimeout( async () => {
        let all_records = await db_all_records()
        populate_with_data(all_records)
      }, doneTypingInterval); // Get all the records
    }else{
      typingTimer = setTimeout(async (search_text, search_url)=>{
        let search_records = await db_search_records(search_text, search_url)
        populate_with_data(search_records)
      }, doneTypingInterval, search_text, search_url); // search with text
    }
  })

  // OpenSearch
  let current_url = window.location.href
  let url = new URL(current_url)
  let open_query = url.searchParams.get('q')
  let client_id = url.searchParams.get('client_id')
  if (client_id) {client_id = client_id.trim()}
  if (open_query){open_query=open_query.trim()}

  if (client_id){
    typingTimer = setTimeout(async (client_id, search_url)=>{
      let search_records = await db_search_records_client_id(client_id, search_url)
      populate_with_data(search_records)
    }, 10, client_id, (DATA.search_url)); // search with text
  }
  else if (open_query){
    typingTimer = setTimeout(async (search_text, search_url)=>{
      let search_records = await db_search_records(search_text, search_url)
      populate_with_data(search_records)
    }, 10, open_query, DATA.search_url); // search with text
  }else{
    // when page loads load all the records
    loadAllRecords();
  }
}

export function loadAllRecords(){
  let loading_indicator = document.querySelector(loading_indicator_selector)
  loading_indicator.classList.remove('hidden')
  setTimeout(async ()=>{
    let all_records = await db_all_records()
    populate_with_data(all_records)
  }, 10); // search with text
}

//====================================================================================================================================
//====================================================================================================================================
//====================================================================================================================================
// commonly used functions
export async function get_tr_for_table(data, template=template, model_fields=fields, update_url=DATA.update_url, delete_url=DATA.delete_url) {
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
    let formated_text = document.createElement('pre')
    let td = instance.getElementById(field)
    if (!td) continue

    let data_field = td.getAttribute('data-field')
    if (data_field) {
      let field_data_format = `{${data_field}}`
      field_data = field_data_format.format(data)
    }
    if (field_data==null) continue

    formated_text.innerHTML = makeSafeHTML(`${field_data}`)
    
    td.classList.add('whitespace-nowrap') // show text in one line
    
    // data to compare elements in table_sort.js
    td.setAttribute('data-cmp', field_data)

    
    // Foreign Data
    let data_url = td.getAttribute('data-url')
    let repr_format = td.getAttribute('data-repr-format')
    if (data_url && field_data){
      //this is a foreign key field. fetch the data and format it
      (!URL_HasQueryParams(data_url)) ? data_url = `${data_url}${field_data}/`: data_url = `${data_url}${field_data}`

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

    // date data
    let date = dayjs(field_data)
    if (!isNaN(date) && typeof(field_data)==="string" && ((field_data[4]==='-' && field_data[7]==='-') || field_data[2]===':')){
      //this is date field so show it in local format 

      // when field_data.length > 10 it's a datetime
      // if (field_data.length>10) td.textContent = date.toLocaleString()
      if (field_data.length>10) td.textContent = date.format(datetime_format)
      
      // when field_data.length == 10 it's a date
      // if (field_data.length==10) td.textContent = date.toLocaleDateString()
      if (field_data.length==10) td.textContent = date.format(date_format)

      // when field_data.length < 10 it's a time
      // if (field_data.length<10) td.textContent = date.toLocaleTimeString()
      if (field_data.length<10) td.textContent = date.format(time_format)
      
      // //GMTString
      // console.log(date.toGMTString())
      // console.log(date.toGMTString().slice(0, 16))
      continue
    }

    // show preformatted text
    td.appendChild(formated_text)

    // pretty-format text
    td.classList.add('whitespace-normal')
    td.style.textAlign = 'justify'
    td.style.minWidth = `${field_data.length+1}ch`
    if (field_data.length >= 37){
      td.classList.remove('whitespace-nowrap')
      td.style.minWidth = '37ch'
      formated_text.style.maxWidth = '37ch'
      formated_text.style.whiteSpace = 'pre-wrap'
    }

  }
  return instance;
}

export async function populate_with_data(
  data_array,
  table_row_getter = get_tr_for_table,
  template_querySelector_string = template_querySelector){
  let template = document.querySelector(template_querySelector_string) //find template
  
  let tbody = document.querySelector('tbody#data') // find data containser
  tbody.innerHTML='' // clear the container
  
  let loading_indicator = document.querySelector(loading_indicator_selector)
  loading_indicator.classList.remove('hidden')
  // Populate the table using the provided data
  for (let record of data_array){
    let table_row = await table_row_getter(record, template)
    tbody.appendChild(table_row)
  }
  loading_indicator.classList.add('hidden')
}

//====================================================================================================================================
//====================================================================================================================================
//====================================================================================================================================
// search database
export async function db_all_records(all_url = DATA.all_url) {
  let loading_indicator = document.querySelector(loading_indicator_selector)
  loading_indicator.classList.remove('hidden')

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
  let loading_indicator = document.querySelector(loading_indicator_selector)
  loading_indicator.classList.remove('hidden')

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
  let loading_indicator = document.querySelector(loading_indicator_selector)
  loading_indicator.classList.remove('hidden')

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


// Url has query params
function URL_HasQueryParams(url){
  let parsed_url = new URL(url, document.location)
  return Boolean(parsed_url.search.trim())
}

// Make markup safe
function makeSafeHTML(string){
  return string.replace(/&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
}


// Javascript object compare
export function deepCompare () {
  var i, l, leftChain, rightChain;

  function compare2Objects (x, y) {
    var p;

    // remember that NaN === NaN returns false
    // and isNaN(undefined) returns true
    if (isNaN(x) && isNaN(y) && typeof x === 'number' && typeof y === 'number') {
         return true;
    }

    // Compare primitives and functions.     
    // Check if both arguments link to the same object.
    // Especially useful on the step where we compare prototypes
    if (x === y) {
        return true;
    }

    // Works in case when functions are created in constructor.
    // Comparing dates is a common scenario. Another built-ins?
    // We can even handle functions passed across iframes
    if ((typeof x === 'function' && typeof y === 'function') ||
       (x instanceof Date && y instanceof Date) ||
       (x instanceof RegExp && y instanceof RegExp) ||
       (x instanceof String && y instanceof String) ||
       (x instanceof Number && y instanceof Number)) {
        return x.toString() === y.toString();
    }

    // At last checking prototypes as good as we can
    if (!(x instanceof Object && y instanceof Object)) {
        return false;
    }

    if (x.isPrototypeOf(y) || y.isPrototypeOf(x)) {
        return false;
    }

    if (x.constructor !== y.constructor) {
        return false;
    }

    if (x.prototype !== y.prototype) {
        return false;
    }

    // Check for infinitive linking loops
    if (leftChain.indexOf(x) > -1 || rightChain.indexOf(y) > -1) {
         return false;
    }

    // Quick checking of one object being a subset of another.
    // todo: cache the structure of arguments[0] for performance
    for (p in y) {
        if (y.hasOwnProperty(p) !== x.hasOwnProperty(p)) {
            return false;
        }
        else if (typeof y[p] !== typeof x[p]) {
            return false;
        }
    }

    for (p in x) {
        if (y.hasOwnProperty(p) !== x.hasOwnProperty(p)) {
            return false;
        }
        else if (typeof y[p] !== typeof x[p]) {
            return false;
        }

        switch (typeof (x[p])) {
            case 'object':
            case 'function':

                leftChain.push(x);
                rightChain.push(y);

                if (!compare2Objects (x[p], y[p])) {
                    return false;
                }

                leftChain.pop();
                rightChain.pop();
                break;

            default:
                if (x[p] !== y[p]) {
                    return false;
                }
                break;
        }
    }

    return true;
  }

  if (arguments.length < 1) {
    return true; //Die silently? Don't know how to handle such case, please help...
    // throw "Need two or more arguments to compare";
  }

  for (i = 1, l = arguments.length; i < l; i++) {

      leftChain = []; //Todo: this can be cached
      rightChain = [];

      if (!compare2Objects(arguments[0], arguments[i])) {
          return false;
      }
  }

  return true;
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}


// source https://gist.github.com/poxip/90a9787be621eeddb82a
/**
 * Python-like string format function
 * @param {String} str - Template string.
 * @param {Object} data - Data to insert strings from.
 * @returns {String}
 */
 var format = function(str, data) {
  var re = /{([^{}]+)}/g;

  return str.replace(/{([^{}]+)}/g, function(match, val) {
    var prop = data;
    val.split('.').forEach(function(key) {
      prop = prop[key];
    });

    return prop;
  });
};

/**
 * Python-like format method
 * @param {Object} data - Data to insert strings from.
 * @returns {String}
 */
String.prototype.format = function(data) {
  return format(this, data);
};
