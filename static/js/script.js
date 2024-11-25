// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------

// BAR CHART
const barChartOptions = {
  series: [
    {
      data: [10, 8, 6, 4, 2],
      name: 'Products',
    },
  ],
  chart: {
    type: 'bar',
    background: 'transparent',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#2962ff', '#d50000', '#2e7d32', '#ff6d00', '#583cb3'],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    opacity: 1,
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  stroke: {
    colors: ['transparent'],
    show: true,
    width: 2,
  },
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
  xaxis: {
    categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
    title: {
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      show: true,
      color: '#55596e',
    },
    axisTicks: {
      show: true,
      color: '#55596e',
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Count',
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
};

const barChart = new ApexCharts(
  document.querySelector('#bar-chart'),
  barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
  series: [
    {
      name: 'Purchase Orders',
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: 'Sales Orders',
      data: [11, 32, 45, 32, 34, 52, 41],
    },
  ],
  chart: {
    type: 'area',
    background: 'transparent',
    height: 350,
    stacked: false,
    toolbar: {
      show: false,
    },
  },
  colors: ['#00ab57', '#d50000'],
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
  dataLabels: {
    enabled: false,
  },
  fill: {
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.1,
      shadeIntensity: 1,
      stops: [0, 100],
      type: 'vertical',
    },
    type: 'gradient',
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  markers: {
    size: 6,
    strokeColors: '#1b2635',
    strokeWidth: 3,
  },
  stroke: {
    curve: 'smooth',
  },
  xaxis: {
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      offsetY: 5,
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: [
    {
      title: {
        text: 'Purchase Orders',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
    {
      opposite: true,
      title: {
        text: 'Sales Orders',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();







// document.addEventListener('DOMContentLoaded', () => {
//     const contentDiv = document.getElementById('content');

//     document.getElementById('btnDataset').addEventListener('click', showDataset);
//     document.getElementById('btnDistribution').addEventListener('click', showDistribution);
//     document.getElementById('btnRelationship').addEventListener('click', showRelationships);
//     document.getElementById('btnStatusCount').addEventListener('click', showStatusCount);
//     document.getElementById('btnPrediction').addEventListener('click', showPrediction);

//     function showDataset() {
//         fetch('data.php')
//             .then(response => response.json())
//             .then(data => {
//                 let table = '<table border="1"><tr>';
//                 Object.keys(data[0]).forEach(header => {
//                     table += `<th>${header}</th>`;
//                 });
//                 table += '</tr>';
//                 data.forEach(row => {
//                     table += '<tr>';
//                     Object.values(row).forEach(value => {
//                         table += `<td>${value}</td>`;
//                     });
//                     table += '</tr>';
//                 });
//                 table += '</table>';
//                 contentDiv.innerHTML = table;
//             });
//     }

//     function showDistribution() {
//         fetch('data.php')
//             .then(response => response.json())
//             .then(data => {
//                 const ranges = data.map(row => parseFloat(row.Range));
//                 const labels = data.map(row => row.Date);

//                 const chartDiv = '<canvas id="distChart"></canvas>';
//                 contentDiv.innerHTML = chartDiv;

//                 const ctx = document.getElementById('distChart').getContext('2d');
//                 new Chart(ctx, {
//                     type: 'bar',
//                     data: {
//                         labels: labels,
//                         datasets: [{
//                             label: 'Range Distribution',
//                             data: ranges,
//                             backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                             borderColor: 'rgba(75, 192, 192, 1)',
//                             borderWidth: 1
//                         }]
//                     },
//                     options: {
//                         scales: {
//                             y: { beginAtZero: true }
//                         }
//                     }
//                 });
//             });
//     }

//     function showRelationships() {
//         contentDiv.innerHTML = `
//             <h2>Select Variables to Analyze Relationships:</h2>
//             <select id="varX">
//                 <option value="Range">Range</option>
//                 <option value="Speed">Speed</option>
//                 <option value="MaintenanceCost">Maintenance Cost</option>
//             </select>
//             <select id="varY">
//                 <option value="Speed">Speed</option>
//                 <option value="MaintenanceCost">Maintenance Cost</option>
//                 <option value="Range">Range</option>
//             </select>
//             <button onclick="plotRelationship()">Plot</button>
//             <div id="chartDiv"></div>
//         `;
//     }

//     function plotRelationship() {
//         const varX = document.getElementById('varX').value;
//         const varY = document.getElementById('varY').value;

//         fetch('data.php')
//             .then(response => response.json())
//             .then(data => {
//                 const xValues = data.map(row => parseFloat(row[varX]));
//                 const yValues = data.map(row => parseFloat(row[varY]));

//                 const chartDiv = document.getElementById('chartDiv');
//                 Plotly.newPlot(chartDiv, [{
//                     x: xValues,
//                     y: yValues,
//                     mode: 'markers',
//                     type: 'scatter'
//                 }], { title: `Relationship: ${varX} vs ${varY}` });
//             });
//     }

//     function showStatusCount() {
//         fetch('data.php')
//             .then(response => response.json())
//             .then(data => {
//                 const statusCount = {};
//                 data.forEach(row => {
//                     const status = row.Status;
//                     statusCount[status] = (statusCount[status] || 0) + 1;
//                 });

//                 const chartDiv = '<canvas id="statusChart"></canvas>';
//                 contentDiv.innerHTML = chartDiv;

//                 const ctx = document.getElementById('statusChart').getContext('2d');
//                 new Chart(ctx, {
//                     type: 'pie',
//                     data: {
//                         labels: Object.keys(statusCount),
//                         datasets: [{
//                             label: 'Status Count',
//                             data: Object.values(statusCount),
//                             backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
//                         }]
//                     }
//                 });
//             });
//     }

//     function showPrediction() {
//         fetch('predict.php')
//             .then(response => response.json())
//             .then(data => {
//                 let form = `
//                     <h2>Predict Range</h2>
//                     <label for="vehicleID">Select Vehicle ID:</label>
//                     <select id="vehicleID">
//                 `;
//                 data.forEach(row => {
//                     form += `<option value="${row.VehicleID}">${row.VehicleID}</option>`;
//                 });
//                 form += `
//                     </select>
//                     <button onclick="getPrediction()">Get Prediction</button>
//                     <div id="predictionResult"></div>
//                 `;
//                 contentDiv.innerHTML = form;
//             });
//     }

//     function getPrediction() {
//         const vehicleID = document.getElementById('vehicleID').value;
//         fetch('predict.php?vehicleID=' + vehicleID)
//             .then(response => response.json())
//             .then(data => {
//                 document.getElementById('predictionResult').innerHTML = `
//                     <h3>Predicted Range for Vehicle ${vehicleID}: ${data.PredictedRange} km</h3>
//                 `;
//             });
//     }
// });


