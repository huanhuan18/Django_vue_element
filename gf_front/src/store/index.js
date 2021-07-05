import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  //state可以理解为data,它的状态会保存在所有组件的上层
  state: {
    userinfo:{}
  },
  mutations: {
    editUserinfo(state, user){
      state.userinfo = user
      console.log('store111',state)
    }
  },
  actions: {
  },
  modules: {
  }
})
