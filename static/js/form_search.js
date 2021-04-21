let typingTimer;
let doneTypingInterval = 300;

// find all searchable select fields
let select_elements = document.querySelectorAll('div[class="search_field"] > select')

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
    search_box.placeholder = selected_option_text
    // search_box.value = selected_option_text
  })
}); 

let search_boxes = document.querySelectorAll('div[class="search_field"] > [name="search"]')
search_boxes.forEach(search_box => 
  search_box.addEventListener('input', (event) => {
    let search_field = event.currentTarget.parentElement
    let search_url_input_tag = search_field.querySelector('[name="search_url"]')
    let all_url_input_tag = search_field.querySelector('[name="all_url"]')
    let repr_format_pre_tag = search_field.querySelector('[name="repr_format"]')

    let search_text = event.currentTarget.value.trim()
    let search_url = search_url_input_tag.value
    let all_url = all_url_input_tag.value
    let repr_format = repr_format_pre_tag.value
    let select_element = event.currentTarget.nextElementSibling
    
    clearTimeout(typingTimer)
    typingTimer =  setTimeout(async (search_text, search_url, all_url, repr_format, select)=>{
      if(!deepCompare(search_text, '')){
        let records = await db_search_records(search_text, search_url)
        update_options(records, repr_format, select)
      }else{
        let records = await db_all_records(all_url)
        update_options(records, repr_format, select)
      }
    }, doneTypingInterval, search_text, search_url, all_url, repr_format, select_element)
  })
)
function update_options(records, repr_format, select_element) {
  // clear options and select default
  let currently_selected_option = select_element.options[select_element.selectedIndex]

  // let default_option = `<option value="" selected>---------</option>`
  select_element.innerHTML = ''
  select_element.add(currently_selected_option)

  // update options
  for (let record of records){
    // create option
    let option = document.createElement('option')
    option.value = record.pk
    option.textContent = repr_format.format(record) // `👥${client_name} 📞${client_phone_number}`
    
    // add option in the select tag
    select_element.add(option)
  }
}






//====================================================================================================================================
//====================================================================================================================================
// search database
async function db_all_records(all_url = '/') {
  const records = await fetch_url(all_url, 'GET')
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}

function db_search_records(search_text, search_url='/') {
  const records = fetch_url(`${search_url}${search_text}/`, 'GET')
    .then(res => res.json()) // convert response to JSON
    .then(data=>data) // recieve json data 
  return records; // return data
}


//====================================================================================================================================
//====================================================================================================================================
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
