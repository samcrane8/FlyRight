<template>
  <v-card
  style="margin:10px;">
    <v-tabs>
      <v-toolbar flat>
        <v-toolbar-title> <span style="font-size:25px;font-weight:200;margin-right:10px;"> INFO </span> </v-toolbar-title>
        <v-icon v-if="_state(flight.clearance) == 'RECOMMEND AGAINST FLIGHT'" right color="red">block</v-icon>
        <v-icon v-if="_state(flight.clearance) == 'CAUTION'" right color="yellow">error</v-icon>
        <v-icon v-if="_state(flight.clearance) == 'NOTIFICATION RECEIVED'" right color="green">check_circle</v-icon>
        <v-icon v-if="_state(flight.clearance) == 'PENDING'" right >radio_button_unchecked</v-icon>
        <v-spacer/>
        <v-toolbar-items>
          <v-tooltip left>
            <v-btn flat slot="activator" icon @click="edit_flight(flight.id)" :disabled="!can_delete(flight.created_by)">
              <v-icon> edit </v-icon>
            </v-btn>
            <span>Edit Flight</span>
          </v-tooltip>
          <v-tooltip>
            <v-btn flat slot="activator" @click="delete_dialog=true" icon :disabled="!can_delete(flight.created_by)">
              <v-icon> delete </v-icon>
            </v-btn>
            <span>Delete Flight</span>
          </v-tooltip>
        </v-toolbar-items>
      </v-toolbar>
      <v-tabs-bar>
        <v-tabs-slider color="primary"></v-tabs-slider>
        <v-tabs-item
          href="tab-details"
        >
            Flight Details
        </v-tabs-item>
        <v-tabs-item
          href="tab-description"
        >
          Description
        </v-tabs-item>
        <v-tabs-item
          href="tab-commander-info"
        >
          Commander Info
        </v-tabs-item>
        <v-tabs-item
          href="tab-clearance"
        >
          Clearance
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-items>
        <v-tabs-content
          id="tab-details"
        >
          <v-card flat>
            <v-card-text>
              <v-layout column>
                <v-layout row>
                  <v-layout column>
                    <v-layout row style="margin-top:10px;">
                      <v-flex>
                        <h4>Start Date/Time:</h4> <span>{{flight.starts_at | datetime_filter}}</span>
                      </v-flex>
                      <v-flex>
                        <h4>End Date/Time: </h4> <span>{{flight.ends_at | datetime_filter}}</span>
                      </v-flex>
                    </v-layout>
                    <v-layout row>
                      <v-flex>
                        <h4>Type: </h4><span>{{flight.type}}</span>
                      </v-flex>
                      <v-flex>
                        <h4>Number of Drones: </h4><span>{{flight.num_drones}}</span>
                      </v-flex>
                    </v-layout>
                    <v-layout row
                      v-if="flight.scheduling">
                        <v-flex>
                          <h4>Frequency: </h4><span>{{flight.scheduling.frequency}}</span><br>
                          <span v-for="(day, index) in flight.scheduling.parameters.days"
                          :key="index"> {{day}} </span>
                        </v-flex>
                        <v-flex>
                          <h4>Ends At: </h4><span>{{flight.scheduling.ends_at | datetime_filter}}</span>
                        </v-flex>
                      </v-layout>
                  </v-layout>
                </v-layout>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-tabs-content>
        <v-tabs-content
            id="tab-clearance"
          >
            <v-card flat>
            <v-card-text>
              <v-layout column>
                <v-layout row v-if="flight.can_edit_clearance" >
                  <select v-model="selected">
                    <option 
                      v-for="presetClearance in presetClearances" 
                      :value="presetClearance.value"
                      :key="presetClearance.text">
                        {{ presetClearance.text }}
                    </option>
                  </select>
                  <v-flex style="margin-top:5px;">
                    <v-text-field 
                      v-if="selected" 
                      label="Write a short message to the commander to explain how you're setting the status."
                      multi-line
                      rows="3"
                      :value="selected"
                      v-model="clearance.message"
                    >
                    </v-text-field>  
                    <v-text-field 
                      v-else 
                      label="Write a short message to the commander to explain how you're setting the status."
                      multi-line
                      rows="3"
                      :value="flight.clearance.message"
                      v-model="clearance.message"
                    >
                    </v-text-field>
                  </v-flex>
                  <v-select
                    :items="clearance_states"
                    v-model="clearance.state"
                    label="Set Clearance"
                    single-line
                    bottom
                  ></v-select>
                </v-layout>
                <v-layout row v-if="!flight.can_edit_clearance" >
                  <v-flex style="margin-top:5px;">
                    <h4>Message:</h4>
                    <span 
                      style="margin-top:10px;
                      height:80px;
                      overflow:scroll;"
                      v-if="flight.clearance.message!=null"
                    >
                      {{flight.clearance.message}}
                    </span>
                    <span 
                      style="margin-top:10px;
                      height:80px;
                      overflow:scroll;"
                      v-else-if="message==null"
                    >
                      No message currently
                    </span>
                  </v-flex>
                  <v-flex style="margin-top:5px;">
                    <h4>Clearance:</h4>
                    <span 
                      style="margin-top:10px;
                      height:80px;
                      overflow:scroll;"
                    >
                      {{flight.clearance.state}}
                    </span>
                  </v-flex>
                </v-layout>
                <v-btn v-if="is_gov_official" @click="update_clearance"
                :disabled="clearance.currState===''" flat>Save Clearance</v-btn>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-tabs-content>
        <v-tabs-content
          id="tab-commander-info"
        >
          <commander-info :created_by="flight.created_by" :commander_name="flight.commander_id"/>
        </v-tabs-content>
        <v-tabs-content
          id="tab-description"
        >
          <description-tab :description="flight.description" />
        </v-tabs-content>
      </v-tabs-items>
    </v-tabs>

    <v-dialog
      v-model="delete_dialog"
      width="500">
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Delete Flight
        </v-card-title>

        <v-card-text>
          The flight will be deleted and can not be restored. Are you sure you want to do this?
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="deleteFlight(flight.id)"
          >
            Yes
          </v-btn>
          <v-btn
            color="secondary"
            flat
            @click="delete_dialog = false"
          >
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
  import moment from 'moment'
  import API from '@/mixins/API.js'
  import router from '@/router'
  import DescriptionTab from '@/views/FlightsPage/FlightTable/DescriptionTab';
  import CommanderInfo from '@/views/FlightsPage/FlightTable/CommanderInfo';

  export default {
    name:'flight-details-info',
    components: {
      DescriptionTab,
      CommanderInfo
    },
    data() {
      return {
        delete_dialog: false,
        clearance: {
          message: '',
          state: ''
        },
        clearance_states: ['RECOMMEND AGAINST FLIGHT', 'NOTIFICATION RECEIVED', 'CAUTION'],
        selected: '',
        presetClearances: [
        { text: 'Preset Message', value: '' },

        { text: 'CLEAR FLIGHT', 
          value: user_info.first_name + ", \n You're all set! The Georgia Tech Police Department Watch " +
          "Commanders and Dispatchers have been notified about your intended flight. " +
          "\n Please note, filing a flight plan with the Georgia Tech Police Department " +
          "does not alleviate you of the responsibility of adhering to all FAA regulations " + 
          "and safety recommendations.As always, if you experience any problems during " +
          "your flight, please immediately call the GTPD at 404-894-2500. \n Fly safe!" },

        { text: 'ANOTHER FLIGHT', 
          value: user_info.first_name + ", \n Please exercise additional caution during your flight, as " +
          "another UAS pilot has filed a flight plan with an overlapping time frame " +
          "in the same location. \n Please note, filing a flight plan with the Georgia " +
          "Tech Police Department does not alleviate you of the responsibility of adhering " +
          "to all FAA regulations and safety recommendations. In the unlikely event that " +
          "you experience any problems during your flight, please immediately call the " +
          "GTPD at 404-894-2500. \n Fly safe!" },

        { text: 'CIVIC TWILIGHT WARNING', 
          value: user_info.first_name + ", \n Please exercise additional caution during your " +
          "flight. You may not fly a small unmanned aircraft system before sunrise civil twilight, " +
          "nor after sunset civil twilight time. Civil twilight is defined as 30 minutes before " +
          "sunrise and 30 minutes after sunset. \n Please note, filing a flight plan with the Georgia " +
          "Tech Police Department does not alleviate you of the responsibility of adhering " +
          "to all FAA regulations and safety recommendations. In the unlikely event " +
          "that you experience any problems during your flight, please immediately " +
          "call the GTPD at 404-894-2500. \n Fly safe!" },

        { text: 'NIGHT FLYING', 
          value: user_info.first_name + ", \n It is NOT advised to fly at the current time, " +
          "as the proposed time of your flight at night. The FAA prohibits the operation of " +
          "small unmanned aircraft systems at night without either a Certificate of " +
          "Authorization or Waiver. Filing a flight plan with the Georgia Tech Police " +
          "Department does not alleviate you of the responsibility of adhering to all FAA " +
          "regulations and safety recommendations.  Please reschedule your flight to comply " +
          "with FAA regulations." }
        ]
      }
    },
    props: {
      flight: {
        type: Object,
        default() {
          return { message: 'hello' }
        }
      },
      user_info: {
        type: Object,
        default() {
          return { message: 'hello' }
        }
      },
      is_gov_official: {
        type: Boolean,
        default() {
          return false;
        }
      }
    },
    methods: {
      _state(clearance) {
				if (clearance == null){
					return false
				}
				return clearance["state"]
      },
      edit_flight(id){
        router.push('/editflight?id='+id)
      },
      can_delete(id){
				return this.user_info.user.id == id
      },
      async deleteMission(mission_id) {
        this.$emit('delete_mission', mission_id)
        this.delete_dialog=false
      },
      update_clearance() {
        this.$emit('update_clearance', this.clearance)
      }
    },
    filters: {
  		date_filter: function (date) {
    		return moment(date).format('MMMM Do, YYYY');
			},
			datetime_filter: function (date) {
    		return moment(date).format('MMMM Do YYYY, h:mm a');
			}
		}
  }
</script>

<style>

</style>
