Array.prototype.count = function(item){
            let appearance = 0; //This is the default value
            this.forEach(index=>{
                if (index === item)
                    appearance++
            });
            return appearance;
        }

// <button type="button" class="websites" name="button" onclick="location.href='/mapper/${data[i]['username']}/${data[i]['website']}';">${data[i]['website']}</button>
// <button type="button" class="websites" name="button" onclick="fetchCoordsData(${data[i]['id']})">${data[i]['website']}</button>

// Displaying registered websites
const websitediv = document.querySelector('.websitediv')
const summarytitle = document.querySelector('.summarytitle')
const site_id_context = document.querySelector('.site_id_context').textContent
const websiteUrl = document.querySelector('.websiteUrl')

// fetch('http://127.0.0.1:8000/registered-sites').then(response => response.json())


fetch('http://127.0.0.1:8000/registered-sites').then(response => response.json()).then(data => {
    generateHTML(data)
    for(let y = 0; y < data.length; y++){
      if(data[y]['id'] == site_id_context){
        websiteUrl.textContent = data[y]['website']
        websiteUrl.href = data[y]['website']
      }
    }
})

function generateHTML(data) {
  let itemTemplate = "";
  for(let i = 0; i < data.length; i++){
  itemTemplate += `<button type="button" class="websites" name="button" onclick="location.href='/mapper/${data[i]['username']}/${data[i]['id']}';">${data[i]['website']}</button>`
  websitediv.innerHTML = itemTemplate;
}}
// Displaying registered websites

const totalvisitors = document.querySelector('.totalvisitors')
// const cities = document.querySelector('.cities')
const states = document.querySelector('.states')
const countries = document.querySelector('.countries')
const visitorgraph = document.querySelector('.visitorgraph')


function fetchCoordsData(site_id) {
  // location.reload()
  var lat_array = []
  var long_array = []
  var sum_lat = 0
  var avg_lat = 0
  var sum_long = 0
  var avg_long = 0
  var cities_array = []
  var states_array = []
  var countries_array = []
  fetch(`http://127.0.0.1:8000/coordsDataJson/${site_id}`).then(response => response.json()).then(data => {
    for(let j = 0; j < data.length; j++) {
      lat_array.push(Number(data[j]['lat']))
      long_array.push(Number(data[j]['long']))
      if(data[j]['city'] != '') {
      cities_array.push(data[j]['city'])
    }
    if(data[j]['state'] != '') {
      states_array.push(data[j]['state'])
    }
    if(data[j]['country']) {
      countries_array.push(data[j]['country'])
    }
    }
      for(let x = 0; x < lat_array.length; x++) {
        sum_lat += lat_array[x]
        avg_lat = sum_lat/lat_array.length
      }
      for(let y = 0; y < long_array.length; y++){
        sum_long += long_array[y]
        avg_long = sum_long/long_array.length
      }
    var map = L.map('map').setView([avg_lat, avg_long], 3);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    if(lat_array.length == long_array.length){
      for(b = 0; b < lat_array.length; b++) {
        marker = new L.marker([lat_array[b], long_array[b]])
          .bindPopup(data[b]['state'] + ' ' + lat_array[b] + ' ' + long_array[b])
          .addTo(map)
      }
    }
    var cities_set = new Set(cities_array)
    var countries_set = new Set(countries_array)
    var states_set = new Set(states_array)
    totalvisitors.textContent = lat_array.length
    states.textContent = states_set.size
    countries.textContent = countries_set.size


    var oldYValues = []
    for(let u = 0; u < states_array.length; u++) {
      oldYValues.push(states_array.count(states_array[u]))
    }
    var dataObj = new Object()
    for(let g = 0; g < oldYValues.length; g++) {
      dataObj[states_array[g]] = oldYValues[g]
    }
    sortedData = Object.entries(dataObj).sort((a,b) => b[1]-a[1]).slice(0,5)
    var newDataObj = new Object()
    for(let y = 0; y < sortedData.length; y++) {
      newDataObj[sortedData[y][0]] = sortedData[y][1]
    }

    var newXValues = []
    var newYValues = []
    for(const key in newDataObj) {
      newXValues.push(key)
      newYValues.push(newDataObj[key])
    }

    var barColors = ["#8589FF", "#7BE0CB","#8589FF","#7BE0CB","#8589FF"];

    if(states_array.length == 0) {
      statesChart.style.display = 'none'
    }
    if(countries_array.length == 0){
      countryChart.style.display = 'none'
    }

    new Chart("statesChart", {
      type: "horizontalBar",
      data: {
      labels: newXValues,
      datasets: [{
        backgroundColor: barColors,
        data: newYValues
      }]
    },
      options: {
        legend: {display: false},
        title: {
          display: false,
          text: "Top States"
        },
        scales: {
          xAxes: [{
            ticks: {
            min: 0,
            fontColor: "white"
          }
        }],
        yAxes: [{
          ticks: {
          display: false,
          fontColor: "white",
      }
  }],

        }
      }
    });


    //
    var oldYValuesCountry = []
    for(let u = 0; u < countries_array.length; u++) {
      oldYValuesCountry.push(countries_array.count(countries_array[u]))
    }
    var dataObjCountry = new Object()
    for(let g = 0; g < oldYValuesCountry.length; g++) {
      dataObjCountry[countries_array[g]] = oldYValuesCountry[g]
    }
    sortedDataCountry = Object.entries(dataObjCountry).sort((a,b) => b[1]-a[1]).slice(0,5)
    var newDataObjCountry = new Object()
    for(let y = 0; y < sortedDataCountry.length; y++) {
      newDataObjCountry[sortedDataCountry[y][0]] = sortedDataCountry[y][1]
    }

    var newXValuesCountry = []
    var newYValuesCountry = []
    for(const key in newDataObjCountry) {
      newXValuesCountry.push(key)
      newYValuesCountry.push(newDataObjCountry[key])
    }


    new Chart("countryChart", {
      type: "horizontalBar",
      data: {
      labels: newXValuesCountry,
      datasets: [{
        backgroundColor: barColors,
        data: newYValuesCountry
      }]
    },
      options: {
        legend: {display: false},
        title: {
          display: false,
          text: "Top Countries"
        },
        scales: {
          xAxes: [{
            ticks: {
            min: 0,
            fontColor: "white"
          }
        }],
        yAxes: [{
          ticks: {
            display: false,
          fontColor: "white",
            }
          }],
        }
      }
  });
}
)}

fetchCoordsData(site_id_context)
