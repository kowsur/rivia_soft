const DB_MAX_INT_VALUE = 2147483647

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

// =============================================================================================================================
// 
let incomeSearchInput = document.querySelector('#add_income_input')
let incomeSearchOptions = document.querySelector('#add_income_options')
let incomesContainer = document.querySelector(".incomes")
incomeSearchInput.addEventListener('input', handleIncomeSearch)
incomeSearchOptions.addEventListener('click', handleIncomeSelect)

let expenseSearchInput = document.querySelector('#add_expense_input')
let expenseSearchOptions = document.querySelector('#add_expense_options')
let expensesContainer = document.querySelector(".expenses")


// =============================================================================================================================
// Fetch data from backend
let urlParams = getAllUrlParams(location.href)
let submissionId = urlParams.pk

const displayingIncomeIds = new Set()
const displayingExpenseIds = new Set()

let submissionDetails = null
let allIncomeSources = null
let allExpenseSources = null
let allMonths = null
let allIncomesForSubmission = null
let allExpensesForSubmission = null

// Maps to speed up the lookup
const monthsMapById = {}
const incomeSourcesMapById = {}
const expenseSourcesMapById = {}
const groupedAllIncomesForSubmissionMapBySourceId = {}
const groupedAllExpensesForSubmissionMapBySourceId = {}


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
  if (allIncomeSources!==null) return allIncomeSources

  let records = await fetch_url({url: '/accounts/income_sources/'})
  allIncomeSources = await records.json()
  mapRecordsByAttribute(allIncomeSources, 'id', incomeSourcesMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allIncomeSources)
  });

  return allIncomeSources
}
async function getExpneseSources(...callbacks){
  if (allExpenseSources!==null) return allExpenseSources
  let records = await fetch_url({url: '/accounts/expense_sources/'})
  allExpenseSources = await records.json()
  mapRecordsByAttribute(allExpenseSources, 'id', expenseSourcesMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allExpenseSources)
  });

  return allExpenseSources
}
async function getMonths(...callbacks){
  if (allMonths!==null) return allMonths
  let records = await fetch_url({url: '/accounts/months/'})
  allMonths = await records.json()
  mapRecordsByAttribute(allMonths, 'id', monthsMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allMonths)
  });
  return allMonths
}
async function getAllIncomesForSubmission(...callbacks){
  if (allIncomesForSubmission!==null) return allIncomesForSubmission

  let records = await fetch_url({url: `/accounts/incomes/${submissionId}/`})
  allIncomesForSubmission = await records.json()
  groupRecordsByAttribute(allIncomesForSubmission, 'income_source', groupedAllIncomesForSubmissionMapBySourceId)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allIncomesForSubmission)
  });

  return allIncomesForSubmission
}
async function getAllExpensesForSubmission(...callbacks){
  if (allExpensesForSubmission!==null) return allExpensesForSubmission

  let records = await fetch_url({url: `/accounts/expenses/${submissionId}/`})
  allExpensesForSubmission = await records.json()
  groupRecordsByAttribute(allExpensesForSubmission, 'expense_source', groupedAllExpensesForSubmissionMapBySourceId)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allExpensesForSubmission)
  });

  return allExpensesForSubmission
}

function mapRecordsByAttribute(records, attributeName, map=null){
  if (map === null) map = {}
  records.forEach(record=>{
    map[record[attributeName]] = record
  })
  return map
}

// =============================================================================================================================
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
  // These are required to load data incase data is not loaded
  let incomeSources = await getIncomeSources()
  let expenseSources = await getExpneseSources()
  let months = await getMonths()
  let allIncomesForSubmission = await getAllIncomesForSubmission()
  let allExpensesForSubmission = await getAllExpensesForSubmission()

  Object.entries(groupedAllIncomesForSubmissionMapBySourceId).forEach(([incomeSourceId, incomes]) => {
    displayIncomeSource(incomeSourceId, incomes, submissionDetails)
  });
  Object.entries(groupedAllExpensesForSubmissionMapBySourceId).forEach(([expenseSourceId, expenses]) => {
    displayExpenseSource(expenseSourceId, expenses, submissionDetails)
  });

  displayIncomeOptions()
}

