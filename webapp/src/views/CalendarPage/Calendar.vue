<template>
  <v-card :elevation="5" style="margin:50px; margin-top:15px;">
    <v-content style="margin:15px;">
      <FullCalendar 
        @eventClick="handleEventClick"
        :margin="3" 
        defaultView="timeGridWeek" 
        :plugins= "calendarPlugins" 
        :events="events"
        :contentHeight="550"
        :nowIndicator="true"
        :scrollTime="scrollTime"
      />
    </v-content>
  </v-card>
</template>

<style>
  @import '@fullcalendar/core/main.css';
  @import '@fullcalendar/timegrid/main.css';
</style>

<script>
  import Vue from 'vue'
  import moment from 'moment'
  import API from '@/mixins/API.js'
  import router from '@/router'
  import FullCalendar from '@fullcalendar/vue'
  import timeGridPlugin from '@fullcalendar/timegrid'



  export default {
    mixins: [API],
    props: ['missions','user_info','is_gov_official', 'department_name'],
    components: {
      FullCalendar
    },
    data() {
      return {
        calendarPlugins: [timeGridPlugin],
          flights:[],
          events:[],
          scrollTime: '09:00'
      }
    },
    methods: {
      handleEventClick(arg) {
        router.push('/flightdetails?id='+arg.event.extendedProps.flightId)
      },
      async get_missions() {
          for(var i = 0; i < this.missions.length; i++) {              
              if(this.missions[i].scheduling.frequency == "Weekly") {
                //gets the scheduled weekdays into an array 
                var schedulingDays = [];
                for(var k = 0; k < this.missions[i].scheduling.parameters.days.length; k++) {
                  switch(this.missions[i].scheduling.parameters.days[k]) {
                    case "SU":
                      schedulingDays[k] = 0
                      break;
                    case "M":
                      schedulingDays[k] = 1
                      break;
                    case "T":
                      schedulingDays[k] = 2
                      break;
                    case "W":
                      schedulingDays[k] = 3
                      break;
                    case "TH":
                      schedulingDays[k] = 4
                      break;
                    case "F":
                      schedulingDays[k] = 5
                      break;
                    case "S":
                      schedulingDays[k] = 6
                      break;
                  }
                }
                //gets the start and end hour
                var startTime = new Date(this.missions[i].starts_at)
                var startHour = startTime.getHours()
                var startMinutes = startTime.getMinutes()
                var endTime = new Date(this.missions[i].ends_at)
                var endHour = endTime.getHours()
                var endMinutes = endTime.getMinutes()

                //sets the flight attribute
                this.flights[i] = {
                  title: this.missions[i].title,
                  extendedProps: {
                    flightId: this.missions[i].id,
                  },
                  daysOfWeek: schedulingDays,
                  // startTime: this.missions[i].starts_at,
                  // endTime: this.missions[i].ends_at,
                  startTime: startHour + ":" + startMinutes,
                  endTime: endHour + ":" + endMinutes,
                  startRecur: this.missions[i].starts_at,
                  endRecur: this.missions[i].scheduling.ends_at,

                }
                    
              } else {
                //sets the flight attribute for non weekly events
                this.flights[i] = {
                  title: this.missions[i].title,
                  start: this.missions[i].starts_at,
                  end: this.missions[i].ends_at,
                  extendedProps: {
                    flightId: this.missions[i].id,
                  }
                }
              }
          }
      }
    },
    watch: {
        missions(val) {
            this.get_missions()
            this.events = this.flights
        }
    }
  }
</script>