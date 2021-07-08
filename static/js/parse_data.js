const jsonData = document.querySelector('pre[type="application/json"]')
let DATA = {}

if (jsonData!==null){
  DATA = JSON.parse(jsonData.innerHTML)
}

export default DATA
