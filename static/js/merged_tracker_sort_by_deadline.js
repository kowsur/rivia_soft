function sort_func(a, b){
    if (a.fields.deadline > b.fields.deadline) return -1
    if (a.fields.deadline < b.fields.deadline) return 1
    return 0
}
function filter_remove_future_deadlines(record){
    return record.fields.deadline <= getToday()
}
function getToday(format="YYYY-MM-DD"){
    return dayjs(new Date).format(format)
}


export default function merge_sorted_trackers(limited_trackers=[], selfassesment_trackers=[], remove_records_with_future_deadlines=false){
    if (remove_records_with_future_deadlines){
        limited_trackers = limited_trackers.filter(filter_remove_future_deadlines)
        selfassesment_trackers = selfassesment_trackers.filter(filter_remove_future_deadlines)
    }
    limited_trackers.sort(sort_func)
    selfassesment_trackers.sort(sort_func)
    let merged = []
    let limited_index = 0;
    let selfassesment_index = 0;

    while (limited_index < limited_trackers.length && selfassesment_index < selfassesment_trackers.length){
        let limited_tracker = limited_trackers[limited_index]
        let selfassesment_tracker = selfassesment_trackers[selfassesment_index]

        if(limited_tracker.fields.deadline > selfassesment_tracker.fields.deadline) {
            merged.push(limited_tracker);
            limited_index++;
        }else{
            merged.push(selfassesment_tracker);
            selfassesment_index++;
        }
    }

    // add remaining
    while (limited_index < limited_trackers.length){
        merged.push(limited_trackers[limited_index])
        limited_index++;
    }
    while (selfassesment_index < selfassesment_trackers.length){
        merged.push(selfassesment_trackers[selfassesment_index])
        selfassesment_index++;
    }
    return merged
}
