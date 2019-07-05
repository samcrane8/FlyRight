<template>
	<v-card>
		<v-card-title>
			<v-layout column>
				<v-flex>
					<span style="font-size:30px;"> Contact </span>
				</v-flex>
				<v-layout column style="margin-left:5px;margin-right:5px;">
					<v-flex class="text-xs-left">
						<div>
							This program is currently a beta that is being tested on the Georgia Tech campus, and is written by undergrads. For that reason, there are going to be tons and tons of bugs. However, if you're so inclined, you can help us out! <br/><br/>
							Go ahead and send any bug, screenshots, and console logs to this email: <a href="mailto:samcrane8@gmail.com?Subject=[ICARUS%20BUG]" target="_top">samcrane8@gmail.com</a>. Please prepend the subject of the email with [ICARUS BUG]. <br/><br/>
							You give us the bugs and we'll fix them; it's a win-win!
						</div>
					</v-flex>
				</v-layout>
			</v-layout>
		</v-card-title>
	</v-card>
</template>

<style>

</style>

<script>
import API from '../../mixins/API.js'

export default {
	mixins: [API],
	data() {
		return {
			
		}
	},
	methods: {
	},
	mounted() {
	}
}
</script>