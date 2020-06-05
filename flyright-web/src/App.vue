<template>
    <v-app id="app">
        <!-- Navigation Bar -->
        <div>
            <template>
                <v-app-bar color="primary" dark dense flat>
                    <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
                    <v-toolbar-title>Flyright</v-toolbar-title>
                </v-app-bar>

                <v-navigation-drawer absolute temporary v-model="drawer">
                    <v-list dense nav>
                        <v-list-item-group v-model="group">
                            <v-list-item>
                                <v-list-item-icon>
                                    <v-icon>mdi-home</v-icon>
                                </v-list-item-icon>
                                <v-spacer></v-spacer>
                                <v-list-item-title>Flights</v-list-item-title>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-icon>
                                    <v-icon>mdi-new-box</v-icon>
                                </v-list-item-icon>
                                <v-spacer></v-spacer>
                                <v-list-item-title>New Flight</v-list-item-title>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-icon>
                                    <v-icon>mdi-drone</v-icon>
                                </v-list-item-icon>
                                <v-spacer></v-spacer>
                                <v-list-item-title>Drones</v-list-item-title>
                            </v-list-item>
                            <v-list-item v-if="">
                                <v-list-item-icon>
                                    <v-icon>mdi-view-dashboard</v-icon>
                                </v-list-item-icon>
                                <v-spacer></v-spacer>
                                <v-list-item-title>Dashboard</v-list-item-title>
                            </v-list-item>


                        </v-list-item-group>
                    </v-list>
                </v-navigation-drawer>
            </template>
        </div>

        <!-- actual content lives in router-view -->
        <v-content>
            <v-container :style="{'background-image': 'url(' + require('./assets/background.png') + ')'}" fill-height fluid ma-0
                         pa-0>
                <router-view></router-view>
            </v-container>
        </v-content>

    </v-app>
</template>

<script>
  export default {
    name: 'App',
    data: () => ({
      drawer: false,
      logged_in: false,
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

    })
  }
</script>


<style>



    #app {
        font-family: Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    html {
        overflow-y: hidden !important;
    }
</style>
