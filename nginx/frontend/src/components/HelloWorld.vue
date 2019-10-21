<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <input type="text" id="search" placeholder="Search" v-model="searchTerm">
    <button @click="searchUsers">Search</button>
    <div class="card" v-for="user in users" :key="user._id">
      <div class="name">Name: <strong>{{ user.last_name }}, {{ user.first_name }}</strong></div>
      <div class="email">Email: <strong>{{ user.email }}</strong></div>
      <div class="age">Age: <strong>{{ user.age }}</strong></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  data () {
    return {
      searchTerm: '',
      users: []
    }
  },
  props: {
    msg: String
  },
  methods: {
    searchUsers () {
      this.appUrl = window.location.href
      axios.get(this.appUrl + 'api/finduser?search_string=' + this.searchTerm)
        .then(res => {
          this.users = res.data.users
        })
    }
  }
}
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
  &, &::before, &::after {
    border-radius: 5px;
  }
  &:hover {
    @include animateShadow;
  }
}
button {
  border-radius: 5px;
  background-color: $primary;
}
</style>
