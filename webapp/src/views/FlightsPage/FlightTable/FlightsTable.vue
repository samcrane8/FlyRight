<template>
  <v-card style="margin:20px;">
    <v-data-table
        v-bind:headers="headers"
        v-bind:items="missions"
        v-bind:search="search"
        :rows-per-page-items="rppi"
        :pagination.sync="pagination"
      >
      <template slot="items" slot-scope="props">
        <tr @click.prevent="expand(props)">
          <td class="text-xs-center">{{ props.item.created_at | date_filter }}</td>
          <td class="text-xs-left">{{ props.item.title }}</td>
          <td class="text-xs-center">{{ props.item.commander_id }}</td>
          <td class="text-xs-center">{{ props.item.starts_at | date_filter}}</td>
          <td class="text-xs-center">
            <v-icon v-if="_state(props.item.clearance) == 'RECOMMEND AGAINST FLIGHT'" right color="red">block</v-icon>
            <v-icon v-if="_state(props.item.clearance) == 'CAUTION'" right color="yellow">error</v-icon>
            <v-icon v-if="_state(props.item.clearance) == 'NOTIFICATION RECEIVED'" right color="green">check_circle</v-icon>
            <v-icon v-if="_state(props.item.clearance) == 'PENDING'" right >radio_button_unchecked</v-icon>
          </td>
        </tr>
      </template>
      <template slot="pageText" slot-scope="{ pageStart, pageStop }">
        From {{ pageStart }} to {{ pageStop }}
      </template>
      <template slot="expand" slot-scope="props">
        <v-tabs>
          <v-toolbar flat>
            <v-toolbar-title>{{props.item.title}}</v-toolbar-title>
            <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-tooltip left>
                  <v-btn flat slot="activator" icon @click="edit_flight(props.item.id)" :disabled="!can_delete(props.item.created_by)">
                    <v-icon> edit </v-icon>
                  </v-btn>
                  <span>Edit Flight</span>
                </v-tooltip>
                <v-tooltip left>
                  <v-btn flat slot="activator" icon @click="flight_details(props.item.id)">
                    <v-icon> map </v-icon>
                  </v-btn>
                  <span>Flight Details</span>
                </v-tooltip>
                <v-tooltip left>
                  <v-btn flat slot="activator" icon @click="showDeleteWarning=true" :disabled="!can_delete(props.item.created_by)">
                    <v-icon> delete </v-icon>
                  </v-btn>
                  <span>Delete Flight</span>
                </v-tooltip>
              <v-dialog v-model="showDeleteWarning" max-width="500px">
                <v-toolbar dark color="primary">
                  <v-icon>warning</v-icon>
                    <v-toolbar-title>Warning</v-toolbar-title>
                  </v-toolbar>
                  <v-card>
                    <v-card-title primary-title>
                        <h1 class="headline mb-0">Are you sure?</h1>
                    </v-card-title>
                    <v-subheader>The following flight will be deleted and cannot be restored: {{props.item.title}}</v-subheader>
                    <v-card-actions>
                      <v-btn flat @click.stop="showDeleteWarning=false">Cancel</v-btn>
                      <v-btn color="primary" @click="deleteMission(props.item.id)">Delete Flight</v-btn>
                    </v-card-actions>
                  </v-card>
                  </v-dialog>
                    <v-tooltip left v-if="false">
                      <v-btn flat slot="activator" icon @click="goToMission(props.item.id)">
                        <v-icon> map </v-icon>
                      </v-btn>
                        <span>Flight Details</span>
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
                            <h4>Start Date/Time:</h4> <span>{{props.item.starts_at | datetime_filter}}</span>
                          </v-flex>
                          <v-flex>
                            <h4>End Date/Time: </h4> <span>{{props.item.ends_at | datetime_filter}}</span>
                          </v-flex>
                        </v-layout>
                        <v-layout row>
                          <v-flex>
                            <h4>Type: </h4><span>{{props.item.type}}</span>
                          </v-flex>
                          <v-flex>
                            <h4>Number of Drones: </h4><span>{{props.item.num_drones}}</span>
                          </v-flex>
                        </v-layout>
                        <v-layout row
                        v-if="props.item.scheduling">
                          <v-flex>
                            <h4>Frequency: </h4><span>{{props.item.scheduling.frequency}}</span><br>
                            <span v-for="(day, index) in props.item.scheduling.parameters.days"
                            :key="index"> {{day}} </span>
                          </v-flex>
                          <v-flex>
                            <h4>Ends At: </h4><span>{{props.item.scheduling.ends_at | datetime_filter}}</span>
                          </v-flex>
                        </v-layout>
                      </v-layout>
                      <v-layout column align-center>
                        <v-flex>
                          <map-thumbnail :mission.sync="props.item"
                          width="250px" height="200px"
                          style="width:250px;"
                          zoomControl="true"
                          ref="map"
                          />
                        </v-flex>
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
                    <v-layout row v-if="props.item.can_edit_clearance" >
                      <!-- <v-flex style="margin-top:5px;">
                        <v-text-field 
                          label="Write a short message to the commander to explain how you're setting the status."
                          multi-line
                          rows="3"
                          v-model="props.item.clearance.message"
                        >
                        </v-text-field>
                      </v-flex>
                       -->
                      
                      <v-flex style="margin-top:5px;">
                        <v-text-field 
                          v-if="selected" 
                          label="Write a short message to the commander to explain how you're setting the status."
                          multi-line
                          rows="3"
                          v-model="selected"
                        >
                        </v-text-field>  
                        <v-text-field 
                          v-else 
                          label="Write a short message to the commander to explain how you're setting the status."
                          multi-line
                          rows="3"
                          v-model="props.item.clearance.message"
                        >
                        </v-text-field>
                      </v-flex>
                      <v-layout column>
                        <select 
                          v-model="selected"
                          style="border:1px solid gray;
                          border-radius:2px;"
                          >
                          <option 
                            v-for="presetClearance in presetClearances" 
                            :value="presetClearance.value"
                            :key="presetClearance.text">
                              {{ presetClearance.text }}
                          </option>
                        </select>
                        <v-select
                          :items="clearance_states"
                          v-model="currState"
                          label="Set Clearance"
                          single-line
                          bottom
                        ></v-select>

                      </v-layout>

                    </v-layout>
                    <v-layout row v-if="!props.item.can_edit_clearance" >
                      <v-flex style="margin-top:5px;">
                        <h4>Message:</h4>
                        <span 
                          style="margin-top:10px;
                          height:80px;
                          overflow:scroll;"
                          v-if="props.item.clearance.message!=null"
                        >
                          {{props.item.clearance.message}}
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
                          {{props.item.clearance.state}}
                        </span>
                      </v-flex>
                    </v-layout>
                    <v-btn v-if="is_gov_official" @click="update_clearance(props.item)"
                    :disabled="currState===''" flat>Save Clearance</v-btn>
                  </v-layout>
                </v-card-text>
              </v-card>
            </v-tabs-content>
            <v-tabs-content
              id="tab-commander-info"
            >
              <commander-info :created_by="props.item.created_by"
              :commander_name="props.item.commander_id"/>
            </v-tabs-content>
            <v-tabs-content
              id="tab-description"
            >
              <description-tab :description="props.item.description" />
            </v-tabs-content>
          </v-tabs-items>
        </v-tabs>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
  import moment from 'moment'
  import API from '@/mixins/API.js'
  import CommanderInfo from './CommanderInfo'
  import DescriptionTab from './DescriptionTab'
  import MapThumbnail from '@/components/MapThumbnail.vue'
  import router from '@/router'

  export default {
    mixins: [API],
    props: ['missions','user_info','is_gov_official'],
    components: {
      'commander-info': CommanderInfo,
      'map-thumbnail': MapThumbnail,
      'description-tab': DescriptionTab
    },
    data() {
      return {
				headers: [
					{ text: 'Created On', align: 'left', value: 'created_at'},
					{ text: 'Title', align: 'center', value: 'title' },
					{ text: 'Commander', align: 'center', value: 'commander'},
					{ text: 'Start Date', align: 'center', value: 'starts_at'},
					{ text: 'Status', align: 'center', value: 'legal_status'}
        ],
        search: '',
        currState: '',
        message: '',
        rppi: [10,20,40,{"text":"All","value":-1}],
        showDeleteWarning: false,
        clearance_states: ['RECOMMEND AGAINST FLIGHT', 'NOTIFICATION RECEIVED', 'CAUTION'],
        pagination: {
          sortBy: 'created_at',
          descending: 'true'
        },
        clearance: {
          message: '',
          state: ''
        },
        clearance_states: ['RECOMMEND AGAINST FLIGHT', 'NOTIFICATION RECEIVED', 'CAUTION'],
        selected: '',
        presetClearances: [
        { text: 'Preset Message', value: '' },

        { text: 'CLEAR FLIGHT', 
          value: "You're all set! The Georgia Tech Police Department Watch " +
          "Commanders and Dispatchers have been notified about your intended flight. " +
          "\nPlease note, filing a flight plan with the Georgia Tech Police Department " +
          "does not alleviate you of the responsibility of adhering to all FAA regulations " + 
          "and safety recommendations.As always, if you experience any problems during " +
          "your flight, please immediately call the GTPD at 404-894-2500. \nFly safe!" },

        { text: 'ANOTHER FLIGHT', 
          value: "Please exercise additional caution during your flight, as " +
          "another UAS pilot has filed a flight plan with an overlapping time frame " +
          "in the same location. \nPlease note, filing a flight plan with the Georgia " +
          "Tech Police Department does not alleviate you of the responsibility of adhering " +
          "to all FAA regulations and safety recommendations. In the unlikely event that " +
          "you experience any problems during your flight, please immediately call the " +
          "GTPD at 404-894-2500. \nFly safe!" },

        { text: 'CIVIC TWILIGHT WARNING', 
          value: "Please exercise additional caution during your " +
          "flight. You may not fly a small unmanned aircraft system before sunrise civil twilight, " +
          "nor after sunset civil twilight time. Civil twilight is defined as 30 minutes before " +
          "sunrise and 30 minutes after sunset. \nPlease note, filing a flight plan with the Georgia " +
          "Tech Police Department does not alleviate you of the responsibility of adhering " +
          "to all FAA regulations and safety recommendations. In the unlikely event " +
          "that you experience any problems during your flight, please immediately " +
          "call the GTPD at 404-894-2500. \nFly safe!" },

        { text: 'NIGHT FLYING', 
          value: "It is NOT advised to fly at the current time, " +
          "as the proposed time of your flight at night. The FAA prohibits the operation of " +
          "small unmanned aircraft systems at night without either a Certificate of " +
          "Authorization or Waiver. Filing a flight plan with the Georgia Tech Police " +
          "Department does not alleviate you of the responsibility of adhering to all FAA " +
          "regulations and safety recommendations.  Please reschedule your flight to comply " +
          "with FAA regulations." }
        ],
      }
    },
    methods: {
      flight_details(id){
        router.push('/flightdetails?id='+id)
      },
      edit_flight(id){
        router.push('/editflight?id='+id)
      },
      expand(props){
        this.message = ''
        props.expanded = !props.expanded
      },
      _state(clearance) {
				if (clearance == null){
					return false
				}
				return clearance["state"]
      },
      _message(clearance) {
				if (clearance == null){
					return false
				}
				return clearance["message"]
      },
      async update_clearance(item) {
        if(this.selected) {
          item.clearance.message = this.selected;
        }
        item.clearance.state = this.currState;
        this.message = item.clearance.message;
				const response = await this.edit_clearance(
					item.id, item.clearance.state, this.message,
					this.$store.state.access_token
				);
				if (response.status == 200) {
					this.$emit('snackbar', 6000, 'Clearance updated.')
				}
			},
      can_delete(id){
				return this.user_info.user.id == id
      },
      async deleteMission(mission) {
        this.$emit('delete_mission', mission)
        this.showDeleteWarning=false
			},
			newMission(){
			  router.push('/newflight')
      },
      goToMission(mission) {
					router.push('map?id='+mission);
			},
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