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

let taxableIncomeSearchInput = document.querySelector('#add_taxable_income_input')
let taxableIncomeSearchOptions = document.querySelector('#add_taxable_income_options')
let taxableIncomesContainer = document.querySelector(".taxable-incomes")
taxableIncomeSearchInput.addEventListener('input', handleTaxableIncomeSearch)
taxableIncomeSearchOptions.addEventListener('click', handleTaxableIncomeSelect)

let selfemploymentIncomeSearchInput = document.querySelector('#add_selfemployment_income_input')
let selfemploymentIncomeSearchOptions = document.querySelector('#add_selfemployment_income_options')
let selfemploymentIncomesContainer = document.querySelector(".selfemployment-incomes")
selfemploymentIncomeSearchInput.addEventListener('input', handleSelfemploymentIncomeSearch)
selfemploymentIncomeSearchOptions.addEventListener('click', handleSelfemploymentIncomeSelect)

let expenseSearchInput = document.querySelector('#add_expense_input')
let expenseSearchOptions = document.querySelector('#add_expense_options')
let expensesContainer = document.querySelector(".expenses")
expenseSearchInput.addEventListener('input', handleExpenseSearch)
expenseSearchOptions.addEventListener('click', handleExpenseSelect)

let deductionSearchInput = document.querySelector('#add_deduction_and_allowance_input')
let deductionSearchOptions = document.querySelector('#add_deduction_and_allowance_options')
let deductionsContainer = document.querySelector(".deductions_and_allowances")
deductionSearchInput.addEventListener('input', handleDeductionSearch)
deductionSearchOptions.addEventListener('click', handleDeductionSelect)

let totalTaxableIncomeContainers = document.querySelectorAll('[data-total-taxable-income-container]')
let totalSelfemploymentIncomeContainers = document.querySelectorAll('[data-total-selfemployment-income-container]')
let totalExpenseContainers = document.querySelectorAll('[data-total-expense-container]')
let totalDeductionContainers = document.querySelectorAll('[data-total-deduction-and-allownce-container]')
let netProfitContainers = document.querySelectorAll('[data-net-profit-container]')
let showUptoDecimalDigits = 2


function calculateTaxableIncome(incomeAmount, paid_income_tax_amount){
  let actualIncome = incomeAmount//-paid_income_tax_amount
  if (actualIncome<0) actualIncome=0
  return actualIncome
}

async function getTotalTaxableIncome(){
  let inputAmountFields = document.querySelectorAll('.taxable-incomes input[data-update-type="amount"]')
  let inputPaidTaxAmountFields = document.querySelectorAll('.taxable-incomes input[data-update-type="paid_income_tax_amount"]')
  let totalIncome = 0

  for (let i=0; i<inputAmountFields.length; i++){
    let amount = parseFloat(inputAmountFields[i].value) || 0
    let paid_income_tax_amount = parseFloat(inputPaidTaxAmountFields[i].value) || 0

    totalIncome+=calculateTaxableIncome(amount, paid_income_tax_amount)
  }

  return totalIncome
}

function calculateSelfemploymentIncome(incomeAmount, comission){
  let actualIncome = incomeAmount-comission
  if (actualIncome<0) actualIncome=0
  return actualIncome
}

async function getTotalSelfemploymentIncomeForSelfemploymentIncomeSection(incomeSectionContainer){
  let inputAmountFields = incomeSectionContainer.querySelectorAll('.selfemployment-incomes input[data-update-type="amount"]')
  let inputComissionFields = incomeSectionContainer.querySelectorAll('.selfemployment-incomes input[data-update-type="comission"]')
  let totalIncome = 0
  
  for (let i=0; i<inputAmountFields.length; i++){
    let amount = parseFloat(inputAmountFields[i].value) || 0
    let comission = parseFloat(inputComissionFields[i].value) || 0

    totalIncome+=calculateSelfemploymentIncome(amount, comission)
  }

  return totalIncome
}

async function getTotalSelfemploymentIncome(){
  let inputAmountFields = document.querySelectorAll('.selfemployment-incomes input[data-update-type="amount"]')
  let inputComissionFields = document.querySelectorAll('.selfemployment-incomes input[data-update-type="comission"]')
  let totalIncome = 0
  
  for (let i=0; i<inputAmountFields.length; i++){
    let amount = parseFloat(inputAmountFields[i].value) || 0
    let comission = parseFloat(inputComissionFields[i].value) || 0

    totalIncome+=calculateSelfemploymentIncome(amount, comission)
  }

  return totalIncome
}

