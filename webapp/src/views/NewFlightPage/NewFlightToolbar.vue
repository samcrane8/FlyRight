<template>
  <v-card
    style="width:40vw;"
  >
    <div
      style="margin-top:10px;margin-left;10px;margin-right:10px;"
    >
      <div
        style="font-weight:200;
          font-size:25px;
          margin-top:15px;
          margin-left:10px;">
        NEW FLIGHT
      </div>
      <div
        style="margin:10px;">
        <v-list dense class="pt-0">
          <v-textarea
            label="Flight Title"
            v-model="flight.title">
          </v-textarea>
          <v-textarea
            label="Description"
            multi-line
            v-model="flight.description">
          </v-textarea>
        </v-list>

        Starts At:
        <div class="text-xs-center">
          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn
                color="primary"
                dark
                v-on="on"
              >
                Dropdown
              </v-btn>
            </template>
            <v-list>
              <v-list-tile
                v-for="(item, index) in items"
                :key="index"
                @click=""
              >
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </div>
        Ends At:
        <datetimepicker v-model="flight.ends_at"
                        style="margin-right:10px;"/>
        <v-select
          :items="types"
          v-model="flight.selectedType"
          label="Flight Type"
          single-line
          menu-props="auto"
          hide-details
        >
        </v-select>
        <v-select
          :items="available_drones"
          item-text="name"
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
        <a href="/drones"> Need to make a drone?</a>
        <v-flex
          style="margin-top:20px"
        >
          <v-select
            :items="frequency_options"
            v-model="frequency"
            label="Frequency"
            single-line
            menu-props="auto"
            hide-details
          >
          </v-select>
        </v-flex>
        <v-layout
          column
          style="margin-top:20px;"
          v-if="frequency == 'Weekly'">
          <v-select
            :items="weekdays"
            v-model="picked_weekdays"
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
              >(+{{ picked_weekdays.length - 5 }})</span>
            </template>
          </v-select>
          <v-flex
            style="margin-top:10px;"
          >
            Repeat Until:
            <datetimepicker v-model="ends_at"
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
  import DateTimePicker from '@/components/DateTimePicker'
  import moment from 'moment'
  import API from '@/mixins/API'

  export default {
    components: {
      'datetimepicker': DateTimePicker
    },
    mixins: [API],
    data () {
      return {
        frequency: 'Does Not Repeat',
        frequency_options: ['Does Not Repeat', 'Weekly'],
        weekdays: ['M', 'T', 'W', 'TH', 'F', 'S', 'SU'],
        picked_weekdays: [],
        ends_at: '',

        flight: {
          title: '',
          description: '',
          selectedType: '',
          starts_at: '',
          ends_at: '',
          added_drones: []
        },
        types: [
          'Recreational', 'Commercial', 'Research'
        ],
        available_drones: ['droney', 'other drone'],

        items: [
          { title: 'Click Me' },
          { title: 'Click Me' },
          { title: 'Click Me' },
          { title: 'Click Me 2' }
        ]

      }
    },
    mounted () {
      this.flight.starts_at = moment().toISOString()
      this.flight.ends_at = moment().toISOString()
      this.ends_at = moment().toISOString()
      this.get_drones()
    },
    methods: {
      submit () {
        var flight_plan = {
          flight: this.flight,
          scheduling: {
            parameters: { 'days': this.picked_weekdays },
            frequency: this.frequency,
            ends_at: this.ends_at
          }
        }
        this.$emit('submit_flight', flight_plan)
      },
      async get_drones () {
        const response = await this.get_user_drones(
          this.$store.state.access_token
        )
        this.available_drones = response.data
      }
    }
  }
</script>

<style>
</style>
