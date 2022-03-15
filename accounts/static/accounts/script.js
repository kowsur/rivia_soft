/*
// update or insert income
fetch_url({
  // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
  url: "/accounts/set_income/46/6/4/",
  req_method: "POST",
  data_object: JSON.stringify({
    // one of them must be specified
    amount: 2000,
    comission: 80
  })
})

// upsert expense
fetch_url({
  // url = "/accounts/set_expense/<submission_id>/<month_id>/<expense_id>/"
  url: "/accounts/set_expense/46/6/4/",
  req_method: "POST",
  data_object: JSON.stringify({
    // amount must be specified
    amount: 2000,
  })
})
*/




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
let incomeSources = null
let expenseSources = null
let months = null
let allIncomesForSubmission = null
let allExpensesForSubmission = null

// get data
getSubmissionDetails(updateDetailsTab, updateIncomeAndExpenseTab, updateTaxCalculationTab, updateDetailsTab)
getIncomeSources()
getExpneseSources()
getMonths()
getAllIncomesForSubmission()
getAllExpensesForSubmission()


async function getSubmissionDetails(...callbacks){
  if (submissionDetails!==null) return submissionDetails

  let record = await fetch_url({url:`/companies/SAS/search/?pk=${submissionId}`, req_method:"get"})
  submissionDetails = await record.json()
  
  if (Array.isArray(callbacks)) {
    callbacks.forEach(callback => {
      callback(submissionDetails)
    });
  }
  return submissionDetails
}
async function getIncomeSources(...callbacks){
  if (incomeSources!==null) return incomeSources

  let records = await fetch_url({url: '/accounts/income_sources/'})
  incomeSources = await records.json()
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(incomeSources)
  });

  return incomeSources
}
async function getExpneseSources(...callbacks){
  if (expenseSources!==null) return expenseSources
  let records = await fetch_url({url: '/accounts/expense_sources/'})
  expenseSources = await records.json()
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(expenseSources)
  });

  return expenseSources
}
async function getMonths(...callbacks){
  if (months!==null) return months
  let records = await fetch_url({url: '/accounts/months/'})
  months = await records.json()
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(months)
  });
  return months
}
async function getAllIncomesForSubmission(...callbacks){
  if (allIncomesForSubmission!==null) return allIncomesForSubmission

  let records = await fetch_url({url: `/accounts/incomes/${submissionId}/`})
  allIncomesForSubmission = await records.json()
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allIncomesForSubmission)
  });

  return allIncomesForSubmission
}
async function getAllExpensesForSubmission(...callbacks){
  if (allExpensesForSubmission!==null) return allExpensesForSubmission

  let records = await fetch_url({url: `/accounts/expenses/${submissionId}/`})
  allExpensesForSubmission = await records.json()
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allExpensesForSubmission)
  });

  return allExpensesForSubmission
}


// Update info in Details tab
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

// Update info in Income and Expense tab
async function updateIncomeAndExpenseTab(submissionDetails){
  let incomeSources = {}
}

// Update info in Tax Calculation tab
function updateTaxCalculationTab(submissionDetails){
    //
}

// Update info in View tab
function updateViewTab(submissionDetails){
    //
}

function handleIncomeSearch(e){
  console.log(e.target.value)
}
function handleIncomeSelect(e){
  console.log(e.target)

  let newIncomeSource = `<div class="income">
  <h2 class="title">${incomeSource}</h2>
  <div class="month">
    <span class="month">${month}</span>
    <input type="number" value="0" step="0.1" data-month-id="${4}" data-submission-id="${45}" data-income-id="${3}" data-update-type="amount">
    <span>Comission</span>
    <input type="number" data-month-id="${4}" data-submission-id="${45}" data-income-id="${3}" data-update-type="comission">
  </div>
</div>`
}


function handleIncomeUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, incomeId, updateType} = inputField.dataset

  if(updateType==="amount"){
    fetch_url({
      // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
      url: `/accounts/set_income/${submissionId}/${monthId}/${incomeId}/`,
      req_method: "POST",
      data_object: JSON.stringify({
        // one of them must be specified
        amount: parseFloat(inputField.value),
        // comission: 0,
      })
    })
  }
  else{
    fetch_url({
      // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
      url: `/accounts/set_income/${submissionId}/${monthId}/${incomeId}/`,
      req_method: "POST",
      data_object: JSON.stringify({
        // one of them must be specified
        // amount: 0,
        comission: parseFloat(inputField.value),
      })
    })
  }
}

function handleExpenseUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, expenseId} = inputField.dataset

  fetch_url({
    // url = "/accounts/set_expense/<submission_id>/<month_id>/<expense_id>/"
    url: `/accounts/set_expense/${submissionId}/${monthId}/${expenseId}/`,
    req_method: "POST",
    data_object: JSON.stringify({
      // amount must be specified
      amount: parseFloat(inputField.value),
    })
  })
}


// =============================================================================================================================
// Api caller
async function fetch_url({url, req_method="GET", data_object={}, headers={'Content-Type': 'application/json'}, others={}}){
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