<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view class="main"/>
    <div class="footer">Placeholder</div>
  </div>
</template>

<style lang="scss">
html {
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
#app {
  font-family: 'Ubuntu', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 18px;
  line-height: 1.5em;
  letter-spacing: normal;
  text-align: left;
  color: #2c3e50;
  box-sizing: border-box;
  display: -ms-grid;
  display: grid;
  grid-template-areas:
    "navigation navigation navigation"
    ". main-area ."
    "footer footer footer";
  -ms-grid-columns: 1fr minmax(700px, 800px) 1fr;
  grid-template-columns: 1fr minmax(700px, 800px) 1fr;
  min-height: 100vh;
  max-width: 100vw;
}

#nav {
  padding: 30px;
  -ms-grid-column: 1;
  -ms-grid-row: 1;
  grid-area: navigation;
  text-align: center;
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: $primary;
    }
  }
}
.main {
  -ms-grid-column: 2;
  -ms-grid-row: 2;
  grid-area: main-area;
}
.footer {
  -ms-grid-column: 1;
  -ms-grid-column-span: 3;
  -ms-grid-row: 3;
  grid-area: footer;
  background: #2c3e50;
}
</style>
