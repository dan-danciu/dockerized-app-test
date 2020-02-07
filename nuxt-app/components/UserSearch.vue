<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <input type="text" id="search" placeholder="Search" v-model="searchTerm" />
    <button @click="searchUsers">Search</button>
    <button name="xtoken" @click="getXtoken">X-Token Test</button>
    <div class="card" v-for="user in users" :key="user.id">
      <div class="name">
        Name:
        <strong>{{ user.last_name }}, {{ user.first_name }}</strong>
      </div>
      <div class="email">
        Email:
        <strong>{{ user.email }}</strong>
      </div>
      <div class="age">
        Age:
        <strong>{{ user.age }}</strong>
      </div>
      <div class="gender">
        Gender:
        <strong>{{ user.gender }}</strong>
      </div>
    </div>
    <div class="xtoken">{{ xtoken }}</div>
  </div>
</template>

<script>
export default {
  name: "UserSearch",
  data() {
    return {
      searchTerm: "",
      users: [],
      xtoken: ""
    };
  },
  props: {
    msg: String
  },
  methods: {
    async searchUsers() {
      this.appUrl = window.location.href;
      await this.$store.dispatch("auth1/checkToken");
      let config = {
        headers: {
          Authorization: this.$store.state.auth.access_token
        }
      };
      this.$axios
        .get(
          "http://localhost/api/users/find?search_string=" + this.searchTerm,
          config
        )
        .then(res => {
          this.users = res.data;
        })
        .catch(err => {
          console.log(err, err.response.data.detail);
        });
    },
    getXtoken() {
      this.appUrl = window.location.href;
      this.$store.dispatch("auth1/checkToken");
      let config = {
        headers: {
          Authorization: this.$store.state.auth.access_token
        }
      };
      this.$axios
        .get("http://localhost/api/users/xtoken", config)
        .then(res => {
          this.xtoken = res.data;
        })
        .catch(err => {
          console.log(err, err.response.data.detail);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
.card {
  font-size: 16px;
  min-height: 100px;
  padding: 10px 30px;
  position: relative;
  z-index: 1;
  margin: 10px 0px;
  @include animateShadowSetup(2, 16);
  &,
  &::before,
  &::after {
    border-radius: 5px;
  }
  &:hover {
    @include animateShadow;
  }
}
.xtoken {
  word-wrap: break-word;
  max-width: 50vw;
}
</style>
