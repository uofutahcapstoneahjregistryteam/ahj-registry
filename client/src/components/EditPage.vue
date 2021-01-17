<template>
  <b-container>
    <b-row>
      <b-col>
        <b-button v-if="editPageViewOnly" size="sm" variant="danger" @click="tryEnterEditPageEditMode">Edit this AHJ</b-button>
      </b-col>
    </b-row>
    <b-row v-if="recordLoading">
      <div class="text-center text-primary my-2">
        <b-spinner class="align-middle"></b-spinner>
        <strong>&nbsp; Loading...</strong>
      </div>
    </b-row>
    <b-row v-else>
      <b-col>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-tabs card>
              <b-tab title="AHJ" active>
                  <b-form-group id="input-group-1" label-for="input-1">
                    <b-tabs card>
                      <b-card-header header-tag="header" class="p-0" role="tab">
                        <b-button block v-b-toggle.accordion-1 variant="info">AHJ Information</b-button>
                      </b-card-header>
                      <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
                        <b-card-body>
                        <div v-for="(valueAHJ, nameAHJ) in constants.AHJ_FIELDS" :key=nameAHJ>
                          <b-row v-if="!isObject(AHJ[nameAHJ]) && (mode === 'create' ? nameAHJ !== 'RecordID' : true)">
                            <b-col cols="4">
                              <label>{{ nameAHJ === "RecordID" ? "AHJ ID" : formatFieldNames(nameAHJ) }}:</label>
                            </b-col>
                            <b-col v-if="editPageViewOnly">
                              <label>{{ AHJ[nameAHJ] }}</label>
                            </b-col>
                            <b-col cols="8" v-else>
                              <label v-if="nameAHJ === 'RecordID' || nameAHJ === 'AHJCode'">{{ AHJ[nameAHJ] }}</label>
                              <b-form-select v-else-if="choiceFields.AHJ[nameAHJ]" v-model="AHJ[nameAHJ]" :options="choiceFields.AHJ[nameAHJ]" />
                              <b-form-input v-else v-model="AHJ[nameAHJ]" type="text" :placeholder="getBFormInputPlaceholder(nameAHJ)" />
                            </b-col>
                          </b-row>
                        </div>
                        <b-row>
                          <b-col>
                            <b-button v-if="!editPageViewOnly && AHJ.Address === null" @click="addAddress(AHJ)">Add Address</b-button>
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
                              <div v-for="(valueAHJAddress, nameAHJAddress) in constants.ADDRESS_FIELDS" :key=nameAHJAddress>
                                <b-row v-if="!isObject(AHJ.Address[nameAHJAddress]) && (mode === 'create' ? nameAHJAddress !== 'RecordID' : true)">
                                  <b-col cols="4">
                                    <label>{{ nameAHJAddress === "RecordID" ? "Address ID" : formatFieldNames(nameAHJAddress) }}:</label>
                                  </b-col>
                                  <b-col v-if="editPageViewOnly">
                                    <label>{{ AHJ.Address[nameAHJAddress] }}</label>
                                  </b-col>
                                  <b-col cols="8" v-else>
                                    <label v-if="nameAHJAddress === 'RecordID'">{{ AHJ.Address[nameAHJAddress] }}</label>
                                    <b-form-select v-else-if="choiceFields.Address[nameAHJAddress]" v-model="AHJ.Address[nameAHJAddress]" :options="choiceFields.Address[nameAHJAddress]" />
                                    <b-form-input v-else v-model="AHJ.Address[nameAHJAddress]" type="text" :placeholder="getBFormInputPlaceholder(nameAHJAddress)" />
                                  </b-col>
                                </b-row>
                              </div>
                              <b-row>
                                <b-col>
                                  <b-button v-if="!editPageViewOnly && AHJ.Address.Location === null" @click="addLocation(AHJ.Address)">Add Location</b-button>
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
                            <div v-for="(valueAHJAddressLocation, nameAHJAddressLocation) in constants.LOCATION_FIELDS" :key=nameAHJAddressLocation>
                              <b-row v-if="mode === 'create' ? nameAHJAddressLocation !== 'RecordID' : true">
                                <b-col cols="4">
                                  <label>{{ nameAHJAddressLocation === "RecordID" ? "Location ID" : formatFieldNames(nameAHJAddressLocation)  }}:</label>
                                </b-col>
                                <b-col v-if="editPageViewOnly">
                                  <label>{{ AHJ.Address.Location[nameAHJAddressLocation] }}</label>
                                </b-col>
                                <b-col cols="8" v-else>
                                  <label v-if="nameAHJAddressLocation === 'RecordID'">{{ AHJ.Address.Location[nameAHJAddressLocation] }}</label>
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
                    <b-tab v-for="i in tabsContact" :key="'dyn-tab-' + i" :title="'Contact ' + getTabTitle('Contact', i)">
                      <b-button size="sm" variant="danger" class="float-right" :disabled="editPageViewOnly" @click="closeTabContact(i)">Delete</b-button>
                      <b-card-header header-tag="header" class="p-0" role="tab">
                        <b-button block v-b-toggle.accordion-4 variant="info">Contact Information</b-button>
                      </b-card-header>
                      <b-collapse id="accordion-4" visible accordion="my-accordion-contact" role="tabpanel">
                        <b-card-body>
                          <div v-for="(valueContact, nameContact) in constants.CONTACT_FIELDS" :key=nameContact>
                            <b-row v-if="!isObject(AHJ.Contacts[i][nameContact]) && (mode === 'create' ? nameContact !== 'RecordID' : true)">
                              <b-col cols="4">
                                <label>{{ nameContact === "RecordID" ? "Contact ID" : formatFieldNames(nameContact)  }}:</label>
                              </b-col>
                              <b-col v-if="editPageViewOnly">
                                <label>{{ AHJ.Contacts[i][nameContact] }}</label>
                              </b-col>
                              <b-col cols="8" v-else>
                                <label v-if="nameContact === 'RecordID'">{{ AHJ.Contacts[i][nameContact] }}</label>
                                <b-form-select v-else-if="choiceFields.Contact[nameContact]" v-model="AHJ.Contacts[i][nameContact]" :options="choiceFields.Contact[nameContact]" />
                                <b-form-input v-else v-model="AHJ.Contacts[i][nameContact]" type="text" :placeholder="getBFormInputPlaceholder(nameContact)" />
                              </b-col>
                            </b-row>
                          </div>
                          <b-row>
                            <b-col>
                              <b-button v-if="!editPageViewOnly && AHJ.Contacts[i].Address === null" @click="addAddress(AHJ.Contacts[i])">Add Address</b-button>
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
                          <div v-for="(valueContactAddress, nameContactAddress) in constants.ADDRESS_FIELDS" :key=nameContactAddress>
                            <b-row v-if="!isObject(AHJ.Contacts[i].Address[nameContactAddress]) && (mode === 'create' ? nameContactAddress !== 'RecordID' : true)">
                              <b-col cols="4">
                                <label>{{ nameContactAddress === "RecordID" ? "Address ID" : formatFieldNames(nameContactAddress) }}:</label>
                              </b-col>
                              <b-col v-if="editPageViewOnly">
                                <label>{{ AHJ.Contacts[i].Address[nameContactAddress] }}</label>
                              </b-col>
                              <b-col cols="8" v-else>
                                <label v-if="nameContactAddress === 'RecordID'">{{ AHJ.Contacts[i].Address[nameContactAddress] }}</label>
                                <b-form-select v-else-if="choiceFields.Address[nameContactAddress]" v-model="AHJ.Contacts[i].Address[nameContactAddress]" :options="choiceFields.Address[nameContactAddress]" />
                                <b-form-input v-else v-model="AHJ.Contacts[i].Address[nameContactAddress]" type="text" :placeholder="getBFormInputPlaceholder(nameContactAddress)" />
                                  </b-col>
                                </b-row>
                              </div>
                              <b-row>
                                <b-col>
                                  <b-button v-if="!editPageViewOnly && AHJ.Contacts[i].Address.Location === null" @click="addLocation(AHJ.Contacts[i].Address)">Add Location</b-button>
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
                            <div v-for="(valueContactAddressLocation, nameContactAddressLocation) in constants.LOCATION_FIELDS" :key=nameContactAddressLocation>
                              <b-row v-if="mode === 'create' ? nameContactAddressLocation !== 'RecordID' : true">
                                <b-col cols="4">
                                  <label>{{ nameContactAddressLocation === "RecordID" ? "Location ID" : formatFieldNames(nameContactAddressLocation)  }}:</label>
                                </b-col>
                                <b-col v-if="editPageViewOnly">
                                  <label>{{ AHJ.Contacts[i].Address.Location[nameContactAddressLocation] }}</label>
                                </b-col>
                                <b-col cols="8" v-else>
                                  <label v-if="nameContactAddressLocation === 'RecordID'">{{ AHJ.Contacts[i].Address.Location[nameContactAddressLocation] }}</label>
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
                      <b-nav-item role="presentation" :disabled="editPageViewOnly" @click.prevent="newTabContact" href="#"><b>+</b></b-nav-item>
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
                    <b-tab v-for="i in tabsEngReqRev" :key="'dyn-tab-' + i" :title="'Engineering Review Requirement ' + getTabTitle('EngineeringReviewRequirement', i)">
                      <b-row>
                        <b-col>
                          <b-button size="sm" variant="danger" class="float-right" :disabled="editPageViewOnly" @click="closeTabEngReqReq(i)">Delete</b-button>
                        </b-col>
                      </b-row>
                      <div v-for="(valueEngRevReq, nameEngRevReq) in constants.ENGINEERINGREVIEWREQUIREMENTS_FIELDS" :key=nameEngRevReq>
                        <b-row v-if="mode === 'create' ? nameEngRevReq !== 'RecordID' : true">
                          <b-col cols="4">
                            <label>{{ nameEngRevReq === "RecordID" ? "Engineering Review Requirement ID" : formatFieldNames(nameEngRevReq) }}:</label>
                          </b-col>
                          <b-col v-if="editPageViewOnly">
                            <label>{{ AHJ.EngineeringReviewRequirements[i][nameEngRevReq] }}</label>
                          </b-col>
                          <b-col cols="8" v-else>
                            <label v-if="nameEngRevReq === 'RecordID'">{{ AHJ.EngineeringReviewRequirements[i][nameEngRevReq] }}</label>
                            <b-form-select v-else-if="choiceFields.EngineeringReviewRequirement[nameEngRevReq]" v-model="AHJ.EngineeringReviewRequirements[i][nameEngRevReq]" :options="choiceFields.EngineeringReviewRequirement[nameEngRevReq]" />
                            <b-form-input v-else v-model="AHJ.EngineeringReviewRequirements[i][nameEngRevReq]" type="text" :placeholder="getBFormInputPlaceholder(nameEngRevReq)" />
                          </b-col>
                        </b-row>
                      </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" :disabled="editPageViewOnly" @click.prevent="newTabEngRevReq" href="#"><b>+</b></b-nav-item>
                    </template>
                  </b-tabs>
                </b-form-group>
              </b-tab>
              <b-tab title="Fee Structures">
                <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                  <b-tabs card>
                    <b-tab v-for="i in tabsFeeStructure" :key="'dyn-tab-' + i" :title="'Fee Structure ' + getTabTitle('FeeStructure', i)">
                      <b-row>
                        <b-col>
                          <b-button size="sm" variant="danger" class="float-right" :disabled="editPageViewOnly" @click="closeTabFeeStructure(i)">Delete</b-button>
                        </b-col>
                      </b-row>
                      <div v-for="(valueFeeStructure, nameFeeStructure) in constants.DOCUMENTSUBMISSIONMETHOD_FIELDS" :key=nameFeeStructure>
                        <b-row v-if="mode === 'create' ? nameFeeStructure !== 'RecordID' : true">
                          <b-col cols="4">
                            <label>{{ nameFeeStructure === "RecordID" ? "Fee Structure ID" : formatFieldNames(nameFeeStructure) }}:</label>
                          </b-col>
                          <b-col v-if="editPageViewOnly">
                            <label>{{ AHJ.FeeStructures[i][nameFeeStructure] }}</label>
                          </b-col>
                          <b-col cols="8" v-else>
                            <label v-if="nameFeeStructure === 'RecordID'">{{ AHJ.FeeStructures[i][nameFeeStructure] }}</label>
                            <b-form-select v-else-if="choiceFields.FeeStructure[nameFeeStructure]" v-model="AHJ.FeeStructures[i][nameFeeStructure]" :options="choiceFields.FeeStructure[nameFeeStructure]" />
                            <b-form-input v-else v-model="AHJ.FeeStructures[i][nameFeeStructure]" type="text" :placeholder="getBFormInputPlaceholder(nameFeeStructure)" />
                          </b-col>
                        </b-row>
                      </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" :disabled="editPageViewOnly" @click.prevent="newTabFeeStructure" href="#"><b>+</b></b-nav-item>
                    </template>
                  </b-tabs>
                </b-form-group>
              </b-tab>
              <b-tab title="Document Submission Methods">
                <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                  <b-tabs card>
                    <b-tab v-for="i in tabsDocSubMethod" :key="'dyn-tab-' + i" :title="'Document Submission Method ' + getTabTitle('DocumentSubmissionMethod', i)">
                      <b-row>
                        <b-col>
                          <b-button size="sm" variant="danger" class="float-right" :disabled="editPageViewOnly" @click="closeTabPerIssMethod(i)">Delete</b-button>
                        </b-col>
                      </b-row>
                      <div v-for="(valueDocSubMethod, nameDocSubMethod) in constants.DOCUMENTSUBMISSIONMETHOD_FIELDS" :key=nameDocSubMethod>
                        <b-row v-if="mode === 'create' ? nameDocSubMethod !== 'RecordID' : true">
                          <b-col cols="4">
                            <label>{{ nameDocSubMethod === "RecordID" ? "Document Submission Method ID" : formatFieldNames(nameDocSubMethod) }}:</label>
                          </b-col>
                          <b-col v-if="editPageViewOnly">
                            <label>{{ AHJ.DocumentSubmissionMethods[i][nameDocSubMethod] }}</label>
                          </b-col>
                          <b-col cols="8" v-else>
                            <label v-if="nameDocSubMethod === 'RecordID'">{{ AHJ.DocumentSubmissionMethods[i][nameDocSubMethod] }}</label>
                            <b-form-select v-else-if="choiceFields.DocumentSubmissionMethods[nameDocSubMethod]" v-model="AHJ.DocumentSubmissionMethods[i][nameDocSubMethod]" :options="choiceFields.DocumentSubmissionMethods[nameDocSubMethod]" />
                            <b-form-input v-else v-model="AHJ.DocumentSubmissionMethods[i][nameDocSubMethod]" type="text" :placeholder="getBFormInputPlaceholder(nameDocSubMethod)" />
                          </b-col>
                        </b-row>
                      </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" :disabled="editPageViewOnly" @click.prevent="newTabDocSubMethod" href="#"><b>+</b></b-nav-item>
                    </template>
                  </b-tabs>
                </b-form-group>
              </b-tab>
              <b-tab title="Permit Issue Methods">
                <b-form-group
                      id="input-group-1"
                      label-for="input-1"
                    >
                  <b-tabs card>
                    <b-tab v-for="i in tabsPerIssMethod" :key="'dyn-tab-' + i" :title="'Permit Issue Method ' + getTabTitle('PermitIssueMethod', i)">
                      <b-row>
                        <b-col>
                          <b-button size="sm" variant="danger" class="float-right" :disabled="editPageViewOnly" @click="cl(i)">Delete</b-button>
                        </b-col>
                      </b-row>
                      <div v-for="(valuePerIssMethod, namePerIssMethod) in constants.DOCUMENTSUBMISSIONMETHOD_FIELDS" :key=namePerIssMethod>
                        <b-row v-if="mode === 'create' ? namePerIssMethod !== 'RecordID' : true">
                          <b-col cols="4">
                            <label>{{ namePerIssMethod === "RecordID" ? "Permit Issue Method ID" : formatFieldNames(namePerIssMethod) }}:</label>
                          </b-col>
                          <b-col v-if="editPageViewOnly">
                            <label>{{ AHJ.DocumentSubmissionMethods[i][namePerIssMethod] }}</label>
                          </b-col>
                          <b-col cols="8" v-else>
                            <label v-if="namePerIssMethod === 'RecordID'">{{ AHJ.DocumentSubmissionMethods[i][namePerIssMethod] }}</label>
                            <b-form-select v-else-if="choiceFields.PermitIssueMethod[namePerIssMethod]" v-model="AHJ.PermitIssueMethods[i][namePerIssMethod]" :options="choiceFields.PermitIssueMethod[namePerIssMethod]" />
                            <b-form-input v-else v-model="AHJ.PermitIssueMethods[i][namePerIssMethod]" type="text" :placeholder="getBFormInputPlaceholder(namePerIssMethod)" />
                          </b-col>
                        </b-row>
                      </div>
                    </b-tab>
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" :disabled="editPageViewOnly" @click.prevent="newTabPerIssMethod" href="#"><b>+</b></b-nav-item>
                    </template>
                  </b-tabs>
                </b-form-group>
              </b-tab>
            </b-tabs>
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
    'selectedAHJ'
  ],
  data() {
    return {
      constants: constants,
      recordLoading: true,
      editPageViewOnly: true,
      beforeEditAHJRecord: {},
      EditTypeAndRecordTypeAndRecordID: "",
      requestType: "post",
      tabsContact: [],
      tabCounterContact: 0,
      tabsEngReqRev: [],
      tabCounterEngReqRev: 0,
      tabsFeeStructure: [],
      tabCounterFeeStructure: 0,
      tabsAHJInspection: [],
      tabCounterAHJInspection: 0,
      tabsAHJInspectionContact: [],
      tabsCounterAHJInspectionContact: 0,
      tabsDocSubMethod: [],
      tabCounterDocSubMethod: 0,
      tabsPerIssMethod: [],
      tabCounterPerIssMethod: 0,
      AHJ: {},
      unconfirmedRecordEdits: [],
      choiceFields: constants.CHOICE_FIELDS
    }
  },
  mounted() {
    this.initiateMode();
  },
  methods: {
    initiateMode() {
      if (!this.mode) {
        return;
      } else if (this.mode === 'create') {
        this.AHJ = this.deepCopyObject(constants.AHJ_FIELDS);
      } else if (this.mode === 'update') {
        this.AHJ = this.setAHJFieldsFromResponse(this.selectedAHJ);
        // this.getUnconfirmedRecordEdits();
        this.setTabCounts();
        this.recordLoading = false;
      }
    },
    tryEnterEditPageEditMode() {
      if (this.$store.state.loginStatus.status !== "success") {
        this.$store.commit("setShowLoginModal", true);
        return;
      }
      this.getConfirmedAHJRecord();
      this.editPageViewOnly = false;
    },
    onSubmit() {
      if (this.mode === "create") {
        this.postCreate("AHJ", this.AHJ);
      } else if (this.mode === "update") {
        this.postUpdate("AHJ", this.AHJ, this.AHJ["RecordID"], this.beforeEditAHJRecord);
      }
    },
    onReset() {

    },
    getConfirmedAHJRecord() {
      this.recordLoading = true;
      axios.get(this.$store.state.apiURL + "ahj/" + this.AHJ.RecordID + "/?view=confirmed", {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {
        this.beforeEditAHJRecord = this.setAHJFieldsFromResponse(response.data);
        this.AHJ = this.deepCopyObject(this.beforeEditAHJRecord);
        this.setTabCounts();
        this.recordLoading = false;
      });
    },
    getUnconfirmedRecordEdits() {
      axios.get(this.$store.state.apiURL + "edit/" + "?RecordID__in=" + this.AHJ.RecordID + "&IsConfirmed__in=None", {
        headers: {
          Authorization: this.constants.TOKEN_AUTH
        }
      }).then(response => {
        this.unconfirmedRecordEdits = response.results;
        this.recordLoading = false;
      });
    },
    setTabCounts() {
      this.tabCounterContact = this.AHJ.Contacts.length;
      this.tabsContact = [];
      for (let i = 0; i < this.tabCounterContact; i++) {
        this.tabsContact.push(i);
      }
      this.tabsEngReqRev = [];
      this.tabCounterEngReqRev = this.AHJ.EngineeringReviewRequirements.length;
      for (let i = 0; i < this.tabCounterEngReqRev; i++) {
        this.tabsEngReqRev.push(i);
      }
      this.tabsDocSubMethod = [];
      this.tabCounterDocSubMethod = this.AHJ.DocumentSubmissionMethods.length;
      for (let i = 0; i < this.tabCounterDocSubMethod; i++) {
        this.tabsDocSubMethod.push(i);
      }
      this.tabsPerIssMethod = [];
      this.tabCounterPerIssMethod = this.AHJ.PermitIssueMethods.length;
      for (let i = 0; i < this.tabCounterPerIssMethod; i++) {
        this.tabsPerIssMethod.push(i);
      }
      this.tabCounterAHJInspection = this.AHJ.AHJInspections.length;
      this.tabsAHJInspection = [];
      for (let i = 0; i < this.tabCounterAHJInspection; i++) {
        this.tabsAHJInspection.push(i);
      }
      // this.tabsAHJInspectionContact = this.AHJ.AHJInspection.Contacts.length;
      // this.tabsAHJInspectionContact = [];
      // for (let i = 0; i < this.tabsCounterAHJInspectionContact; i++) {
      //   this.tabsAHJInspectionContact.push(i);
      // }
      this.tabCounterFeeStructure = this.AHJ.FeeStructures.length;
      this.tabsFeeStructure = [];
      for (let i = 0; i < this.tabCounterFeeStructure; i++) {
        this.tabsFeeStructure.push(i);
      }
    },
    setAHJFieldsFromResponse(record) {
      let result = {};
      if (record.hasOwnProperty("EditID")) {
        result["RecordID"] = record["RecordID"];
        result["Value"] = record["Value"];
        return result;
      } else {
        Object.keys(record).filter(key => key !== "mpoly").forEach(key => { // do not include mpoly for now
          let field = record[key];
          if (field) {
            if (field.hasOwnProperty("Value")) {
              let value = field["Value"];
              if (value && field["RecordID"] === value) {
                key = "RecordID";
              }
              result[key] = value;
            } else if (this.isArray(field)) {
              result[key] = [];
              field.forEach(item => {
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
      }
    },
    postCreate(RecordType, fields, ParentID, ParentRecordType) {
      let createEditObject = {EditType: "create", RecordType: RecordType}
      if (ParentID && ParentRecordType) {
        createEditObject["ParentID"] = ParentID;
        createEditObject["ParentRecordType"] = ParentRecordType;
      }
      axios.post(this.$store.state.apiURL + "edit/submit/", createEditObject,
        {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
      }).then(response => {
        let RecordID = response.data["RecordID"];
        fields["RecordID"] = RecordID;
        this.postUpdate(RecordType, fields, RecordID);
      }).catch(error => {
      });
    },
    postUpdate(RecordType, fields, RecordID, beforeEditFields) {
      let updateEditObjects = [];
      Object.keys(fields).forEach(key => {
        let field = fields[key];
        if(field !== null) {
          if (this.isArray(field)) {
            if (this.mode === "update" && beforeEditFields) {
              this.deleteRemovedRecordsInArray(key, field, beforeEditFields);
            }
            for (let i = 0; i < field.length; i++) {
              let subRecordID = field[i]["RecordID"];
              if (subRecordID) {
                this.postUpdate(this.getSingularRecordType(key), field[i], subRecordID, beforeEditFields[key][i]);
              } else {
                this.postCreate(this.getSingularRecordType(key), field[i], RecordID, RecordType);
              }
            }
          } else if (this.isObject(field)) {
            let subRecordID = field["RecordID"];
            if (subRecordID) {
              this.postUpdate(key, field, subRecordID, beforeEditFields[key]);
            } else {
              this.postCreate(key, field, RecordID, RecordType);
            }
          } else if(key === "RecordID" || (this.mode === "create" ? field === "" : false)
            || (this.mode === "update" && beforeEditFields ? this.checkEditMade(fields, beforeEditFields, key) : false)) {
            return;
          } else {
            let updateEditObject = {EditType: "update", RecordType: RecordType, RecordID: RecordID};
            updateEditObject["FieldName"] = key;
            updateEditObject["Value"] = field;
            updateEditObjects.push(updateEditObject);
          }
        }
      });
      if (updateEditObjects.length > 0) {
        axios.post(this.$store.state.apiURL + "edit/submit/", updateEditObjects,
          {
          headers: {
            Authorization: this.$store.state.loginStatus.authToken
          }
        }).then(response => {

        }).catch(error => {
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
      axios.post(this.$store.state.apiURL + "edit/submit/", deleteEditObject,
        {
        headers: {
          Authorization: this.$store.state.loginStatus.authToken
        }
      }).then(response => {

      }).catch(error => {
      });
    },
    getSingularRecordType(name) {
      return name.splice(0, -1);
    },
    addContact(parent) {
      parent["Contacts"].push(this.deepCopyObject(constants.CONTACT_FIELDS));
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
    addDocSubMethod() {
      this.AHJ.DocumentSubmissionMethods.push(this.deepCopyObject(constants.DOCUMENTSUBMISSIONMETHOD_FIELDS));
    },
    addPerIssMethod() {
      this.AHJ.PermitIssueMethods.push(this.deepCopyObject(constants.PERMITSUBMISSIONMETHOD_FIELDS));
    },
    addFeeStructure() {
      this.AHJ.FeeStructures.push(this.deepCopyObject(constants.FEESTRUCTURE_FIELDS));
    },
    addAHJInspection() {
      this.AHJ.AHJInspections.push(this.deepCopyObject(constants.AHJINSPECTION_FIELDS));
    },
    newTabContact() {
      this.addContact(this.AHJ);
      this.tabsContact.push(this.tabCounterContact++);
    },
    newTabAHJInspectionContact(ahjInspection) {
      this.addContact(ahjInspection);
      this.tabsAHJInspectionContact.push(this.tabCounterAHJInspection++);
    },
    newTabEngRevReq() {
      this.addEngRevReq();
      this.tabsEngReqRev.push(this.tabCounterEngReqRev++);
    },
    newTabDocSubMethod() {
      this.addDocSubMethod();
      this.tabsDocSubMethod.push(this.tabCounterDocSubMethod++);
    },
    newTabPerIssMethod() {
      this.addPerIssMethod();
      this.tabsPerIssMethod.push(this.tabCounterPerIssMethod++);
    },
    newTabFeeStructure() {
      this.addFeeStructure();
      this.tabsFeeStructure.push(this.tabCounterFeeStructure++);
    },
    newTabAHJInspection() {
      this.addAHJInspection();
      this.tabsAHJInspection.push(this.tabCounterAHJInspection++);
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
    closeTabDocSubMethod(x) {
      for (let i = 0; i < this.tabsDocSubMethod.length; i++) {
        if (this.tabsDocSubMethod[i] === x) {
          this.AHJ.DocumentSubmissionMethods.splice(i, 1);
          this.tabsDocSubMethod.splice(i, 1);
        }
        for (let i = 0; i < this.tabsDocSubMethod.length; i++) {
          this.tabsDocSubMethod[i] = i;
        }
        this.tabCounterDocSubMethod = this.tabsDocSubMethod.length;
      }
    },
    closeTabPerIssMethod(x) {
      for (let i = 0; i < this.tabsPerIssMethod.length; i++) {
        if (this.tabsPerIssMethod[i] === x) {
          this.AHJ.PermitIssueMethods.splice(i, 1);
          this.tabsPerIssMethod.splice(i, 1);
        }
        for (let i = 0; i < this.tabsPerIssMethod.length; i++) {
          this.tabsPerIssMethod[i] = i;
        }
        this.tabCounterPerIssMethod = this.tabsPerIssMethod.length;
      }
    },
    closeTabFeeStructure(x) {
      for (let i = 0; i < this.tabsFeeStructure.length; i++) {
        if (this.tabsFeeStructure[i] === x) {
          this.AHJ.FeeStructures.splice(i, 1);
          this.tabsFeeStructure.splice(i, 1);
        }
        for (let i = 0; i < this.tabsFeeStructure.length; i++) {
          this.tabsFeeStructure[i] = i;
        }
        this.tabCounterFeeStructure = this.tabsFeeStructure.length;
      }
    },
    closeTabAHJInspection(x) {
      for (let i = 0; i < this.tabsAHJInspection.length; i++) {
        if (this.tabsAHJInspection[i] === x) {
          this.AHJ.AHJInspections.splice(i, 1);
          this.tabsAHJInspection.splice(i, 1);
        }
        for (let i = 0; i < this.tabsAHJInspection.length; i++) {
          this.tabsAHJInspection[i] = i;
        }
        this.tabCounterAHJInspection = this.tabsAHJInspection.length;
      }
    },
    closeTabAHJInspectionContact(ahjInspection, x) {
      for (let i = 0; i < this.tabsAHJInspectionContact.length; i++) {
        if (this.tabsAHJInspectionContact[i] === x) {
          ahjInspection.Contacts.splice(i, 1);
          this.tabsAHJInspectionContact.splice(i, 1);
        }
        for (let i = 0; i < this.tabsAHJInspectionContact.length; i++) {
          this.tabsAHJInspectionContact[i] = i;
        }
        this.tabsCounterAHJInspectionContact = this.tabsAHJInspectionContact.length;
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
    getBFormInputPlaceholder(fieldName) {
      return "Enter a " + this.formatFieldNames(fieldName) + "...";
    },
    getTabTitle(type, index) {
      let RecordID = this.AHJ[type + "s"][index].RecordID;
      if (RecordID) {
        return RecordID;
      }
      return "(new)";
    },
    formatFieldNames(name) {
      let result = "";
      let index = 0;
      while (name[index] >= 'A' && name[index] <= 'Z') {
        index++;
      }
      index--;
      result += name.substring(0, index);
      if (name.substring(0, 3) === "AHJ") {
        result += "AHJ ";
        name = name.substring(3);
      }
      for (let i = index; i < name.length; i++) {
        if (/([^A-Za-z0-9\.\$]+)|([A-Z])(?=[A-Z][a-z])|([A-Za-z])(?=\$?[0-9]+(?:\.[0-9]+)?)|([0-9])(?=[^\.0-9])|([a-z])(?=[A-Z])/.test(name.substring(index, i))) {
          result += name.substring(index, i - 1) + " ";
          index = i - 1;
        }
      }
      result += name.substring(index, name.length);
      return result;
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

</style>
