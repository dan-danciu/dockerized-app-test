<template>
  <div class="container">
    <div>Nothing to see here!</div>
  </div>
</template>

<script>
export default {
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
  text-align: left;
}
</style>
