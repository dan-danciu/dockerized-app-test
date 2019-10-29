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
    },
    clearData(state) {
        Object.assign(state, getDefaultState())
    }
  }

  const actions = {
      async signIn({ commit, dispatch }, formData) {
        let token = localStorage.getItem('access_token')
        if (token) {
            let jsonPayload = jwt_decode(token)
            let expires = jsonPayload.exp
            if (expires < Math.floor(Date.now()/1000)) {
                dispatch('signOut')
            }
            else {
                let payload = {'access_token': token, 'token_expires': jsonPayload.exp}
                commit('setCredentials', payload)
                router.replace({name: 'home'})
            }
        }
        else {
            let config = {
                header : {
                    'Content-Type' : 'multipart/form-data'
                }
            }
            let res = await axios.post('/api/auth/token', formData, config)
            let jsonPayload = jwt_decode(res.data.access_token)
            let payload = {'access_token': res.data.access_token, 'token_expires': jsonPayload.exp}
            commit('setCredentials', payload)
            localStorage.setItem('access_token', res.data.access_token)
            router.replace({name: 'home'})
        }
        
      },
      signOut({ commit }) {
        localStorage.clear()
        commit('clearData')
      }

  }

  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }