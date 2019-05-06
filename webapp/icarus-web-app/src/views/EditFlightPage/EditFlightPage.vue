<template>
  <v-layout style="width:100vw;height:90vh;margin-top:10vh;" fixed @click="showDeleteMenu">
    <newflight-toolbar
    style="
      overflow: scroll;
      height:90vh;
      padding:2px;
      z-index:1;
    "
    v-if="flight && available_drones && added_drones"
    :data="flight"
    :available_drone_data="available_drones"
    :added_drone_data="added_drones"
    v-on:submit_flight="isFilledOut"
    />

    <newflight-map
    style="width:70vw;
    z-index:0;"
    v-if="flight"
    v-on:new_area="update_area"
    v-model="flight"/>

    <v-dialog v-model="alertMissingCriteria" max-width="500px">
      <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Flight Did Not Save</h3>
          <h4>Please Make Sure the Following Items are Filled Out:</h4>
          <div>
            <br>
            <ul style="list-style-position: inside; margin-left: 25%;">
              <li v-for= "(message,index) in alertMissingMessage"
              :key="index"
              >
                {{message}}
              </li>
            </ul>
          </div>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" flat @click.stop="alertMissingCriteria=false">Close</v-btn>
      </v-card-actions>
    </v-card>
    </v-dialog>

    <v-dialog v-model="disclaimerDialog" max-width="500px">
      <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-1">DISCLAIMER</h3>
          <p>“Please note, filing a Flight Plan with GTPD does NOT relieve the Pilot of the responsibility
              of adhering to all FAA regulations and community-based safety guidelines. The ICARUS Campus Drone 
              Management System is NOT currently integrated with the FAA. You, the Pilot, are responsible for 
              contacting any local airport/heliport Air Traffic Control towers in order to comply with
              FAA requirements.”</p>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn color="secondary" flat @click.stop="updateFlight()">Accept</v-btn>
        <v-btn color="primary" flat @click.stop="disclaimerDialog = false">Decline</v-btn>
      </v-card-actions>
    </v-card>
    </v-dialog>
  </v-layout>
</template>

<style>
  .map-panel {
    height:100%;
    width:100%;
  }
  .btn-toggle {
    flex-direction: column;
  }
</style>

