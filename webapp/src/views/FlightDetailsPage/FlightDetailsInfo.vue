<template>
  <div>
    <v-card
      style="margin:10px;">
      <div>
        <v-toolbar color="primary" dark tabs>
          <v-icon color="red" right v-if="_state(flight.clearance) == 'RECOMMEND AGAINST FLIGHT'">block</v-icon>
          <v-icon color="yellow" right v-if="_state(flight.clearance) == 'CAUTION'">error</v-icon>
          <v-icon color="secondary" right v-if="_state(flight.clearance) == 'NOTIFICATION RECEIVED'">check_circle
          </v-icon>
          <v-icon right v-if="_state(flight.clearance) == 'PENDING'">radio_button_unchecked</v-icon>
          <v-toolbar-title>FLIGHT INFORMATION</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn @click="edit_flight(flight.id)" icon>
            <v-icon>edit</v-icon>
          </v-btn>
          <v-btn @click="delete_dialog=true" icon>
            <v-icon>delete</v-icon>
          </v-btn>



        <v-tabs
          slot="extension"
          v-model="model"
          centered
          color="primary"
          slider-color="secondary"
        >
          <v-tab
            v-for="tab in tabs"
            :key="tab.id"
            :href="`#${tab.id}`"
          >
            {{ tab.title }}
          </v-tab>
        </v-tabs>
        </v-toolbar>
        <v-tabs-items v-model="model">
          <v-tab-item :id="`flight-details`">


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
                      <v-layout row v-if="flight.scheduling">
                        <v-flex>
                          <h4>Frequency: </h4><span>{{flight.scheduling.frequency}}</span><br>
                          <span :key="index"
                                v-for="(day, index) in flight.scheduling.parameters.days"> {{day}} </span>
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



          </v-tab-item>
          <v-tab-item :id="`description`">
            <description-tab :description="flight.description"/>
          </v-tab-item>
          <v-tab-item :id="`commander`">

            <commander-info :commander_name="flight.commander_id" :created_by="flight.created_by"/>

          </v-tab-item>
          <v-tab-item :id="`clearance`">


            <v-card flat>
              <v-card-text>
                <v-layout column>
                  <v-layout row v-if="flight.can_edit_clearance">
                    <v-flex style="margin-top:5px;">
                      <v-text-field
                        label="Write a short message to the commander to explain how you're setting the status."
                        multi-line
                        rows="3"
                        v-if="selected"
                        v-model="selected"
                      >
                      </v-text-field>
                      <v-text-field
                        label="Write a short message to the commander to explain how you're setting the status."
                        multi-line
                        rows="3"
                        v-else
                        v-model="flight.clearance.message"
                      >
                      </v-text-field>
                    </v-flex>
                    <v-layout column>
                      <select
                        style="border:1px solid gray;
                      border-radius:2px;"
                        v-model="selected"
                      >
                        <option
                          :key="presetClearance.text"
                          :value="presetClearance.value"
                          v-for="presetClearance in presetClearances">
                          {{ presetClearance.text }}
                        </option>
                      </select>
                      <v-select
                        :items="clearance_states"
                        bottom
                        label="Set Clearance"
                        single-line
                        v-model="clearance.state"
                      ></v-select>
                    </v-layout>

                  </v-layout>
                  <v-layout row v-if="!flight.can_edit_clearance">
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
                  <v-btn :disabled="clearance.currState===''" @click="update_clearance"
                         flat v-if="is_gov_official">Save Clearance
                  </v-btn>
                </v-layout>
              </v-card-text>
            </v-card>



          </v-tab-item>
        </v-tabs-items>

      </div>
    </v-card>

    <v-card
      style="margin:10px;">
      <v-tabs>
        <v-toolbar flat>
          <v-toolbar-title><span style="font-size:25px;font-weight:200;margin-right:10px;"> INFO </span>
          </v-toolbar-title>
          <v-icon color="red" right v-if="_state(flight.clearance) == 'RECOMMEND AGAINST FLIGHT'">block</v-icon>
          <v-icon color="yellow" right v-if="_state(flight.clearance) == 'CAUTION'">error</v-icon>
          <v-icon color="green" right v-if="_state(flight.clearance) == 'NOTIFICATION RECEIVED'">check_circle</v-icon>
          <v-icon right v-if="_state(flight.clearance) == 'PENDING'">radio_button_unchecked</v-icon>
          <v-spacer/>


          <v-toolbar-items>
            <v-tooltip left>
              <v-btn :disabled="!can_delete(flight.created_by)" @click="edit_flight(flight.id)" flat icon
                     slot="activator">
                <v-icon> edit</v-icon>
              </v-btn>
              <span>Edit Flight</span>
            </v-tooltip>
            <v-tooltip>
              <v-btn :disabled="!can_delete(flight.created_by)" @click="delete_dialog=true" flat icon slot="activator">
                <v-icon> delete</v-icon>
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

          </v-tabs-content>
          <v-tabs-content
            id="tab-clearance"
          >
            <v-card flat>
              <v-card-text>
                <v-layout column>
                  <v-layout row v-if="flight.can_edit_clearance">
                    <v-flex style="margin-top:5px;">
                      <v-text-field
                        label="Write a short message to the commander to explain how you're setting the status."
                        multi-line
                        rows="3"
                        v-if="selected"
                        v-model="selected"
                      >
                      </v-text-field>
                      <v-text-field
                        label="Write a short message to the commander to explain how you're setting the status."
                        multi-line
                        rows="3"
                        v-else
                        v-model="flight.clearance.message"
                      >
                      </v-text-field>
                    </v-flex>
                    <v-layout column>
                      <select
                        style="border:1px solid gray;
                      border-radius:2px;"
                        v-model="selected"
                      >
                        <option
                          :key="presetClearance.text"
                          :value="presetClearance.value"
                          v-for="presetClearance in presetClearances">
                          {{ presetClearance.text }}
                        </option>
                      </select>
                      <v-select
                        :items="clearance_states"
                        bottom
                        label="Set Clearance"
                        single-line
                        v-model="clearance.state"
                      ></v-select>
                    </v-layout>

                  </v-layout>
                  <v-layout row v-if="!flight.can_edit_clearance">
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
                  <v-btn :disabled="clearance.currState===''" @click="update_clearance"
                         flat v-if="is_gov_official">Save Clearance
                  </v-btn>
                </v-layout>
              </v-card-text>
            </v-card>
          </v-tabs-content>
          <v-tabs-content
            id="tab-commander-info"
          >

          </v-tabs-content>
          <v-tabs-content
            id="tab-description"
          >

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
              @click="deleteFlight(flight.id)"
              color="primary"
              flat
            >
              Yes
            </v-btn>
            <v-btn
              @click="delete_dialog = false"

              color="secondary"
            >
              No
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </div>
</template>

