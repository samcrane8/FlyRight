<template>
  <div>
    <v-layout class="background_drone">
      <v-flex xs4>
        <drone-sidebar
        v-on:register_drone="registerDrone"
        />
      </v-flex>
      <v-flex xs8>
        <drones-table
        :drones="items"
        v-on:delete_drones="deleteDrone"
        v-on:update_drone="updateDrone"/>
      </v-flex>
    </v-layout>
    <icarus-footer/>
  </div>
</template>


<script>

import Vue from 'vue';
import Vuetify from 'vuetify'
import router from '@/router'
import API from '@/mixins/API.js'
import DronesTable from './DronesTable'
import DroneSidebar from './DroneSidebar'
import Footer from '@/components/Footer'

export default {
  name: 'Login',
  mixins: [API],
  components: {
    'drones-table': DronesTable,
    'drone-sidebar': DroneSidebar,
    'icarus-footer': Footer
  },
  data () {
    return {
      max25chars: (v) => v.length <= 25 || 'Input too long!',
      tmp: '',
      pagination: {},
      items: [],

      text: 'Drone Succesfully Added!',
      text2: 'Drone Successfully Removed!',

      drone_id: null,
      validADD: false

    }
  },
  methods: {
    async getUserDrones() {
      const response = await this.get_user_drones(this.$store.state.access_token)
      this.drone_data = response.data
      this.items = []
      for(var i=0; i<this.drone_data.length; i++) {
        this.items.push(this.drone_data[i])
      }
    },
    async registerDrone(registration_info) {
      if (registration_info.faa_registration_number == null) {
        registration_info.faa_registration_number = "unregistered"
      }
      if (registration_info.description == null) {
        registration_info.description = "No description added"
      }
      const response = await this.register_drone(registration_info.faa_registration_number, registration_info.description,
      registration_info.manufacturer, registration_info.type,
      registration_info.color, registration_info.name,
        this.$store.state.access_token
      );
      if (response.status == 200) {
          this.drone_id = true;
          this.$emit('snackbar',6000, 'Drone Registered Successfully');
          this.getUserDrones();
        } else if (response.status == 400) {
          throw error;
        }
    },
    toggleAll () {
      if (this.selected.length) this.selected = []
      else this.selected = this.items.slice()
    },
    changeSort (column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = column
        this.pagination.descending = false
      }
    },
    async deleteDrone(selected) {
      var response = await this.delete_drone(selected, this.$store.state.access_token);
      if (response.status == 200) {
        //this.snackbar2 = true;
        this.$emit('snackbar',6000, 'Drone Removed Successfully');
        this.getUserDrones();
        this.selected = [];
      } else if (response.data['code'] == 31) {
        throw error;
      }
    },
    async updateDrone(drone_changes) {
      var response = await this.edit_drone_details(drone_changes,this.$store.state.access_token)
      if (response.status == 200) {
        //this.snackbar2 = true;
        this.$emit('snackbar',6000, 'Drone Updated Successfully');
        this.getUserDrones();
      } else if (response.data['code'] == 31) {
        throw error;
      }
    }
  },
  mounted () {
    this.getUserDrones();
  }
}

</script>

<!-- styling for the component -->
<style>
.background_drone {
  background-image: none;
  background-color: #F0F0F0;
}
#drone_ADD {
  margin-top: 80px; 
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 10px;
}
#drone_TABLE {
  margin-top: 80px;
  margin-bottom: 10px;
  margin-right: 20px;
}
#testing {
  margin-top: 70px;
}
</style>

