// =========================
// CAMPAIGN_LIST
// =========================

// function copyCampaignLink(campaignId) {

//     console.log("Campaign ID:", campaignId);

//     const input = document.getElementById(`link-${campaignId}`);

//     console.log("Input found:", input);

//     if (!input) {
//         return;
//     }

//     navigator.clipboard.writeText(input.value);

//     alert("Referral link copied!");
// }

// =========================
// CAMPAIGN_DETAILS
// =========================
// function copyReferralLink() {
//     const input = document.getElementById("referralLink");
//     navigator.clipboard.writeText(input.value);
//     const button = document.querySelector(".copy-btn");
//     button.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
//     setTimeout(() => {

//         button.innerHTML =
//         '<i class="fa-regular fa-copy"></i> Copy';

//     },2000);

// }