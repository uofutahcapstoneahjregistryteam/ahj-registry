<template>
  <div class="ahj-search-container">
    <!-- <div class="breadcrumbs">
      <router-link to="/" class="nav-link">Home Page</router-link>/
      <router-link to="/" class="nav-link disabled">Product Search</router-link>
    </div>-->
    <div class="download-search-results">
      <a href @click.prevent="exportResults">Download Search Results</a>
    </div>
    <div class="ahj-count">
      <br />
      <strong>{{ ahjCount }} Authorities Having Jurisdiction</strong>
    </div>
    <div class="ahj-search-sidebar">
      <component-ahj-filter></component-ahj-filter>
    </div>
    <div class="ahj-search-body">
      <component-ahj-list></component-ahj-list>
    </div>
  </div>
</template>

<script>
import AHJFilter from "../components/AHJFilter.vue";
import AHJList from "../components/AHJList.vue";
export default {
  components: {
    "component-ahj-list": AHJList,
    "component-ahj-filter": AHJFilter
  },
  computed: {
    ahjCount() {
      return this.$store.state.ahjCount;
    }
  },
  methods: {
    exportResults() {
      this.$store.commit("exportResults");
    }
  }
};
</script>

<style scoped>
.ahj-search-container {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 0px 250px 15px auto 25px;
  grid-template-rows: 25px auto;
}

.ahj-search-sidebar {
  grid-column: 2 / 3;
  grid-row: 1 / 3;
}

.ahj-search-body {
  grid-column: 4 / span 2;
  grid-row: 1 / span 2;
}

.breadcrumbs {
  grid-column: 2 / span 3;
  grid-row: 1 / 2;
}

.nav-link {
  display: inline;
  padding: 0;
  padding-right: 5px;
}

.download-search-results {
  grid-column: 4 / 5;
  grid-row: 1 / 2;
  font-family: "Roboto Condensed";
}

#sort-by-button {
  float: right;
}

.ahj-count {
  grid-column: 4 / 5;
  grid-row: 1 / 2;
  font-family: "Roboto Condensed";
}

a {
  color: #4285f4;
}
</style>
