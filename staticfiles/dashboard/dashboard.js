console.log("Dashboard Loaded");
const greeting = document.getElementById("greeting");

if (greeting) {

    const hour = new Date().getHours();

    let icon = "";
    let message = "";

    if (hour < 12) {

        icon = '<i class="fa-solid fa-sun"></i>';
        message = "Good Morning";

    } else if (hour < 18) {

        icon = '<i class="fa-solid fa-cloud-sun"></i>';
        message = "Good Afternoon";

    } else {
        icon = '<i class="fa-solid fa-moon"></i>';
        message = "Good Evening";
    }
    const username = greeting.dataset.username;
    greeting.innerHTML = `${icon} ${message}, ${username}`;
}

// ==============================
// toggle for mobile
// ==============================
const menuToggle = document.querySelector(".menu-toggle");
const sidebar = document.querySelector(".sidebar");

menuToggle.addEventListener("click", () => {

sidebar.classList.toggle("active");

});

// =========================
// CAMPAIGN_LIST
// =========================

function copyCampaignLink(campaignId) {

    console.log("Campaign ID:", campaignId);

    const input = document.getElementById(`link-${campaignId}`);

    console.log("Input found:", input);

    if (!input) {
        return;
    }

    navigator.clipboard.writeText(input.value);

    alert("Referral link copied!");
}

// =========================
// CAMPAIGN_DETAILS
// =========================
function copyReferralLink() {
    const input = document.getElementById("referralLink");
    navigator.clipboard.writeText(input.value);
    const button = document.querySelector(".copy-btn");
    button.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
    setTimeout(() => {

        button.innerHTML =
        '<i class="fa-regular fa-copy"></i> Copy';

    },2000);

}
// NOTIFICATION BAR DROPDOWN
const notificationBtn = document.querySelector(".notification-btn");
const notificationDropdown = document.querySelector(".notification-dropdown");

if (notificationBtn && notificationDropdown) {

    notificationBtn.addEventListener("click", function (e) {

        e.stopPropagation();

        notificationDropdown.classList.toggle("show");

    });

    document.addEventListener("click", function () {

        notificationDropdown.classList.remove("show");

    });

    notificationDropdown.addEventListener("click", function (e) {

        e.stopPropagation();

    });

}

// Notifications page mark read

document.querySelectorAll(".mark-read-btn").forEach(button => {

    button.addEventListener("click", function(e) {

        e.preventDefault();

        const url = this.dataset.url;

        fetch(url, {

            method: "POST",

            headers: {

                "X-CSRFToken": csrftoken,

                "X-Requested-With": "XMLHttpRequest"

            }

        })

        .then(response => response.json())

        .then(data => {

            console.log("Fetch successful", data);

            if (data.success) {

                const card =
                this.closest(".notification-card");

                if (card) {

                    card.classList.add("removing");

                    setTimeout(() => {

                        card.remove();

                        const body =
                        document.querySelector(".notification-list");

                        if (body) {

                            const remainingNotifications =
                            body.querySelectorAll(
                                ".notification-card"
                            );

                            console.log(
                                "Remaining:",
                                remainingNotifications.length
                            );

                            if (
                                remainingNotifications.length === 0
                            ) {

                                body.innerHTML = `

                                    <div class="empty-state">

                                        <i class="fa-regular fa-bell-slash"></i>

                                        <h3>No notifications yet</h3>

                                        <p>
                                            You'll see referral activity,
                                            rewards and important updates here.
                                        </p>

                                    </div>

                                `;

                            }

                        }

                    }, 300);

                }


                // 🔔 Update notification count

                const badge =
                document.getElementById(
                    "notification-count"
                );

                if (badge) {

                    let count =
                    parseInt(badge.textContent);

                    count--;

                    if (count <= 0) {

                        badge.remove();

                    } else {

                        badge.textContent = count;

                    }

                }


                // 🔔 Shake notification bell

                const bell =
                document.querySelector(
                    ".notification-btn"
                );

                if (bell) {

                    bell.classList.add("shake");

                    setTimeout(() => {

                        bell.classList.remove("shake");

                    }, 400);

                }

            }

        });

    });

});