async function getTotalExpense(){
  let inputAmountFields = document.querySelectorAll('.expenses input[data-update-type="amount"]')
  let inputPersonalUsagePercentageFields = document.querySelectorAll('.expenses input[data-update-type="personal_usage_percentage"]')
  let totalExpense = 0

  for (let i=0; i<inputAmountFields.length; i++){
      let amount = parseFloat(inputAmountFields[i].value) || 0
      let personal_usage_percentage = parseFloat(inputPersonalUsagePercentageFields[i].value) || 0

      // Calculate actual personal usage
      let personal_usage = amount*(personal_usage_percentage/100)

      let actualExpense = amount-personal_usage
      if (actualExpense<0) actualExpense = 0

      totalExpense+=actualExpense
  }

  return totalExpense
}
// update the function
async function getTotalDeduction(){
  let inputAmountFields = document.querySelectorAll('.deductions_and_allowances input[data-update-type="amount"]')
  let inputAllowancePercentageFields = document.querySelectorAll('.deductions_and_allowances input[data-update-type="allowance_percentage"]')
  let inputPersonalUsagePercentageFields = document.querySelectorAll('.deductions_and_allowances input[data-update-type="personal_usage_percentage"]')
  let totalDeduction = 0

  for (let i=0; i<inputAmountFields.length; i++){
      let amount = parseFloat(inputAmountFields[i].value) || 0
      let allowance_percentage = parseFloat(inputAllowancePercentageFields[i].value) || 0
      let personal_usage_percentage = parseFloat(inputPersonalUsagePercentageFields[i].value) || 0

      // Calculate actual allowance
      let allowance = amount*(allowance_percentage/100)

      // Calculate actual personal usage
      let personal_usage = allowance*(personal_usage_percentage/100)

      let actualDeduction = (allowance-personal_usage)
      if (actualDeduction<0) actualDeduction = 0

      totalDeduction+=actualDeduction
  }

  return totalDeduction
}

async function getNetProfit(){
  let totalIncome = await getTotalSelfemploymentIncome()
  let totalExpense = await getTotalExpense()
  let totalDeduction = await getTotalDeduction()
  return totalIncome - (totalExpense + totalDeduction)
}

async function updateTotalSelfemploymentIncomeForSelfemploymentIncomeSection(incomeSectionContainer, totalIncomeContainerForSection){
  let totalIncome = await getTotalSelfemploymentIncomeForSelfemploymentIncomeSection(incomeSectionContainer)
  totalIncome = parseFloat(totalIncome).toFixed(showUptoDecimalDigits) || 0

  totalIncomeContainerForSection.textContent = totalIncome
}

async function updateTotalTaxableIncome(){
  let totalIncome = await getTotalTaxableIncome()
  totalIncome = parseFloat(totalIncome).toFixed(showUptoDecimalDigits) || 0

  totalTaxableIncomeContainers.forEach((totalIncomeContainer)=>totalIncomeContainer.textContent = totalIncome)
}

async function updateTotalSelfemploymentIncome(){
  let totalIncome = await getTotalSelfemploymentIncome()
  totalIncome = parseFloat(totalIncome).toFixed(showUptoDecimalDigits) || 0

  totalSelfemploymentIncomeContainers.forEach((totalIncomeContainer)=>totalIncomeContainer.textContent = totalIncome)
}

async function updateTotalExpense(){
  let totalExpense = await getTotalExpense()
  totalExpense = parseFloat(totalExpense).toFixed(showUptoDecimalDigits) || 0

  totalExpenseContainers.forEach((totalExpenseContainer)=>totalExpenseContainer.textContent = totalExpense)
}

async function updateTotalDeduction(){
  let totalDeduction = await getTotalDeduction()
  totalDeduction = parseFloat(totalDeduction).toFixed(showUptoDecimalDigits) || 0

  totalDeductionContainers.forEach((totalDeductionContainer)=>totalDeductionContainer.textContent = totalDeduction)
}

async function updateNetProfit(){
  let netProfit = await getNetProfit()
  netProfit = parseFloat(netProfit).toFixed(showUptoDecimalDigits) || 0

  netProfitContainers.forEach((netProfitcontainer)=>netProfitcontainer.textContent = netProfit)
}


// =============================================================================================================================
// Fetch data from backend
let urlParams = getAllUrlParams(location.href)
let submissionId = urlParams.pk

const displayingTaxableIncomeIds = new Set()
const displayingSelfemploymentIncomeIds = new Set()
const displayingExpenseIds = new Set()
const displayingDeductionIds = new Set()

let submissionDetails = null
let allTaxableIncomeSources = null
let allSelfemploymentIncomeSources = null
let allExpenseSources = null
let allDeductionSources = null
let allMonths = null
let allTaxableIncomesForSubmission = null
let allSelfemploymentIncomesForSubmission = null
let allExpensesForSubmission = null
let allDeductionsForSubmission = null