function displayIncomeSource(incomeSourceId, incomes, submission){
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingIncomeIds.add(parseInt(incomeSourceId))
  let incomeSource = incomeSourcesMapById[incomeSourceId]
  
  let incomeContainer = createNodeFromMarkup(`
  <div class="income">
    <div class="toggle">
      <h2 class="income-source">${incomeSource.name}</h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
    </div>
  </div>`)
  let monthContainer = incomeContainer.querySelector('.months')
  let toggle = incomeContainer.querySelector('.toggle')
  let toggleImg = incomeContainer.querySelector('.toggle img')

  // adding event listener to show or hide details for an income source
  toggle.addEventListener('click', (e)=>{
    if (monthContainer.classList.contains('invisible')) {
      monthContainer.classList.remove('invisible')
      toggleImg.src = '/static/accounts/collapse.svg'
    }else{
      monthContainer.classList.add('invisible')
      toggleImg.src = '/static/accounts/expand.svg'
    }
  })

  allMonths.forEach(month=>{
    // Get the existing/default income object
    let income = incomes.find(income=>income.month===month.id) || {
      "amount": 0,
      "comission": 0,
      "income_source": incomeSourceId,
      "client": submissionId,
      "month": month.id
    }
    let inputAmountId = `income_amount_${month.id}_${submission.submission_id}_${income.income_source}`
    let inputComissionId = `income_comission_${month.id}_${submission.submission_id}_${income.income_source}`


    // Prepare markup for a single month
    let incomeMarkup = `
        <div class='month'>
          <h3 class='month-name'>${month.month_name} - ${submission.tax_year.tax_year}</h3>
          <div>
            <label for="${inputAmountId}">Amount</label>
            <input type="number" max=${DB_MAX_INT_VALUE} id=${inputAmountId} value="${income?.amount}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="amount">
          </div>
  
          <div>
            <label for=${inputComissionId}>Comission</label>
            <input type="number" max=${DB_MAX_INT_VALUE} id=${inputComissionId} value="${income?.comission}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="comission">
          </div>
        </div>
        `
    let node = createNodeFromMarkup(incomeMarkup)
    let inputAmount = node.querySelector(`#${inputAmountId}`)
    let inputComission = node.querySelector(`#${inputComissionId}`)

    inputAmount.addEventListener('input', validateMaxValue)
    inputAmount.addEventListener('input', handleIncomeUpdate)
    inputComission.addEventListener('input', validateMaxValue)
    inputComission.addEventListener('input', handleIncomeUpdate)

    monthContainer.appendChild(node)
  })

  // add the newly prepared income source to incomes
  incomesContainer.appendChild(incomeContainer)
}
function displayExpenseSource(expenseSourceId, expenses, submission){
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingIncomeIds.add(parseInt(expenseSourceId))
  let incomeSource = incomeSourcesMapById[expenseSourceId]
  
  let incomeContainer = createNodeFromMarkup(`
  <div class="expense">
    <div class="toggle">
      <h2 class="income-source">${incomeSource.name}</h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
    </div>
  </div>`)
  let monthContainer = incomeContainer.querySelector('.months')
  let toggle = incomeContainer.querySelector('.toggle')
  let toggleImg = incomeContainer.querySelector('.toggle img')

  // adding event listener to show or hide details for an expense source
  toggle.addEventListener('click', (e)=>{
    if (monthContainer.classList.contains('invisible')) {
      monthContainer.classList.remove('invisible')
      toggleImg.src = '/static/accounts/collapse.svg'
    }else{
      monthContainer.classList.add('invisible')
      toggleImg.src = '/static/accounts/expand.svg'
    }
  })

  allMonths.forEach(month=>{
    // Get the existing/default income object
    let income = expenses.find(income=>income.month===month.id) || {
      "amount": 0,
      "comission": 0,
      "income_source": expenseSourceId,
      "client": submissionId,
      "month": month.id
    }
    let inputAmountId = `income_amount_${month.id}_${submission.submission_id}_${income.income_source}`
    let inputComissionId = `income_comission_${month.id}_${submission.submission_id}_${income.income_source}`


    // Prepare markup for a single month
    let incomeMarkup = `
        <div class='month'>
          <h3 class='month-name'>${month.month_name} - ${submission.tax_year.tax_year}</h3>
          <div>
            <label for="${inputAmountId}">Amount</label>
            <input type="number" max=${DB_MAX_INT_VALUE} id=${inputAmountId} value="${income?.amount}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="amount">
          </div>
  
          <div>
            <label for=${inputComissionId}>Comission</label>
            <input type="number" max=${DB_MAX_INT_VALUE} id=${inputComissionId} value="${income?.comission}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="comission">
          </div>
        </div>
        `
    let node = createNodeFromMarkup(incomeMarkup)
    let inputAmount = node.querySelector(`#${inputAmountId}`)
    let inputComission = node.querySelector(`#${inputComissionId}`)

    inputAmount.addEventListener('input', validateMaxValue)
    inputAmount.addEventListener('input', handleIncomeUpdate)
    inputComission.addEventListener('input', validateMaxValue)
    inputComission.addEventListener('input', handleIncomeUpdate)

    monthContainer.appendChild(node)
  })

  // add the newly prepared income source to incomes
  incomesContainer.appendChild(incomeContainer)
}

