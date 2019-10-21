<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Example app - Search some users by name!"/>
    <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Illo pariatur reprehenderit assumenda quas suscipit harum distinctio aliquid deserunt, aperiam totam provident exercitationem eaque necessitatibus laudantium porro repellendus voluptas. Ex, odio!</p>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  },
  data () {
    return {
      appUrl: '',
      userData: {
        first_name: '',
        last_name: '',
        email: '',
        age: 0
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.home {
  .card {
    font-size: 16px;
    min-height: 100px;
    padding: 10px 30px;
    position: relative;
    z-index: 1;
    @include animateShadowSetup(2, 16);
    &, &::before, &::after {
      border-radius: 5px;
    }
    &:hover {
      @include animateShadow;
    }
  }
}

</style>