// Maps to speed up the lookup
const monthsMapById = {}
const taxableIncomeSourcesMapById = {}
const selfemploymentIncomeSourcesMapById = {}
const expenseSourcesMapById = {}
const deductionSourcesMapById = {}
const groupedAllTaxableIncomesForSubmissionMapBySourceId = {}
const groupedAllSelfemploymentIncomesForSubmissionMapBySourceId = {}
const groupedAllExpensesForSubmissionMapBySourceId = {}
const groupedAllDeductionsForSubmissionMapBySourceId = {}


// get data
getSubmissionDetails(updateDetailsTab, updateIncomeAndExpenseTab, updateTaxCalculationTab, updateDetailsTab)
getTaxableIncomeSources()
getSelfemploymentIncomeSources()
getExpneseSources()
getDeductionSources()
getMonths()
getAllTaxableIncomesForSubmission()
getAllSelfemploymentIncomesForSubmission()
getAllExpensesForSubmission()
getAllDeductionsForSubmission()


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
async function getTaxableIncomeSources(...callbacks){
  if (allTaxableIncomeSources!==null) return allTaxableIncomeSources

  let records = await fetch_url({url: '/accounts/taxable_income_sources/'})
  allTaxableIncomeSources = await records.json()
  mapRecordsByAttribute(allTaxableIncomeSources, 'id', taxableIncomeSourcesMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allTaxableIncomeSources)
  });

  return allTaxableIncomeSources
}
async function getSelfemploymentIncomeSources(...callbacks){
  if (allSelfemploymentIncomeSources!==null) return allSelfemploymentIncomeSources

  let records = await fetch_url({url: '/accounts/income_sources/'})
  allSelfemploymentIncomeSources = await records.json()
  mapRecordsByAttribute(allSelfemploymentIncomeSources, 'id', selfemploymentIncomeSourcesMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allSelfemploymentIncomeSources)
  });

  return allSelfemploymentIncomeSources
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
async function getDeductionSources(...callbacks){
  if (allDeductionSources!==null) return allDeductionSources
  let records = await fetch_url({url: '/accounts/deduction_sources/'})
  allDeductionSources = await records.json()
  mapRecordsByAttribute(allDeductionSources, 'id', deductionSourcesMapById)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allDeductionSources)
  });

  return allDeductionSources
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
async function getAllTaxableIncomesForSubmission(...callbacks){
  if (allTaxableIncomesForSubmission!==null) return allTaxableIncomesForSubmission

  let records = await fetch_url({url: `/accounts/taxable_incomes/${submissionId}/`})
  allTaxableIncomesForSubmission = await records.json()
  groupRecordsByAttribute(allTaxableIncomesForSubmission, 'taxable_income_source', groupedAllTaxableIncomesForSubmissionMapBySourceId)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allTaxableIncomesForSubmission)
  });

  return allTaxableIncomesForSubmission
}
async function getAllSelfemploymentIncomesForSubmission(...callbacks){
  if (allSelfemploymentIncomesForSubmission!==null) return allSelfemploymentIncomesForSubmission

  let records = await fetch_url({url: `/accounts/incomes/${submissionId}/`})
  allSelfemploymentIncomesForSubmission = await records.json()
  groupRecordsByAttribute(allSelfemploymentIncomesForSubmission, 'income_source', groupedAllSelfemploymentIncomesForSubmissionMapBySourceId)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allSelfemploymentIncomesForSubmission)
  });

  return allSelfemploymentIncomesForSubmission
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
async function getAllDeductionsForSubmission(...callbacks){
  if (allDeductionsForSubmission!==null) return allDeductionsForSubmission

  let records = await fetch_url({url: `/accounts/deductions/${submissionId}/`})
  allDeductionsForSubmission = await records.json()
  groupRecordsByAttribute(allDeductionsForSubmission, 'deduction_source', groupedAllDeductionsForSubmissionMapBySourceId)
  
  if (Array.isArray(callbacks)) callbacks.forEach(callback => {
    callback(allDeductionsForSubmission)
  });

  return allDeductionsForSubmission
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
    let clientNino = document.querySelector('#client-nino')
    let clientAccountStatus = document.querySelector('#client-account-status')

    taxYear.textContent = submissionDetails.tax_year.tax_year
    clientName.textContent = submissionDetails.client_id.client_name
    clientPersonalAddress.textContent = submissionDetails.client_id.personal_address
    clientBusinessAddress.textContent = submissionDetails.client_id.business_address
    clientDob.textContent = submissionDetails.client_id.date_of_birth
    clientUtr.textContent = submissionDetails.client_id.UTR
    clientNino.textContent = submissionDetails.client_id.NINO
    clientAccountStatus.textContent = submissionDetails.status
    clientAccountStatus.href = `/companies/SAS/update/${submissionId}/`
}

