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
    search_box.placeholder = select.options[select.selectedIndex].textContent
  })
});
