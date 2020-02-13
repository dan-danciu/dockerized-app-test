import jwt_decode from "jwt-decode";

const getDefaultState = () => {
  return {
  };
};

const state = () => {
  return getDefaultState();
};

const actions = {
  async signIn({ dispatch }, formData) {
    let token = this.$auth.getToken("local");
    let refresh_token = this.$auth.getRefreshToken("local");
    if (token && refresh_token) {
      await dispatch("checkToken")
    } else if (formData) {
      await dispatch("requestToken", formData);
    }
    else {
      dispatch("signOut")
    }
  },

  signOut({}) {
    localStorage.clear();
    sessionStorage.clear();
    this.$auth.logout()
  },

  async requestToken({ dispatch }, formData) {
    let config = {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    };
    let res = await this.$axios.post(
      "http://localhost/api/auth/token",
      formData,
      config
    );

    this.$auth.setToken("local", "Bearer " + res.data.access_token);
    this.$auth.setRefreshToken("local", res.data.refresh_token);

    await dispatch("getUser")

  },

  async refreshToken({ dispatch }, formData) {
    console.log("refreshing")
    let config = {
      headers: {
        Authorization: this.$auth.getToken("local")
      }
    };
    let res = await this.$axios.post(
      "http://localhost/api/auth/refresh",
      formData,
      config
    );
    this.$auth.setToken("local", "Bearer " + res.data.access_token);
    this.$auth.setRefreshToken("local", res.data.refresh_token);

    await dispatch("getUser")
  },

  async checkToken({ dispatch }) {
    let jsonPayload = jwt_decode(this.$auth.getToken("local"));
    let expires = jsonPayload.exp;
    if (expires < Math.floor(Date.now() / 1000)) {
      if (this.$auth.loggedIn) {
        let formData = new FormData();
        formData.append("refresh_token", this.$auth.getRefreshToken("local"));
        await dispatch("refreshToken", formData);
      }
    }
    return;
  },

  async getUser({}) {
    let config = {
      headers: {
        Authorization: this.$auth.getToken("local")
      }
    };
    let user = await this.$axios.get(
      "/api/users/me",
      config
    )
    
    this.$auth.setUser(user.data)
  }
};


export default {
  state,
  actions
};
