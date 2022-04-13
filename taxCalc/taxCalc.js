// Took these from https://www.which.co.uk/static/tools/new-reviews/income-tax-calculator/income-tax-calculator.html
// Files:
//      1. income-tax-calculator.js - https://www.which.co.uk/static/tools/new-reviews/income-tax-calculator/js/income-tax-calculator.js
//      2. master-tax-values.js - https://www.which.co.uk/static/tools/new-reviews/js/master-tax-values.js

let lowThreshold, midThreshold, highThreshold, lowRate, midRate, highRate, taxYear;

taxYear='21-22'
setTaxYear(taxYear)
// Income tax

lowRate = 0.2
midRate = 0.4
highRate = 0.45

highThreshold = 150000


function setTaxYear(taxYear){
    if (taxYear == '18-19') {
        // Income tax
        lowThreshold = 11850
        midThreshold = 46350
    } else if (taxYear == '19-20') {
        // Income tax
        lowThreshold = 12500
        midThreshold = 50000
    } else if (taxYear == '20-21') {
        // Income tax
        lowThreshold = 12500
        midThreshold = 50000
    } else if (taxYear == '21-22') {
        // Income tax
        lowThreshold = 12570
        midThreshold = 50270
    } else if (taxYear == '22-23') {
        // Income tax
        lowThreshold = 12570
        midThreshold = 50270
    }
}



export function calculateTax(income, updateTaxYear, personalAllowanceLimit = 100000) {
    if (updateTaxYear) setTaxYear(updateTaxYear)
    
    income = Number(income);
    let totalTax = 0

    // Calculate threshold when earning over 100,000
    let subtractor = 0
    if (income >= personalAllowanceLimit) {
      subtractor = (income - personalAllowanceLimit) / 2;
      if (subtractor > lowThreshold) {
        subtractor = lowThreshold;
      }
      lowThreshold = lowThreshold - subtractor;
      midThreshold = midThreshold - subtractor;
    }

    if (income >= highThreshold) {
        let highPayment = (income - highThreshold) * highRate;
        let midPayment = (highThreshold - midThreshold) * midRate;
        let lowPayment = (midThreshold - lowThreshold) * lowRate;
        totalTax = highPayment + midPayment + lowPayment;

    } else if (income < highThreshold && income >= midThreshold) {
        let midPayment = (income - midThreshold) * midRate;
        let lowPayment = (midThreshold - lowThreshold) * lowRate;
        totalTax = midPayment + lowPayment;

    } else if (income < midThreshold && income >= lowThreshold) {
        let lowPayment = (income - lowThreshold) * lowRate;
        totalTax = lowPayment;
    }

    let incomeTax = Number(totalTax).toFixed(2);
    return incomeTax
}


let totalTaxContainer = document.querySelector('[data-total-tax-container]')

let form = document.querySelector('form')
let incomeInput = document.querySelector('input#income')

form.addEventListener('submit', updateTotalIncome)


function updateTotalIncome(e){
    e.preventDefault()

    let income = incomeInput.value

    totalTaxContainer.textContent = calculateTax(income, '22-23')
}

let incomes = [10000, 20000, 50000, 75000, 80000, 110000, 130000, 180000, 200000]

incomes.forEach(inc=>{
    console.log('income', inc, 'tax', calculateTax(inc))
    console.log('\n')
})
