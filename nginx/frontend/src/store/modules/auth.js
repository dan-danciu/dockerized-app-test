import axios from 'axios'
import jwt_decode from 'jwt-decode'
import { router } from '../../router'

const getDefaultState = () => {
    return {
      access_token: null,
      token_expires: null,
      refresh_token: null
    }
  }
  
  const state = getDefaultState()

  const getters = {
  }

  const mutations = {
    setCredentials(state, payload) {
        state.access_token = payload.access_token
        state.token_expires = payload.token_expires
        state.refresh_token = payload.refresh_token
    },
    clearData(state) {
        Object.assign(state, getDefaultState())
    }
  }

  const actions = {
      async signIn({ commit, dispatch }, formData) {
        let token = localStorage.getItem('access_token')
        let refresh_token = sessionStorage.getItem('refresh_token')
        if (token) {
            let jsonPayload = jwt_decode(token)
            let expires = jsonPayload.exp
            if (expires < Math.floor(Date.now()/1000)) {
              if (refresh_token) {
                dispatch('requestToken', formData)
              }
              else {
                dispatch('signOut')
              }
            }
            else {
                let payload = {
                  'access_token': token, 
                  'token_expires': jsonPayload.exp,
                  refresh_token
                }
                commit('setCredentials', payload)
                router.replace({name: 'home'})
            }
        }
        else {
            dispatch('requestToken', formData)
        }
        
      },

      signOut({ commit }) {
        localStorage.clear()
        commit('clearData')
        router.replace({name: 'login'})
      },

      async requestToken({state, commit}, formData) {
        let config = {
          header : {
              'Content-Type' : 'multipart/form-data',
              'Authorization': 'Bearer ' + state.access_token
          }
        }
        let res = await axios.post('/api/auth/token', formData, config)
        let jsonPayload = jwt_decode(res.data.access_token)
        let payload = {
          'access_token': res.data.access_token, 
          'token_expires': jsonPayload.exp, 
          'refresh_token': res.data.refresh_token
        }
        commit('setCredentials', payload)
        localStorage.setItem('access_token', res.data.access_token)
        sessionStorage.setItem('refresh_token', res.data.refresh_token)
        router.replace({name: 'home'})
      },

      async checkToken({state, dispatch}) {
        if (state.token_expires < Math.floor(Date.now()/1000) && state.refresh_token) {
          let formData = new FormData()
          formData.append('grant_type', "refresh_token")
          formData.append('refresh_token', state.refresh_token)
          await dispatch('requestToken', formData)
        }
        else {
          dispatch('signOut')
        }
      }

  }

  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }