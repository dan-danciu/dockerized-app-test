export default function ({ $auth, redirect }) {
  // If the user is authenticated redirect to home page
    if ($auth.loggedIn) {
      return redirect('/')
    }
  }
  