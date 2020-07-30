<template>
  <b-container>
    <b-modal id="mode-modal" title="Edit Mode" v-model="showModeModal">
      <template v-slot:modal-footer>
        <b-button variant="primary" @click="initiateMode">OK</b-button>
      </template>
      <b-form>
        <b-form-group id="export-form-filename" label="Select a mode:" label-for="export-input-filename">
          <b-form-select :options="modes" v-model="mode" required />
        </b-form-group>
        <b-form-group v-if="mode === 'update'" id="choose-edit-record" label="Record to edit:">
          <b-form-input placeholder="Place enter an AHJID..." v-model="editingRecordID" :state="validateEditAHJID()" required />
        </b-form-group>
      </b-form>
  </b-modal>
    <b-row>
      <b-col>
        <b-form @submit="onSubmit" @reset="onReset">
          <b-card no-body>
            <b-tabs card>
              <b-tab title="AHJ" active>
                  <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                    <b-tabs card>
                      <b-card-header header-tag="header" class="p-0" role="tab">
                        <b-button block v-b-toggle.accordion-1 variant="info">AHJ Information</b-button>
                      </b-card-header>
                      <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
                        <b-card-body>
                        <div v-for="(valueAHJ, nameAHJ) in AHJ" :key=nameAHJ>
                          <b-row v-if="!checkObjectOrArray(valueAHJ) && (mode === 'create' ? nameAHJ !== 'RecordID' : true)">
                            <b-col cols="4">
                              <label>{{ nameAHJ }}:</label>
                            </b-col>
                            <b-col cols="8">
                              <label v-if="nameAHJ === 'RecordID'">{{ valueAHJ }}</label>
                              <b-form-select v-else-if="choiceFields.AHJ[nameAHJ]" v-model="AHJ[nameAHJ]" :options="choiceFields.AHJ[nameAHJ]" />
                              <b-form-input v-else v-model="AHJ[nameAHJ]" type="text" :placeholder="getBFormInputPlaceholder(nameAHJ)" />
                            </b-col>
                          </b-row>
                        </div>
                        <b-row>
                          <b-col>
                            <b-button v-if="AHJ.Address === null" @click="addAddress(AHJ)">Add Address</b-button>
                          </b-col>
                        </b-row>
                        </b-card-body>
                      </b-collapse>
                      <div v-if="AHJ.Address">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-2 variant="info">Address</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
                          <b-card-body>
                              <div v-for="(valueAHJAddress, nameAHJAddress) in AHJ.Address" :key=nameAHJAddress>
                                <b-row v-if="!checkObjectOrArray(valueAHJAddress) && (mode === 'create' ? nameAHJAddress !== 'RecordID' : true)">
                                  <b-col cols="4">
                                    <label>{{ nameAHJAddress }}:</label>
                                  </b-col>
                                  <b-col cols="8">
                                    <label v-if="nameAHJAddress === 'RecordID'">{{ valueAHJAddress }}</label>
                                    <b-form-select v-else-if="choiceFields.Address[nameAHJAddress]" v-model="AHJ.Address[nameAHJAddress]" :options="choiceFields.Address[nameAHJAddress]" />
                                    <b-form-input v-else v-model="AHJ.Address[nameAHJAddress]" type="text" :placeholder="getBFormInputPlaceholder(nameAHJAddress)" />
                                  </b-col>
                                </b-row>
                              </div>
                              <b-row>
                                <b-col>
                                  <b-button v-if="AHJ.Address.Location === null" @click="addLocation(AHJ.Address)">Add Location</b-button>
                                </b-col>
                              </b-row>
                          </b-card-body>
                        </b-collapse>
                      </div>
                      <div v-if="AHJ.Address && AHJ.Address.Location">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-3 variant="info">Location</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
                          <b-card-body>
                            <div v-for="(valueAHJAddressLocation, nameAHJAddressLocation) in AHJ.Address.Location" :key=nameAHJAddressLocation>
                              <b-row v-if="mode === 'create' ? nameAHJAddressLocation !== 'RecordID' : true">
                                <b-col cols="4">
                                  <label>{{ nameAHJAddressLocation }}:</label>
                                </b-col>
                                <b-col cols="8">
                                  <label v-if="nameAHJAddressLocation === 'RecordID'">{{ valueAHJAddressLocation }}</label>
                                  <b-form-select v-else-if="choiceFields.Location[nameAHJAddressLocation]" v-model="AHJ.Address.Location[nameAHJAddressLocation]" :options="choiceFields.Location[nameAHJAddressLocation]" />
                                  <b-form-input v-else v-model="AHJ.Address.Location[nameAHJAddressLocation]" type="text" :placeholder="getBFormInputPlaceholder(nameAHJAddressLocation)" />
                                </b-col>
                              </b-row>
                            </div>
                          </b-card-body>
                        </b-collapse>
                      </div>
                    </b-tabs>
                  </b-form-group>
              </b-tab>
              <b-tab title="Contacts">
                <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                <b-tabs card>
                  <b-tab title="Contact">
                    <div v-for="Contact in AHJ.Contacts" :key=Contact.vueIndex>
                      <b-card-header header-tag="header" class="p-0" role="tab">
                        <b-button block v-b-toggle.accordion-1 variant="info">Contact Information</b-button>
                      </b-card-header>
                      <b-collapse id="accordion-1" visible accordion="my-accordion-contact" role="tabpanel">
                        <div v-for="(valueContact, nameContact) in Contact" :key=nameContact>
                          <b-row>
                            <b-col>
                              <label>{{ nameContact }}:</label>
                            </b-col>
                            <b-col>
                              <label v-if="nameContact === 'RecordID'">{{ Contact[nameContact] }}</label>
                              <b-form-input
                                v-else-if="nameContact !== 'Address'"
                                v-model="Contact[nameContact]"
                                type="text"
                                :placeholder="'Enter ' + nameContact"
                              ></b-form-input>
                                <b-button v-if="nameContact === 'Address' && Contact.Address === null" @click="addAddress(Contact)">Add Address</b-button>
                            </b-col>
                          </b-row>
                        </div>
                      </b-collapse>
                      <div v-if="Contact.Address">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-2 variant="info">Address</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-2" accordion="my-accordion-contact" role="tabpanel">
                          <div v-for="(valueContactAddress, nameContactAddress) in Contact.Address" :key=nameContactAddress>
                            <b-row>
                              <b-col>
                                <label>{{ nameContactAddress }}:</label>
                              </b-col>
                              <b-col>
                                <label v-if="nameContactAddress === 'RecordID'">{{ Contact[nameContactAddress] }}</label>
                                <b-form-input
                                  v-else-if="nameContactAddress !== 'Location'"
                                  v-model="Contact.Address[nameContactAddress]"
                                  type="text"
                                  :placeholder="'Enter ' + nameContactAddress"
                              ></b-form-input>
                                <b-button v-if="nameContactAddress === 'Address' && Contact.Address === null" @click="addLocation(Contact.Address)">Add Location</b-button>
                              </b-col>
                            </b-row>
                          </div>
                        </b-collapse>
                      </div>
                      <div v-if="Contact.Address && Contact.Address.Location">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-3 variant="info">Location</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-3" accordion="my-accordion-contact" role="tabpanel">
                          <div v-for="(valueContactAddressLocation, nameContactAddressLocation) in Contact.Address.Location" :key=nameContactAddressLocation>
                            <b-row>
                              <b-col>
                                <label>{{ nameContactAddressLocation }}:</label>
                              </b-col>
                              <b-col>
                                <label v-if="nameContactAddressLocation === 'RecordID'">{{ Contact.Address.Location[nameContactAddressLocation] }}</label>
                                <b-form-input
                                  v-else
                                  v-model="Contact.Address.Location[nameContactAddressLocation]"
                                  type="text"
                                  :placeholder="'Enter ' + nameContactAddressLocation"
                              ></b-form-input>
                              </b-col>
                            </b-row>
                          </div>
                        </b-collapse>
                      </div>
                    </div>
                  </b-tab>
                </b-tabs>
                </b-form-group>
              </b-tab>
              <b-tab title="Engineering Review Requirements">
                <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                  <b-tabs card>
                    <b-tab v-for="i in tabsEngReqRev" :key="'dyn-tab-' + i" :title="'Engineering Review Requirement ' + i">
                      Tab contents {{ i }}
                      <b-button size="sm" variant="danger" class="float-right" @click="closeTabEngReqReq(i)">
                        Close tab
                      </b-button>
                      <div v-for="(valueEngRevReq, nameEngRevReq) in AHJ.EngineeringReviewRequirements[i]" :key=nameEngRevReq>
                          <b-row>
                            <b-col>
                              <label>{{ nameEngRevReq }}:</label>
                            </b-col>
                            <b-col>
                              <label v-if="nameEngRevReq === 'RecordID'">{{ AHJ.EngineeringReviewRequirements[i][nameEngRevReq] }}</label>
                              <b-form-input
                                v-else-if="nameEngRevReq !== 'Address'"
                                v-model="AHJ.EngineeringReviewRequirements[i][nameEngRevReq]"
                                type="text"
                                :placeholder="'Enter ' + nameEngRevReq"
                              ></b-form-input>
                            </b-col>
                          </b-row>
                        </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" @click.prevent="newTabEngRevReq" href="#"><b>+</b></b-nav-item>
                    </template>
                  </b-tabs>
                </b-form-group>
              </b-tab>
            </b-tabs>
          </b-card>
          <b-button variant="primary" class="float-right" @click="onSubmit">Submit</b-button>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  data() {
    return {
      modes: [
        { value: "create", text: "Submit a new AHJ..."},
        { value: "update", text: "Edit an existing AHJ..."}
      ],
      showModeModal: true,
      mode: "",
      editingRecordID: "",
      beforeEditAHJRecord: {},

      showStatusModal: false,
      statusMessage: "",
      EditTypeAndRecordTypeAndRecordID: "",
      requestType: "post",
      tabsContact: [],
      tabCounterContact: 0,
      tabsEngReqRev: [],
      tabCounterEngReqRev: 0,
      AHJ: {
        RecordID: "",
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
        WindCode: "",
        WindCodeNotes: "",
        DocumentSubmissionMethod: "",
        DocumentSubmissionMethodNotes: "",
        FileFolderURL: "",
        Address: null
      },
      choiceFields: constants.CHOICE_FIELDS
    }
  },
  beforeCreate() {
    this.$store.commit("setApiUrlAddon", "edit/submit/");
  },
  mounted() {
    if(this.$store.state.loginStatus["status"] !== "success") {
      this.$router.replace({ name: "login" });
    }
  },
  methods: {
    validateEditAHJID() {
      return /[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}/.test(this.editingRecordID);
    },
    initiateMode() {
      if (!this.mode) {
        return;
      } else if (this.mode === 'update') {
        if (!this.validateEditAHJID()) {
          return;
        }
        this.getAHJRecord();
      }
      this.showModeModal = false;
    },
    onSubmit(evt) {
      console.log('in onSubmit');
      evt.preventDefault();
      this.postCreate("AHJ", this.AHJ);
    },
    onReset() {

    },
    show() {
      
    },
    getAHJRecord() {
      console.log('getting AHJ record...');
      axios.get(this.$store.state.apiURL + "ahj/" + this.editingRecordID + "/", {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        console.log('got the AHJ record...');
        this.beforeEditAHJRecord = this.setAHJFieldsFromResponse(response.data);
        this.AHJ = this.beforeEditAHJRecord;
      });
    },
    setAHJFieldsFromResponse(record) {
      console.log(record);
      let result = {};
      Object.keys(record).forEach(key => {
        console.log(key);
        let field = record[key];
        if (field) {
          if ("Value" in field) {
            let value = field["Value"];
            if (value && field["RecordID"] === value) {
              key = "RecordID";
            }
            result[key] = value;
          } else if (field.constructor === Array) {
            result[key] = [];
            field.forEach(item => {
              result[key].push(this.setAHJFieldsFromResponse(item));
            });
          } else {
            result[key] = this.setAHJFieldsFromResponse(record[key]);
          }
        }
      });
      return result;
    },
    postCreate(RecordType, fields, ParentID, ParentRecordType) {
      console.log('in postCreate for ' + RecordType);
      let createEditObject = {"EditType": "create", "RecordType": RecordType}
      if (ParentID && ParentRecordType) {
        createEditObject["ParentID"] = ParentID;
        createEditObject["ParentRecordType"] = ParentRecordType;
      }
      console.log(createEditObject);
      axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, createEditObject,
        {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
      }).then(response => {
        console.log("response for " + RecordType + ": ");
        console.log(response)
        let RecordID = response.data["RecordID"];
        fields["RecordID"] = RecordType;
        console.log(RecordID);
        this.postUpdate(RecordType, fields, RecordID);
      }).catch(error => {
        console.log(error);
      });
    },
    postUpdate(RecordType, fields, RecordID) {
      let updateEditObjects = [];
      Object.keys(fields).forEach(key => {
        if(fields[key] === "" || fields[key] === null) {
          return;
          } else if (fields[key].constructor === Array) {
          for(let i = 0; i < fields[key].length; i++) {
            let subRecordID = fields[key][i]["RecordID"];
            if (subRecordID) {
              this.postUpdate(this.getSingularRecordType(key), fields[key][i], subRecordID);
            } else {
              console.log('will create ' + key + ' from update');
              this.postCreate(this.getSingularRecordType(key), fields[key][i], RecordID, RecordType);
            }
          }
        } else if (typeof fields[key] === "object") {
          let subRecordID = fields[key]["RecordID"];
          if (subRecordID) {
            this.postUpdate(key, fields[key], subRecordID);
          } else {
            console.log('will create ' + key + ' from update');
            this.postCreate(key, fields[key], RecordID, RecordType);
          }
        } else {
          if (key === "RecordID") {
            return;
          }
          let updateEditObject = {"EditType": "update", "RecordType": RecordType, "RecordID": RecordID};
          updateEditObject["FieldName"] = key;
          updateEditObject["Value"] = fields[key];
          updateEditObjects.push(updateEditObject);
          console.log(updateEditObject);
          console.log(updateEditObjects);
        }
      });
      for (let i = 0; i < updateEditObjects.length; i++) {
        axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, updateEditObjects[i],
          {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
        }).then(response => {
          
        }).catch(error => {
          this.statusMessage = "Failed to update AHJ information.";
          this.showStatusModal = true;
        });
      }
    },
    getSingularRecordType(name) {
      if (name === "Contacts") {
        return "Contact";
      } else if (name === "EngineeringReviewRequirements") {
        return "EngineeringReviewRequirement";
      }
    },
    addContact() {
      this.AHJ.Contacts.push({
        RecordID: "",
        ContactTimezone: "",
        ContactType: "",
        Description: "",
        Email: "",
        FirstName: "",
        MiddleName: "",
        LastName: "",
        MobilePhone: "",
        WorkPhone: "",
        HomePhone: "",
        Title: "",
        PreferredContactMethod: "",
        Address: null
      });
    },
    addAddress(parent) {
      parent["Address"] = {
        RecordID: "",
        AddrLine1: "",
        AddrLine2: "",
        AddrLine3: "",
        AddressType: "",
        City: "",
        Country: "",
        County: "",
        Description: "",
        StateProvince: "",
        ZipPostalCode: "",
        Location: null
      };
    },
    addLocation(parent) {
      parent["Location"] = {
        RecordID: "",
        Altitude: "",
        Description: "",
        Elevation: "",
        Longitude: "",
        Latitude: "",
        LocationDeterminationMethod: "",
        LocationType: ""
      };
    },
    addEngRevReq() {
      this.AHJ.EngineeringReviewRequirements.push({
        RecordID: "",
        Description: "",
        EngineeringReviewType: "",
        RequirementLevel: "",
        StampType: ""
      });
    },
    newTabEngRevReq() {
      this.addEngRevReq();
      this.tabsEngReqRev.push(this.tabCounterEngReqRev++);
    },
    closeTabEngReqReq(x) {
      for (let i = 0; i < this.tabsEngReqRev.length; i++) {
        if (this.tabsEngReqRev[i] === x) {
          this.AHJ.EngineeringReviewRequirements.splice(i, 1);
          this.tabsEngReqRev.splice(i, 1);
        }
      }
      this.tabCounterEngReqRev--;
    },
    checkObjectOrArray(item) {
      return typeof item === 'object' || item.constructor === Array;
    },
    getBFormInputPlaceholder(fieldName) {
      return "Enter a " + fieldName + "...";
    }
  }
};
</script>

<style scoped>

.container {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 54px 1fr 50px;
  background-color: #f7f7f7;
}

.card {
  margin-top: 25px;
  height: 750px;
  width: 200%;
  border: #d3d3d3 solid 1px;
  overflow-y: auto;
}
</style>
