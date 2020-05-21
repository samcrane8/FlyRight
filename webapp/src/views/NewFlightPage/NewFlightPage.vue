<template>
  <v-layout style="width:100vw;height:90vh;margin-top:10vh;" fixed @click="showDeleteMenu">
    <newflight-toolbar
    style="
      overflow: scroll;
      height:90vh;
      padding:2px;
      z-index:1;
    "
    v-on:submit_flight="isFilledOut"
    />

    <newflight-map
    style="width:70vw;
    z-index:0;"
    v-if="departments"
    :departments="departments"
    v-model="area"/>

    <v-dialog v-model="show" max-width="500px">
      <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Tips for selecting a Flight Area:</h3>
          <div>
            <br>
            <ul style="list-style-position: inside; margin-left: 25%;">
              <li> Fly below 400 ft. </li>
              <li> Fly within visual line-of-sight </li>
              <li> Fly in clear weather conditions </li>
              <li> Fly over green spaces and not over traffic </li>
              <li> Fly where there are no people under you </li>
              <li> Fly during the day </li>
              <li> Never fly near other aircrafts </li>
            </ul>
          </div>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" flat @click.stop="show=false">Close</v-btn>
      </v-card-actions>
    </v-card>
    </v-dialog>

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
              of adhering to all FAA regulations and community-based safety guidelines. The Georgia Tech Police Department Campus Drone
              Management System is NOT currently integrated with the FAA. You, the Pilot, are responsible for
              contacting any local airport/heliport Air Traffic Control towers in order to comply with
              FAA requirements.”</p>
          <h4 class="headline mb-1">By Clicking 'Accept', you agree to abide by all FAA regulations.</h4>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn color="secondary" flat @click.stop="submitFlight()">Accept</v-btn>
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
  import SchedulingRuleAPI from '@/mixins/SchedulingRuleAPI.js'
  import moment from 'moment'
  import router from '@/router';
  import NewFlightToolbar from './NewFlightToolbar';
  import NewFlightMap from './NewFlightMap'

  export default {
    name: 'NewFlightsPage',
    mixins: [API, SchedulingRuleAPI],
    components: {
      'newflight-toolbar': NewFlightToolbar,
      'newflight-map': NewFlightMap
    },
    data: function data() {
      return {
        flight: {},
        scheduling: {},
        show: false,
        alertMissingCriteria: false,
        alertMissingMessage: [],
        disclaimerDialog: false,
        deleteMenu: false,
        area:[],
        departments: null,
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
        if (flight.selectedType == '' || flight.selectedType == null) {
          isComplete = false
          this.alertMissingMessage += 'Set a type,'
        }
        if (this.area.length < 3) {
          isComplete = false;
          this.alertMissingMessage += 'Set a flight area (click the pen button on the far right to set points on the map),'
        }
        var startTime = new Date(this.flight.starts_at)
        var endTime = new Date(this.flight.ends_at)
        var duration = endTime - startTime
        startTime = startTime.getHours() + ":" + startTime.getMinutes()
        endTime = endTime.getHours() + ":" + endTime.getMinutes()
        if (startTime == endTime) {
          isComplete = false;
          this.alertMissingMessage += 'The start time and date time cannot be the same time,'
        }
        //if the flight is longer than 12 hours
        if (duration > (1000*60*60*12)) {
          isComplete = false;
          this.alertMissingMessage += 'The flight time is too long. Please check the time again,'
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
      async submitFlight() {
        var geoJ = this.makeGeoJson();
        var response = await this.register_mission(
          this.flight.title,
          geoJ,
          this.flight.description,
          this.flight.starts_at,
          this.flight.ends_at,
          this.flight.selectedType,
          this.$store.state.access_token
        );
        if (response['status'] == 200) {
          this.$emit('snackbar',6000, 'Flight Successfully Saved');

          this.flight.added_drones.forEach(async x => {
            var resp = await this.add_drone_to_mission(
              x.id, response.data.id, 'CURRENT_USER',
              this.$store.state.access_token
            );
          })
          this.scheduling['flight_id'] = response.data.id
          if (this.scheduling['frequency'] != "Does Not Repeat"){
            var scheduling_response = await this.register_scheduling_rule(
              this.$store.state.access_token,
              this.scheduling
            )
          }
          router.push(`/flightdetails?id=${response.data.id}`)
        }
      },
      leaving () {
        document.body.style.cursor= 'default';
      }
    },
    async mounted() {
      const response = await this.get_departments(
        this.$store.state.access_token
      )
      if (response.status == 200) {
        this.departments = response.data
      }
    }
  };
</script>
