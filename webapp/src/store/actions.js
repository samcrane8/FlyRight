export const actions = {
    changeAccessToken ({commit}) {
        commit('setAccessToken')
      },
    changeUserInfo ({commit}) {
        commit('setUserInfo')
    },
    init(store) {
        store.commit('setAccessToken', localStorage.getItem('access_token'))
        // store.commit('setUserInfo', localStorage.getItem('user_info'))
    }
}