// Update info in Income and Expense tab
async function updateIncomeAndExpenseTab(submissionDetails){
  let clientName = document.querySelector('#ie-client-name')
  clientName.textContent = submissionDetails.client_id.client_name
  let taxYear = document.querySelector('#ie-client-tax-year')
  taxYear.textContent = submissionDetails.tax_year.tax_year

  // These are required to load data incase data is not loaded
  let taxableIncomeSources = await getTaxableIncomeSources()
  let selfemploymentIncomeSources = await getSelfemploymentIncomeSources()
  let expenseSources = await getExpneseSources()
  let deductionSources = await getDeductionSources()
  let months = await getMonths()
  let allTaxableIncomesForSubmission = await getAllTaxableIncomesForSubmission()
  let allSelfemploymentIncomesForSubmission = await getAllSelfemploymentIncomesForSubmission()
  let allExpensesForSubmission = await getAllExpensesForSubmission()
  let allDeductionsForSubmission = await getAllDeductionsForSubmission()

  Object.entries(groupedAllTaxableIncomesForSubmissionMapBySourceId).forEach(([taxableIncomeSourceId, taxableIncomes]) => {
    displayTaxableIncomeSource(taxableIncomeSourceId, taxableIncomes, submissionDetails)
  });
  displayTaxableIncomeOptions()
  updateTotalTaxableIncome()

  Object.entries(groupedAllSelfemploymentIncomesForSubmissionMapBySourceId).forEach(([incomeSourceId, incomes]) => {
    displaySelfemploymentIncomeSource(incomeSourceId, incomes, submissionDetails)
  });
  displaySelfemploymentIncomeOptions()
  updateTotalSelfemploymentIncome()

  // Show expenses with data from backend
  Object.entries(groupedAllExpensesForSubmissionMapBySourceId).forEach(([expenseSourceId, expenses]) => {
    displayExpenseSource(expenseSourceId, expenses, submissionDetails)
  });

  // Show other expenses that doesn't have data
  allExpenseSources.forEach(expenseSource=>{
    if (!displayingExpenseIds.has(expenseSource.id)){
      displayExpenseSource(expenseSource.id, [], submissionDetails)
    }
  })

  displayExpenseOptions()
  updateTotalExpense()
  
  Object.entries(groupedAllDeductionsForSubmissionMapBySourceId).forEach(([deductionSourceId, deductions]) => {
    displayDeductionSource(deductionSourceId, deductions, submissionDetails)
  });
  displayDeductionOptions()
  updateTotalDeduction()

  updateNetProfit()
}

function displayTaxableIncomeSource(taxableIncomeSourceId, taxableIncomes, submission){
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingTaxableIncomeIds.add(parseInt(taxableIncomeSourceId))
  let incomeSource = taxableIncomeSourcesMapById[taxableIncomeSourceId]
  
  let taxableIncomeContainer = createNodeFromMarkup(`
  <div class="taxable-income" data-income-section="${incomeSource.id}">
    <div class="toggle">
      <h2 class="taxable-income-source">${incomeSource.name} Total: <span data-total-container-for-taxable-income-source>0</span></h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
    </div>
  </div>`)

}

