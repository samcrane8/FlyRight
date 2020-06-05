<template>
  <v-dialog
    ref="dialog"
    v-model="dialog"
    :return-value.sync="time"
    persistent
    lazy
    full-width
    width="400px"
  >
    <v-text-field
      slot="activator"
      label="Datetime"
      v-model="datetime_formatted"
      readonly
      prepend-icon="event"
      @click="dialog = true"
    />
    <v-card>
      <template>
        <v-stepper v-model="e6" vertical >
          <v-stepper-step :complete="e6 > 1" step="1">
            Select a Date
          </v-stepper-step>

          <v-stepper-content step="1">
            <div>
              <v-date-picker ref="timepicker" v-model="date" color="primary" :show-current="false"></v-date-picker>
            </div>
            <v-btn color="primary" @click="e6 = 2">Continue</v-btn>
          </v-stepper-content>

          <v-stepper-step step="2">Select a Time</v-stepper-step>
          <v-stepper-content step="2">
            <v-card color="white" class="mb-5" height="390px" width="290px" flat>
              <div>
                <v-time-picker v-model="picker" :landscape="false"></v-time-picker>
              </div>
            </v-card>
            <v-btn color="primary" @click="update">Continue</v-btn>
          </v-stepper-content>
        </v-stepper>
      </template>
    </v-card>
  </v-dialog>
</template>

<script>
  import moment from 'moment'
  export default {
    props: ['value'],
    data() {
      return {
        dialog: false,
        date: '',
        time: null,
        datetime_formatted: '',
        e6: 1,
        datepicker: null,
        picker: null
      }
    },
    methods: {
      update() {
        this.e6 = 1
        this.dialog = false
        this.datetime_formatted = moment(`${this.date} ${this.picker}`, 'YYYY-MM-DD h:mm a').format('MMMM Do YYYY, hh:mm a')
        this.$emit('input', moment(`${this.date} ${this.picker}`, 'YYYY-MM-DD h:mm a').toISOString())
      },
    },
    created() {
      if (this.value) {
        this.date = moment(this.value).format('YYYY-MM-DD');
        this.time = moment(this.value).format('h:mm a');
        this.datetime_formatted = moment(this.value).format('MMMM Do YYYY, hh:mm a')
      } else {
        this.date = moment().format('YYYY-MM-DD');
        this.time = moment().format('h:mm a');
        this.datetime_formatted = moment().format('MMMM Do YYYY, hh:mm a')
      }
    }
  }
</script>