function validateMaxValue(e){
  let input = e.target
  let value = parseFloat(e.target.value)
  if (value>DB_MAX_INT_VALUE){
    input.setCustomValidity(`Your input is grater than ${DB_MAX_INT_VALUE}!`);
    input.reportValidity();
  }else{
    input.setCustomValidity("");
  }
}

function createNodeFromMarkup(html){
  return document.createRange().createContextualFragment(html)
}

function createHtmlElement(tag='div', attributes={}){
  let element = document.createElement(tag)
  Object.entries(attributes).forEach(([key, value])=>{
    element.setAttribute(key, value)
  })
  return element
}

function groupRecordsByAttribute(records, attributeName, groupedRecords=null){
  if (groupedRecords===null) groupedRecords = {}

  records.forEach(record=>{
    if (record[attributeName] in groupedRecords) groupedRecords[record[attributeName]].push(record)
    else groupedRecords[record[attributeName]] = [record]
  })

  return groupedRecords
}

// Update info in Tax Calculation tab
function updateTaxCalculationTab(submissionDetails){
    //
}

// Update info in View tab
function updateViewTab(submissionDetails){
    //
}


// =============================================================================================================================
// Handlers
async function handleIncomeSearch(e){
  let searchText = e.target.value
  let displayableIncomeSources = await getDisplayableIncomeSources(searchText)

  displayIncomeOptions(displayableIncomeSources)
}
async function getDisplayableIncomeSources(searchText=''){
  let incomeSources = await getIncomeSources()
  let displayableIncomeSources = incomeSources.filter(incomeSource=>!displayingIncomeIds.has(incomeSource.id) && incomeSource.name.toLowerCase().includes(searchText.trim()))
  return displayableIncomeSources
}
async function displayIncomeOptions(displayableIncomeSources=null){
  if (displayableIncomeSources==null) displayableIncomeSources = await getDisplayableIncomeSources()
  incomeSearchOptions.innerHTML = ''
    displayableIncomeSources.forEach(incomeSource=>{
      let option = createHtmlElement('div', {'data-income-id': incomeSource.id})
      option.textContent = incomeSource.name
      incomeSearchOptions.appendChild(option)
    })
}

async function handleIncomeSelect(e){
  let {incomeId} = e.target.dataset
  if (incomeId && parseInt(incomeId)){
    incomeId = parseInt(incomeId)
    displayIncomeSource(incomeId, [], await getSubmissionDetails())
    displayIncomeOptions()
  }
}


function handleIncomeUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, incomeId, updateType} = inputField.dataset
  let data_object = {} // amount or comission or both must be specified

  if (updateType==="amount") data_object.amount = parseFloat(inputField.value)
  else if (updateType==="comission") data_object.comission = parseFloat(inputField.value)

  fetch_url({
    // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
    url: `/accounts/set_income/${submissionId}/${monthId}/${incomeId}/`,
    req_method: "POST",
    data_object: JSON.stringify(data_object)
  })
}

function handleExpenseUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, expenseId} = inputField.dataset
  let data_object = { amount: parseFloat(inputField.value) } // amount must be specified

  fetch_url({
    // url = "/accounts/set_expense/<submission_id>/<month_id>/<expense_id>/"
    url: `/accounts/set_expense/${submissionId}/${monthId}/${expenseId}/`,
    req_method: "POST",
    data_object: JSON.stringify(data_object)
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