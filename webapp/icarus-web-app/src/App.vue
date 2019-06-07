<template>
	<v-app id="inspire">
		<v-toolbar primary fixed :flat = "is_flat" :color="toolbar_color"
		>
			<v-toolbar-title style="margin-right:20px;">
				<router-link v-if="!logged_in" to="/" tag="span" style="cursor: pointer;color: white;font-weight:200;">
					<img src="static/GT_Logo.png" width="40px" style="padding-top:10px;"/>
				</router-link>
				<router-link v-if="logged_in" to="/homepage" tag="span" style="cursor: pointer;color: white;font-weight:200;">
					<img src="static/GT_Logo.png" width="40px" style="padding-top:10px;"/>
				</router-link>
			</v-toolbar-title>
			<v-toolbar-items class="hidden-xs-only">
				<v-btn
					flat
					v-for="item in menuItems"
					:key="item.title"
					:to="item.path">
					<span style="color:white;"> {{ item.title }} </span>
				</v-btn>
				<v-menu offset-y
				v-if="this.departments.length > 0 && logged_in">
					<v-btn
						flat
						slot="activator"
					>
						<span style="color:white;"> DEPARTMENT </span>
					</v-btn>
					<v-list>
						<v-list-tile
							v-for="(department, index) in departments"
							:key="index"
							@click="toDepartment(department)"
						>
							<v-list-tile-title>{{ department.name }}</v-list-tile-title>
						</v-list-tile>
					</v-list>
				</v-menu>
			</v-toolbar-items>
			<v-spacer></v-spacer>
      <v-menu offset-y v-if="logged_in"
      :close-on-content-click="false"
      v-model="notification_menu_open"
			absolute
			attach="inspire"
      style="z-index:9999;">
        <v-btn icon slot="activator" dark
        style="z-index:9999"
				id="notificationWindow"
        >
          <v-icon
          style="z-index:9999"
          :color="notification_color"
          >notification_important</v-icon>
        </v-btn>
        <v-list
				style="
				overflow:scroll;max-height:40vh;
				">
					<v-list-tile
          v-for="(notification, key) in notifications"
          :key="key"
          >
						<notification-li :data="notification"
						v-on:snackbar="_snackbar"
						v-on:update_notifications="get_notifications"/>
					</v-list-tile>
				</v-list>
        <v-flex
        class="text-xs-center"
        style="z-index:9999;background-color:#ffffff"
        >
          <v-btn
          flat
          color="primary"
          style="z-index:9999;background-color:#ffffff"
          @click="read_all_notifications">
            mark all as read
          </v-btn>
        </v-flex>
      </v-menu>
      <span
      style="color:white;
      font-weight:200;
      font-size:16px;"
      v-if="logged_in">
        ({{unread_notification_count}})
      </span>
			<v-menu bottom left v-if="logged_in">
				<v-btn icon slot="activator" dark>
					<v-icon>more_vert</v-icon>
				</v-btn>
				<v-list>
					<v-list-tile to="/settings">
						<v-list-tile-title> settings</v-list-tile-title>
					</v-list-tile>
					<v-list-tile @click="_logout()">
						<v-list-tile-title> sign out</v-list-tile-title>
					</v-list-tile>
				</v-list>
			</v-menu>
			<v-toolbar-items class="hidden-xs-and-down" v-if="!logged_in">
				<v-btn
				style="color:white;"
				flat
				to="/login"
				>
					<v-icon style="margin-right:5px">lock_outline</v-icon>
				Login</v-btn>
			</v-toolbar-items>
		</v-toolbar>
		<router-view v-on:login="login" v-on:snackbar="_snackbar" v-on:change-toolbar-color="change_toolbar_color"/>
		<v-snackbar
			:timeout="timeout"
			:top="y === 'top'"
			:bottom="y === 'bottom'"
			:right="x === 'right'"
			:left="x === 'left'"
			:multi-line="mode === 'multi-line'"
			:vertical="mode === 'vertical'"
			v-model="snackbar"
			color="white"
			class="hidden-xs-and-down"
		>
			<span style="color:black"> {{ text }} </span>
			<v-btn flat color="secondary" @click.native="snackbar = false">Close</v-btn>
		</v-snackbar>
	</v-app>
</template>

