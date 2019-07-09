<template>
  <v-content>
    <section>
      <v-layout row wrap
      class="background"
      style="padding-top:15vh;height:95vh"
      px-5
      >
        <v-layout column style="margin-top:25vh">
          <v-flex mt-2>
            <v-flex class="text-xs-center" style="color:#ffffff">
              <span style="font-size:30px;color:#ffffff;">Campus Drone Management</span><br/>
              <span style="font-size:20px;color:#ffffff;">The drone policy toolkit.</span>
            </v-flex>
          </v-flex>
        </v-layout>
        <v-spacer/>
        <v-flex class="hidden-xs-only">
          <reg-step
          v-on:snackbar="_snackbar"
          />
        </v-flex>
      </v-layout>
      <first-section/>
      <icarus-footer/>
    </section>
  </v-content>
</template>

<style>
  .background {
		background: linear-gradient( rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4) ), url('/static/result.jpg');
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
    width:100%;
	}
</style>

<script>
  import Vue from 'vue';
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import VideoBg from 'vue-videobg'
  import RegistrationStepper from './RegistrationStepper'
  import FirstSection from './FirstSection'
  import Footer from '@/components/Footer'

  Vue.use(VueAxios, axios)

  export default {
    name: 'Login',
    components: {
      'video-bg': VideoBg,
      'reg-step': RegistrationStepper,
      'first-section': FirstSection,
      'icarus-footer': Footer,
    },
    methods: {
      handleScroll(event){
        if (window.scrollY > 350) {
          this.$emit('change-toolbar-color', 'primary')
        } else {
          this.$emit('change-toolbar-color', 'transparent')
        }
      },
      _snackbar(timeout, text) {
        this.$emit('snackbar', timeout, text)
      },
      methods: {
        goto(loc){
          router.push(loc)
        }
      },
    },
    created () {
      window.addEventListener('scroll', this.handleScroll);
    },
    destroyed () {
      window.removeEventListener('scroll', this.handleScroll);
    },
    mounted() {
      this.$emit('change-toolbar-color', 'transparent')
    }
  }
</script>
