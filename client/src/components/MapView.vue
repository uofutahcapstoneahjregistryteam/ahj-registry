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
      locationMarker: null,
      polygonLayer: null,
      markerLayerGroup: null
    };
  },
  methods: {
    /*
     * Initialize the leaflet map and set it as the store's leaflet map
     */
    setupLeafletMap() {
      this.leafletMap = L.map("mapdiv").setView(constants.MAP_INIT_CENTER, constants.MAP_INIT_ZOOM);
      L.tileLayer(constants.MAP_TILE_API_URL,{
        attribution: constants.MAP_TILE_API_ATTR
      }).addTo(this.leafletMap);
      this.markerLayerGroup = L.layerGroup().addTo(this.leafletMap);
    },
    addPolygonLayer() {
      let polygons = this.$store.state.apiData.results.ahjlist
        .map(ahj => ahj.mpoly)
        .filter(mpoly => mpoly !== null);
      this.polygonLayer = L.geoJSON(polygons, {
        style: constants.MAP_PLYGN_SYTLE
      });
      this.polygonLayer.addTo(this.leafletMap);
      this.$store.state.polygons = polygons;
      this.$store.state.currPolyInd = 0;
      let initialPolygonSelected = polygons[0];
      // This triggers the watch for selectedAHJID below to select the polygon
      this.$store.commit("setSelectedAHJIDFromTable", initialPolygonSelected.properties.AHJID);
      for (let i = 0; i < polygons.length; i++) {
        L.marker([
          polygons[i].properties.INTPTLAT,
          polygons[i].properties.INTPTLON
        ])
          .bindTooltip(
            "The Registry does not \n have Address or Contact Info \n for this AHJ."
          )
          .addTo(this.markerLayerGroup);
      }
    },
    selectPolygon(polygonAHJID, oldPolygonAHJID) { // TODO: pass polygon so that clicking on table adds mpoly to map (when address hasn't been searched)
      let map = this.leafletMap;
      map.eachLayer(function(layer) {
        if (layer.feature) {
          if (layer.feature.properties.AHJID === polygonAHJID) {
            map.fitBounds(layer.getBounds());
            layer.setStyle(constants.MAP_PLYGN_SLCTD_SYTLE());
          } else if (layer.feature.properties.AHJID === oldPolygonAHJID) {
            layer.setStyle(constants.MAP_PLYGN_SYTLE());
          }
        }
      });
    },
    resetLeafletMapLayers() {
      if (this.polygonLayer !== null) {
        this.polygonLayer.removeFrom(this.leafletMap);
      }
      this.markerLayerGroup.clearLayers();
    }
  },
  /*
   * Load the leaflet map when this component is mounted
   */
  mounted() {
    this.setupLeafletMap();
  },
  watch: {
    "$store.state.apiLoading": function(newVal) {
      if (newVal === false) {
        let location = this.$store.state.apiData.results.Location;
        if (location["Latitude"] !== null) {
          let latlngArray = [location["Latitude"], location["Longitude"]];
          this.resetLeafletMapLayers();
          this.addPolygonLayer();
          if (this.locationMarker === null) {
            this.locationMarker = L.marker(latlngArray, {
              icon: constants.MAP_SEARCHED_ADDR_ICON
            })
              .bindTooltip("entered address")
              .addTo(this.leafletMap);
          } else {
            this.locationMarker.setLatLng(latlngArray);
          }
          this.leafletMap.setView(latlngArray);
        }
      }
    },
    "$store.state.selectedAHJID": function(newVal, oldVal) {
      this.selectPolygon(newVal, oldVal);
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
