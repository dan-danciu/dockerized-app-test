export default function({ store, redirect }) {
  console.log(store.state.auth1.authenticated)
  if (!store.state.auth1.authenticated) {
    return redirect("/login");
  }
  
}
