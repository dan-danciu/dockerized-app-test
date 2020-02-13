<template>
  <nav>
    <div class="nav-links">
      <nuxtLink to="/">Home</nuxtLink>
      <nuxtLink to="/login" v-show="!isAuthenticated">Login</nuxtLink>
      <nuxtLink to="/about">About</nuxtLink>
      <nuxtLink to="/users" v-show="isAuthenticated">User Search</nuxtLink>
      <a class="signout" @click="signout" v-show="isAuthenticated">Sign out</a>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return this.$auth.loggedIn;
    }
  },
  methods: {
    signout() {
      this.$store
        .dispatch("auth1/signOut")
        .then(() => this.$router.replace({ name: "login" }));
    }
  }
};
</script>

<style lang="scss" scoped>
.nav-links {
  margin-left: auto;
  margin-right: auto;
  text-align: right;
  max-width: 1200px;
  a {
    margin-left: 10px;
    text-decoration: none;
    color: $primary;
    &:visited {
      color: $primary;
    }
  }
  .signout {
    display: inline-block;
    margin-left: 10px;
    cursor: pointer;
    color: $primary;
  }
}
</style>