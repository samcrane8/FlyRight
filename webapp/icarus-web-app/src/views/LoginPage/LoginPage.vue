<template>
  <v-content>
    <section>
      <v-layout row wrap 
      style="height:100vh"
      px-5
      class="background"
      >
        <v-layout column style="margin-top:35vh">
          <v-flex mt-2>
            <v-flex class="text-xs-center" style="color:#ffffff">
              <span style="font-size:30px;color:#ffffff;">Campus Drone Management.</span><br/>
              <span style="font-size:20px;color:#ffffff;">An intuitive drone  policy toolkit.</span>
            </v-flex>
          </v-flex>
        </v-layout>
        <v-layout column style="margin-top:15vh">
          <v-flex ma-1>
            <v-card style="background-color:#ffffff;opacity:0.90">
              <v-form 
              @success="onLogin"
              lazy-validation
              v-model="valid" ref="form"
              >
                <v-card-title>
                  <v-flex class="text-xs-left" style="padding-top:0px;">
                    <h2 style="font-size:28px;font-weight:200"> Login </h2>
                  </v-flex>
                </v-card-title>
                <v-card-text>
                  <v-layout column>
                    <v-flex>
                      <v-text-field
                        name="loginUsername"
                        label="Username"
                        id="loginUsername"
                        type="username"
                        :rules=[rules.required]
                        v-model="loginUsername"
                        required></v-text-field>
                    </v-flex>
                    <v-flex>
                      <v-text-field
                        name="loginPassword"
                        label="Password"
                        id="loginPassword"
                        type="password"
                        :rules=[rules.required]
                        v-model="loginPassword"
                        required></v-text-field>
                    </v-flex>
                    <v-flex>
                      <a @click="forgotPassword"> forgot password? </a>
                    </v-flex>
                    <v-flex id="warning" class="text-xs-center" style="visibility:hidden;color:#ff0000;">
                      <p> Member does not exist </p>
                    </v-flex>
                    <v-flex class="text-xs-center">
                      <v-btn v-on:click="userLogin" color="primary"
                      flat
                      outline
                      >
                        Login
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-text>
              </v-form>
            </v-card>
          </v-flex>
        </v-layout>
      </v-layout>
    </section> 
    <icarus-footer/>

    <v-dialog
      v-model="dialog"
      width="500"
    >
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Password Reset
        </v-card-title>

        <v-card-text>
          An email will be sent to the address you submit below 
          with a link to a page to reset your password.
        </v-card-text>
        <v-flex
        style="margin-left:20px;margin-right:20px;"
        >
          <v-text-field
            name="password_reset_email"
            label="Account Email"
            id="password_reset_email"
            type="email"
            :rules=[rules.required]
            v-model="passwordResetEmail"
            required>
          </v-text-field>
        </v-flex>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            flat
            @click="sendPasswordResetEmail"
          >
            Submit
          </v-btn>
          <v-btn
            color="primary"
            flat
            @click="dialog=false"
          >
            Nevermind
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import router from '@/router'
import API from '@/mixins/API.js'
import VideoBg from 'vue-videobg'
import Footer from '@/components/Footer'

Vue.component('video-bg', VideoBg)

Vue.use(VueAxios, axios)

export default {
  name: 'Login',
  mixins: [API],
  components: {
    'icarus-footer': Footer,
  },
  data () {
    return {
      signUpUsername: '',
      signUpEmail: '',
      signUpPassword: '',
      loginUsername: '',
      loginPassword: '',
      passwordConfirm: '',
      loginDialog: false,
      signUpDialog: false,
      valid: true,
      dialog: false,
      passwordResetEmail: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
      rules: {
          required: value => !!value || 'Required.'
        }
    }
  },
  methods: {
    async userLogin() {
      if (this.$refs.form.validate()) {
        try {
          var response = await this.login(this.loginUsername, this.loginPassword)
          if (response.status == 200) {
            this.loginDialog = true;
            this.signUpDialog = false;
            const data = response.data;
            this.$store.commit('setAccessToken', data['access_token'])
            localStorage.setItem('access_token', data['access_token'])
            this.$emit('change-toolbar-color', 'primary')
            this.$emit('login')
            router.push('/homepage')
          }

          response = await this.get_current_user_info(
            this.$store.state.access_token
          )
          if (response.status == 200) {
            const data = response.data;
            this.$store.commit('user_info', data)
            localStorage.setItem('user_info', JSON.stringify(data) )
          }
        }
        catch(error) {
          this.$emit('snackbar', 6000, 'Either email has not been verified or invalid login info.')
        }

      } else {
        this.$emit('snackbar', 6000, 'Fill out login info.')
      }
    },
    onLogin() {
      router.push('/homepage')
    },
    forgotPassword() {
      this.dialog = true
    },
    async sendPasswordResetEmail() {
      var response = await this.forgot_password(this.passwordResetEmail)
      this.dialog = false
      this.$emit('snackbar', 6000, response.data.message)
    }
  },
  computed: {
    comparePasswords () {
      return this.signUpPassword === this.passwordConfirm ? true : 'Passwords don\'t match'
    }
  }
}
</script>