<script>
	import Vue from 'vue';
	import axios from 'axios'
	import VueAxios from 'vue-axios'
	import router from '@/router'
	import API from './mixins/API.js'
  import Vuetify from 'vuetify'
  import NotificationListItem from '@/components/NotificationListItem';

	Vue.use(VueAxios, axios)
	Vue.use(Vuetify, {
		theme: {
			primary: '#000000',
			secondary: '#E5B43D',
			accent: '#8c9eff',
			error: '#b71c1c'
		}
	})

	export default {
    mixins: [API],
    components: {
      'notification-li': NotificationListItem
    },
		data () {
			return {
				is_flat: true,
				toolbar_color: "primary",
				sidebar: false,
				logged_in: false,
				snackbar: false,
				mode: '',
				y: 'top',
				x: null,
				timeout: 6000,
				text: 'Clearance updated.',
				menuItems: [
					{ title: 'Flights', path: '/flights', icon: 'home'},
					{ title: 'New Flight', path: '/newflight', icon: 'lock'},
					{ title: 'Drones', path: '/drones', icon: 'lock'}
				],
				menuLoggedIn: [
					{ title: 'Flights', path: '/flights', icon: 'home'},
					{ title: 'New Flight', path: '/newflight', icon: 'lock'},
					{ title: 'Drones', path: '/drones', icon: 'lock'}
				],
				notLoggedIn: [

				],
				settings_menu: [
					'profile',
					'settings',
					'sign out'
        ],
        notifications: [

        ],
        notification_color: "white",
        unread_notification_count: 0,
				notification_menu_open: false,
				departments: [],
			}
		},
		methods: {
      async read_all_notifications() {
        this.notification_color = "white"
        this.unread_notification_count = 0

        const response = await this.read_all(
          this.$store.state.access_token
        );
				this.notification_menu_open = false
				await this.get_notifications()
      },
			change_toolbar_color(color) {
				this.toolbar_color = color
			},
			async login() {
				this.logged_in = true
				const is_gov_response = await this.is_government_official(
					this.$store.state.access_token
				)
				this.menuItems = this.menuLoggedIn
				await this.get_departments()
				await this.get_notifications()
			},
			async _logout() {
				const response = await this.logout(
					this.$store.state.access_token
				);
				if (response.status == 200) {
					this.logged_in = false
					this.menuItems = this.notLoggedIn
					router.push('/')
				}
      },
      async get_notifications() {
				if (!this.logged_in) {
					return;
				}

        var response = await this.unread_count(
          this.$store.state.access_token
        );
        this.unread_notification_count = response.data.unread_count
        if (response.status == 200) {
          if (response.data.unread_count > 0) {
            this.notification_color = "secondary"
          } else {
            this.notification_color = "white"
          }
        }

        response = await this.notification_feed(
          this.$store.state.access_token, 7
        );
        if (response.status == 200) {
          this.notifications = response.data
        }
      },
			_snackbar(timeout,text) {
				this.timeout = timeout
				this.text = text
				this.snackbar = true
			},
			async get_departments() {
				const response = await this.get_user_departments(
					this.$store.state.access_token
				);
				if (response.status == 200){
					this.departments = response.data
				}
			},
			toDepartment(department) {
				router.push(`/dashboard?id=${department.id}`)
			}
		},
		async mounted() {
			const response = await this.isLoggedIn(
				this.$store.state.access_token
			);
			if (JSON.stringify(response.data) == 'true') {
				const is_gov_response = await this.is_government_official(
					this.$store.state.access_token
				)
				this.logged_in = true
        this.toolbar_color = 'primary'
        await this.get_notifications()
			} else {
				this.logged_in = false
				this.menuItems = this.notLoggedIn
				this.toolbar_color = 'transparent'
			}
			await this.get_departments()
      setInterval(function () {
        if (this.logged_in) {
          this.get_notifications()
        }
      }.bind(this), 5000)
		}
	}
</script>

<style lang="stylus">
	@import './stylus/main'

	@require '../../node_modules/vuetify/src/stylus/settings/_colors'
	@import url("https://fonts.googleapis.com/css?family=Barlow")
	@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500');


	$theme := {
		primary: $red.darken-2
		accent: $red.accent-2
		secondary: $grey.lighten-1
		info: $blue.lighten-1
		warning: $amber.darken-2
		error: $red.accent-4
		success: $green.lighten-2
	}

	body {
		margin: 0;
		font-family: 'Roboto', sans-serif;
	}

</style>
