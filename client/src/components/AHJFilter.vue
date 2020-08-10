<template>
  <div class="public-filter">
    <form @submit.prevent>
      <div class="form-group">
        <input type="text" class="form-control keyword_search" v-model="searchKeyword" placeholder="Search..." @keyup.enter="updateQuery" />
        <input class ="form-control keyword_search" v-model="query_data.AHJID" placeholder="AHJID..." @keyup.enter="updateQuery" />
        <input type="text" class="form-control keyword_search" v-model="query_data.Address" placeholder="Address..." />
        <!-- <b-row>
          <b-col cols="6">
            <input type="text" class="form-control location_search" v-model="query_data.Address" placeholder="Longitude..." />
          </b-col>
          <b-col cols="6">
            <input type="text" class="form-control location_search" v-model="query_data.Address" placeholder="Latitude..." />
          </b-col>
        </b-row> -->
      </div>
      <h1>View Mode</h1>
      <div class="form-group">
        <select v-model="query_data.view">
          <option value="latest">Latest</option>
          <option value="highest_voted">Highest Voted</option>
          <option value="confirmed">Confirmed</option>
        </select>
      </div>
      <div class="form-group">
        <h1>Building Codes</h1>
        <b-form-select v-model="query_data.BuildingCode" :options="choiceFields.AHJ.BuildingCode" multiple :select-size="3" />
        <h1>Electric Codes</h1>
        <b-form-select v-model="query_data.ElectricCode" :options="choiceFields.AHJ.ElectricCode" multiple :select-size="3" />
        <h1>Fire Codes</h1>
        <b-form-select v-model="query_data.FireCode" :options="choiceFields.AHJ.FireCode" multiple :select-size="3" />
        <h1>Residential Codes</h1>
        <b-form-select v-model="query_data.ResidentialCode" :options="choiceFields.AHJ.ResidentialCode" multiple :select-size="3" />
        <h1>Wind Codes</h1>
        <b-form-select v-model="query_data.WindCode" :options="choiceFields.AHJ.WindCode" multiple :select-size="3" />
      </div>
      <div class="button-group">
        <button type="button" class="btn btn-primary" @click="updateQuery">
          <v-icon name="search" class="search-icon" />&nbsp; Search
        </button>
        <button type="button" class="btn btn-primary" @click="clearFilters">
          <v-icon name="times" class="clear-icon" />&nbsp;&nbsp;Clear filters
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import constants from "../constants.js";

export default {
  data() {
    return {
      query_data: {
        view: "latest",
        AHJID: "",
        Address: "",
        Longitude: "",
        Latitude: "",
        BuildingCode: [],
        ElectricCode: [],
        FireCode: [],
        ResidentialCode: [],
        WindCode: []
      },
      searchKeyword: "",
      choiceFields: constants.CHOICE_FIELDS
    };
  },
  methods: {
    updateQuery() {
      // Create select filter query
      let selectFilterString = "?";
      Object.keys(this.query_data).forEach(key => {
        if (this.query_data[key].length != 0) {
          if (selectFilterString == "?") {
            if(key === "view") {
              selectFilterString += key + "=";
            } else {
              selectFilterString += key + "__in=";
            }
          } else {
            selectFilterString += "&" + key + "__in=";
          }
          if(this.query_data[key].contrustor  === Array) {
            for (let i in this.query_data[key]) {
              selectFilterString += this.query_data[key][i] + ",";
            }
          } else {
            selectFilterString += this.query_data[key];
          }
          // selectFilterString = selectFilterString.slice(0, -1);
        }
      });

      // Create keyword search query
      let searchString = "";
      if (this.searchKeyword) {
        // Split keywords
        let queryStrings = this.searchKeyword.split(" ");
        for(let i = 0; i < queryStrings.length - 1; i++) {
          searchString += queryStrings[i] + ",";
        }
        searchString += queryStrings[queryStrings.length - 1] + "&";
        searchString = "search=" + searchString;
      }

      // Combine queries
      if (selectFilterString == "?") {
        selectFilterString = selectFilterString + searchString;
      } else {
        selectFilterString = selectFilterString + "&" + searchString;
      }

      // Don't search if no keywords or filters were provided
      if (selectFilterString === "?") {
        return;
      }
      console.log(selectFilterString);
      this.$store.commit("toggleAPILoading");
      this.$store.commit("callAPI", selectFilterString);
    },
    clearFilters() {
      this.$store.commit("toggleAPILoading");
      this.searchKeyword = "";
      this.query_data.AHJID = "";
      this.query_data.City = "";
      this.query_data.County = "";
      this.query_data.StateProvince = "";
      this.query_data.Country = "";
      this.query_data.ZipPostalCode = "";
      this.query_data.BuildingCode = [];
      this.query_data.ElectricCode = [];
      this.query_data.FireCode = [];
      this.query_data.ResidentialCode = [];
      this.$store.commit("clearQueryString");
      this.$store.commit("callAPI");
      this.$store.commit("updateCurrentPage", 1);
    },
    updateSearch() {
      this.$store.commit("toggleAPILoading");

      let searchString = "?search=" + this.searchKeyword;
      // console.log(searchString);
      this.$store.commit("callAPI", searchString);
    }
  }
};
</script>

<style scoped>
.clear-icon {
  color: #db4437;
  margin-bottom: 3px;
}

.search-icon {
  color: #4285f4;
  margin-bottom: 3px;
}
h1 {
  font-size: 18px;
  color: #4b4e52;
  font-family: "Roboto Condensed";
  font-weight: bold;
}

.public-filter {
  padding-left: 20px;
  padding-top: 5px;
}

.form-group {
  font-family: "Roboto Condensed";
  display: block;
}

select.custom-select {
  margin-bottom: 5px;
  width: 170px;
}

button {
  margin: 5px;
  margin-bottom: 15px;
}

label {
  display: block;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
  margin-left: -17px;
}

.btn-primary,
.btn-primary:active,
.btn-primary:visited,
.btn-primary:focus,
.btn-primary:disabled {
  background-color: white;
  border-color: #4b4e52;
  color: #4b4e52;
}

.btn-primary:hover {
  background-color: #eeeeee;
  color: #4b4e52;
  border-color: #4b4e52;
}

label {
  margin-top: 3px;
  margin-bottom: 3px;
}

.location_search {
  width: 84%;
  padding-right: 1px;

}

.keyword_search {
  width: 214px;
  margin-bottom: 5px;
}
</style>
