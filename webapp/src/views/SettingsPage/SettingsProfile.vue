<template>
  <v-layout column>
    <v-card style="padding:15px;">
      <v-flex style="margin-bottom:20px;">
        <span style="margin-left:0px;font-size:30px;"> PROFILE </span>
      </v-flex>
      <v-layout row>
        <v-layout column>
          <form>
            <v-flex>
              <v-text-field
                name="name"
                label="Username"
                id="name"
                type="username"
                v-model="user_info.user.username"
                required></v-text-field>
              <v-text-field
                name="email"
                label="Email"
                id="email"
                type="email"
                v-model="user_info.user.email"
                required></v-text-field>
              <v-text-field
                name="first_name"
                label="First Name"
                id="first_name"
                type="username"
                v-model="user_info.user.first_name"
                required></v-text-field>
              <v-text-field
                name="last_name"
                label="Last Name"
                id="last_name"
                type="last_name"
                v-model="user_info.user.last_name"
                required></v-text-field>
            </v-flex>
            <v-layout row>
              <v-flex class="text-xs-center">
                <v-btn flat outline @click="save_profile_changes()">
                  Save
                </v-btn>
              </v-flex>
            </v-layout>
          </form>
        </v-layout>

        <v-layout column v-if="false">
          <v-flex class="text-xs-center">
            <span style="font-size:20px;"> Profile Picture </span>
          </v-flex>
          <v-flex class="text-xs-center">
            <v-badge overlap>
                  <v-btn
                        color="primary"
                        dark
                        small
                        absolute
                        fab
                        slot="badge"
                        @click='pickFile'
                    >
                      <v-icon>file_upload</v-icon>
                    </v-btn>
                  <v-avatar
                      :size="size"
                      >
                      <img :src="profile_info.image" :width="size" :height="size"/>
              </v-avatar>
              <input
                type="file"
                style="display: none"
                id="myBtn"
                @change="onFilePicked"
                accept="image/*"
              >
              </v-badge>
          </v-flex>
        </v-layout>
      </v-layout>
    </v-card>
    <v-card style="padding:15px;margin-top:15px;">
      <v-flex style="margin-bottom:20px;">
        <span style="margin-left:0px;font-size:30px;"> PASSWORD </span>
      </v-flex>
      <v-layout column>
          <v-form
          lazy-validation
          v-model="password.valid" ref="form">
            <v-flex>
              <v-text-field
                name="old_password"
                label="Old Password"
                id="old_password"
                type="password"
                v-model="password.old"
                required></v-text-field>
              <v-text-field
                name="new_password"
                label="New Password"
                id="new_password"
                type="password"
                v-model="password.new"
                required></v-text-field>
              <v-text-field
                name="confirm_password"
                label="Confirm Password"
                id="confirm_password"
                type="password"
                v-model="password.confirm"
                :rules="[comparePasswords]"
                required></v-text-field>
            </v-flex>
            <v-layout row>
              <v-flex class="text-xs-center">
                <v-btn flat 
                outline 
                @click="_change_password()"
                :disabled="!password.valid || password.old === ''||
                password.new === '' || password.confirm === ''">
                  Save
                </v-btn>
              </v-flex>
            </v-layout>
          </v-form>
        </v-layout>
    </v-card>
  </v-layout>
</template>

<style>

</style>

<script>
import API from '@/mixins/API.js'

export default {
	mixins: [API],
	props: ['user_info'],
	data() {
		return {
			size:'150px',
			items: [
				{'title': 'Profile'},
				{'title': 'Licenses'},
				{'title': 'Delete'}
      ],
      password: {
        old: '',
        new: '',
        confirm: '',
        valid: false
      },
			profile_info: {
				image: 'https://avatars0.githubusercontent.com/u/8029035?s=400&v=4',
				documents: [
					{ type: 'part_107', location: 'https://drive.google.com/file/d/1j8jXiXbI05VogHVKivfavdZgbaD0yrwP/view?usp=sharing'},
					{ type: 'part_333', location: 'https://drive.google.com/file/d/1j8jXiXbI05VogHVKivfavdZgbaD0yrwP/view?usp=sharing'}
				]
      },
      rules: {
        required: value => !!value || 'Required.'
      }
		}
	},
	methods: {
		async save_profile_changes() {
      var info = {'username': this.user_info.user.username, 'email': this.user_info.user.email,
      'first_name': this.user_info.user.first_name, 'last_name': this.user_info.user.last_name}
			try {
				const response = await this.update_user_info(info,
					this.$store.state.access_token
				);
				if (response.status == 200) {
					this.$emit('snackbar',6000, 'Profile Updated');
				} else if (response.status == 31) {
					throw error
				}
			} catch (err) {
          		this.$emit('snackbar', 6000, 'Username already taken!')
			}
    },
    async _change_password() {
      try {
        const response = await this.change_password(this.password.old,
          this.password.new,
          this.$store.state.access_token
        );
        if (response.status == 200) {
          this.$emit('snackbar',6000, 'Profile Updated');
        }
      } catch(err) {
        const response = err.response
        if (response.status == 400) {
          this.$emit('snackbar',6000, response.data.message);
        } 
      }
    }
	},
  computed: {
    comparePasswords () {
      return this.password.new === this.password.confirm ? true : 'Passwords don\'t match'
    }
  }
}
</script>