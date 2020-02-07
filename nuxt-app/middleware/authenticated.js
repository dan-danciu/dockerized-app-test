export default function({ store, redirect }) {
  console.log(store.state.auth.authenticated)
  if (!store.state.auth.authenticated) {
    return redirect("/login");
  }
  
}
