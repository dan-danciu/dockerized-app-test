<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Example app - Search some users by name!"/>
    <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Illo pariatur reprehenderit assumenda quas suscipit harum distinctio aliquid deserunt, aperiam totam provident exercitationem eaque necessitatibus laudantium porro repellendus voluptas. Ex, odio!</p>
    <div class="card">
      <div class="name">Name: <strong>{{ userData.last_name }}, {{ userData.first_name }}</strong></div>
      <div class="email">Email: <strong>{{ userData.email }}</strong></div>
      <div class="age">Age: <strong>{{ userData.age }}</strong></div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import axios from 'axios'

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
  },
  mounted () {
    this.appUrl = window.location.href
    axios.get(this.appUrl + 'api/firstuser')
      .then(res => {
        this.userData = res.data
      })
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