function displaySelfemploymentIncomeSource(incomeSourceId, incomes, submission){
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingSelfemploymentIncomeIds.add(parseInt(incomeSourceId))
  let incomeSource = selfemploymentIncomeSourcesMapById[incomeSourceId]
  
  let incomeContainer = createNodeFromMarkup(`
  <div class="selfemployment-income" data-income-section="${incomeSource.id}">
    <div class="toggle">
      <h2 class="selfemployment-income-source">${incomeSource.name} Total: <span data-total-container-for-selfemployment-income-source>0</span></h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
      <div class="table income-display-table" data-display-table-name="income">
        <div class="thead">
          <div class="row">
            <span>Month</span>
            <span>Amount</span>
            <span>Comission</span>
            <span>Note</span>
          </div>
        </div>
        <div class="body">
          <div class="row"></div>
        </div>
      </div>
    </div>
  </div>`)

  let displayTable = incomeContainer.querySelector('[data-display-table-name="income"] div.body')
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

  let innerTableBody = ''

  allMonths.forEach(month=>{
    // Get the existing/default income object
    let income = incomes.find(income=>income.month===month.id) || {
      "amount": 0,
      "comission": 0,
      "note": '',
      "income_source": incomeSourceId,
      "client": submissionId,
      "month": month.id
    }
    let inputAmountId = `income_amount_${month.id}_${submission.submission_id}_${income.income_source}`
    let inputComissionId = `income_comission_${month.id}_${submission.submission_id}_${income.income_source}`
    let inputNoteId = `income_note_${month.id}_${submission.submission_id}_${income.income_source}`

    // Prepare markup for a single month
    let incomeMarkup = `
      <div class="row">
        <span>${month.month_name}</span>
        <span><input type="number" max=${DB_MAX_INT_VALUE} id=${inputAmountId} value="${income?.amount}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="amount"></span>
        <span><input type="number" max=${DB_MAX_INT_VALUE} id=${inputComissionId} value="${income?.comission}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}" data-update-type="comission"></span>
        <span>
          <textarea id=${inputNoteId} data-update-type="note" data-month-id="${month.id}" data-submission-id="${submissionId}" data-income-id="${income.income_source}">${income?.note}</textarea>
        </span>
      </div>
      `
    innerTableBody += incomeMarkup
    })

  displayTable.innerHTML = innerTableBody
  let inputAmountElements = displayTable.querySelectorAll('input[data-update-type="amount"]')
  let inputComissionElements = displayTable.querySelectorAll('input[data-update-type="comission"]')
  let inputNoteElements = displayTable.querySelectorAll('textarea[data-update-type="note"]')
  addEventListenersToElements(Array.from(inputAmountElements), 'input', [validateMaxValue, handleSelfemploymentIncomeUpdate, updateTotalSelfemploymentIncome, updateNetProfit])
  addEventListenersToElements(Array.from(inputComissionElements), 'input', [validateMaxValue, handleSelfemploymentIncomeUpdate, updateTotalSelfemploymentIncome, updateNetProfit])
  addEventListenersToElements(Array.from(inputNoteElements), 'input', [handleSelfemploymentIncomeUpdate])
  
  // add the newly prepared income source to incomes
  selfemploymentIncomesContainer.appendChild(incomeContainer)
  
  let incomeSectionContainer = document.querySelector(`.selfemployment-income[data-income-section="${incomeSource.id}"]`)
  let totalIncomeContainerForSection = incomeSectionContainer.querySelector('span[data-total-container-for-selfemployment-income-source]')
  
  let handleTotalSelfemploymentIncomeUpdateForSection = updateTotalSelfemploymentIncomeForSelfemploymentIncomeSection.bind(undefined, incomeSectionContainer, totalIncomeContainerForSection)
  addEventListenersToElements([...Array.from(inputAmountElements), ...Array.from(inputComissionElements)], 'input', handleTotalSelfemploymentIncomeUpdateForSection)
  // Initially Call to update the seciton total
  handleTotalSelfemploymentIncomeUpdateForSection()
}

function addEventListenersToElements(element_or_elements, eventName, eventFunction_or_Functions){
  if (Array.isArray(element_or_elements)){
    element_or_elements.forEach(element=>{
      if (Array.isArray(eventFunction_or_Functions)){
        eventFunction_or_Functions.forEach(eventFunction=>element.addEventListener(eventName, eventFunction))
      }else{
        element.addEventListener(eventName, eventFunction_or_Functions)
      }
    })
  }else{
    if (Array.isArray(eventFunction_or_Functions)){
      eventFunction_or_Functions.forEach(eventFunction=>element_or_elements.addEventListener(eventName, eventFunction))
    }else{
      element_or_elements.addEventListener(eventName, eventFunction_or_Functions)
    }
  }
}


