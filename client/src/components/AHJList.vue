<template>
  <div class="ahj-public-list-container">
    <component-pagination class="pagination" id="top-buttons"></component-pagination>
    <div class="ahj-public-list">
      <b-table ref="selectableTable" class="ahj-table" selectable :select-mode="'single'" @row-selected="onRowSelected" striped hover outlined small :fields="fields" :items="apiData.results" :busy="apiLoading">
        <template v-slot:table-busy>
          <div class="text-center text-primary my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>&nbsp; Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>
    <component-pagination class="pagination" id="bottom-buttons"></component-pagination>
    <b-modal size="xl" v-model="showEditPageModal">
      <template v-slot:modal-header>
        <b-button :disabled="!editPageViewOnly" size="md" variant="danger" @click="tryEnterEditPageEditMode">Edit this AHJ</b-button>
      </template>
      <template v-slot:modal-footer>
      <b-button size="sm" variant="primary" :disabled="editPageViewOnly || $refs.editpage.recordLoading" @click="$refs.editpage.onSubmit(); showEditPageModal = false;">Submit</b-button>
      <b-button size="sm" variant="danger" :disabled="editPageViewOnly || $refs.editpage.recordLoading" @click="showEditPageModal = false">Cancel</b-button>
    </template>
      <component-edit-page ref="editpage" :editPageViewOnly="editPageViewOnly" :mode="editPageMode" :selectedRowToEdit="selectedRow"></component-edit-page>
    </b-modal>
  </div>
</template>

<script>
import Pagination from "./Pagination.vue";
import EditPage from "./EditPage.vue";
export default {
  components: {
    "component-pagination": Pagination,
    "component-edit-page": EditPage
  },
  props: ["admin_page"],
  data() {
    return {
      fields: [
        {
          key: "AHJName.Value",
          label: "AHJ Name",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "BuildingCode.Value",
          label: "Building Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "BuildingCodeNotes.Value",
          label: "Building Code Notes",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "ElectricCode.Value",
          label: "Electric Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "ElectricCodeNotes.Value",
          label: "Electric Code Notes",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "FireCode.Value",
          label: "Fire Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "FireCodeNotes.Value",
          label: "Fire Code Notes",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "ResidentialCode.Value",
          label: "Residential Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "ResidentialCodeNotes.Value",
          label: "Residential Code Notes",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.AddrLine1.Value",
          label: "Address Line 1",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.AddrLine2.Value",
          label: "Address Line 2",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.AddrLine3.Value",
          label: "Address Line 3",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.City.Value",
          label: "City",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.County.Value",
          label: "County",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.Country.Value",
          label: "Country",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.StateProvince.Value",
          label: "State/Province",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.ZipPostalCode.Value",
          label: "ZIP Postal Code",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.Location.Altitude.Value",
          label: "Address Location Altitude",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.Location.Elevation.Value",
          label: "Address Location Elevation",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.Location.Latitude.Value",
          label: "Address Location Latitude",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.Location.Longitude.Value",
          label: "Address Location Longitude",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "AHJID.Value",
          label: "AHJ ID",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
      ],
      selectedRow: null,
      editPageMode: "",
      editPageHeader: "",
      editPageViewOnly: true,
      showEditPageModal: false
    };
  },
  beforeCreate() {
    console.log('loading data');
    this.$store.commit("setApiUrlAddon", "ahj/");
    this.$store.commit("toggleAPILoading");
    this.$store.commit("callAPI");
  },
  beforeDestroy() {
    this.$store.commit("deleteAPIData");
  },
  computed: {
    apiData() {
      return this.$store.state.apiData;
    },
    apiLoading() {
      return this.$store.state.apiLoading;
    },
    hasNext() {
      return this.$store.state.hasNext;
    },
    hasPrevious() {
      return this.$store.state.hasPrevious;
    },
    ahjCount() {
      return this.$store.state.ahjCount;
    },
    dataReady() {
      return this.$store.state.dataReady;
    }
  },
  methods: {
    onRowSelected(items) {
      for (let i = 0; i < this.$refs.selectableTable.selectedRows.length; i++) {
        if (this.$refs.selectableTable.selectedRows[i]) {
          this.selectedRow = i;
          this.editPageMode = "update";
          this.editPageHeader = "Edit an AHJ";
          this.editPageViewOnly = true;
          this.showEditPageModal = true;
          this.$refs.selectableTable.selectedRows[i] = false; // this causes onRowSelected to be called again
          return;
        }
      }  
    },
    tryEnterEditPageEditMode() {
      if (this.$store.state.loginStatus.status !== "success") {
        this.$store.commit("setShowLoginModal", true);
        return;
      }
      this.$refs.editpage.getConfirmedAHJRecord();
      this.editPageViewOnly = false;
    },
    ahjCodeFormatter(value) {
      if(value) {
        if (value === "NoSolarRegulations") {
          return "No Solar Regulations";
        }
        return value.substring(0, 4) + " " + value.substring(4);
      }
      return value;
    },
    nextPage() {
      this.$store.commit("toggleAPILoading");
      return this.$store.commit("callAPI", this.$store.state.nextPage);
    },
    previousPage() {
      this.$store.commit("toggleAPILoading");

      return this.$store.commit("callAPI", this.$store.state.previousPage);
    }
  }
};
</script>

<style>
modal-content {
  width: 200%;
}
.btn {
  margin: 5px;
}
.ahj-public-list-container {
  display: grid;
  grid-template-rows: 50px 720px 50px;
  grid-template-columns: auto;
  height: 100%;
  padding-top: 5px;
  width: 1163px;
}

li {
  margin-top: -6px;
  margin-bottom: -6px;
}
ul {
  padding: 0;
  list-style: none;
}

.card {
  border: 2px solid #444549;
  box-shadow: 3px 3px 8px 0px rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  height: 227px;
  width: 488px;
  padding: 10px;
  margin-right: 10px;
  margin-bottom: 10px;
  display: grid;
  grid-template-columns: 33% 1fr;
  grid-template-rows: 140px auto;
  font-family: "Roboto Condensed";
}

.logo {
  width: 140px;
  height: 140px;
  background-color: #d8d8d8;
}

.card-body {
  padding: 0;
  grid-column: 2 / 3;
}

.ahj-public-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  background-color: white;
  height: 725px;
  justify-content: flex-start;
  align-content: flex-start;
  grid-row: 2 / 3;
  grid-column: 1 /2;
  width: 1163px;
  overflow-y: auto;
}

a.nav-link {
  padding: 0px;
}

.loader {
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  margin-left: 400px;
  margin-top: 150px;
  grid-row: 2 / 3;
  grid-column: 1 /2;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

#top-buttons {
  grid-row: 1 / 2;
  margin-top: -20px;
  position: relative;
  margin-left: auto;
  margin-right: 0;
}

#bottom-buttons {
  grid-row: 3 / 4;
  position: relative;
  margin-left: auto;
  margin-right: 0;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.btn-primary,
.btn-primary:hover,
.btn-primary:active,
.btn-primary:visited,
.btn-primary:focus,
.btn-primary:disabled {
  background-color: #1d4679;
  border-color: #1d4679;
}

a {
  color: #1d4679;
}

.ahj-table {
  margin-left: 0px;
}

.ahj-code-field-col {
  width: 400px;
  text-align: center;
}

.col-field-styling {
  text-align: center;
}

.table {
  margin-bottom: 0px !important;
}
</style>