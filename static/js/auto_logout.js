const ACTIVITY_CHECK_INTERVAL = 1000; // Check activity every 1 second
const AUTO_LOGOUT_AFTER = (20 * 60 * 1000) - (2 * ACTIVITY_CHECK_INTERVAL); // 20 minutes in milliseconds
const LOGOUT_URL = "/u/logout/"; // URL to logout endpoint
const LOGIN_URL = "/u/login/"; // URL to redirect after logout
const LAST_ACTIVITY_KEY = "auto_logout_last_activity"; // Key to store last activity timestamp

const other_tabs_creation_time = [];
const tab_creation_time = new Date();
const auto_logout_bc = new BroadcastChannel("auto_logout_channel");
let auto_logout_interval = null;


// Listen to broadcast messages
auto_logout_bc.addEventListener("message", (event) => {
	let msg = event.data;
	switch (msg.type) {
        // actions to be performed by all tabs
		case "do__reload":
			if (location.href.includes("login")) {
                location.reload()
            };
			break;
		case "do__redirect_to_login":
			if (!location.href.includes("/u/login")) {
                redirect_to_login()
            };
			break;

        // queries from other tabs
		case "query__tab_creation_time?":
			auto_logout_bc.postMessage({
				type: "reply__tab_creation_time?",
				tab_creation_time: tab_creation_time,
			});
			break;

        // replies from other tabs
		case "reply__tab_creation_time?":
			other_tabs_creation_time.push(msg.tab_creation_time);
			break;
		default:
			break;
	}
});

auto_logout_bc.postMessage({ type: "query__tab_creation_time?" });

// Wait for the reply from other tabs
setTimeout(() => {
	if (!location.href.includes("login")) {
        addActivityListeners();
		auto_logout_bc.postMessage({ type: "do__reload" }); // reload tabs that were logged out
    
        auto_logout_interval = setInterval(
            checkActivity,
            ACTIVITY_CHECK_INTERVAL
        );
	}
}, ACTIVITY_CHECK_INTERVAL);


//================================================================================================
// functions 
const debounced_writeLastActivity = debounce(()=>{
    let last_activity = new Date();
    localStorage.setItem(LAST_ACTIVITY_KEY, last_activity.toISOString());
}, ACTIVITY_CHECK_INTERVAL/2);
debounced_writeLastActivity();
function updateLastActivity() {
    debounced_writeLastActivity();
}

function logout() {
	window.location.href = LOGOUT_URL; // Redirect to logout endpoint
	auto_logout_bc.postMessage({ type: "do__redirect_to_login" });
}
function redirect_to_login() {
	next_url = window.location.href;
	window.location.href = `${LOGIN_URL}?next=${next_url}`; // Redirect to login page
}

function checkActivity() {
	let last_activity = localStorage.getItem(LAST_ACTIVITY_KEY);
	if (!last_activity) return;

    auto_logout_bc.postMessage({ type: "query__tab_creation_time?" });
    last_activity = new Date(Date.parse(last_activity));
    let current_time = new Date();
    let time_diff = current_time - last_activity;

    setTimeout(() => {
        other_tabs_creation_time.sort((a, b) => b-a);
        let am_i_oldest = other_tabs_creation_time.length>0 && tab_creation_time > other_tabs_creation_time[0];
        if (time_diff > AUTO_LOGOUT_AFTER && (other_tabs_creation_time.length==0 || am_i_oldest)) {
            logout();
        }
    }, ACTIVITY_CHECK_INTERVAL);
}

const ACTIVITY_EVENTS = [
    "click",
    "scroll",
	"mousemove",
	"keypress",
	"touchstart",
	"visibilitychange",
];
function removeActivityListeners() {
	ACTIVITY_EVENTS.forEach((event) => {
		document.removeEventListener(event, updateLastActivity);
	});
}
function addActivityListeners() {
	ACTIVITY_EVENTS.forEach((event) => {
		document.addEventListener(event, updateLastActivity);
	});
}


function debounce(func, delay) {
    let last_call = 0;
    let timerId;
    return function (...args) {
        clearTimeout(timerId);
        let curr_call = new Date().getTime();
        
        if (curr_call-last_call > delay) {
            func(...args);
            last_call = curr_call;
            timerId = null;
        } else{
            timerId = setTimeout(function () {
                func(...args);
            }, delay);
        }
    };
}

