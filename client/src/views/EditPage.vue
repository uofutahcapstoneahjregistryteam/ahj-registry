<template>
  <div class="ahj-public-list-container">
    <h1 class="title">Create Update Delete AHJ</h1>
    <p>Mode: <select v-model="requestType">
      <option value="post">Create</option>
      <option value="put">Update</option>
      <option value="delete">Delete</option>
    </select></p>
    <p v-if="requestType === 'put' || requestType === 'delete'">Enter an Internal ID of an AHJ: <input v-model="internalID" placeholder="edit me"><button @click="getAHJFields">Retrieve AHJ</button></p>
    <div class="form-group">
      <p>AHJ Name: <input v-model="AHJName" placeholder="edit me"></p>
      <p>Description: <input v-model="Description" placeholder="edit me"></p>
      <p>Building Code: <select v-model="BuildingCode">
        <option value="2021IBC">2021 IBC</option>
        <option value="2018IBC">2018 IBC</option>
        <option value="2015IBC">2015 IBC</option>
        <option value="2012IBC">2012 IBC</option>
        <option value="2009IBC">2009 IBC</option>
        <option value="NoSolarRegulations">No Solar Regulations</option>
      </select></p>
      <p>Building Code Notes: <input v-model="BuildingCodeNotes" placeholder="edit me"></p>
      <p>Electric Code: <select v-model="ElectricCode">
        <option value="2020NEC">2020 NEC</option>
        <option value="2017NEC">2017 NEC</option>
        <option value="2014NEC">2014 NEC</option>
        <option value="2011NEC">2011 NEC</option>
        <option value="NoSolarRegulations">No Solar Regulations</option>
      </select></p>
      <p>Electric Code Notes: <input v-model="ElectricCodeNotes" placeholder="edit me"></p>
      <p>Fire Code: <select v-model="FireCode">
        <option value="2021IFC">2021 IFC</option>
        <option value="2018IFC">2018 IFC</option>
        <option value="2015IFC">2015 IFC</option>
        <option value="2012IFC">2012 IFC</option>
        <option value="2009IFC">2009 IFC</option>
        <option value="NoSolarRegulations">No Solar Regulations</option>
      </select></p>
      <p>Fire Code Notes: <input v-model="FireCodeNotes" placeholder="edit me"></p>
      <p>Residential Code: <select v-model="ResidentialCode">
        <option value="2021IRC">2021 IRC</option>
        <option value="2018IRC">2018 IRC</option>
        <option value="2015IRC">2015 IRC</option>
        <option value="2012IRC">2012 IRC</option>
        <option value="2009IRC">2009 IRC</option>
        <option value="NoSolarRegulations">No Solar Regulations</option>
      </select></p>
      <p>Residential Code Notes: <input v-model="ResidentialCodeNotes" placeholder="edit me"></p>
      <p>Document Submission Method: <select v-model="DocumentSubmissionMethod">
          <option value="Epermitting">Epermitting</option>
          <option value="Email">Email</option>
          <option value="InPerson">In Person</option>
        </select></p>
      <p>Document Submission Method Notes: <input v-model="DocumentSubmissionMethodNotes" placeholder="edit me"></p>
      <div v-if="Address !== null">
        <p>Address</p>
        <p>AddrLine1: <input v-model="Address['AddrLine1']" placeholder="edit me"></p>
        <p>AddrLine2: <input v-model="Address['AddrLine2']" placeholder="edit me"></p>
        <p>AddrLine3: <input v-model="Address['AddrLine3']" placeholder="edit me"></p>
        <p>AddressType: <input v-model="Address['AddressType']" placeholder="edit me"></p>
        <p>City: <input v-model="Address['City']" placeholder="edit me"></p>
        <p>County: <input v-model="Address['County']" placeholder="edit me"></p>
        <p>Country: <input v-model="Address['Country']" placeholder="edit me"></p>
        <p>StateProvince: <input v-model="Address['StateProvince']" placeholder="edit me"></p>
        <p>ZipPostalCode: <input v-model="Address['ZipPostalCode']" placeholder="edit me"></p>
        <p>Description: <input v-model="Address['Description']" placeholder="edit me"></p>
        <p>Location</p>
        <!-- <p>Altitude: <input v-model="Address['Location']['Altitude']" placeholder="edit me"></p>
        <p>Description: <input v-model="Address['Location']['Description']" placeholder="edit me"></p>
        <p>Elevation: <input v-model="Address['Location']['Elevation']" placeholder="edit me"></p>
        <p>Latitude: <input v-model="Address['Location']['Latitude']" placeholder="edit me"></p>
        <p>LocationDeterminationMethod: <input v-model="Address['Location']['LocationDeterminationMethod']" placeholder="edit me"></p>
        <p>LocationType: <input v-model="Address['Location']['LocationType']" placeholder="edit me"></p>
        <p>Longitude: <input v-model="Address['Location']['Longitude']" placeholder="edit me"></p> -->
      </div>
      <div v-for="contact in Contacts" v-bind:key="contact.id">
        <p>Contact {{contact.id}}</p>
        <p>Contact Timezone: <input v-model="contact.ContactTimezone" placeholder="edit me"></p>
        <p>Contact Type: <input v-model="contact.ContactType" placeholder="edit me"></p>
        <p>Description: <input v-model="contact.Description" placeholder="edit me"></p>
        <p>Email: <input v-model="contact.Email" placeholder="edit me"></p>
        <p>First Name: <input v-model="contact.FirstName" placeholder="edit me"></p>
        <p>Middle Name: <input v-model="contact.MiddleName" placeholder="edit me"></p>
        <p>Last Name: <input v-model="contact.LastName" placeholder="edit me"></p>
        <p>Home Phone: <input v-model="contact.HomePhone" placeholder="edit me"></p>
        <p>Mobile Phone: <input v-model="contact.MobilePhone" placeholder="edit me"></p>
        <p>Work Phone: <input v-model="contact.WorkPhone" placeholder="edit me"></p>
        <!-- <p>Address {{contact.Address.id}}</p>
        <p>AddrLine1: <input v-model="Address['AddrLine1']" placeholder="edit me"></p>
        <p>AddrLine2: <input v-model="Address['AddrLine2']" placeholder="edit me"></p>
        <p>AddrLine3: <input v-model="Address['AddrLine3']" placeholder="edit me"></p>
        <p>AddressType: <input v-model="Address['AddressType']" placeholder="edit me"></p>
        <p>City: <input v-model="Address['City']" placeholder="edit me"></p>
        <p>County: <input v-model="Address['County']" placeholder="edit me"></p>
        <p>Country: <input v-model="Address['Country']" placeholder="edit me"></p>
        <p>StateProvince: <input v-model="Address['StateProvince']" placeholder="edit me"></p>
        <p>ZipPostalCode: <input v-model="Address['ZipPostalCode']" placeholder="edit me"></p>
        <p>Description: <input v-model="Address['Description']" placeholder="edit me"></p>
        <p>Location</p> -->
        <!-- <p>Altitude: <input v-model="Address['Location']['Altitude']" placeholder="edit me"></p>
        <p>Description: <input v-model="Address['Location']['Description']" placeholder="edit me"></p>
        <p>Elevation: <input v-model="Address['Location']['Elevation']" placeholder="edit me"></p>
        <p>Latitude: <input v-model="Address['Location']['Latitude']" placeholder="edit me"></p>
        <p>LocationDeterminationMethod: <input v-model="Address['Location']['LocationDeterminationMethod']" placeholder="edit me"></p>
        <p>LocationType: <input v-model="Address['Location']['LocationType']" placeholder="edit me"></p>
        <p>Longitude: <input v-model="Address['Location']['Longitude']" placeholder="edit me"></p> -->
      </div>
    </div>
    <div class="button-group">
      <button type="button" class="btn btn-primary" @click="submitForm">
         Submit
      </button>
      <button type="button" class="btn btn-primary" @click="deleteAHJ">
        <v-icon name="times" class="clear-icon" />&nbsp;&nbsp;Clear
      </button>
      <button type="button" class="btn btn-primary" @click="addContact">
         Add Contact
      </button>
    </div>
    <b-modal
      id="modal-create-node"
      title="Status"
      ref="create-modal-warning"
      centered
      no-stacking
      v-model="showStatusModal"
    >
      <p>
        {{ statusMessage }}
      </p>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  data() {
    return {
      showStatusModal: false,
      statusMessage: "",
      requestType: "post",
      internalID: "",
      AHJName: "",
      Description: "",
      BuildingCode: "",
      BuildingCodeNotes: "",
      ElectricCode: "",
      ElectricCodeNotes: "",
      FireCode: "",
      FireCodeNotes: "",
      ResidentialCode: "",
      ResidentialCodeNotes: "",
      DocumentSubmissionMethod: "",
      DocumentSubmissionMethodNotes: "",
      Address: null,
      Contacts: [],
      EngRevReqs: []
    }
  },
  beforeCreate() {
    this.$store.commit("setApiUrlAddon", "ahj/");
  },
  mounted() {
    if(this.$store.state.loginStatus["status"] !== "success") {
      this.$router.replace({ name: "login" });
    }
  },
  methods: {
    addContact() {
      this.Contacts.push({
        "ContactID": "",
        "ContactTimezone": "",
        "ContactType": "",
        "Description": "",
        "Email": "",
        "FirstName": "",
        "HomePhone": "",
        "LastName": "",
        "MiddleName": "",
        "MobilePhone": "",
        "WorkPhone": "",
        "Address": null
      });
    },
    addAddress() {
      if(this.Address !== null) {
        this.Address = {
          "AddressID": "",
          "AddrLine1": "",
          "AddrLine2": "",
          "AddrLine3": "",
          "AddressType": "",
          "City": "",
          "Country": "",
          "County": "",
          "Description": "",
          "StateProvince": "",
          "ZipPostalCode": "",
          "Location": null
        };
      }
    },
    addLocation() {
      if(this.Address["Location"] !== null) {
        this.Address["Location"] = {
          "Altitude": "",
            "Description": "",
            "Elevation": "",
            "Latitdue": "",
            "LocationDetermininationMethod": "",
            "LocationID": "",
            "LocationType": "",
            "Longitude": ""
        };
      }
    },
    addEngRevReq() {
      this.EngRevReqs.push({
        "Description": "",
        "EngineeringReviewType": "",
        "RequirementLevel": "",
        "StampType": ""
      });
    },
    submitForm() {
      if(this.requestType === "post") {
        this.createAHJ();
      } else if(this.requestType === "put") {
        this.updateAHJ();
      } else if(this.requestType === "delete") {
        this.deleteAHJ();
      }
    },
    createAHJ() {
      axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, {
          "AHJName": this.AHJName,
          "Description": this.Description,
          "BuildingCode": this.BuildingCode,
          "BuildingCodeNotes": this.BuildingCodeNotes,
          "ElectricCode": this.ElectricCode,
          "ElectricCodeNotes": this.ElectricCodeNotes,
          "FireCode": this.FireCode,
          "FireCodeNotes": this.FireCodeNotes,
          "ResidentialCode": this.ResidentialCode,
          "ResidentialCodeNotes": this.ResidentialCodeNotes,
          "DocumentSubmissionMethod": this.DocumentSubmissionMethod,
          "DocumentSubmissionMethodNotes": this.DocumentSubmissionMethodNotes,
          "Address": this.Address,
          "Contacts": this.Contacts,
          "EngineeringReviewRequirements": []
        },
        {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
        }).then(response => {
        this.statusMessage = "Successfully submitted AHJ information.";
        this.showStatusModal = true;
      }).catch(error => {
        this.statusMessage = "Failed to submit AHJ information.";
        this.showStatusModal = true;
      });
    },
    getAHJFields() {
      axios.get(this.$store.state.apiURL + this.$store.state.apiURLAddon + this.internalID + "/",
      {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        this.AHJName = response.data["AHJName"];
        this.Description = response.data["Description"];
        this.BuildingCode = response.data["BuildingCode"];
        this.BuildingCodeNotes = response.data["BuildingCodeNotes"];
        this.ElectricCode = response.data["ElectricCode"];
        this.ElectricCodeNotes = response.data["ElectricCodeNotes"];
        this.FireCode = response.data["FireCode"];
        this.FireCodeNotes = response.data["FireCodeNotes"];
        this.ResidentialCode = response.data["ResidentialCode"];
        this.ResidentialCodeNotes = response.data["ResidentialCodeNotes"];
        this.DocumentSubmissionMethod = response.data["DocumentSubmissionMethod"];
        this.DocumentSubmissionMethodNotes = response.data["DocumentSubmissionMethodNotes"];
        this.Address = response.data["Address"];
        this.Contacts = response.data["Contacts"];
        this.EngRevReqs = response.data["EngineeringReviewRequirements"];
      }).catch(error => {
        this.statusMessage = "Failed to retrieve AHJ information.";
        this.showStatusModal = true;
      });
    },
    updateAHJ() {
      axios.put(this.$store.state.apiURL + this.$store.state.apiURLAddon + this.internalID + "/", {
          "AHJName": this.AHJName,
          "Description": this.Description,
          "BuildingCode": this.BuildingCode,
          "BuildingCodeNotes": this.BuildingCodeNotes,
          "ElectricCode": this.ElectricCode,
          "ElectricCodeNotes": this.ElectricCodeNotes,
          "FireCode": this.FireCode,
          "FireCodeNotes": this.FireCodeNotes,
          "ResidentialCode": this.ResidentialCode,
          "ResidentialCodeNotes": this.ResidentialCodeNotes,
          "DocumentSubmissionMethod": this.DocumentSubmissionMethod,
          "DocumentSubmissionMethodNotes": this.DocumentSubmissionMethodNotes,
          "Address": this.Address,
          "Contacts": this.Contacts,
          "EngineeringReviewRequirements": this.EngRevReqs
        },
        {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        this.statusMessage = "Successfully updated AHJ information.";
        this.showStatusModal = true;
      }).catch(error => {
        this.statusMessage = "Failed to update AHJ information.";
        this.showStatusModal = true;
      });
    },
    deleteAHJ() {
      axios.delete(this.$store.state.apiURL + this.$store.state.apiURLAddon + this.internalID + "/", {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
        }).then(response => {
          this.statusMessage = "Successfully deleted AHJ information.";
          this.showStatusModal = true;
        }).catch(error => {
        this.statusMessage = "Failed to delete AHJ information.";
        this.showStatusModal = true;
      });
    }
  }
}
</script>

<style scoped>
.ahj-public-list-container {
  display: grid;
  grid-template-rows: 50px 720px 50px;
  grid-template-columns: auto;
  height: 100%;
  padding-top: 5px;
  width: 1163px;
}
#admin-table {
  border-style: none;
}

.table {
  border-style: solid;
  border-width: 1px;
}

.admin-logs {
  grid-column: 4 / 5;
  grid-row: 3 / 4;
}

.title {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
}

.breadcrumbs {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.admin-function {
  text-align: right;
}

.admin-options {
  grid-column: 2 / 3;
  grid-row: 3 / 4;
}
.admin-container {
  display: grid;
  grid-template-columns: 100px 500px 25px 500px 1fr;
  grid-template-rows: 70px 30px auto;
}

.nav-link {
  display: inline;
  padding: 0;
  padding-right: 10px;
}

thead th {
  background-color: #e66026;
  color: white;
}

.highlight-row {
  background-color: #f0f8ff;
}
</style>