function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;

            }

        }

    }

    return cookieValue;

}

// mark all as read
const markAll =
document.getElementById("mark-all-read");

if(markAll){

    markAll.addEventListener("click", function(){

        fetch("/notifications/read-all/",{

            method:"POST",

            headers:{

                "X-CSRFToken":csrftoken,

                "X-Requested-With":"XMLHttpRequest"

            }

        })

        .then(response=>response.json())

        .then(data=>{

            if(data.success){

                document.querySelectorAll(".notification-item")
                .forEach(card=>{

                    card.classList.remove("unread");

                });

                document.querySelectorAll(".mark-read-btn")
                .forEach(button=>{

                    button.remove();

                });

                const badge =
                document.getElementById("notification-count");

                if(badge){

                    badge.remove();

                }

            }

        });

    });

}

const csrftoken = getCookie("csrftoken");

// Notification modal

const modal =
document.getElementById("confirm-modal");

const clearBtn =
document.getElementById("clear-all-btn");

const cancelBtn =
document.getElementById("cancel-delete");


if (modal && clearBtn && cancelBtn) {

    clearBtn.addEventListener("click", () => {

        modal.classList.add("show");

    });


    cancelBtn.addEventListener("click", () => {

        modal.classList.remove("show");

    });


    modal.addEventListener("click", (e) => {

        if (e.target === modal) {

            modal.classList.remove("show");

        }

    });

}

// Confirm delete

const confirmDelete =
document.getElementById("confirm-delete");

if (confirmDelete) {

    confirmDelete.addEventListener("click", () => {

        fetch("/notifications/clear/", {

            method: "POST",

            headers: {

                "X-CSRFToken": csrftoken,

                "X-Requested-With": "XMLHttpRequest"

            }

        })

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                if (modal) {

                    modal.classList.remove("show");

                }

                const body =
                document.querySelector(".notification-list");

                if (body) {

                    body.innerHTML = `

                        <div class="empty-state">

                            <i class="fa-regular fa-bell-slash"></i>

                            <h3>No notifications yet</h3>

                            <p>
                                You'll see referral activity,
                                rewards and important updates here.
                            </p>

                        </div>

                    `;

                }

                const badge =
                document.getElementById("notification-count");

                if (badge) {

                    badge.remove();

                }

            }

        });

    });

}

// CHART ANALYTICS
const referralChart = document.getElementById("referralStatusChart");

if (referralChart) {

    const pending =
        JSON.parse(
            document.getElementById("pending-data").textContent
        );

    const approved =
        JSON.parse(
            document.getElementById("approved-data").textContent
        );

    const rewarded =
        JSON.parse(
            document.getElementById("rewarded-data").textContent
        );

    new Chart(referralChart, {

        type: "doughnut",

        data: {

            labels: [

                "Pending",

                "Approved",

                "Rewarded"

            ],

            datasets: [

                {

                    data: [

                        pending,

                        approved,

                        rewarded

                    ],

                    backgroundColor: [

                        "#F59E0B",

                        "#10B981",

                        "#2563EB"

                    ],

                    borderWidth: 0

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

const monthlyChart =
document.getElementById("monthlyGrowthChart");

if(monthlyChart){

const labels =
JSON.parse(
document.getElementById("growth-labels").textContent
);

const data =
JSON.parse(
document.getElementById("growth-data").textContent
);

new Chart(monthlyChart,{

type:"line",

data:{

labels:labels,

datasets:[{

label:"Referrals",

data:data,

borderColor:"#2563EB",

backgroundColor:"rgba(37,99,235,.08)",

fill:true,

tension:.4,

pointRadius:4,

pointHoverRadius:6

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{
display:false
}

},

scales:{

y:{
beginAtZero:true
}

},
interaction:{
mode:"index",
intersect:false
},

elements:{
line:{
borderWidth:3
}
}

}

});

}

