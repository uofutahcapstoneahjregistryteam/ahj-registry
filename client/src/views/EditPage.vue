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
                    <div v-for="Contact in AHJ.Contacts">
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
                      <b-button size="sm" variant="danger" class="float-right" @click="closeTabEngReqReq(i)">Remove</b-button>
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
      AHJ: {},
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
      return /^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$)/.test(this.editingRecordID);
    },
    initiateMode() {
      if (!this.mode) {
        return;
      } else if (this.mode === 'create') {
        this.AHJ = this.deepCopyObject(constants.AHJ_FIELDS);
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
      if (this.mode === "create") {
        this.postCreate("AHJ", this.AHJ);
      } else if (this.mode === "update") {
        console.log("in update");
        this.postUpdate("AHJ", this.AHJ, this.AHJ["RecordID"], this.beforeEditAHJRecord);
      }
    },
    onReset() {

    },
    show() {
      
    },
    getAHJRecord() {
      console.log('getting AHJ record...');
      axios.get(this.$store.state.apiURL + "ahj/" + this.editingRecordID + "/?view=confirmed", {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        console.log('got the AHJ record...');
        this.beforeEditAHJRecord = this.setAHJFieldsFromResponse(response.data);
        this.AHJ = this.deepCopyObject(this.beforeEditAHJRecord);
      });
    },
    setAHJFieldsFromResponse(record) {
      let result = {};
      Object.keys(record).forEach(key => {
        console.log(Object.keys(record));
        let field = record[key];
        if (field) {
          if ("Value" in field) {
            let value = field["Value"];
            if (value && field["RecordID"] === value) {
              key = "RecordID";
            }
            result[key] = value;
          } else if (this.isArray(field)) {
            result[key] = [];
            field.forEach(item => {
              console.log(' in array');
              console.log(item);
              result[key].push(this.setAHJFieldsFromResponse(item));
            });
          } else {
            result[key] = this.setAHJFieldsFromResponse(record[key]);
          }
        } else {
          result[key] = field;
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
        console.log("fields");
        console.log(fields);
        let RecordID = response.data["RecordID"];
        fields["RecordID"] = RecordID;
        console.log(RecordID);
        this.postUpdate(RecordType, fields, RecordID);
      }).catch(error => {
        console.log(error);
      });
    },
    postUpdate(RecordType, fields, RecordID, beforeEditFields) {
      console.log('in postUpdate');
      console.log(fields);
      let updateEditObjects = [];
      Object.keys(fields).forEach(key => {
        console.log('in update loop');
        console.log(key);
        if(fields[key]) {
          if (this.isArray(fields[key])) {
            console.log('in array for');
            console.log(fields[key]);
            let recordsToDelete = beforeEditFields[key].filter(item => {
              let deleted = true;
              for (let i = 0; i < fields[key].length; i++) {
                if (item["RecordID"] === fields[key][i]["RecordID"]) {
                  deleted = false;
                }
              }
              return deleted;
            });
            recordsToDelete.forEach(record => this.postDelete(key, record["RecordID"]));
            for (let i = 0; i < fields[key].length; i++) {
              let subRecordID = fields[key][i]["RecordID"];
              if (subRecordID) {
                this.postUpdate(this.getSingularRecordType(key), fields[key][i], subRecordID, beforeEditFields[key][i]);
              } else {
                console.log('will create ' + key + ' from update');
                this.postCreate(this.getSingularRecordType(key), fields[key][i], RecordID, RecordType);
              }
            }
          } else if (this.isObject(fields[key])) {
            console.log('in object for');
            console.log(fields[key]);
            let subRecordID = fields[key]["RecordID"];
            if (subRecordID) {
              this.postUpdate(key, fields[key], subRecordID, beforeEditFields[key]);
            } else {
              console.log('will create ' + key + ' from update');
              this.postCreate(key, fields[key], RecordID, RecordType);
            }
          } else if(key === "RecordID" || fields[key] === ""
            || (this.mode === "update" && beforeEditFields ? this.checkEditMade(fields, beforeEditFields, key) : false)) {
              console.log(fields[key]);
              console.log('skipped');
            return;
          } else {
            console.log('in else for');
            console.log(fields[key]);
            let updateEditObject = {"EditType": "update", "RecordType": RecordType, "RecordID": RecordID};
            updateEditObject["FieldName"] = key;
            updateEditObject["Value"] = fields[key];
            updateEditObjects.push(updateEditObject);
          }
        }
      });
      console.log(updateEditObjects);
      axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, updateEditObjects,
        {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        
      }).catch(error => {
        this.statusMessage = "Failed to update AHJ information.";
        this.showStatusModal = true;
      });
    },
    postDelete(RecordType, RecordID) {
      let deleteEditObject = {RecordType: RecordType, RecordID: RecordID};
      axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, deleteEditObject,
        {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        
      }).catch(error => {
        this.statusMessage = "Failed to update AHJ information.";
        this.showStatusModal = true;
      });
    },
    getSingularRecordType(name) {
      if (name === "Contacts") {
        return "Contact";
      } else if (name === "EngineeringReviewRequirements") {
        return "EngineeringReviewRequirement";
      }
    },
    addContact() {
      this.AHJ.Contacts.push(this.deepCopyObject(constants.CONTACT_FIELDS));
    },
    addAddress(parent) {
      parent["Address"] = this.deepCopyObject(constants.ADDRESS_FIELDS);
    },
    addLocation(parent) {
      parent["Location"] = this.deepCopyObject(constants.LOCATION_FIELDS);
    },
    addEngRevReq() {
      this.AHJ.EngineeringReviewRequirements.push(this.deepCopyObject(constants.ENGINEERINGREVIEWREQUIREMENTS_FIELDS));
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
        for (let i = 0; i < this.tabsEngReqRev.length; i++) {
          this.tabsEngReqRev[i] = i;
        }
        this.tabCounterEngReqRev = this.tabsEngReqRev.length;
      }
    },
    deepCopyObject(objectToCopy) {
      let result = {};
      Object.keys(objectToCopy).forEach(key => {
        let field = objectToCopy[key];
        if (field) {
          if (this.isArray(field)) {
            result[key] = [];
            field.forEach(item => {
              result[key].push(this.setAHJFieldsFromResponse(item));
            });
          } else if(this.isObject(field)) {
            result[key] = this.deepCopyObject(field);
          } else {
            result[key] = field;
          }
        } else {
          result[key] = field;
        }
      });
      return result;
    },
    checkEditMade(before, after, field) {
      return before[field] === after[field]
    },
    isArray(item) {
      return item.constructor === Array;
    },
    isObject(item) {
      return typeof item === "object";
    },
    checkObjectOrArray(item) {
      return this.isObject(item) || this.isArray(item);
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
}

.card {
  margin-top: 25px;
  height: 750px;
  width: 200%;
  border: #d3d3d3 solid 1px;
  overflow-y: auto;
}
</style>
