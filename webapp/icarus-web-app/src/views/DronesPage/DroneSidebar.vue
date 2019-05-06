<template>
  <v-card id="drone_ADD">
    <v-form v-model="valid" ref="form" validation>
      <v-card flat>
        <v-card-title>
          <v-flex xs12 >
            <h1 style="font-size:25px;font-weight:200">
              New Drone
            </h1>
          </v-flex>
        </v-card-title>
      </v-card>
      <v-container fluid>
        <v-layout column>
          <v-flex xs12>
            <v-text-field
              name="input-7-1"
              label="Name"
              v-model="registration_info.name"
              required
              :rules="[v => !!v || 'You must specify a Name!']"
            ></v-text-field>
          </v-flex>
          <v-flex>
            <v-select
              label="Type"
              :items="type_options"
              item-value="text"
              aria-autocomplete
              required
              v-model="registration_info.type"
              :rules="[v => !!v || 'You must specify a Type!']"
            />
          </v-flex>
          <v-layout row>
            <v-flex xs6
            style="padding-right:5px;">
              <v-select
                label="Manufacturer"
                :items="manufacturer_options"
                item-value="text"
                autocomplete
                required
                v-model="registration_info.manufacturer"
                :rules="[v => !!v || 'You must specify a Manufacturer!']"
              ></v-select>
            </v-flex>
            <v-flex xs6
              style="padding-left:5px;">
              <v-select
                label="Color"
                :items="color_options"
                autocomplete
                required
                v-model="registration_info.color"
                :rules="[v => !!v || 'You must specify a color!']"
              ></v-select>
            </v-flex>
          </v-layout>
          <v-flex xs12>
            <v-text-field
              name="input-7-1"
              label="FAA Registration Number (optional)"
              v-model="registration_info.faa_registration_number"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-if="registration_info.manufacturer==='Other / Not Listed'"
              name="input-7-1"
              label="Other (manufacturer)"
              v-model="other.manufacturer"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              name="input-7-1"
              label="Description (optional)"
              multi-line
              v-model="registration_info.description"
            ></v-text-field>
          </v-flex>
          <div id="add_drone_button" >
            <v-layout row>
              <v-btn 
                :disabled="!valid"
                v-on:click="registerDrone()"
              > Add Drones 
              </v-btn>
              <v-spacer/>
              <v-btn
                @click="clear()"
                flat
                >
                Clear
              </v-btn>
            </v-layout>
          </div>
        </v-layout>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
  export default {
    data () {
      return {
        manufacturer_options: ['3D Robotics', 'ActionDrone', 'Aerialtronics', 'AeroVironment',
         'Aeryon Labs', 'Ambarella', 'CyPhy', 'DJI', 'Ehang', 'FLyability',
          'Freefly', 'GoPro','Institu', 'Kespry', 'Nutel Robotics', 'Parrot', 
          'Yuneec', 'draganfly', 'senseFly', 'CUSTOM BUILD', 'Other / Not Listed'],
        num_blades_options: [
          '1', '2', '3', '4', '5', '6', '7', '8', '9', "10"
        ],
        color_options: [
          'White', 'Black', 'Grey', 'Blue', 'Red', 'Orange'
        ],
        type_options: [
          "Fixed-Wing",
          "Rotor",
          "Tilt-Rotor"
        ],
        valid: false,
        other: {
          manufacturer: ''
        },
        registration_info: {
          name: '',
          type: '',
          manufacturer: '',
          color: '',
          description: '',
          faa_registration_number: ''
        }
      }
    },
    methods: {
      registerDrone(){
        var reg_info = this.registration_info
        if (this.registration_info.manufacturer == 'Other / Not Listed') {
          reg_info.manufacturer = this.other.manufacturer
        }
        this.$emit('register_drone', reg_info)
        this.$refs.form.reset()
      },
      clear() {
        this.$refs.form.reset()
      }
    }
  }
</script>

<style>
  #drone_ADD {
    margin-top: 80px; 
    margin-left: 20px;
    margin-right: 20px;
    margin-bottom: 10px;
  }
</style>
