export const getters = {
    accessToken: (state, getters, rootState) => {
        return state;
    },

    getAccessToken: (state, getters) => {
    return getters.accessToken.reduce((total, product) => {
        return total + product.price * product.quantity
    }, 0)
    }
}