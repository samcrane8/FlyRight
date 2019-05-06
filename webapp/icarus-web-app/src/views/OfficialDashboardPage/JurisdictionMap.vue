<template>
  <v-flex
  class="text-xs-center">
		<div
        id="map"
				:style="map_style"
      >
		</div>
  </v-flex>
</template>

<style>
	@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500');

	.mission_body {
		font-family: 'Roboto', sans-serif;
	}
</style>

<script>
	import Vue from 'vue';
	import Vuetify from 'vuetify'
	import router from '@/router'
	import API from '@/mixins/API.js'
  import L from 'leaflet';
  import 'leaflet-path-drag';

	export default {
		name: 'MissionsPage',
		mixins: [API],
		props: ['jurisdiction'],
	  data () {
	    return {
				map_style: "width:350px;height:350px;",
        newCenter: "",
        zoom: 15.4,
        center: { lat: 33.778463, lng: -84.398881 },
        mapType: 'hybrid',
        scrollwheel: false,
        width: '55vw',
        height: '100vh',
	      tmp: '',
	      search: '',
	      pagination: {},
	      headers: [
	        { text: 'Title', align: 'left', value: 'title' },
	        { text: 'Commander', align: 'center', value: 'commander'},
	        { text: 'Drones', align: 'center', value: 'Drones#'},
	        { text: 'Start Date', align: 'center', value: 'starts_at'},
	        { text: 'Approval Status', align: 'center', value: 'legal_status'}
	      ],
	      items: [],
	      start_date: null,
	      start_menu: false,
	      end_date: null,
	      end_menu: false,
	      clearance_states: [
	      	'APPROVED',
	      	'DECLINED'
	      ],
	      is_gov_official: false,
	      snackbar: false,
        y: 'top',
        x: null,
        mode: '',
        timeout: 6000,
        text: 'Clearance updated.',
				mapLoaded: false,
				mapbox_url: 'https://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw',
	    }
    },
    methods: {
      set_map() {
        this.map_style= `width:${this.width};height:${this.height};z-index:0;`
      }
    },
		mounted() {
      this.set_map();
			this.$nextTick(() => {
        var mapbox_layer = new L.TileLayer(this.mapbox_url);
        this.map = L.map('map').addLayer(mapbox_layer);
        this.map.zoomControl.setPosition('bottomright');
        var juri_polygon = L.polygon(this.jurisdiction.area.features[0].geometry.coordinates)
        this.map.fitBounds(juri_polygon.getBounds())
        juri_polygon.addTo(this.map);
			})
		}
	}
</script>
