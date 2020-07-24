<template>
  <div class="login-container">
    <div class="card text-center" id="login-card">
      <div class="card-header">Sign In</div>
      <div class="card-body">
        <input type="text" placeholder="Username" v-model="username"  @keyup.enter="login"/>
        <br />
        <input type="password" placeholder="Password" v-model="password"  @keyup.enter="login"/>
        <br />
        <a href="#" class="btn btn-primary" @click="login">Login</a>
        <a href="#/register" class="btn btn-outline-primary">Sign Up</a>
      </div>
      <div class="card-footer text-muted">Forgot Password?</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  data() {
    return {
      username: "",
      password: ""
    }
  },
  methods: {
    login() {
        axios.post(this.$store.state.apiURL + "login/", {
          "username": this.username,
          "password": this.password
        }).then(response => {
        console.log(response);
          this.$store.commit("changeUserLoginStatus", {
          status: response.data["status"],
          isSuper: response.data["is_superuser"],
          isStaff: response.data["is_staff"],
          authToken: "Token " + response.data["auth_token"]
        });
        if(this.$store.state.loginStatus["status"] === "success") {
          if(this.$store.state.loginStatus["isSuper"]) {
            this.$router.push({ name: "edit" });
          } else {
            this.$router.push({name: "edit"});
          }
        } else {
          this.$router.push({name: "login"});
        }
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
  height:   400px;
}
</style>