function displayExpenseSource(expenseSourceId, expenses, submission){
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingExpenseIds.add(parseInt(expenseSourceId))
  let expenseSource = expenseSourcesMapById[expenseSourceId]
  
  let expenseContainer = createNodeFromMarkup(`
  <div class="expense">
    <div class="toggle">
      <h2 class="selfemployment-income-source">${expenseSource.name}</h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
    </div>
  </div>`)
  let monthContainer = expenseContainer.querySelector('.months')
  let toggle = expenseContainer.querySelector('.toggle')
  let toggleImg = expenseContainer.querySelector('.toggle img')

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

  // =====================================================================================================================
  // Start Show a single month
  let month = allMonths[0]

  // Get the existing/default expense object
  let expense = expenses.find(expense=>expense.month===month.id) || {
    "amount": 0,
    "personal_usage_percentage": expenseSource?.default_personal_usage_percentage||0,
    'note': '',
    "expense_source": expenseSourceId,
    "client": submissionId,
    "month": month.id
  }
  let inputAmountId = `expense_amount_${month.id}_${submission.submission_id}_${expense.expense_source}`
  let inputPersonalUsageId = `expense_personalUsage_${month.id}_${submission.submission_id}_${expense.expense_source}`
  let inputNoteId = `expense_note_${month.id}_${submission.submission_id}_${expense.expense_source}`

  // Prepare markup for a single month
  let expenseMarkup = `
      <div class='month'>
        <div>
          <label for="${inputAmountId}">Amount</label>
          <input type="number" max=${DB_MAX_INT_VALUE} id=${inputAmountId} value="${expense?.amount}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-expense-id="${expense.expense_source}" data-update-type="amount">
        </div>
        <div>
          <label for="${inputPersonalUsageId}">Personal Usage(%)</label>
          <input type="number" min="0" max='100' id=${inputPersonalUsageId} value="${expense?.personal_usage_percentage}" data-month-id="${month.id}" data-submission-id="${submissionId}" data-expense-id="${expense?.expense_source}" data-update-type="personal_usage_percentage">
        </div>
        <div>
          <label for="${inputNoteId}">Note</label>
          <textarea id=${inputNoteId} data-month-id="${month.id}" data-submission-id="${submissionId}" data-expense-id="${expense?.expense_source}" data-update-type="note">${expense?.note}</textarea>
        </div>
      </div>
      `
  let node = createNodeFromMarkup(expenseMarkup)
  let inputAmount = node.querySelector(`#${inputAmountId}`)
  let inputPersonalUsage = node.querySelector(`#${inputPersonalUsageId}`)
  let inputNote = node.querySelector(`#${inputNoteId}`)
  
  addEventListenersToElements(inputAmount, 'input', [validateMaxValue, handleExpenseUpdate, updateTotalExpense, updateNetProfit])
  addEventListenersToElements(inputPersonalUsage, 'input', [validatePercentageValue, handleExpenseUpdate, updateTotalExpense, updateNetProfit])
  addEventListenersToElements(inputNote, 'input', [handleExpenseUpdate])

  monthContainer.appendChild(node)
  expensesContainer.appendChild(expenseContainer)

  // Dispatch input event to make sure the loaded default percentage value gets saved to backend.
  // But, for existing records this will not change anything the value remains the same as before.
  inputPersonalUsage.dispatchEvent(new Event('input'))
}
function displayDeductionSource(deductionSourceId, deductions, submission){
  deductionSourceId = parseInt(deductionSourceId)
  // add current incomeSourceId to displayingIncomeIds set to filter them out while searching
  displayingDeductionIds.add(parseInt(deductionSourceId))
  let deductionSource = deductionSourcesMapById[deductionSourceId]
  

  let deductionContainer = createNodeFromMarkup(`
  <div class="deduction">
    <div class="toggle">
      <h2 class="selfemployment-income-source">${deductionSource.name}</h2>
      <img src='/static/accounts/expand.svg'/>
    </div>
    <div class="months invisible">
    </div>
  </div>`)
  let monthContainer = deductionContainer.querySelector('.months')
  let toggle = deductionContainer.querySelector('.toggle')
  let toggleImg = deductionContainer.querySelector('.toggle img')

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

  // Get the existing/default deduction object
  let deduction = deductions.find(deduction=>deduction.deduction_source===deductionSourceId) || {
    "amount": 0,
    "allowance_percentage": 0,
    "personal_usage_percentage": 0,
    "note": '',
    "deduction_source": deductionSourceId,
    "client": submissionId,
  }
  let inputAmountId = `deduction_amount_${submission.submission_id}_${deduction.deduction_source}`
  let inputAllowancePercentageId = `deduction_allowance_percentage_${submission.submission_id}_${deduction.deduction_source}`
  let inputPersonalUsagePercentageId = `deduction_personalUsage_percentage_${submission.submission_id}_${deduction.deduction_source}`
  let inputNoteId = `deduction_note_${submission.submission_id}_${deduction.deduction_source}`

  // Prepare markup for a single month
  let deductionMarkup = `
      <div class='month'>
        <div>
          <label for="${inputAmountId}">Amount</label>
          <input type="number" max=${DB_MAX_INT_VALUE} id=${inputAmountId} value="${deduction?.amount}" data-submission-id="${submissionId}" data-deduction-id="${deduction.deduction_source}" data-update-type="amount">
        </div>
        <div>
          <label for="${inputAllowancePercentageId}">Allowance(%)</label>
          <input type="number" min="0" max='100' id=${inputAllowancePercentageId} value="${deduction?.allowance_percentage}" data-submission-id="${submissionId}" data-deduction-id="${deduction?.deduction_source}" data-update-type="allowance_percentage">
        </div>
        <div>
          <label for="${inputPersonalUsagePercentageId}">Personal Usage(%)</label>
          <input type="number" min="0" max='100' id=${inputPersonalUsagePercentageId} value="${deduction?.personal_usage_percentage}" data-submission-id="${submissionId}" data-deduction-id="${deduction?.deduction_source}" data-update-type="personal_usage_percentage">
        </div>
        <div>
          <label for="${inputNoteId}">Note</label>
          <textarea id=${inputNoteId} data-submission-id="${submissionId}" data-deduction-id="${deduction?.deduction_source}" data-update-type="note">${deduction?.note}</textarea>
        </div>
      </div>
      `
  let node = createNodeFromMarkup(deductionMarkup)
  let inputAmount = node.querySelector(`#${inputAmountId}`)
  let inputAllowancePercentage = node.querySelector(`#${inputAllowancePercentageId}`)
  let inputPersonalUsage = node.querySelector(`#${inputPersonalUsagePercentageId}`)
  let inputNote = node.querySelector(`#${inputNoteId}`)

  addEventListenersToElements(inputAmount, 'input', validateMaxValue)
  addEventListenersToElements([inputAmount, inputAllowancePercentage, inputPersonalUsage, inputNote], 'input', handleDeductionUpdate)
  addEventListenersToElements([inputAmount, inputAllowancePercentage, inputPersonalUsage], 'input', [updateTotalDeduction, updateNetProfit])
  addEventListenersToElements([inputAllowancePercentage, inputPersonalUsage], 'input', validatePercentageValue)

  monthContainer.appendChild(node)

  deductionsContainer.appendChild(deductionContainer)
}

