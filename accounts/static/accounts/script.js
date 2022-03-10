let tabNavList = document.querySelector(".tab-nav")

tabNavList.addEventListener("click", (e)=>{
    // Making sure the tab name exists in the navigation item
    let selectedTabName = e.target.dataset.tabName    
    if (!selectedTabName) return;

    // Making sure user selected tab exists
    let newActiveTab = document.querySelector(`.tab[data-tab-name='${selectedTabName}']`)
    if (!newActiveTab) return;
    
    // Update the newly selected tab to active tab in tab navigation
    let currentActiveTabInNav = document.querySelector(".tab-nav-item.active")
    currentActiveTabInNav.classList.remove("active")
    e.target.classList.add("active")
    
    // Show the newly selected tab
    let currentActiveTab = document.querySelector(".tab.active")
    currentActiveTab.classList.remove("active")
    newActiveTab.classList.add("active")
})

let urlParams = getAllUrlParams(location.href)
let submissionId = urlParams.pk
let submissionDetails = null

async function getSubmissionDetails(){
    let record = await fetch_url({url:`/companies/SAS/search/?pk=${submissionId}`, req_method:"get"})
    submissionDetails = await record.json()

    // Update info in Details tab
    updateDetailsTab(submissionDetails)

    // // Update info in Income and Expense tab
    // updateIncomeAndExpenseTab(submissionDetails)

    // // Update info in Tax Calculation tab
    // updateTaxCalculationTab(submissionDetails)

    // // Update info in View tab
    // updateViewTab(submissionDetails)
}

getSubmissionDetails()


function updateDetailsTab(submissionDetails){
    let taxYear = document.querySelector('#tax-year')
    let clientName = document.querySelector('#client-name')
    let clientPersonalAddress = document.querySelector('#client-personal-address')
    let clientBusinessAddress = document.querySelector('#client-business-address')
    let clientDob = document.querySelector('#client-dob')
    let clientUtr = document.querySelector('#client-utr')
    let clientAccountStatus = document.querySelector('#client-account-status')

    taxYear.textContent = submissionDetails.tax_year.tax_year
    clientName.textContent = submissionDetails.client_id.client_name
    clientPersonalAddress.textContent = submissionDetails.client_id.personal_address
    clientBusinessAddress.textContent = submissionDetails.client_id.business_address
    clientDob.textContent = submissionDetails.client_id.date_of_birth
    clientUtr.textContent = submissionDetails.client_id.UTR
    clientAccountStatus.textContent = submissionDetails.status
}

function updateIncomeAndExpenseTab(submissionDetails){
    // get
}

function updateTaxCalculationTab(submissionDetails){
    //
}

function updateViewTab(submissionDetails){
    //
}


// =============================================================================================================================
// Api caller
async function fetch_url({url, req_method, data_object={}, headers={'Content-Type': 'application/json'}, others={}}){
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


  function getAllUrlParams(url) {

    // get query string from url (optional) or window
    var queryString = url ? url.split('?')[1] : window.location.search.slice(1);
  
    // we'll store the parameters here
    var obj = {};
  
    // if query string exists
    if (queryString) {
  
      // stuff after # is not part of query string, so get rid of it
      queryString = queryString.split('#')[0];
  
      // split our query string into its component parts
      var arr = queryString.split('&');
  
      for (var i = 0; i < arr.length; i++) {
        // separate the keys and the values
        var a = arr[i].split('=');
  
        // set parameter name and value (use 'true' if empty)
        var paramName = a[0];
        var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];
  
        // (optional) keep case consistent
        paramName = paramName.toLowerCase();
        if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();
  
        // if the paramName ends with square brackets, e.g. colors[] or colors[2]
        if (paramName.match(/\[(\d+)?\]$/)) {
  
          // create key if it doesn't exist
          var key = paramName.replace(/\[(\d+)?\]/, '');
          if (!obj[key]) obj[key] = [];
  
          // if it's an indexed array e.g. colors[2]
          if (paramName.match(/\[\d+\]$/)) {
            // get the index value and add the entry at the appropriate position
            var index = /\[(\d+)\]/.exec(paramName)[1];
            obj[key][index] = paramValue;
          } else {
            // otherwise add the value to the end of the array
            obj[key].push(paramValue);
          }
        } else {
          // we're dealing with a string
          if (!obj[paramName]) {
            // if it doesn't exist, create property
            obj[paramName] = paramValue;
          } else if (obj[paramName] && typeof obj[paramName] === 'string'){
            // if property does exist and it's a string, convert it to an array
            obj[paramName] = [obj[paramName]];
            obj[paramName].push(paramValue);
          } else {
            // otherwise add the property
            obj[paramName].push(paramValue);
          }
        }
      }
    }
  
    return obj;
  }