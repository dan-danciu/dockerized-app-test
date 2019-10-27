import axios from 'axios'
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
            let jsonPayload = decodeToken(token)
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
            let jsonPayload = decodeToken(res.data.access_token)
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

  const decodeToken = token => {
    let base64Url = token.split('.')[1]
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    let jsonPayload = JSON.parse(decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join('')))
    return jsonPayload    
  }

  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }