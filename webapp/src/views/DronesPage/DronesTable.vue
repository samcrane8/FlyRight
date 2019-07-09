<template>
  <v-card id="drone_TABLE">
    <v-card-title>
      <h1 style="font-size:28px;font-weight:200">
        Connected Drones
      </h1>
      <v-spacer/>
      <v-text-field
        append-icon="search"
        label="Search"
        single-line
        hide-details
        v-model="search"
      />
    </v-card-title>
    <v-flex class="text-xs-right">
      <v-spacer/>
      <v-btn flat
          :disabled = "selected.length == 0"
          v-on:click="deleteDrone()"
          ><v-icon> delete </v-icon>
      </v-btn>
    </v-flex>
    <v-data-table
      :headers="headers"
      :items="drones"
      :search="search"
      v-model="selected"
      item-key="id"
      select-all
      class="elevation-1"
      hide-actions
    >
      <template slot="items" slot-scope="props">
        <tr>
          <td>
            <v-checkbox
              primary
              v-model="props.selected"
            ></v-checkbox>
          </td>
          <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.name }}</td>
            <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.color }}</td>
          <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.manufacturer }}</td>
          <td class="text-xs-right" @click="props.expanded = !props.expanded" @mouseover="mouseOverM()">{{ props.item.type }}</td>
        </tr>
      </template>
      <template slot="expand" slot-scope="props">
        <v-card flat>
          <v-card-text v-if="!edit">
            <v-layout row justify-space-between>
              <v-flex xs12>
                <h3> FAA Registration Number: </h3>
                {{props.item.faa_registration_number}}
              </v-flex>
            </v-layout>
            <v-layout row justify-space-between>
              <v-flex xs8>
                <h3> Description: </h3>
                {{props.item.description}}
              </v-flex>
              <v-flex xs2>
                <v-btn flat @click="openEditWindow(props.item)">
                  <v-icon>edit</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-text v-if="edit">
            <v-layout column>
              <v-layout row justify-space-around>
                <v-flex xs4>
                  <v-text-field
                    name="input-7-1"
                    label="Name"
                    v-model="edit_drone.name"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4
                  style="padding-left:5px;">
                  <v-select
                    label="Color"
                    :items="color_options"
                    autocomplete
                    required
                    v-model="edit_drone.color"
                    :rules="[v => !!v || 'You must specify a color!']"
                  ></v-select>
                </v-flex>
                <v-flex xs4>
                  <v-text-field
                    name="input-7-1"
                    label="Other (manufacturer)"
                    v-model="edit_drone.manufacturer"
                  ></v-text-field>
                </v-flex>
              </v-layout>
              <v-layout row justify-space-between>
                <v-flex xs6>
                  <v-layout column>
                    <v-text-field
                      label="FAA Registration Number"
                      name="input-faa_registration_number"
                      v-model="edit_drone.faa_registration_number"
                    ></v-text-field>
                    <v-text-field
                      label="Description"
                      name="input-description"
                      v-model="edit_drone.description"
                      multi-line
                    ></v-text-field>
                  </v-layout>
                </v-flex>
                <v-flex xs6 class="text-xs-center">
                  <v-radio-group 
                    v-model="edit_drone.type" 
                    required 
                    :rules="[v => !!v || 'You must specify a Type!']"
                  >
                    <v-layout column>
                      <v-radio label="Fixed-Wing" value="Fixed-Wing"></v-radio>
                      <v-radio label="Rotor" value="Rotor"></v-radio>
                    </v-layout>
                  </v-radio-group>
                </v-flex>
                <v-flex xs2>
                  <v-btn flat @click="edit=false">
                    <v-icon>close</v-icon>
                  </v-btn>
                  <v-btn flat @click="updateDrone(props.item)">
                    <v-icon>save</v-icon>
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-layout>
          </v-card-text>
        </v-card>
      </template>
      <v-alert slot="no-results" :value="true" color="error" icon="warning">
        Your search for "{{ search }}" found no results.
      </v-alert>
    </v-data-table>
  </v-card>
</template>


<script>
  import API from '@/mixins/API.js'
  
  export default {
    mixins: [API],
    props: ['drones'],
    data() { 
      return {
        search: '',
        selected: [],
        headers: [     
          { text: 'Name', value: 'name' },
          { text: 'Color', value: 'color' },
          { text: 'Manufacturer', value: 'manufacturer' },
          { text: 'Type', value: 'type' }
        ],
        edit: false,
        edit_drone: {},
        color_options: [
          'White', 'Black', 'Grey', 'Blue', 'Red', 'Orange'
        ],
      }
    },
    methods: {
      mouseOverM () {
        document.body.style.cursor= 'default';
      },
      deleteDrone() {
        this.$emit('delete_drones', this.selected)
      },
      updateDrone(original_drone) {
        var drone_changes = {}

        Object.keys(original_drone).forEach(key => {
          if (this.edit_drone[key] !== original_drone[key]) {
            drone_changes[key] = this.edit_drone[key]
          }
        });

        drone_changes['id'] = original_drone['id']
        this.edit = false;
        this.$emit('update_drone', drone_changes)
      },
      openEditWindow (item) {
        this.edit = true;
        this.edit_drone = Object.assign({}, item)
      }
    }
  }

</script>



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
