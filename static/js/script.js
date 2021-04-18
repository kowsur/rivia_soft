import {
  DATA, get_tr_for_table
} from './companies/selfassesment/script.js';

let template_querySelector = 'template#data-template';


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

  // when page loads load all the records
  window.addEventListener('load', () => {
    setTimeout(async ()=>{
      let all_records = await db_all_records()
      populate_with_data(all_records)
    }, 10); // search with text
  })
}


// commonly used functions
function populate_with_data(
  data_array,
  table_row_getter = get_tr_for_table,
  template_querySelector_string = template_querySelector){
  // Populate the table using the provided data

  let template = document.querySelector(template_querySelector_string) //find template

  let tbody = document.querySelector('tbody#data') // find data containser
  tbody.innerHTML='' // clear the container
  
  // populate the table
  data_array.forEach(record => {
    tbody.appendChild(table_row_getter(record, template))
  })
}

//========================================================================================
// search database
async function db_all_records(all_url = DATA.all_url) {
  const records = await fetch_url(all_url, 'GET')
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}

async function db_search_records(search_text, search_url = DATA.search_url) {
  const records = await fetch_url(`${search_url}${search_text}/`, 'GET')
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}

//========================================================================================
// SelfassesmentAccountSubmission
if (document.getElementById('search_SelfassesmentAccountSubmission')){
    document.getElementById('search_SelfassesmentAccountSubmission').addEventListener('keyup', (event)=>{
        let search_bar = document.getElementById('search_SelfassesmentAccountSubmission')
        let search_url = search_bar.dataset.url.slice(0, search_bar.dataset.url.lastIndexOf('/')+1)
        let search_text = search_bar.value
        search_text = search_text.trim()
        
        clearTimeout(typingTimer);
        if (search_text===''){
            typingTimer = setTimeout(all_SelfassesmentAccountSubmission, doneTypingInterval);
        }else{
            typingTimer = setTimeout(search_SelfassesmentAccountSubmission, doneTypingInterval, search_text, search_url);
        }
    })

    function search_SelfassesmentAccountSubmission(text, url) {
        return fetch(`${url}${text}`, {headers: {'Content-Type': 'application/json'}, method: 'GET'})
            .then(res => res.json())
            .then((json_data) => {
                let tbody = document.getElementById('data')
                tbody.innerHTML=''
                let template = document.getElementById('data-template')
                json_data.forEach((item) => {
                    tbody.appendChild(get_tr_for_table(template, item))
                })
        }).catch(err => console.error(err));
    }

    function all_SelfassesmentAccountSubmission(url='/companies/SelfassesmentAccountSubmission/all/') {
        return fetch(url, {headers: {'Content-Type': 'application/json'}, method: 'GET'})
            .then(res => res.json())
            .then((json_data) => {
                let tbody = document.getElementById('data')
                tbody.innerHTML=''
                let template = document.getElementById('data-template')
                json_data.forEach((item) => {
                    tbody.appendChild(get_tr_for_table(template, item))
                })
        }).catch(err => console.error(err));
    }

    function get_tr_for_table(template, item, update_url='/companies/SelfassesmentAccountSubmission/update/') {
        // prepare table row for table using template and item
        let instance = template.content.cloneNode(true)
        let link = `<a href="/${update_url}${item.pk}">edit</a>`
        instance.getElementById('submission_id').href = `${update_url}${item.pk}`
        instance.getElementById('client_id').innerText = item.fields['client_id']
        instance.getElementById('date_of_submission').textContent = item.fields['date_of_submission'] 
        instance.getElementById('tax_year').textContent = item.fields['tax_year'] 
        instance.getElementById('submitted_by').textContent = item.fields['submitted_by'] 
        instance.getElementById('account_prepared_by').textContent = item.fields['account_prepared_by'] 
        instance.getElementById('remarks').textContent = item.fields['remarks'] 
        instance.getElementById('paid_amount').textContent = item.fields['paid_amount'] 
        instance.getElementById('is_paid').textContent = item.fields['is_paid'] 
        instance.getElementById('is_submitted').textContent = item.fields['is_submitted'] 
        console.log(item)
        return instance
    }

    all_SelfassesmentAccountSubmission()
}



// =============================================================================================================================
// Api caller
async function fetch_url(url, req_method, data_object={'name': 'IFTAKHAR HUSAN'}, headers={'Content-Type': 'application/json'}, others={}){
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
  if (req_method.toUpperCase()=='GET'){
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
function deepCompare () {
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
