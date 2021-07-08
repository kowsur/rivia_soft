import { populate_with_data } from './table.js'
import { db_all_records, db_search_records, db_search_records_client_id } from './fetch_data.js'
import DATA from './parse_data.js'
//table cell compare attribute name = "data-cmp"

// clear messsage after 10 seconds
let delete_message_after = 10000 //milisecond
setTimeout(function(){
  let messages = document.querySelectorAll('.message')
  if (messages){
    for (let element of messages){
      element.remove()
    }
  };
}, delete_message_after);

// ================================================================================================
// Handle reload
document.querySelector('.action-reload').addEventListener('click', async (event) => {
  loadAllRecords()
})

// Search functionality
//setup before functions
let typingTimer;                  //timer identifier
//                milliseconds * seconds
let doneTypingInterval = 1000;//time in ms (4/5 seconds)
//on keyup, start the countdown
// document.getElementById('element-id').addEventListener('keyup', () => {
//     clearTimeout(typingTimer);
//     if (myInput.value) {
//         typingTimer = setTimeout(search_function, doneTypingInterval);
//     }
// });
const search_bar = document.querySelector('input[name="search"]');
if (search_bar){
  search_bar.addEventListener('input', (event)=>{
    let search_url = DATA.search_url
    let search_text = search_bar.value.trim()
    
    // reset timer to prevent extra search
    clearTimeout(typingTimer);
    // set the timer again to call api after doneTypingInterval
    if (search_text===''){
      typingTimer = setTimeout( async () => {
        loadAllRecords()
      }, doneTypingInterval); // Get all the records
    }else{
      typingTimer = setTimeout(async (search_text, search_url)=>{
        let search_records = await db_search_records(search_text, search_url)
        populate_with_data(search_records)
      }, doneTypingInterval, search_text, search_url); // search with text
    }
  })

  // OpenSearch
  let current_url = window.location.href
  let url = new URL(current_url)
  let open_query = url.searchParams.get('q')
  let client_id = url.searchParams.get('client_id')
  if (client_id) {client_id = client_id.trim()}
  if (open_query){open_query=open_query.trim()}

  if (client_id){
    typingTimer = setTimeout(async (client_id, search_url)=>{
      let search_records = await db_search_records_client_id(client_id, search_url)
      populate_with_data(search_records)
    }, 10, client_id, (DATA.search_url)); // search with text
  }
  else if (open_query){
    typingTimer = setTimeout(async (search_text, search_url)=>{
      let search_records = await db_search_records(search_text, search_url)
      populate_with_data(search_records)
    }, 10, open_query, DATA.search_url); // search with text
  }else{
    // when page loads load all the records
    loadAllRecords();
  }
}

export function loadAllRecords(){
  setTimeout(async ()=>{
    let all_records = await db_all_records()
    populate_with_data(all_records)
  }, 10); // search with text
}
