<template>
  <div class="card">
    <form @submit.prevent="login" @keyup.enter="login">
      <label for="username" hidden>username</label>
      <input
        type="text"
        id="username"
        v-model="username"
        autocomplete="username"
        placeholder="username"
      />
      <br />
      <label for="password" hidden>password</label>
      <input
        type="password"
        id="password"
        v-model="password"
        autocomplete="current-password"
        placeholder="password"
      />
      <br />
      <br />
      <input type="submit" value="Login" />
    </form>
  </div>
</template>

<script>
export default {
  middleware: "notAuthenticated",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  mounted() {
    if (localStorage.getItem("access_token")) {
      this.$store.dispatch("auth/signIn", "");
    }
  },
  methods: {
    async login() {
      let formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);
      this.$store
        .dispatch("auth/signIn", formData)
        .then(() => this.$router.replace({ name: "index" }));
    }
  }
};
</script>
