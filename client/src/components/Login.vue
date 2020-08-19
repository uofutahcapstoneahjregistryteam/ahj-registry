<template>
  <b-modal title="Sign In" v-model="$store.state.showLoginModal" @show="clearForm()">
    <div v-if="hasAccount" class="text-center">
      <input type="text" placeholder="Username" v-model="username"  @keyup.enter="login"/>
      <br />
      <input type="password" placeholder="Password" v-model="password"  @keyup.enter="login"/>
      <br />
      <b-button variant="primary" @click="login">Login</b-button>
      <b-button @click="hasAccount = false">Sign Up</b-button>
    </div>
    <div v-else class="text-center">
      <input type="email" placeholder="Email" required v-model="Email"/>
      <br />
      <input type="text" placeholder="FirstName" v-model="FirstName"/>
      <br />
      <input type="text" placeholder="LastName" v-model="LastName"/>
      <br />
      <input type="password" placeholder="Password" required v-model="Password"/>
      <br />
      <b-button variant="primary" :disabled="sentRegistration" @click="submitRegistration">{{submitButtonText}}</b-button>
      <b-button @click="hasAccount = true">Login</b-button>
      <b-alert variant="success" :show="sentRegistration">Success! Please check your email.</b-alert> 
    </div>
    <template v-slot:modal-footer class="align-center text-muted"><label>Forgot Password?</label></template>
  </b-modal>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  data() {
    return {
      hasAccount: true,

      username: "",
      password: "",

      Email: "",
      Password: "",
      FirstName: "",
      LastName: "",
      submitButtonText: "Submit",
      sentRegistration: false
    }
  },
  methods: {
    login() {
      axios.post(this.$store.state.apiURL + "login/", {
        "username": this.username,
        "password": this.password
      }).then(response => {
          this.$store.commit("changeUserLoginStatus", {
          status: response.data["status"],
          isSuper: response.data["is_superuser"],
          isStaff: response.data["is_staff"],
          authToken: "Token " + response.data["auth_token"]
        });
        this.$store.commit("setShowLoginModal", false);
      }).catch(error => {

      });
    },
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
    },
    clearForm() {
      this.hasAccount = true;
      this.username = "";
      this.password = "";
      this.Email = "";
      this.Password = "";
      this.FirstName = "";
      this.LastName = "";
      this.sentRegistration = false;
    }
  }
}
</script>

<style scoped>
.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  height: 100%;
}

#login-card {
  grid-column: 2 / 3;
  height:   400px;
}

input {
  margin-bottom: 10px;
}
</style>