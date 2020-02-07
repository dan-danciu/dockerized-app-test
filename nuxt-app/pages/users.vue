<template>
  <div class="container">
    <div>
      <UserSearch msg="Example app - Search some users by name!" />
    </div>
  </div>
</template>

<script>
export default {
  components: {
    UserSearch: () => import("../components/UserSearch")
  },
  middleware: "authenticated"
};
</script>

<style lang="scss">
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: left;
}
</style>
