export default function ({ store, redirect }) {
  console.log(store.state.auth1.authenticated)
  // If the user is authenticated redirect to home page
    if (store.state.auth1.authenticated) {
      return redirect('/')
    }
  }
  