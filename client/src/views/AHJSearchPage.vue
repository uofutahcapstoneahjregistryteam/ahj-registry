<template>
  <div class="ahj-search-container">
    <div class="download-search-results">
      Download Search Results:
      <span v-if="$store.state.apiLoading">
        ...
      </span>
      <span v-else-if="!$store.state.resultsDownloading">
        <a href @click.prevent="exportResults('application/json')">
          JSON
        </a>
        or
        <a href @click.prevent="exportResults('text/csv')">
          CSV
        </a>
      </span>
      <span v-else>
        (<b-spinner small class="text-center" />
        {{ $store.state.downloadCompletion }}%)
      </span>
    </div>
    <div class="ahj-count">
      <br />
      <strong>
        {{ ahjCount ? ahjCount : "..." }} Authorities Having Jurisdiction</strong>
    </div>
    <div class="ahj-search-sidebar">
      <component-ahj-map></component-ahj-map>
    </div>
    <div class="ahj-search-body">
      <component-ahj-list></component-ahj-list>
    </div>
  </div>
</template>

<script>
import MapView from "../components/MapView";
import AHJList from "../components/AHJList.vue";
export default {
  components: {
    "component-ahj-list": AHJList,
    "component-ahj-map": MapView
  },
  computed: {
    ahjCount() {
      return this.$store.state.ahjCount;
    }
  },
  methods: {
    exportResults(fileType) {
      this.$store.commit("exportResults", fileType);
    }
  }
};
</script>

<style scoped>
.ahj-search-container {
  display: grid;
  grid-template-columns: 50% 50%;
}

.ahj-search-sidebar {
  grid-column: 1;
  grid-row: 1 / 3;
  padding-right: 1em;
}

.ahj-search-body {
  grid-column: 2;
  grid-row: 1 / span 2;
}

.download-search-results {
  grid-column: 2;
  grid-row: 1 / 2;
  font-family: "Roboto Condensed";
  z-index: 1;
}

.ahj-count {
  grid-column: 2;
  grid-row: 1 / 2;
  font-family: "Roboto Condensed";
}

a {
  color: #4285f4;
}
</style>
