import { deepCompare, catchErrorAndLog } from "./utilities.js";
import DATA from "./parse_data.js";

//====================================================================================================================================
// get data from backend
export async function db_all_records(all_url = DATA.all_url, tax_year = null) {
	if (tax_year === null) tax_year = DATA.tax_year;
	let params = { tax_year: tax_year };
	let search_param = new URLSearchParams(params).toString();

	let url_to_fetch = `${all_url}?${search_param}`;

	let kwargs = {
		url: url_to_fetch,
		req_method: "GET",
	};
	const records = await fetch_url(kwargs)
		.then((res) => res.json()) // convert response to JSON
		.then((data) => data); // recieve json data
	return records; // return data
}

export async function db_search_records(
	search_text,
	search_url = DATA.search_url,
	tax_year = null
) {
	if (tax_year === null) tax_year = DATA.tax_year;
	let params = { q: search_text, tax_year: tax_year };
	let search_param = new URLSearchParams(params).toString();

	let url_to_fetch = `${search_url}?${search_param}`;

	let kwargs = {
		url: url_to_fetch,
		req_method: "GET",
	};
	const records = await fetch_url(kwargs)
		.then((res) => res.json()) // convert response to JSON
		.then((data) => data); // recieve json data
	return records; // return data
}
export async function db_search_records_client_id(
	client_id,
	search_url = DATA.search_url
) {
	let params = { client_id: client_id };
	let search_param = new URLSearchParams(params).toString();
	let kwargs = {
		url: `${search_url}?${search_param}`,
		req_method: "GET",
	};
	const records = await fetch_url(kwargs)
		.then((res) => res.json()) // convert response to JSON
		.then((data) => data); // recieve json data
	return records; // return data
}

// =============================================================================================================================
// Api caller

function cache_duration_calc({
	hours = 0,
	minutes = 0,
	seconds = 0,
	milliseconds = 0,
}) {
	return (hours * 60 * 60 + minutes * 60 + seconds) * 1000 + milliseconds;
}
let API_CACHE = null;
let cache_duration_obj = { hours: 3 };
const max_cache_duration = cache_duration_calc(cache_duration_obj);

async function evict_cache() {
	if (API_CACHE !== null) return;

	let keys = await caches.keys();
	let new_key = new Date().getTime();
	let keys_to_number = keys.map((key) => Number(key)).sort((a, b) => a - b);

	let is_latest_key_valid =
		new Date().getTime() - keys_to_number[keys_to_number.length - 1] <
		max_cache_duration;
	if (is_latest_key_valid) {
		// Reuse valid cache
		new_key = keys_to_number.pop();
	}

	for (let key of keys_to_number) {
		// Remove expired caches
		caches.delete(key.toString());
	}

	caches.open(new_key.toString()).then((cache) => {
		console.log("Cache duration:", cache_duration_obj);
		console.log("Cache created:", new Date(new_key).toISOString());
		console.log(
			"Eviction time:",
			new Date(new_key + max_cache_duration).toISOString()
		);
		API_CACHE = cache;
		globalThis.API_CACHE = cache;
	});
}
await evict_cache();

// Evict cache after max_cache_duration
// setTimeout(() => {
//   evict_cache();
// }, max_cache_duration);

const cache_url_match_rules = [RegExp("\/details|\/all|id=")];
const no_cache_url_match_rules = [RegExp("/search")];
export async function fetch_url({
	url,
	req_method,
	data_object = {},
	headers = { "Content-Type": "application/json" },
	others = {},
}) {
	catchErrorAndLog(showLoadingIndicator);
	req_method = req_method.toUpperCase();
	if (deepCompare(others, {})) {
		others = {
			credentials: "same-origin",
			cache: "no-cache",
			mode: "cors", // no-cors, *cors, same-origin
			redirect: "follow", // manual, *follow, error
			referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin,
			// same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
		};
	}
	if (req_method === "GET") {
		// send GET request
		let request = new Request(url, {
			method: req_method,
			headers: headers,
			...others,
		});

		if (
			no_cache_url_match_rules.some((rule) => rule.test(url)) ||
			!cache_url_match_rules.some((rule) => rule.test(url))
		) {
			let response = await fetch(request); // none of the rules matched, do not cache
			catchErrorAndLog(hideLoadingIndicator);
			return response;
		}

		// check if request is in cache
		if (!API_CACHE) await evict_cache();
		let response = await API_CACHE.match(request);
		if (response) {
			catchErrorAndLog(hideLoadingIndicator);
			return response;
		}
		// not found in cache so fetch from server
		response = await fetch(request);
		API_CACHE.put(request, response.clone());
		catchErrorAndLog(hideLoadingIndicator);
		return response;
	} else {
		// send other requests
		let response = await fetch(url, {
			method: req_method,
			headers: headers,
			body:
				typeof data_object == "string"
					? data_object
					: JSON.stringify(data_object),
			...others,
		});
		catchErrorAndLog(hideLoadingIndicator);
		return response;
	}
}

// =============================================================================================================================
// Show and hide loading indicator when data is loading
const loading_indicator_selector = "#loading-indicator";

export function showLoadingIndicator() {
	let loading_indicator = document.querySelector(loading_indicator_selector);
	if (loading_indicator !== null)
		loading_indicator.classList.remove("hidden");
}

export function hideLoadingIndicator() {
	let loading_indicator = document.querySelector(loading_indicator_selector);
	if (loading_indicator !== null) loading_indicator.classList.add("hidden");
}
