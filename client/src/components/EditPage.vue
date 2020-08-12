<template>
  <b-container>
    <b-row>
      <b-col>
        <b-form @submit="onSubmit" @reset="onReset">
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
                <b-form-group id="input-group-1" label-for="input-1">
                  <b-tabs card>
                    <b-tab v-for="i in tabsContact" :key="'dyn-tab-' + i" :title="'Contact ' + i">
                      Contact {{ i }}
                      <b-button size="sm" variant="danger" class="float-right" @click="closeTabContact(i)">Remove</b-button>
                      <b-card-header header-tag="header" class="p-0" role="tab">
                        <b-button block v-b-toggle.accordion-4 variant="info">Contact Information</b-button>
                      </b-card-header>
                      <b-collapse id="accordion-4" visible accordion="my-accordion-contact" role="tabpanel">
                        <b-card-body>
                          <div v-for="(valueContact, nameContact) in AHJ.Contacts[i]" :key=nameContact>
                            <b-row v-if="!checkObjectOrArray(valueContact) && (mode === 'create' ? nameContact !== 'RecordID' : true)">
                              <b-col cols="4">
                                <label>{{ nameContact }}:</label>
                              </b-col>
                              <b-col cols="8">
                                <label v-if="nameContact === 'RecordID'">{{ AHJ.Contacts[i][nameContact] }}</label>
                                <b-form-select v-else-if="choiceFields.Contact[nameContact]" v-model="AHJ.Contacts[i][nameContact]" :options="choiceFields.Contact[nameContact]" />
                                <b-form-input v-else v-model="AHJ.Contacts[i][nameContact]" type="text" :placeholder="getBFormInputPlaceholder(nameContact)" />
                              </b-col>
                            </b-row>
                          </div>
                          <b-row>
                            <b-col>
                              <b-button v-if="AHJ.Contacts[i].Address === null" @click="addAddress(AHJ.Contacts[i])">Add Address</b-button>
                            </b-col>
                          </b-row>
                        </b-card-body>
                      </b-collapse>
                      <div v-if="AHJ.Contacts[i].Address">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-5 variant="info">Address</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-5" accordion="my-accordion-contact" role="tabpanel">
                          <b-card-body>
                          <div v-for="(valueContactAddress, nameContactAddress) in AHJ.Contacts[i].Address" :key=nameContactAddress>
                            <b-row v-if="!checkObjectOrArray(valueContactAddress) && (mode === 'create' ? nameContactAddress !== 'RecordID' : true)">
                              <b-col cols="4">
                                <label>{{ nameContactAddress }}:</label>
                              </b-col>
                              <b-col cols="8">
                                <label v-if="nameContactAddress === 'RecordID'">{{ valueContactAddress }}</label>
                                <b-form-select v-else-if="choiceFields.Address[nameContactAddress]" v-model="AHJ.Contacts[i].Address[nameContactAddress]" :options="choiceFields.Address[nameContactAddress]" />
                                <b-form-input v-else v-model="AHJ.Contacts[i].Address[nameContactAddress]" type="text" :placeholder="getBFormInputPlaceholder(nameContactAddress)" />
                                  </b-col>
                                </b-row>
                              </div>
                              <b-row>
                                <b-col>
                                  <b-button v-if="AHJ.Contacts[i].Address.Location === null" @click="addLocation(AHJ.Contacts[i].Address)">Add Location</b-button>
                                </b-col>
                              </b-row>
                          </b-card-body>
                        </b-collapse>
                      </div>
                      <div v-if="AHJ.Contacts[i].Address && AHJ.Contacts[i].Address.Location">
                        <b-card-header header-tag="header" class="p-0" role="tab">
                          <b-button block v-b-toggle.accordion-6 variant="info">Location</b-button>
                        </b-card-header>
                        <b-collapse id="accordion-6" accordion="my-accordion-contact" role="tabpanel">
                          <b-card-body>
                            <div v-for="(valueContactAddressLocation, nameContactAddressLocation) in AHJ.Contacts[i].Address.Location" :key=nameContactAddressLocation>
                              <b-row v-if="mode === 'create' ? nameContactAddressLocation !== 'RecordID' : true">
                                <b-col cols="4">
                                  <label>{{ nameContactAddressLocation }}:</label>
                                </b-col>
                                <b-col cols="8">
                                  <label v-if="nameContactAddressLocation === 'RecordID'">{{ valueContactAddressLocation }}</label>
                                  <b-form-select v-else-if="choiceFields.Location[nameContactAddressLocation]" v-model="AHJ.Contacts[i].Address.Location[nameContactAddressLocation]" :options="choiceFields.Location[nameContactAddressLocation]" />
                                  <b-form-input v-else v-model="AHJ.Contacts[i].Address.Location[nameContactAddressLocation]" type="text" :placeholder="getBFormInputPlaceholder(nameContactAddressLocation)" />
                                </b-col>
                              </b-row>
                            </div>
                          </b-card-body>
                        </b-collapse>
                      </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" @click.prevent="newTabContact" href="#"><b>+</b></b-nav-item>
                    </template>
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
                        <b-row v-if="mode === 'create' ? nameEngRevReq !== 'RecordID' : true">
                          <b-col cols="4">
                            <label>{{ nameEngRevReq }}:</label>
                          </b-col>
                          <b-col cols="8">
                            <label v-if="nameEngRevReq === 'RecordID'">{{ AHJ.EngineeringReviewRequirements[i][nameEngRevReq] }}</label>
                            <b-form-select v-else-if="choiceFields.EngineeringReviewRequirement[nameEngRevReq]" v-model="AHJ.EngineeringReviewRequirements[i][nameEngRevReq]" :options="choiceFields.EngineeringReviewRequirement[nameEngRevReq]" />
                            <b-form-input v-else v-model="AHJ.EngineeringReviewRequirements[i][nameEngRevReq]" type="text" :placeholder="getBFormInputPlaceholder(nameEngRevReq)" />
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
          <!-- <b-button variant="primary" class="float-right" @click="onSubmit">Submit</b-button> -->
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  props: [
    'mode',
    'editingRecordID'
  ],
  data() {
    return {
      previousAPIURLAddon: "",
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
  mounted() {
    this.previousAPIURLAddon = this.$store.state.apiURLAddon;
    this.$store.commit("setApiUrlAddon", "edit/submit/");
    if(this.$store.state.loginStatus["status"] !== "success") {
      this.$router.replace({ name: "login" });
    }
    this.initiateMode();
  },
  beforeDestroy() {
    console.log('in before destroy');
    this.$store.commit("setApiUrlAddon", this.previousAPIURLAddon);
  },
  methods: {
    validateEditAHJID() {
      return /^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$)/.test(this.editingRecordID);
    },
    initiateMode() {
      console.log('in initiate');
      console.log('mode: ' + this.mode);
      if (!this.mode) {
        console.log('no mode')
        return;
      } else if (this.mode === 'create') {
        this.AHJ = this.deepCopyObject(constants.AHJ_FIELDS);
      } else if (this.mode === 'update') {
        console.log('in update');
        if (!this.validateEditAHJID()) {
          console.log('failed uuid validation');
          return;
        }
        this.getAHJRecord();
      }
    },
    onSubmit() {
      console.log('in onSubmit');
      if (this.mode === "create") {
        this.postCreate("AHJ", this.AHJ);
      } else if (this.mode === "update") {
        console.log("in update");
        this.postUpdate("AHJ", this.AHJ, this.AHJ["RecordID"], this.beforeEditAHJRecord);
      }
    },
    onReset() {

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
        this.setTabCounts();
      });
    },
    setTabCounts() {
      this.tabCounterContact = this.AHJ.Contacts.length;
      for (let i = 0; i < this.tabCounterContact; i++) {
        this.tabsContact.push(i);
      }
      this.tabCounterEngReqRev = this.AHJ.EngineeringReviewRequirements.length;
      for (let i = 0; i < this.tabCounterEngReqRev; i++) {
        this.tabsEngReqRev.push(i);
      }
    },
    setAHJFieldsFromResponse(record) {
      let result = {};
      console.log(record);
      Object.keys(record).forEach(key => {
        console.log(Object.keys(record));
        let field = record[key];
        if (field) {
          if (field.hasOwnProperty("Value")) {
            console.log('in value');
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
            console.log('in object');
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
      let createEditObject = {EditType: "create", RecordType: RecordType}
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
        console.log(response);
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
        let field = fields[key];
        console.log('in update loop');
        console.log(key);
        if(field !== null) {
          if (this.isArray(field)) {
            console.log('in array for');
            console.log(field);
            if (this.mode === "update" && beforeEditFields) {
              this.deleteRemovedRecordsInArray(key, field, beforeEditFields);
            }
            for (let i = 0; i < field.length; i++) {
              let subRecordID = field[i]["RecordID"];
              if (subRecordID) {
                this.postUpdate(this.getSingularRecordType(key), field[i], subRecordID, beforeEditFields[key][i]);
              } else {
                console.log('will create ' + key + ' from update');
                this.postCreate(this.getSingularRecordType(key), field[i], RecordID, RecordType);
              }
            }
          } else if (this.isObject(field)) {
            console.log('in object for');
            console.log(field);
            let subRecordID = field["RecordID"];
            if (subRecordID) {
              this.postUpdate(key, field, subRecordID, beforeEditFields[key]);
            } else {
              console.log('will create ' + key + ' from update');
              this.postCreate(key, field, RecordID, RecordType);
            }
          } else if(key === "RecordID" || (this.mode === "create" ? field === "" : false)
            || (this.mode === "update" && beforeEditFields ? this.checkEditMade(fields, beforeEditFields, key) : false)) {
              console.log(field);
              console.log('skipped');
            return;
          } else {
            console.log('in else for');
            console.log(field);
            let updateEditObject = {EditType: "update", RecordType: RecordType, RecordID: RecordID};
            updateEditObject["FieldName"] = key;
            updateEditObject["Value"] = field;
            updateEditObjects.push(updateEditObject);
          }
        }
      });
      console.log(updateEditObjects);
      if (updateEditObjects.length > 0) {
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
      }
    },
    deleteRemovedRecordsInArray(key, field, beforeEditFields) {
      let recordsToDelete = beforeEditFields[key].filter(item => {
        let deleted = true;
        for (let i = 0; i < field.length; i++) {
          if (item["RecordID"] === field[i]["RecordID"]) {
            deleted = false;
          }
        }
        return deleted;
      });
      recordsToDelete.forEach(record => this.postDelete(this.getSingularRecordType(key), record["RecordID"]));
    },
    postDelete(RecordType, RecordID) {
      let deleteEditObject = {EditType: "delete", RecordType: RecordType, RecordID: RecordID};
      axios.post(this.$store.state.apiURL + this.$store.state.apiURLAddon, deleteEditObject,
        {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        
      }).catch(error => {
        console.log(error);
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
    newTabContact() {
      this.addContact();
      this.tabsContact.push(this.tabCounterContact++);
    },
    newTabEngRevReq() {
      this.addEngRevReq();
      this.tabsEngReqRev.push(this.tabCounterEngReqRev++);
    },
    closeTabContact(x) {
      for (let i = 0; i < this.tabsContact.length; i++) {
        if (this.tabsContact[i] === x) {
          this.AHJ.Contacts.splice(i, 1);
          this.tabsContact.splice(i, 1);
        }
        for (let i = 0; i < this.tabsContact.length; i++) {
          this.tabsContact[i] = i;
        }
        this.tabCounterContact = this.tabsContact.length;
      }
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
              result[key].push(this.deepCopyObject(item));
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
  },
  computed: {
    modes() {
      if(this.$store.state.loginStatus["isSuper"]) {
        return [
          { value: "update", text: "Edit an existing AHJ..."},
          { value: "create", text: "Submit a new AHJ..."}
        ];
      } else {
        return [
          { value: "update", text: "Edit an existing AHJ..."}
        ];
      }
    }
  }
};
</script>

<style scoped>
/* .container {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 54px 1fr 50px;
} */

/* .card {
  margin-top: 25px;
  height: 750px;
  width: 100%;
  border: #d3d3d3 solid 1px;
  overflow-y: auto;
} */
</style>
