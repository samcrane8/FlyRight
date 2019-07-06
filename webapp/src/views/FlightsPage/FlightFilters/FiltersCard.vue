<template>
  <v-card style="margin:20px;">
    <v-card-text>
      <v-flex>
        <h3 style="
        font-weight:200;
        font-size:28px;
        ">
          FILTERS
        </h3>
      </v-flex>
      <v-flex style="margin-top:20px;">
        <v-layout row>
          <v-flex
          xs3
          style="margin-right:2px;"
          >
            {{filters[0].type}}
          </v-flex>
          <v-flex
          style="margin-top:-25px;margin-right:8px;"
          xs9>
            <datetimepicker :value="filters[0].datetime" @input="afterHandler"/>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex
          xs3
          style="margin-right:2px;"
          >
            {{filters[1].type}}
          </v-flex>
          <v-flex
          style="margin-top:-25px;margin-right:8px;"
          xs9>
            <datetimepicker :value="filters[1].datetime" @input="beforeHandler"/>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex class="text-xs-center">
        <v-btn flat outline style="margin:10px;"
          @click="refreshMissions();">
          APPLY
        </v-btn>
      </v-flex>
    </v-card-text>
  </v-card>
</template>


<script>
  import moment from 'moment'
  import DateTimePicker from '@/components/DateTimePicker'

  export default {
    components: {
      'datetimepicker': DateTimePicker
    },
    data() {
      return {
        filters: [{
          type: 'Only after',
          datetime: ''
          },
          {
          type: 'Only before',
          datetime: ''
          }
        ],
      }
    },
    methods: {
      refreshMissions(){
        this.$emit('refresh_missions', this.filters)
      },
      afterHandler(value) {
        this.$emit('afterchange', value)
      },
      beforeHandler(value) {
        this.$emit('beforechange', value)
      }
    }
  }
</script>