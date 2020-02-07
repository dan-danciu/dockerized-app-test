import jwt_decode from "jwt-decode";

const getDefaultState = () => {
  return {
    access_token: null,
    token_expires: null,
    refresh_token: null,
    authenticated: false
  };
};

const state = () => {
  return getDefaultState();
};

const getters = {};

const mutations = {
  setCredentials(state, payload) {
    state.access_token = payload.access_token;
    state.token_expires = payload.token_expires;
    state.refresh_token = payload.refresh_token;
    state.authenticated = true;
  },
  clearData(state) {
    Object.assign(state, getDefaultState());
  }
};

// will need to do this:
// use auth to log in
// serve refresh token with users/me
// update token with axios refresh token
// tomorrow...


const actions = {
  async signIn({ commit, dispatch }, formData) {
    let token = this.$auth.getToken("local");
    let refresh_token = this.$auth.getRefreshToken("local");
    if (token) {
      let jsonPayload = jwt_decode(token);
      let expires = jsonPayload.exp;
      if (expires < Math.floor(Date.now() / 1000)) {
        if (refresh_token) {
          await dispatch("requestToken", formData);
        } else {
          await dispatch("signOut");
        }
      } else {
        let payload = {
          access_token: token,
          token_expires: jsonPayload.exp,
          refresh_token
        };
        await commit("setCredentials", payload);
      }
    } else {
      await dispatch("requestToken", formData);
    }
  },

  signOut({ commit }) {
    localStorage.clear();
    sessionStorage.clear();
    commit("clearData");
  },

  async requestToken({ commit }, formData) {
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

    let jsonPayload = jwt_decode(res.data.access_token);
    let payload = {
      access_token: res.data.access_token,
      token_expires: jsonPayload.exp,
      refresh_token: res.data.refresh_token
    };
    await commit("setCredentials", payload);
    this.$auth.setToken("local", "Bearer " + payload.access_token);
    this.$auth.setRefreshToken("local", payload.refresh_token);

    // localStorage.setItem("access_token", res.data.access_token);
    // sessionStorage.setItem("refresh_token", res.data.refresh_token);
  },

  async refreshToken({ state, commit }, formData) {
    let config = {
      headers: {
        Authorization: state.access_token
      }
    };
    let res = await this.$axios.post(
      "http://localhost/api/auth/refresh",
      formData,
      config
    );
    let jsonPayload = jwt_decode(res.data.access_token);
    let payload = {
      access_token: res.data.access_token,
      token_expires: jsonPayload.exp,
      refresh_token: res.data.refresh_token
    };
    await commit("setCredentials", payload);
    this.$auth.setToken("local", "Bearer " + payload.access_token);
    this.$auth.setRefreshToken("local", payload.refresh_token);
    // localStorage.setItem("access_token", res.data.access_token);
    // sessionStorage.setItem("refresh_token", res.data.refresh_token);
  },

  async checkToken({ state, dispatch }) {
    if (state.token_expires < Math.floor(Date.now() / 1000)) {
      if (state.refresh_token) {
        let formData = new FormData();
        formData.append("refresh_token", state.refresh_token);
        await dispatch("refreshToken", formData);
      }
    }
    return;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
