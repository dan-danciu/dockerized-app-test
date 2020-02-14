import jwt_decode from "jwt-decode";

const getDefaultState = () => {
  return {};
};

const state = () => {
  return getDefaultState();
};

const actions = {
  async signIn({ dispatch }, formData) {
    let token = this.$auth.getToken("local");
    let refresh_token = sessionStorage.getItem("refresh_token");
    if (token && refresh_token) {
      await dispatch("checkToken");
    } else {
      await dispatch("requestToken", formData);
    }
  },

  signOut({}) {
    localStorage.clear();
    sessionStorage.clear();
    this.$auth.logout();
  },

  async requestToken({ dispatch }, formData) {
    let config = {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    };
    let res = await this.$axios.post("/api/auth/token", formData, config);
    await dispatch("setTokens", res.data);
  },

  async refreshToken({ dispatch }, formData) {
    let config = {
      headers: {
        Authorization: this.$auth.getToken("local")
      }
    };
    let res = await this.$axios.post("/api/auth/refresh", formData, config);
    await dispatch("setTokens", res.data);
  },

  async checkToken({ dispatch }) {
    let jsonPayload = jwt_decode(this.$auth.getToken("local"));
    let expires = jsonPayload.exp;
    if (expires < Math.floor(Date.now() / 1000)) {
      if (this.$auth.loggedIn) {
        let formData = new FormData();
        formData.append(
          "refresh_token",
          sessionStorage.getItem("refresh_token")
        );
        await dispatch("refreshToken", formData);
      }
    }
    return;
  },

  async setTokens({ dispatch }, { access_token, refresh_token }) {
    await this.$auth.setToken("local", "Bearer " + access_token);
    sessionStorage.setItem("refresh_token", refresh_token);

    await dispatch("getUser");
  },

  async getUser({}) {
    let config = {
      headers: {
        Authorization: this.$auth.getToken("local")
      }
    };
    let user = await this.$axios.get("/api/users/me", config);

    this.$auth.setUser(user.data);
  }
};

export default {
  state,
  actions
};