function validateMaxValue(e){
  let input = e.target
  let value = parseFloat(e.target.value) || 0
  if (value>DB_MAX_INT_VALUE){
    input.setCustomValidity(`Your input is grater than ${DB_MAX_INT_VALUE}!`);
    input.reportValidity();
  }else{
    input.setCustomValidity("");
  }
}

function validatePercentageValue(e){
  let input = e.target
  let value = parseFloat(e.target.value) || 0
  if (!(value>=0 && value<=100)){
    input.setCustomValidity(`Your input should be between 0 and 100!`);
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
async function handleTaxableIncomeSearch(e){
  let searchText = e.target.value || ''
  let taxableIncomeSources = await getTaxableIncomeSources()
  let displayableIncomeSources = await getDisplayableSources(taxableIncomeSources, displayingTaxableIncomeIds, searchText)

  displayTaxableIncomeOptions(displayableIncomeSources)
}
async function handleSelfemploymentIncomeSearch(e){
  let searchText = e.target.value || ''
  let incomeSources = await getSelfemploymentIncomeSources()
  let displayableIncomeSources = await getDisplayableSources(incomeSources, displayingSelfemploymentIncomeIds, searchText)

  displaySelfemploymentIncomeOptions(displayableIncomeSources)
}
async function handleExpenseSearch(e){
  let searchText = e.target.value || ''
  let expenseSources = await getExpneseSources()
  let displayableExpenseSources = await getDisplayableSources(expenseSources, displayingExpenseIds, searchText)

  displayExpenseOptions(displayableExpenseSources)
}
async function handleDeductionSearch(e){
  let searchText = e.target.value || ''
  let deductionSources = await getDeductionSources()
  let displayableDeductionSources = await getDisplayableSources(deductionSources, displayingDeductionIds, searchText)
  
  displayDeductionOptions(displayableDeductionSources)
}
async function getDisplayableSources(allSources, displayingSourceIds, searchText=''){
  let displayableIncomeSources = allSources.filter(source=>!displayingSourceIds.has(source.id) && source.name.toLowerCase().includes(searchText.trim().toLowerCase()))
  return displayableIncomeSources
}
async function displayTaxableIncomeOptions(displayableTaxableIncomeSources=null){
  let incomeSources = await getTaxableIncomeSources()
  if (displayableTaxableIncomeSources==null) displayableTaxableIncomeSources = await getDisplayableSources(incomeSources, displayingTaxableIncomeIds)
  taxableIncomeSearchOptions.innerHTML = ''
  displayableTaxableIncomeSources.forEach(incomeSource=>{
    let option = createHtmlElement('div', {'data-taxable-income-id': incomeSource.id})
    option.textContent = incomeSource.name
    taxableIncomeSearchOptions.appendChild(option)
  })
}
async function displaySelfemploymentIncomeOptions(displayableIncomeSources=null){
  let incomeSources = await getSelfemploymentIncomeSources()
  if (displayableIncomeSources==null) displayableIncomeSources = await getDisplayableSources(incomeSources, displayingSelfemploymentIncomeIds)
  selfemploymentIncomeSearchOptions.innerHTML = ''
    displayableIncomeSources.forEach(incomeSource=>{
      let option = createHtmlElement('div', {'data-income-id': incomeSource.id})
      option.textContent = incomeSource.name
      selfemploymentIncomeSearchOptions.appendChild(option)
    })
}
async function displayExpenseOptions(displayableExpenseSources=null){
  let expenseSources = await getExpneseSources()
  if (displayableExpenseSources==null) displayableExpenseSources = await getDisplayableSources(expenseSources, displayingExpenseIds)
  expenseSearchOptions.innerHTML = ''
  displayableExpenseSources.forEach(expenseSource=>{
      let option = createHtmlElement('div', {'data-expense-id': expenseSource.id})
      option.textContent = expenseSource.name
      expenseSearchOptions.appendChild(option)
    })
}
async function displayDeductionOptions(displayableDeductionSources=null){
  let deductionSources = await getDeductionSources()
  if (displayableDeductionSources==null) displayableDeductionSources = await getDisplayableSources(deductionSources, displayingDeductionIds)
  deductionSearchOptions.innerHTML = ''
  displayableDeductionSources.forEach(deductionSource=>{
      let option = createHtmlElement('div', {'data-deduction-id': deductionSource.id})
      option.textContent = deductionSource.name
      deductionSearchOptions.appendChild(option)
    })
}

async function handleTaxableIncomeSelect(e){
  let {taxableIncomeId} = e.target.dataset
  if (taxableIncomeId && parseInt(taxableIncomeId)){
    taxableIncomeId = parseInt(taxableIncomeId)
    displayTaxableIncomeSource(taxableIncomeId, [], await getSubmissionDetails())
    displayTaxableIncomeOptions()
  }
}
async function handleSelfemploymentIncomeSelect(e){
  let {incomeId} = e.target.dataset
  if (incomeId && parseInt(incomeId)){
    incomeId = parseInt(incomeId)
    displaySelfemploymentIncomeSource(incomeId, [], await getSubmissionDetails())
    displaySelfemploymentIncomeOptions()
  }
}
async function handleExpenseSelect(e){
  let {expenseId} = e.target.dataset
  if (expenseId && parseInt(expenseId)){
    expenseId = parseInt(expenseId)
    displayExpenseSource(expenseId, [], await getSubmissionDetails())
    displayExpenseOptions()
  }
}
async function handleDeductionSelect(e){
  let {deductionId} = e.target.dataset
  if (deductionId && parseInt(deductionId)){
    deductionId = parseInt(deductionId)
    displayDeductionSource(deductionId, [], await getSubmissionDetails())
    displayDeductionOptions()
  }
}


function handleTaxableIncomeUpdate(e){
  let inputField = e.target
  let {submissionId, taxableIncomeId, updateType} = inputField.dataset
  let data_object = {} // amount or comission or both must be specified

  if (updateType==="amount") data_object.amount = parseFloat(inputField.value) || 0
  else if (updateType==="taxable_income_tax_amount") data_object.taxable_income_tax_amount = parseFloat(inputField.value) || 0
  else if (updateType==="note") data_object.note = inputField.value

  fetch_url({
    // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
    url: `/accounts/set_taxable_income/${submissionId}/${taxableIncomeId}/`,
    req_method: "POST",
    data_object: JSON.stringify(data_object)
  })
}

function handleSelfemploymentIncomeUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, incomeId, updateType} = inputField.dataset
  let data_object = {} // amount or comission or both must be specified

  if (updateType==="amount") data_object.amount = parseFloat(inputField.value) || 0
  else if (updateType==="comission") data_object.comission = parseFloat(inputField.value) || 0
  else if (updateType==="note") data_object.note = inputField.value

  fetch_url({
    // url = "/accounts/set_income/<submission_id>/<month_id>/<income_id>/"
    url: `/accounts/set_income/${submissionId}/${monthId}/${incomeId}/`,
    req_method: "POST",
    data_object: JSON.stringify(data_object)
  })
}

