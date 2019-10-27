import axios from 'axios'
import { router } from '../../router'

const getDefaultState = () => {
    return {
      access_token: null,
      refresh_token: null
    }
  }
  
  const state = getDefaultState()

  const getters = {
  }

  const mutations = {
    setCredentials(state, access_token) {
        state.access_token = access_token
    },
    clearData(state) {
        Object.assign(state, getDefaultState())
    }
  }

  const actions = {
      async signIn({ commit }, formData) {
        let token = localStorage.getItem('access_token')
        if (token) {
            commit('setCredentials', token)
        }
        else {
            let config = {
                header : {
                    'Content-Type' : 'multipart/form-data'
                }
            }
            let res = await axios.post('/api/auth/token', formData, config)
            commit('setCredentials', res.data.access_token)
            localStorage.setItem('access_token', res.data.access_token)
        }
        router.replace({name: 'home'})
        
      },
      signOut({ commit }) {
        localStorage.clear()
        commit('clearData')
        router.replace({name: 'login'})
      }

  }

  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }