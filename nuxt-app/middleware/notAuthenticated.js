export default function ({ store, redirect }) {
  console.log(store.state.auth.authenticated)
  // If the user is authenticated redirect to home page
    if (store.state.auth.authenticated) {
      return redirect('/')
    }
  }
  