function handleExpenseUpdate(e){
  let inputField = e.target
  let {submissionId, monthId, expenseId, updateType} = inputField.dataset
  let data_object = { } // amount or personal_usage_percentage must be specified

  if (updateType==="amount") data_object.amount = parseFloat(inputField.value) || 0
  else if (updateType==="personal_usage_percentage") data_object.personal_usage_percentage = parseFloat(inputField.value) || 0
  else if (updateType==="note") data_object.note = inputField.value

  fetch_url({
    // url = "/accounts/set_expense/<submission_id>/<month_id>/<expense_id>/"
    url: `/accounts/set_expense/${submissionId}/${monthId}/${expenseId}/`,
    req_method: "POST",
    data_object: JSON.stringify(data_object)
  })
}

function handleDeductionUpdate(e){
  let inputField = e.target
  let {submissionId, deductionId, updateType} = inputField.dataset
  let data_object = { } // amount or personal_usage_percentage or allowance_percentage must be specified

  if (updateType==="amount") data_object.amount = parseFloat(inputField.value) || 0
  else if (updateType==="allowance_percentage") data_object.allowance_percentage = parseFloat(inputField.value) || 0
  else if (updateType==="personal_usage_percentage") data_object.personal_usage_percentage = parseFloat(inputField.value) || 0
  else if (updateType==="note") data_object.note = inputField.value

  fetch_url({
    // url = "/accounts/set_deduction/<submission_id>/<deduction_id>/"
    url: `/accounts/set_deduction/${submissionId}/${deductionId}/`,
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