<script>
  import moment from 'moment'
  import router from '@/router'
  import DescriptionTab from '@/views/FlightsPage/FlightTable/DescriptionTab'
  import CommanderInfo from '@/views/FlightsPage/FlightTable/CommanderInfo'

  export default {
    name: 'flight-details-info',
    components: {
      DescriptionTab,
      CommanderInfo
    },
    data () {
      return {
        model: 'tab-2',
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        tabs: [
          {title: 'Flight Details', id: 'flight-details'},
          {title: 'Description', id: 'description'},
          {title: 'Commander Info', id: 'commander'},
          {title: 'Clearance', id: 'clearance'},
        ],
        active: null,
        delete_dialog: false,
        clearance: {
          message: '',
          state: ''
        },
        clearance_states: ['RECOMMEND AGAINST FLIGHT', 'NOTIFICATION RECEIVED', 'CAUTION'],
        selected: '',
        presetClearances: [
          { text: 'Preset Message', value: '' }
        ]
      }
    },
    props: {
      flight: {
        type: Object,
        default () {
          return { message: 'hello' }
        }
      },
      user_info: {
        type: Object,
        default () {
          return { message: 'hello' }
        }
      },
      is_gov_official: {
        type: Boolean,
        default () {
          return false
        }
      },
      department_info: {
        type: Object,
        default () {
          return { message: 'hello' }
        }
      },
      department_name: String
    },
    methods: {
      next () {
        const active = parseInt(this.active)
        this.active = (active < 2 ? active + 1 : 0)
      },
      _state (clearance) {
        if (clearance == null) {
          return false
        }
        return clearance['state']
      },
      edit_flight (id) {
        router.push('/editflight?id=' + id)
      },
      can_delete (id) {
        return this.user_info.user.id == id
      },
      async deleteMission (mission_id) {
        this.$emit('delete_mission', mission_id)
        this.delete_dialog = false
      },
      update_clearance () {
        if (this.selected) {
          //if there's a preset message selected
          this.clearance.message = this.selected
        } else {
          this.clearance.message = this.flight.clearance.message
        }
        this.$emit('update_clearance', this.clearance)
      }
    },
    filters: {
      date_filter: function (date) {
        return moment(date).format('MMMM Do, YYYY')
      },
      datetime_filter: function (date) {
        return moment(date).format('MMMM Do YYYY, h:mm a')
      }
    },
    watch: {
      department_name (val) {
        //true clause
        if (this.presetClearances != null) {

          this.presetClearances = [
            { text: 'Preset Message', value: '' },

            {
              text: 'CLEAR FLIGHT',
              value: 'You\'re all set! The ' + this.department_name +
                ' Commanders and Dispatchers have been notified about your intended flight. ' +
                '\nPlease note, filing a flight plan with the ' + this.department_name +
                ' does not alleviate you of the responsibility of adhering to all FAA regulations ' +
                'and safety recommendations. As always, if you experience any problems during ' +
                'your flight, please immediately call the ' + this.department_name + ' at ' +
                this.user_info.pilot.mobile_phone_number + '. \nFly safe!'
            },

            {
              text: 'ANOTHER FLIGHT',
              value: 'Please exercise additional caution during your flight, as ' +
                'another UAS pilot has filed a flight plan with an overlapping time frame ' +
                'in the same location. \nPlease note, filing a flight plan with the ' + this.department_name +
                ' does not alleviate you of the responsibility of adhering ' +
                'to all FAA regulations and safety recommendations. In the unlikely event that ' +
                'you experience any problems during your flight, please immediately call the ' +
                this.department_name + ' at ' + this.user_info.pilot.mobile_phone_number +
                '. \nFly safe!'
            },

            {
              text: 'CIVIC TWILIGHT WARNING',
              value: 'Please exercise additional caution during your ' +
                'flight. You may not fly a small unmanned aircraft system before sunrise civil twilight, ' +
                'nor after sunset civil twilight time. Civil twilight is defined as 30 minutes before ' +
                'sunrise and 30 minutes after sunset. \nPlease note, filing a flight plan with the ' +
                this.department_name + ' does not alleviate you of the responsibility of adhering ' +
                'to all FAA regulations and safety recommendations. In the unlikely event ' +
                'that you experience any problems during your flight, please immediately ' +
                'call the ' + this.department_name + ' at ' + this.user_info.pilot.mobile_phone_number +
                '. \nFly safe!'
            },

            {
              text: 'NIGHT FLYING',
              value: 'It is NOT advised to fly at the current time, ' +
                'as the proposed time of your flight at night. The FAA prohibits the operation of ' +
                'small unmanned aircraft systems at night without either a Certificate of ' +
                'Authorization or Waiver. Filing a flight plan with the ' + this.department_name +
                ' does not alleviate you of the responsibility of adhering to all FAA ' +
                'regulations and safety recommendations.  Please reschedule your flight to comply ' +
                'with FAA regulations.'
            }
          ]

        }
      }
    },
  }
</script>

<style>

</style>
