export const mutations = {
    setAccessToken (state, newAccessToken) {
        state.access_token = newAccessToken;
    },
    setUserInfo (state, newUserInfo) {
        state.user_info = newUserInfo
    }
}