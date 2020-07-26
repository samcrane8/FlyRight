<template>
    <v-card
      style="width:40vw;"
    >
      <div
      style="margin-top:10px;margin-left:10px; margin-right:10px;"
      >
        <div
          style="font-weight:200;
          font-size:25px;
          margin-top:15px;
          margin-left:10px;">
            EDIT FLIGHT
        </div>
        <div
        style="margin:10px;">
          <v-list dense class="pt-0">
            <v-text-field
            label="Flight Title"
            v-model="flight.title">
            </v-text-field>
            <v-text-field
            label="Description"
            multi-line
            v-model="flight.description">
            </v-text-field>
          </v-list>
          <datetimepicker
          v-if="starts_at"
          v-model="starts_at"
          />
          <datetimepicker
          v-if="ends_at"
          v-model="ends_at"/>
          <v-select
              :items="types"
              v-model="flight.type"
              label="Flight Type"
              single-line
              auto
              hide-details
              >
          </v-select>
          <v-select
            :items="available_drones"
            item-text="name"
            v-if="flight.added_drones!=='placeholder'"
            v-model="flight.added_drones"
            label="Drones"
            style="margin-top:20px;"
            multiple
          >
            <template
              slot="selection"
              slot-scope="{ item, index }"
            >
              <v-chip v-if="index === 0">
                <span>{{ item.name }}</span>
              </v-chip>
              <span
                v-if="index === 1"
                class="grey--text caption"
              >(+{{ flight.added_drones.length - 1 }} others)</span>
            </template>
          </v-select>

          <v-flex
            style="margin-top:20px"
          >
            <v-select
              :items="frequency_options"
              v-model="flight.scheduling.frequency"
              label="Frequency"
              single-line
              auto
              hide-details
              >
            </v-select>
          </v-flex>
          <v-layout
            column
            style="margin-top:20px;"
            v-if="flight.scheduling.frequency == 'Weekly'">
            <v-select
              :items="weekdays"
              v-model="flight.scheduling.parameters.days"
              label="Days"
              style="margin-top:20px;"
              multiple
            >
              <template
                slot="selection"
                slot-scope="{ item, index }"
              >
                <v-chip v-if="index < 5">
                  <span>{{ item }}</span>
                </v-chip>
                <span
                  v-if="index === 5"
                  class="grey--text caption"
                >(+{{ flight.scheduling.parameters.days.length - 5 }})</span>
              </template>
            </v-select>
            <v-flex
            style="margin-top:10px;"
            >
            Repeat Until:
            <datetimepicker v-model="flight.scheduling.ends_at"
            style="margin-right:10px;"/>
            </v-flex>
          </v-layout>

          <v-flex
          style="margin-top:20px;"
          class="text-xs-center"
          >
            <v-btn @click="submit()" dark
                color="primary">
                Save Flight
            </v-btn>
          </v-flex>
        </div>
      </div>
    </v-card>
</template>

<script>
  import Vue from 'vue'
  import Vuetify from 'vuetify'
  import moment from 'moment'
  import API from '@/mixins/API'
  import DatetimePicker from '@/components/DateTimePicker'


  export default {
    mixins: [API],
    components: {
      'datetimepicker': DatetimePicker
    },
    props: ['data', 'added_drone_data', 'available_drone_data'],
    data() {
      return {
        flight: {
          title: '',
          description: '',
          added_drones: [''],
          real: true,
          scheduling: {
            frequency: '',
            parameters: {
              days: []
            },
            ends_at: ''
          }
        },
        starts_at: null,
        ends_at: null,
        types:[
            'Recreational', 'Commercial', 'Research'
        ],
        available_drones: [''],

        frequency_options: ["Does Not Repeat", "Weekly"],
        weekdays: ['M', 'T', 'W', 'TH', 'F', 'S', 'SU'],
      }
    },
    async mounted() {
      this.available_drones = this.available_drone_data
      this.flight = this.data
      this.starts_at = this.flight.starts_at
      this.ends_at = this.flight.ends_at
      this.flight.added_drones = this.added_drone_data
    },
    methods: {
      submit() {
        this.flight.starts_at = this.starts_at
        this.flight.ends_at = this.ends_at
        var flight_plan = {
          flight: this.flight,
          scheduling: this.flight.scheduling
        }
        delete flight_plan.flight.scheduling
        this.$emit('submit_flight', flight_plan)
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
