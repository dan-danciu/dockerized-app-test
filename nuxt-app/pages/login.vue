<template>
  <div class="card">
    <form @submit.prevent @keyup.enter="login">
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
      <input type="submit" value="Login" @click="login" />
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
  methods: {
    async login(event) {
      event.preventDefault();
      let formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);
      this.$store.dispatch("auth1/signIn", formData).then(() => {
        if (this.$route.name !== "users") {
          this.$router.replace({ name: "users" });
        }
      });
    }
  }
};
</script>
