/*
 * Playing around with leaflet
 * by creating a heatmap.
 */

/* sets up the map at the lat/long location */
var map = L.map('map').setView([38, -99], 4);

/* sets up attribution properties on the map */
var mapID = "taylorkline.iheaicei";
L.tileLayer('https://{s}.tiles.mapbox.com/v3/' + mapID + '/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
      '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 18
      }).addTo(map);

var heatmapLayer = new L.DivHeatmapLayer(
      {
         radius: 20
      });

/* Load heatmap data from a .js file */
heatmapLayer.setData(heatmapData); //heatmap data defined by external js file

heatmapLayer.addTo(map);

/* Create a legend */
var legend = L.control({position: 'topright'});

legend.onAdd = function (map) {
   var div = L.DomUtil.create('div','info');
   //user defined by external js file
   div.innerHTML += usersFound + " followers of <b><a target=\"_blank\""
      + "href=\"http://instagram.com/" + user + "\">" + user + "</a></b>"; 
   return div;
};

legend.addTo(map);
