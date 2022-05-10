const jsonData = document.querySelector('pre[type="application/json"]')
let DATA = {}

const tax_year_select_input = document.querySelector('select#tax_years')
function getSelectedTaxYear(){
  if (tax_year_select_input===null) return null

  let selectedTaxYearOption = tax_year_select_input.options[tax_year_select_input.selectedIndex]
  let tax_year = selectedTaxYearOption.value
  return tax_year
}

if (jsonData!==null){
  DATA = JSON.parse(jsonData.innerHTML)
  DATA.tax_year = getSelectedTaxYear()
  if (tax_year_select_input!==null) {
    tax_year_select_input.addEventListener('input', (e)=>{
      let taskCounters = document.querySelectorAll('.task')
      taskCounters.forEach(taskCounter=>{
        setTimeout(()=>{
          taskCounter.dispatchEvent(new CustomEvent('click', {bubbles:true, cancelable:true, detail: {update_counters_only: true}}))
        }, 600)
      })
    })
    tax_year_select_input.addEventListener('input', (e)=>{
      DATA.tax_year = getSelectedTaxYear()
    })
  }
}

export default DATA