<script>
  import Vue from 'vue';
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import API from '@/mixins/API.js'
  import SchedulingRuleAPI from '@/mixins/SchedulingRuleAPI'
  import moment from 'moment'
  import router from '@/router';
  import EditFlightToolbar from './EditFlightToolbar';
  import FlightMap from './EditFlightMap'

  export default {
    name: 'EditFlightPage',
    mixins: [API, SchedulingRuleAPI],
    components: {
      'newflight-toolbar': EditFlightToolbar,
      'newflight-map': FlightMap
    },
    data: function data() {
      return {
        flight: null,
        scheduling: {},
        available_drones: null,
        added_drones: null,
        old_mission_drones: null,
        show: false,
        alertMissingCriteria: false,
        alertMissingMessage: [],
        disclaimerDialog: false,
        deleteMenu: false,
        area:[]
      };
    },
    methods: {
      showDeleteMenu (e) {
        if(this.deleteable) {
          if (this.clickedOnPoly) {
            if (this.selectedPolyline != null) {
                this.deleteMenu = false
                this.x = e.clientX
                this.y = e.clientY
                this.$nextTick(() => {
                  this.deleteMenu = true
                })
            } else {
              if(this.selectedPolygon != null) {
                this.deleteMenu = false
                this.x = e.clientX
                this.y = e.clientY
                this.$nextTick(() => {
                  this.deleteMenu = true
                })
              }
            }
          }  else {
            if(this.selectedPolygon != null) {
              this.unselectPolygon();
            }
          }
        }
        this.clickedOnPoly = false;
      },
      saveDate (date) {
        this.$refs.menuDate.save(date)
      },
      makeGeoJson: function() {
        var gJson = {
              "type": "FeatureCollection",
              "features": []
            };
        var temp = {
              "type": "Feature",
              "geometry":{
                "type": "Polygon", 
                "coordinates": []
              },
              "properties":{}
            }
        temp.geometry.coordinates = this.area;
        gJson.features.push(temp);
        return gJson;
      },
      checkCriteria(flight) {
        this.alertMissingMessage = []
        var isComplete = true
        if (flight.added_drones.length == 0){
          isComplete = false
          this.alertMissingMessage +="Add at least one drone,"
        }
        if (flight.title == '' || flight.title == null) {
          isComplete = false
          this.alertMissingMessage += "Set a title,"
        }

        if (moment(flight.ends_at).isBefore(flight.starts_at)) {
          isComplete = false
          this.alertMissingMessage += "End time is before start time,"
        }

        if (flight.description === '' || flight.description === null) {
          isComplete = false
          this.alertMissingMessage += 'Set a description,'
        }
        if (flight.type == '' || flight.type == null) {
          isComplete = false
          this.alertMissingMessage += 'Set a type,'
        }
        if (this.area.length < 3) {
          isComplete = false;
          this.alertMissingMessage += 'Set a flight area (click the pen button on the far right to set points on the map),'
        }
        if (!isComplete) {
          this.alertMissingMessage = this.alertMissingMessage.slice(0,-1).split(',')
        }
        this.alertMissingCriteria = !isComplete;
        return isComplete;
      },
      isFilledOut(flight_plan) {
        this.flight = flight_plan.flight;
        this.scheduling = flight_plan.scheduling;
        if (this.checkCriteria(this.flight)) {
          this.disclaimerDialog = true
        }
      },
      async updateFlight() {
        var area = this.makeGeoJson();
        var details = {
          mission_id: this.flight.id,
          starts_at: this.flight.starts_at,
          ends_at: this.flight.ends_at,
          title: this.flight.title,
          description: this.flight.description,
          type: this.flight.type,
          area
        }
        var response = await this.edit_mission_details(
          details,
          this.$store.state.access_token,
        );
        if (response['status'] == 200) {

          this.flight.added_drones.forEach(async added_drone => {
            var drone_already_added = false
            this.old_mission_drones.forEach(async old_drone => {
              if (old_drone === added_drone) {
                drone_already_added = true
              }
            })
            if (!drone_already_added) {
              var resp = await this.add_drone_to_mission(
              added_drone.id, this.flight.id, 'CURRENT_USER',
              this.$store.state.access_token
            );
            }
          })

          this.old_mission_drones.forEach(async old_drone => {
            var drone_should_be_removed = true
            this.flight.added_drones.forEach(async added_drone => {
              if (old_drone === added_drone) {
                drone_should_be_removed = false
              }
            })

            if (drone_should_be_removed) {
              var resp = await this.remove_drone_from_mission(
                old_drone.id, this.flight.id,
                this.$store.state.access_token
              );
            }
          })
          this.scheduling['flight_id'] = this.flight.id
          if (this.scheduling['frequency'] != "Does Not Repeat"){
            var scheduling_response = await this.edit_scheduling_rule(
              this.$store.state.access_token,
              this.scheduling
            )
          } else {
            try {
            var scheduling_response = await this.delete_scheduling_rule(
              this.$store.state.access_token,
              this.flight.id
            )
            } catch(error) {
              
            }
          }
          this.$emit('snackbar',6000, 'Flight Successfully Saved');
          router.push(`/flightdetails?id=${this.flight.id}`)
        }
      },
      update_area(new_area) {
        this.area = new_area
      },
      leaving () {
        document.body.style.cursor= 'default';
      },
      async get_added_drones() {
        var response = await this.get_mission_drones(
          this.flight.id,
          this.$store.state.access_token
        )
        return response.data
      },
      async get_available_drones() {
        var response = await this.get_user_drones(
          this.$store.state.access_token
        );
        return response.data
      },
      async fetch_mission_info() {
        const response = await this.get_mission_info(
          this.mission_id,
          this.$store.state.access_token
        );
        if (response.status == 200) {
          this.flight = response.data
          this.added_drones = await this.get_added_drones()
          this.old_mission_drones = this.added_drones
          this.available_drones = await this.get_available_drones()
        }
      }
    },
    async mounted() {
      this.mission_id = this.$route.query.id
      await this.fetch_mission_info();
    }
  };
</script>