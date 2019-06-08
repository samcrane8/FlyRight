<template>
    <v-layout class="background_drone">
      <v-flex>
      <v-card id="drone_ADD">
        <template>
          <v-form v-model="valid" ref="form" validation>
            <v-container fluid>
              <v-layout row wrap>
                <v-flex xs12 >
                  <v-subheader>Type</v-subheader>
                </v-flex>
                <v-flex>
                    <v-container fluid>
                      <v-radio-group
                        v-model="type0"
                        required
                        :rules="[v => !!v || 'You must specify a Type!']"
                      >
                        <v-radio label="Hover" value="Hover"></v-radio>
                        <v-radio label="Glide" value="Glide"></v-radio>
                      </v-radio-group>
                    </v-container>
                </v-flex>
                <v-flex xs12 >
                  <v-select
                    label="Manufacturer"
                    :items="manufacturer_op"
                    item-value="text"
                    autocomplete
                    required
                    v-model="man1"
                    :rules="[v => !!v || 'You must specify a Manufacturer!']"
                  ></v-select>
                </v-flex>
                <v-flex xs12 >
                  <v-select
                    label="Number of Blades"
                    :items="num_blades_op"
                    item-value="text"
                    autocomplete
                    required
                    v-model="blades2"
                    :rules="[v => !!v || 'You must specify the Number of Blades!']"
                  ></v-select>
                </v-flex>
                <v-flex xs12 >
                  <v-select
                    label="Color"
                    :items="color_op"
                    autocomplete
                    required
                    v-model="color3"
                    :rules="[v => !!v || 'You must specify a color!']"
                  ></v-select>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    name="input-7-1"
                    label="Description (optionial)"
                    multi-line
                    v-model="descr"
                  ></v-text-field>
                </v-flex>
            <div id="add_drone_button" >
              <v-btn
                @click="submit"
                :disabled="!valid"
                v-on:click="registerDrone()"
              > Add Drones
              </v-btn>
            </div>
            </v-layout>
            </v-container>
          </v-form>
          </template>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card id="drone_TABLE">
          <v-card-title>
            Connected Drones
            <v-spacer></v-spacer>
            <v-text-field
              append-icon="search"
              label="Search"
              single-line
              hide-details
              v-model="search"
            ></v-text-field>
          </v-card-title>
          <div>
            <v-btn
                @click="submitting"
                v-on:click="deleteDrone()"
               >Remove Selected
            </v-btn>
          </div>
          <v-data-table
            :headers="headers"
            :items="items"
            :search="search"
            v-model="selected"
            item-key="id"
            select-all
            class="elevation-1"
            hide-actions
          >
            <template slot="items" slot-scope="props">
              <tr @click = "editDescription=false">
                <td>
                  <v-checkbox
                    primary
                    v-model="props.selected"
                  ></v-checkbox>
                </td>
                <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.color }}</td>
                 <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.id }}</td>
                <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.manufacturer }}</td>
                 <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.number_of_blades }}</td>
                <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.type }}</td>
              </tr>
            </template>
            <template slot="expand" slot-scope="props">
              <v-card flat>
                <v-card-text v-if="!editDescription">
                  <v-layout row justify-space-between>
                    <v-flex xs8>
                      <h3> Description: </h3> <br>
                      {{props.item.description}}
                    </v-flex>
                    <v-flex xs2>
                      <v-btn flat @click="editDescription=true">
                        <v-icon>edit</v-icon>
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-text>
                <v-card-text v-if="editDescription">
                  <v-layout row justify-space-between>
                    <v-flex xs8>
                      <v-text-field
                        name="input-description"
                        :value="props.item.description"
                        multi-line
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs2>
                      <v-btn flat @click="editDescription=false">
                        <v-icon>close</v-icon>
                      </v-btn>
                      <v-btn flat @click="">
                        <v-icon>save</v-icon>
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-text>
              </v-card>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="warning">
              Your search for "{{ search }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
      </v-flex>


    </v-layout>
