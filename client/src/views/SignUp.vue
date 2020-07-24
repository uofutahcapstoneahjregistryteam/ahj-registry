<template>
  <div class="login-container">
    <div class="card text-center" id="login-card">
      <div class="card-header">Sign Up</div>
      <div class="card-body">
        <input type="email" placeholder="Email" required v-model="Email"/>
        <br />
        <input type="text" placeholder="FirstName" v-model="FirstName"/>
        <br />
        <input type="text" placeholder="LastName" v-model="LastName"/>
        <br />
        <input type="password" placeholder="Password" required v-model="Password"/>
        <br />
        <b-button class="btn btn-primary" variant="primary" :disabled="sentRegistration" @click="submitRegistration">{{submitButtonText}}</b-button>
        <a href="#/login" class="btn btn-outline-primary">Login</a>
        <b-alert variant="success" :show="sentRegistration">Success! Please check your email.</b-alert> 
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  data() {
    return {
      Email: "",
      Password: "",
      FirstName: "",
      LastName: "",
      submitButtonText: "Submit",
      sentRegistration: false
    }
  },
  methods: {
    submitRegistration() {
      this.sentRegistration = true;
      this.submitButtonText = "Submitted!"
      axios.post(this.$store.state.apiURL + "register/", {
        "Email": this.Email,
        "Password": this.Password,
        "FirstName": this.FirstName,
        "LastName": this.LastName
      },
      {
        headers: {
          Authorization: constants.TOKEN_AUTH
        }
      }).catch(error => {

      });
    }
  }
}
</script>

<style>
.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  height: 100%;
}

#login-card {
  grid-column: 2 / 3;
  height: 400px;
}
</style>