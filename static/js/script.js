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
  if (open_query){open_query=open_query.trim()}

  if (open_query){
    typingTimer = setTimeout(async (search_text, search_url)=>{
      let search_records = await db_search_records(search_text, search_url)
      populate_with_data(search_records)
    }, 10, open_query, DATA.search_url); // search with text
  }else{
    // when page loads load all the records
    window.addEventListener('load', () => {
      setTimeout(async ()=>{
        let all_records = await db_all_records()
        populate_with_data(all_records)
      }, 10); // search with text
    })
  }
}


//====================================================================================================================================
//====================================================================================================================================
//====================================================================================================================================
// commonly used functions
export function get_tr_for_table(data, template=template, model_fields=fields, update_url=DATA.update_url, delete_url=DATA.delete_url) {
  // prepare table row for table using template and data
  let instance = template.content.cloneNode(true)

  let update_link = `${update_url}${data.pk}/`
  let delete_link = `${delete_url}${data.pk}/`
  instance.getElementById('edit').href = `${update_link}`
  instance.getElementById('delete').href = `${delete_link}`
  
  // fill the template
  for (let field of model_fields){
    let td = instance.getElementById(field)
    // when field exists in the template fill it in with data
    if (td){
      td.classList.add('whitespace-nowrap')
      let field_data = data.fields[field]
      if (!(field_data===true || field_data===false)){
        // field data is text so show it as text
        // if the field is foriegn key of other model the it should contain data-url and data-repr-format
        let data_url = td.getAttribute('data-url')
        let repr_format = td.getAttribute('data-repr-format')
        if (data_url && field_data){
          data_url = `${data_url}${field_data}/`
          let kwargs = {
            url: data_url,
            req_method: 'GET'
          }
          fetch_url(kwargs).then(response => response.json()).then(data => {
            td.textContent = repr_format.format(data)
          })
        }else{
          td.textContent = field_data
        }
        
        if (field_data && field_data.length>=30){
          td.classList.remove('whitespace-nowrap')
          td.classList.add('whitespace-normal')
          td.style.minWidth = '35ch'
        }
      }else{
        //data is boolean so show it as checkbox
        let checked_checkbox = `<input type="checkbox" checked="" disabled>`
        let unchecked_checkbox = `<input type="checkbox" disabled>`
        if(field_data) {td.innerHTML=checked_checkbox} else{td.innerHTML=unchecked_checkbox}
      } 
    }
  }return instance; //return table row instance
}

export async function populate_with_data(
  data_array,
  table_row_getter = get_tr_for_table,
  template_querySelector_string = template_querySelector){
  // Populate the table using the provided data

  let template = document.querySelector(template_querySelector_string) //find template

  let tbody = document.querySelector('tbody#data') // find data containser
  tbody.innerHTML='' // clear the container
  
  // populate the table
  for (let record of data_array){
    let table_row = table_row_getter(record, template)
    tbody.appendChild(table_row)
  }
}

//====================================================================================================================================
//====================================================================================================================================
//====================================================================================================================================
// search database
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
