<template>
  <div class="container">
    <div>
      <div class="title">Test</div>
      <UserSearch msg="Example app - Search some users by name!" />
    </div>
  </div>
</template>

<script>
export default {
  middleware: "authenticated",
  components: {
    UserSearch: () => import("../components/UserSearch")
  }
};
</script>

<style lang="scss">
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
