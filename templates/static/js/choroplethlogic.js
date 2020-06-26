// Creating map object
var myMap = L.map("map", {
  center: [39.916668, 116.383331],
  zoom: 4
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/light-v10",
  accessToken: API_KEY
}).addTo(myMap);


function getColor(d) {
  return d > 100 ? '#800026' :
         d > 80  ? '#E31A1C' :
         d > 50   ? '#FC4E2A' :
         d > 30   ? '#FD8D3C' :
         d > 15   ? '#FED976' :
                    '#FFEDA0';
};

var geoData = "https://enjalot.github.io/wwsd/data/world/world-110m.geojson";

d3.json(geoData, function(data) {
  d3.json("./static/js/data.json", function(aqidata){
    
    // console.log(aqidata);
    var tableData=[]
    aqidata.forEach( x=> {
      if (x.status === 'success'){
        tableData.push(x);
      };
    });
    // Select only the array where the required information is present  
    var dataY=[];
    tableData.forEach(function(element) {
        dataY.push(element.data);
    });
    // console.log(dataY);
    var cleanData = dataY.filter(function(d){return d.current.pollution != null;});
    console.log(cleanData);
    var number = cleanData.map(x =>
       x.current.pollution.aqius);
    // console.log(number);
    var countryincleanData = cleanData.map(x=>
      x.country);
    // console.log(countryincleanData);
    
    var together = countryincleanData.map(function(e,i){
      return [e,number[i]];
    });
    // console.log(together);

    var countriesingeo = data.features.map(x=>
       x.properties);
    // console.log(countriesingeo);
    // console.log(data.features[0].properties);
    var ri = data.features;
    // console.log(data.features);
    for (var i=0; i < together.length; i++){
      for (var j=0; j < together.length; j++){
        try {
          if( together[i][0] === countriesingeo[j].name) {
            ri[j].properties['aqius']= together[i][1]}
          

        } catch(err){console.log('ok')} ; //finally {console.log('ok')}
      };
    };
    console.log(ri);
    
    // add color
    function style(feature) {
      return {
          fillColor: getColor(feature.properties.aqius),
          weight: 2,
          opacity: 1,
          color: 'white',
          dashArray: '3',
          fillOpacity: 0.7
      };
    };

    L.geoJson(data, {style:style}).addTo(myMap);

    //Adding Interaction
    //First we’ll define an event listener for layer mouseover event:

    function highlightFeature(e) {
      var layer = e.target;
      info.update(layer.feature.properties);
  
      layer.setStyle({
          weight: 5,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7      
      });
  
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
    };

    //Next we’ll define what happens on mouseout:
    function resetHighlight(e) {
      geojson.resetStyle(e.target);
      info.update();
    };

    function zoomToFeature(e) {
      myMap.fitBounds(e.target.getBounds());
    }

    function onEachFeature(feature, layer) {
      layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight,
          click: zoomToFeature
      });
    }
  
    geojson = L.geoJson(data, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(myMap);


    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (myMap) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 15, 30, 50, 80, 100],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }

        return div;
    };

    legend.addTo(myMap);


    //add info top right,howing it on state hover inside a custom control.

    var info = L.control();

    info.onAdd = function (myMap) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {
        this._div.innerHTML = '<h4>AQI Value</h4>' +  (props ?
            '<b>' + props.name + '</b><br />' + props.aqius 
            : 'Hover over a state');
    };

    info.addTo(myMap);

  }); //datajson end
}); // geojson end








// d3.json("./static/js/data.json", function(data) {

//   // Select only the values which have status as "success"
//   var tableData=[]
//   data.forEach( x=> {
//     if (x.status === 'success'){
//       tableData.push(x);
//     };
//   });
//   // Select only the array where the required information is present  
//   var dataY=[];
//   tableData.forEach(function(element) {
//       dataY.push(element.data);
//   });
//   console.log(dataY);
//   // Checking elements of the required polluion data
//   var elements = Object.keys(dataY[0].current.pollution)
//   .filter(function(d){
//     return ((d != "ts") & (d != "maincn") & (d != "mainus"));
//   });

//   console.log(elements);

//   // Cleaning data of the values which have no pollution parammeter
//   var cleanData = dataY.filter(function(d){return d.current.pollution != null;});
//   console.log(cleanData);


// }); //end datajson







// Load in geojson data
// var faultLine = new L.LayerGroup();
// var geoData = "http://enjalot.github.io/wwsd/data/world/world-110m.geojson";

// var geojson;

// // Grab data with d3
// d3.json(geoData, function(data) {

//   // Create a new choropleth layer
//   geojson = L.choropleth(data, {

//     // Define what  property in the features to use
//     valueProperty: "MHI2016",

//     // Set color scale
//     scale: ["#ffffb2", "#b10026"],

//     // Number of breaks in step range
//     steps: 10,

//     // q for quartile, e for equidistant, k for k-means
//     mode: "q",
//     style: {
//       // Border color
//       color: "red",
//       weight: 1,
//       fillOpacity: 0.8
//     },
//     // Binding a pop-up to each layer
//     // onEachFeature: function(feature, layer) {
//     //   layer.bindPopup("Zip Code: " + feature.properties.ZIP + "<br>Median Household Income:<br>" +
//     //     "$" + feature.properties.MHI2016);
//     // }
    
//   }).addTo(myMap);

//   console.log(geojson);
//   // Set up the legend
//   var legend = L.control({ position: "bottomright" });
//   legend.onAdd = function() {
//     var div = L.DomUtil.create("div", "info legend");
//     var limits = geojson.options.limits;
//     var colors = geojson.options.colors;
//     var labels = [];

//     // Add min & max
//     var legendInfo = "<h1>Median Income</h1>" +
//       "<div class=\"labels\">" +
//         "<div class=\"min\">" + limits[0] + "</div>" +
//         "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
//       "</div>";

//     div.innerHTML = legendInfo;

//     limits.forEach(function(limit, index) {
//       labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
//     });

//     div.innerHTML += "<ul>" + labels.join("") + "</ul>";
//     return div;
//   };

//   // Adding legend to the map
//   legend.addTo(myMap);

// });
