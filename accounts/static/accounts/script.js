const Account = {
    clientPK: 0,
    taxYearPK: 0
}


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


let searchOpitonsList = document.querySelectorAll(".search-options")


searchOpitonsList.forEach(searchOptions=>{
    searchOptions.addEventListener("click", e=>{
        let selectedOption = searchOptions.querySelector(".search-option.selected")
        let newSelectedOption = e.target
        if (selectedOption && newSelectedOption) selectedOption.classList.remove("selected")
        if (newSelectedOption) newSelectedOption.classList.add("selected")
    })
})

let clientSearchInput = document.querySelector("#client")
let taxYearSearchInput = document.querySelector("#tax-year")

clientSearchInput.addEventListener("input", (e)=>{
    console.log(e.target.value)
})

taxYearSearchInput.addEventListener("input", (e)=>{
    console.log(e.target.value)
})


