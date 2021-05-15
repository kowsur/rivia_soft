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
  let search_field = search_box.parentElement
  let options_container = search_field.querySelector('div.select')
  // Add event listenners to update selected option
  for(let option of options_container.children){
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
function update_options(records, repr_format, select_element, options_container, option_element_tag='span') {
  // clear options and select default
  options_container.innerHTML = ''
  let currently_selected_option = select_element.options[select_element.selectedIndex]
  if (currently_selected_option.value){
    let selected = document.createElement(option_element_tag)
    selected.classList.add('option')
    selected.classList.add('selected')
    selected.value = currently_selected_option.value
    selected.setAttribute('data-value', currently_selected_option.value)
    selected.textContent = currently_selected_option.textContent
    options_container.appendChild(selected)
    selected.addEventListener('click', option_selected)
  }

  // update options
  for (let record of records){
    // create option
    let option = document.createElement(option_element_tag)
    option.value = record.pk
    option.setAttribute('data-value', record.pk)
    option.textContent = repr_format.format(record) // `👥{fields.client_name} 📁{fields.client_file_number} 📞{fields.personal_phone_number} ☎{fields.business_phone_number}`
    // add class
    option.classList.add('option')
    
    // add event listenner to this option
    option.addEventListener('click', option_selected)
    
    // add option in the select tag
    options_container.appendChild(option)
  }
}

//====================================================================================================================================
//
function option_selected(event) {
  // Option clicked on
  let clicked_option = event.currentTarget
  if(clicked_option.hasAttribute('disabled')) return false

  let value = clicked_option.getAttribute('data-value')
  let text = clicked_option.textContent
  let options_container = clicked_option.parentElement
  let search_field = options_container.parentElement
  
  // Create option that is selected
  let selected_option = document.createElement('option')
  selected_option.textContent = text
  selected_option.value = value
  selected_option.setAttribute('data-value', value)
  
  // Clear select element
  let select_element = search_field.querySelector('select')
  select_element.innerHTML = ''
  // add option
  select_element.add(selected_option)

  // Update options_container
  clicked_option.remove()
  clicked_option.classList.add('selected')
  if (options_container.firstElementChild){
    options_container.firstElementChild.classList.remove('selected')
  }
  options_container.prepend(clicked_option)

  // Update search_bar
  let search_bar = search_field.querySelector('input[name="search"]')
  search_bar.placeholder = text
  search_bar.value = text
  return true
}


//====================================================================================================================================
//====================================================================================================================================
// search database
async function db_all_records(all_url = '/') {
  let kwargs = {
    url: all_url,
    req_method: 'GET',
  }
  const records = await fetch_url(kwargs)
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}

async function db_search_records(search_text, search_url='/') {
  let params = {q:search_text}
  let search_param = new URLSearchParams(params).toString()
  let kwargs = {
    url: `${search_url}?${search_param}`,
    req_method: 'GET',
  }
  
  const records = await fetch_url(kwargs)
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}


//====================================================================================================================================
//====================================================================================================================================
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
