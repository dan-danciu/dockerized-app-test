<template>
  <nav>
    <div class="nav-links">
      <nuxt-link to="/">Home</nuxt-link>
      <nuxt-link to="/login">Login</nuxt-link>
      <nuxt-link to="/about">About</nuxt-link>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return this.$store.state.auth.authenticated;
    }
  }
};
</script>

<style lang="scss" scoped>
nav {
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
  }
}
</style>