</template>


<script>

import Vue from 'vue';
import Vuetify from 'vuetify'
import router from '@/router'
import API from '../mixins/API.js'

export default {
  name: 'Login',
  mixins: [API],
  data () {
    return {
      manufacturer_op: [
        'AeroVironment', "Ambarella", "DJI", "GoPro", "Parrot", "Yuneec", "Kespry", "Nutel Robotics", "Institu", "Ehang", "Aeryon Labs", "CyPhy", "senseFly", "Aerialtronics", "Freefly", "FLyability", "draganfly", "ActionDrone",
        "3D Robotics", "CUSTOM BUILD"
      ],
      num_blades_op: [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', "10"
      ],
      color_op: [
        'White', 'Black', 'Grey', 'Blue', 'Red', 'Orange'
      ],

      max25chars: (v) => v.length <= 25 || 'Input too long!',
      tmp: '',
      search: '',
      pagination: {},
      headers: [
        { text: 'Color', value: 'color' },
        { text: 'ID', value: 'id' },
        { text: 'Manufacturer', value: 'manufacturer' },
        { text: 'Number of Blades', value: 'number_of_blades' },
        { text: 'Type', value: 'type' }
      ],
      items: [],
      selected: [],
      type0: null,
      valid: false,
      man1: null,
      blades2: null,
      color3: null,
      descr: null,

      snackbar: false,
      snackbar2: false,
      y: 'top',
      x: null,
      mode: '',
      timeout: 6000,
      text: 'Drone Succesfully Added!',
      text2: 'Drone Successfully Removed!',

      drone_id: null,
      validADD: false,

      editDescription: false

    }
  },
  methods: {
    getUserDrones() {
      this.get_user_drones(
        response => {
          this.drone_data = response.data
          this.items = []
          for(var i=0; i<this.drone_data.length; i++) {
            this.items.push(this.drone_data[i])
          }
      },
      error => {
        alert('Hmmm something went wrong with our servers when fetching stations!! Sorry Ladd!')
      })
    },
    registerDrone() {
      if (this.descr == null) {
        this.descr = "No description added"
      }
      this.register_drone(this.descr, this.man1, this.type0, this.color3, this.blades2,
        response => {
          if (response.status == 200) {
            this.drone_id = true;
            this.$emit('snackbar',6000, 'Drone Registered Successfully');
            this.getUserDrones();
            this.$refs.form.reset();
          } else if (response.status == 400) {
            throw error;
          }
        },
        error => {
        })
    },

    deleteDrone() {
      //console.log("drone to be slected, id: " + JSON.stringify(this.selected)) // just making sure this gives what i want
      this.delete_drone(this.selected,
        response => {
          if (response.status == 200) {
            //this.snackbar2 = true;
            this.$emit('snackbar',6000, 'Drone Removed Successfully');
            this.getUserDrones();
            this.selected = [];
          } else if (response.data['code'] == 31) {
            throw error;
          }
        },
        error => {
        })
    },

    toggleAll () {
      if (this.selected.length) this.selected = []
      else this.selected = this.items.slice()
    },
    changeSort (column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = column
        this.pagination.descending = false
      }
    },
    mouseOverM () {
      document.body.style.cursor= 'default';
    },
    submit () {
      if (this.$refs.form.validate()) {
        this.snackbar = true;
      }
    },
    submitting () {
      //console.log("!@#$%^& Ladd Jones")
    }

  },
  mounted () {
    this.getUserDrones();
  }
}

</script>

<!-- styling for the component -->
<style>
.background_drone {
  background-image: none;
  background-color: #F0F0F0;
}
#drone_ADD {
  margin-top: 80px;
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 10px;
}
#drone_TABLE {
  margin-top: 80px;
  margin-bottom: 10px;
  margin-right: 20px;
}
#testing {
  margin-top: 70px;
}
</style>

