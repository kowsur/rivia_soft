import { fetch_url } from "./fetch_data.js";


document.querySelector('button[type="submit"]').addEventListener('click', async (event) => {
    let forms = document.querySelectorAll('form')
    for (let form of forms){
        let statusElement = form.querySelector('select[data-field-name="task_status"]')
        let noteElement = form.querySelector('textarea[data-field-name="note"]')

        let status = statusElement[statusElement.selectedIndex].value
        let note = noteElement.value
        
        let data = {
            'task_id': form.getAttribute('data-task-id'),
            'task_status': status,
            'note': note
        }
        
        fetch_url({
            url: form.action,
            req_method: form.method,
            data_object: data
        })
    }
})
