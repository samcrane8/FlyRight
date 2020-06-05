import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        light : true,
        themes: {
            light: {
                primary: '#B3A369',
                secondary: '#003057',
                background: '#FFFFFF'
            },
        },
    },
});
