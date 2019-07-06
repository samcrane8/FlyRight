<template>
  <v-dialog
      v-model="dialog"
      full-width
      width="290"
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
      <v-tabs>
        <v-tabs-bar>
          <v-tabs-slider color="primary"></v-tabs-slider>
          <v-tabs-item href="tab-calendar">
            <v-icon>event</v-icon>
          </v-tabs-item>
          <v-tabs-item href="tab-timer">
            <v-icon>access_time</v-icon>
          </v-tabs-item>
          <v-spacer/>
          <v-btn
            flat icon
            color="primary"
            @click="update"
          >
            <v-icon>check</v-icon>
          </v-btn>
        </v-tabs-bar>
        <v-tabs-items>
          <v-tabs-content id="tab-calendar">
            <v-date-picker
              ref="datepicker"
              v-model="date"
              color ="primary"
              :show-current="false"
            />
          </v-tabs-content>
          <v-tabs-content id="tab-timer">
            <v-time-picker
              ref="timepicker"
              v-model="time"
              color ="primary"
              :show-current="false"
            />
          </v-tabs-content>
        </v-tabs-items>
      </v-tabs>
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
        time: '',
        datetime_formatted: ''
      }
    },
    methods: {
      update() {
        this.dialog = false
        this.datetime_formatted = moment(`${this.date} ${this.time}`, 'YYYY-MM-DD h:mm a').format('MMMM Do YYYY, hh:mm a')
        this.$emit('input', moment(`${this.date} ${this.time}`, 'YYYY-MM-DD h:mm a').toISOString())
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