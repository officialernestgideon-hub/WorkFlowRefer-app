// CHART ANALYTICS
// const referralChart = document.getElementById("referralStatusChart");

// if (referralChart) {

//     const pending =
//         JSON.parse(
//             document.getElementById("pending-data").textContent
//         );

//     const approved =
//         JSON.parse(
//             document.getElementById("approved-data").textContent
//         );

//     const rewarded =
//         JSON.parse(
//             document.getElementById("rewarded-data").textContent
//         );

//     new Chart(referralChart, {

//         type: "doughnut",

//         data: {

//             labels: [

//                 "Pending",

//                 "Approved",

//                 "Rewarded"

//             ],

//             datasets: [

//                 {

//                     data: [

//                         pending,

//                         approved,

//                         rewarded

//                     ],

//                     backgroundColor: [

//                         "#F59E0B",

//                         "#10B981",

//                         "#2563EB"

//                     ],

//                     borderWidth: 0

//                 }

//             ]

//         },

//         options: {

//             responsive: true,

//             maintainAspectRatio: false,

//             plugins: {

//                 legend: {

//                     position: "bottom"

//                 }

//             }

//         }

//     });

// }

// const monthlyChart =
// document.getElementById("monthlyGrowthChart");

// if(monthlyChart){

// const labels =
// JSON.parse(
// document.getElementById("growth-labels").textContent
// );

// const data =
// JSON.parse(
// document.getElementById("growth-data").textContent
// );

// new Chart(monthlyChart,{

// type:"line",

// data:{

// labels:labels,

// datasets:[{

// label:"Referrals",

// data:data,

// borderColor:"#2563EB",

// backgroundColor:"rgba(37,99,235,.08)",

// fill:true,

// tension:.4,

// pointRadius:4,

// pointHoverRadius:6

// }]

// },

// options:{

// responsive:true,

// maintainAspectRatio:false,

// plugins:{

// legend:{
// display:false
// }

// },

// scales:{

// y:{
// beginAtZero:true
// }

// },
// interaction:{
// mode:"index",
// intersect:false
// },

// elements:{
// line:{
// borderWidth:3
// }
// }

// }

// });

// }

