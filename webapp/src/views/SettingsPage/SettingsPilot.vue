<template>
	<v-card style="padding:15px;">
		<v-flex style="margin-bottom:20px;">
			<span style="margin-left:0px;font-size:30px;"> PILOT INFO </span>
		</v-flex>
		<v-layout row>
			<v-layout column>
				<form>
					<v-flex>
            <v-text-field
              name="remote_pilot_certificate_number"
              label="Remote Pilot Certificate Number"
              id="remote_pilot_certificate_number"
              type="username"
              v-model="user_info.pilot.remote_pilot_certificate_number"
              required/>
            <v-text-field
              name="mobile_phone_number"
              label="Mobile Phone Number"
              id="mobile_phone_number"
              type="username"
              v-model="user_info.pilot.mobile_phone_number"
              required/>
					</v-flex>
					<v-layout row>
						<v-flex class="text-xs-center">
							<v-btn flat outline @click="_update_pilot_info()">
								Save
							</v-btn>
						</v-flex>
					</v-layout>
				</form>
			</v-layout>
		</v-layout>
	</v-card>
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

		}
	},
	methods: {
    async _update_pilot_info() {
      var pilot_info = {
        'remote_pilot_certificate_number': this.user_info.pilot.remote_pilot_certificate_number,
        'mobile_phone_number': this.user_info.pilot.mobile_phone_number
      }

      try {
				const response = await this.update_pilot_info(pilot_info,
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
    }
  }
}
</script>