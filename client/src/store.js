import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import constants from "./constants.js";
import FileSaver from "file-saver";

Vue.use(Vuex);

// TODO: Refactor API calls so hasNext and hasPrevious are set via a function to reduce repeated code. will need to move some mutations to actions
// Add query string to set offsets against for pagination
export default new Vuex.Store({
  state: {
    apiData: [],
    apiURL: constants.API_ENDPOINT,
    apiURLAddon: "",
    apiLoading: true,
    hasNext: false,
    hasPrevious: false,
    currentPage: 1,
    nextPage: "",
    previousPage: "",
    ahjCount: "",
    dataReady: false,
    perPage: 20,
    queryString: "",
    loginStatus: {
      status: "",
      isSuper: false,
      isStaff: false,
      authToken: ""
    }
  },
  getters: {
    apiData: state => state.apiData
  },
  mutations: {
    callAPI(state, payload) {
      let url = state.apiURL + state.apiURLAddon;
      if (payload == null) {
        axios
          .get(url, {
            headers: {
              Authorization: constants.TOKEN_AUTH
            }
          })
          .then(response => {
            state.apiLoading = false;
            state.apiData = response.data;
            state.ahjCount = response.data.count;

            if (response.data.next == null) {
              state.hasNext = false;
            } else {
              state.hasNext = true;
              state.nextPage = response.data.next;
            }
            if (response.data.previous == null) {
              state.hasPrevious = false;
            } else {
              state.hasPrevious = true;
              state.previousPage = response.data.previous;
            }
            state.dataReady = true;
          });
      } else if (payload.charAt(0) == "?") {
        state.queryString = payload;

        let query_string = url + payload;

        axios
          .get(query_string, {
            headers: {
              Authorization: constants.TOKEN_AUTH
            }
          })
          .then(response => {
            state.apiData = response.data;

            state.apiLoading = false;
            state.ahjCount = response.data.count;

            if (response.data.next == null) {
              state.hasNext = false;
            } else {
              state.hasNext = true;
              state.nextPage = response.data.next;
            }
            if (response.data.previous == null) {
              state.hasPrevious = false;
            } else {
              state.hasPrevious = true;
              state.previousPage = response.data.previous;
            }
            state.dataReady = true;
          });
      } else {
        let query_string = payload;
        axios
          .get(query_string, {
            headers: {
              Authorization: constants.TOKEN_AUTH
            }
          })
          .then(response => {
            state.apiData = response.data;
            state.ahjCount = response.data.count;
            state.apiLoading = false;

            if (response.data.next == null) {
              state.hasNext = false;
            } else {
              state.hasNext = true;
              state.nextPage = response.data.next;
            }
            if (response.data.previous == null) {
              state.hasPrevious = false;
            } else {
              state.hasPrevious = true;
              state.previousPage = response.data.previous;
            }
            state.dataReady = true;
          });
      }
    },
    toggleAPILoading(state) {
      state.apiLoading = !state.apiLoading;
    },
    toggleDataReady(state) {
      state.dataReady = false;
    },
    clearQueryString(state) {
      state.queryString = "";
    },
    updateCurrentPage(state, value) {
      state.currentPage = value;
    },
    setApiUrlAddon(state, value) {
      state.apiURLAddon = value;
    },
    exportResults(state) {
      let url = state.apiURL + state.apiURLAddon;
      let queryLimit = "limit=" + state.ahjCount;

      // Check if a query was made
      if (state.queryString) {
        url += state.queryString + queryLimit;
      } else {
        url += "?" + queryLimit;
      }

      axios
          .get(url, {
            headers: {
              Authorization: constants.TOKEN_AUTH
            }
          })
          .then(response => {
            let resultsStringified = "";
            for(let i = 0; i < response.data.results.length; i++) {
              resultsStringified += JSON.stringify(response.data.results[i], null, 2) + "\n";
            }
            let jsonFileToExport = new Blob(
              [resultsStringified],
              { type: "application/json" }
            );
            FileSaver.saveAs(jsonFileToExport, "results.json");
          });
    },
    changeUserLoginStatus(state, payload) {
      state.loginStatus = payload;
    }
  }
});
