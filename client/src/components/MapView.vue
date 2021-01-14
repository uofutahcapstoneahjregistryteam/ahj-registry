<template>
  <div id="mapdiv">
    <ahj-search-filter></ahj-search-filter>
  </div>
</template>

<script>
import L from "leaflet";
import constants from "../constants.js";
import AHJSearchPageFilter from "./AHJFilter.vue";

export default {
  components: {
    "ahj-search-filter": AHJSearchPageFilter
  },
  name: "Map",
  data() {
    return {
      leafletMap: null,
      polygonLayer: null,
      currSearchMarker: null,
      markerLayerGroup: null
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    },
    /*
     * Initialize the leaflet map and set it as the store's leaflet map
     */
    setupLeafletMap() {
      this.leafletMap = L.map("mapdiv").setView(
        constants.MAP_INIT_CENTER,
        constants.MAP_INIT_ZOOM
      );
      L.tileLayer(constants.MAP_TILE_API_URL, {
        attribution: constants.MAP_TILE_API_ATTR
      }).addTo(this.leafletMap);
      this.markerLayerGroup = L.layerGroup().addTo(this.leafletMap);
    },
    // Replace map's existing polygons and markers with ones from the new search
    updateMap(ahjlist) {
      let missingPolygon = false;
      ahjlist = ahjlist.filter(ahj => {
        if (ahj.mpoly === null) {
          missingPolygon = true;
          return false;
        } else {
          return true;
        }
      });
      if (missingPolygon) {
        console.log("polygon is missing");
      }
      this.markerLayerGroup.clearLayers();
      this.addPolygonLayer(ahjlist);
      this.updateMapMarkers(ahjlist);
    },
    addPolygonLayer(ahjlist) {
      let polygons = ahjlist.map(ahj => ahj.mpoly);
      if (polygons.length === 0) {
        return;
      }
      this.polygonLayer = L.geoJSON(polygons, {
        style: constants.MAP_PLYGN_SYTLE
      });
      this.polygonLayer.addTo(this.leafletMap);
      let initialPolygonSelected = polygons[0];
      this.selectPolygon(initialPolygonSelected.properties.AHJID);
    },
    selectPolygon(newAHJID) {
      let map = this.leafletMap;
      map.eachLayer(function(layer) {
        if (layer.feature) {
          if (layer.feature.properties.AHJID === newAHJID) {
            map.fitBounds(layer.getBounds());
            layer.setStyle(constants.MAP_PLYGN_SLCTD_SYTLE());
          } else {
            layer.setStyle(constants.MAP_PLYGN_SYTLE());
          }
        }
      });
    },
    updateMapMarkers(ahjlist) {
      let location = this.$store.state.apiData.results.Location;
      if (location["Latitude"]["Value"] !== null) {
        let searchMarker = L.AwesomeMarkers.icon({
          icon: "circle",
          prefix: "fa",
          markerColor: "cadetblue"
        });
        let searchedLocation = [
          location["Latitude"]["Value"],
          location["Longitude"]["Value"]
        ];
        this.currSearchMarker = L.marker(searchedLocation, {
          icon: searchMarker
        })
          .bindTooltip("Searched Address")
          .addTo(this.leafletMap);
      }
      for (let ahj of ahjlist) {
        let polygon = ahj.mpoly;
        let ahjMarker = L.AwesomeMarkers.icon({
          icon: "building",
          prefix: "fa",
          markerColor: this.selectMarkerColor(polygon)
        });
        let polygonInternalPoint = [
          polygon.properties.INTPTLAT,
          polygon.properties.INTPTLON
        ];
        let marker = L.marker(polygonInternalPoint, {
          icon: ahjMarker,
          riseOnHover: true
        })
          .bindTooltip(`<b>${ahj.AHJName.Value}</b><br><b>Address</b>: The AHJ Registry does not have an Address for this AHJ`)
          .addTo(this.markerLayerGroup);
        let that = this;
        marker.on("click", function() {
          that.$store.commit("setSelectedAHJ", ahj);
        });
      }
    },
    selectMarkerColor(polygon) {
      switch (polygon.properties.GEOID.length) {
        case 7: // the polygon is a city/place
          return "lightblue";
        case 5: // the polygon is a county
          return "blue";
        case 2: // the polygon is a state
          return "darkblue";
        default:
          return "blue"; // ??
      }
    },
    resetLeafletMapLayers() {
      if (this.polygonLayer !== null) {
        this.polygonLayer.removeFrom(this.leafletMap);
        this.polygonLayer = null;
      }
      if (this.currSearchMarker !== null) {
        this.leafletMap.removeLayer(this.currSearchMarker);
        this.currSearchMarker = null;
      }
      this.markerLayerGroup.clearLayers();
    },
    resetMapView() {
      this.leafletMap.setView(constants.MAP_INIT_CENTER, constants.MAP_INIT_ZOOM);
    }
  },
  /*
   * Load the leaflet map when this component is mounted
   */
  mounted() {
    this.setupLeafletMap();
  },
  watch: {
    "$store.state.selectedAHJ": function(newVal) {
      if (newVal === null) {
        // the search filter was cleared, and selectedAHJ reset to null
        this.locationSearched = false;
        this.resetLeafletMapLayers();
        this.resetMapView();
      } else {
        if (this.$store.state.apiData.results.Location["Latitude"]["Value"] !== null) { // check if a location/address was searched
          if (this.polygonLayer === null) {
            this.updateMap(this.$store.state.apiData.results.ahjlist);
          } else {
            // there are multiple polygons on the map at once to select
            this.selectPolygon(newVal.AHJID.Value);
          }
        } else {
          // there is one polygon at a time on the map
          this.resetLeafletMapLayers();
          this.updateMap([newVal]);
        }
      }
    },
    "$store.state.showTable": function() {
      this.leafletMap.invalidateSize(true);
    }
  }
};
</script>

<style scoped>
#mapdiv {
  height: 92vh;
  width: 100%;
}
</style>
