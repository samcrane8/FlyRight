<template>
  <v-flex
  class="text-xs-center">
		<div
		style="z-index:2">
			<l-map
        id="map"
        ref="map"
        :zoom.sync="mission.zoom"
        :center="mission.center"
				:style="gmap_style"
				:options="{watch: true, zoomControl}"
      >
				<l-tile-layer
          :url="url"
          :attribution="attribution"
          :token="token"
        />
				<l-polyline
          :latLngs="mission.paths"
          color.default= "#ff0000"
        >
        </l-polyline>
				<l-polygon
          class="polygon"
          :latLngs="mission.paths"
          color.default= "#ff0000"
          fillColor.default= "#ff0000"
        />
			</l-map>
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
	import { LMap, LTileLayer, LPolygon, LPolyline, LCircleMarker } from 'vue2-leaflet';
	import L from 'leaflet';
	import 'leaflet-path-drag';

	export default {
		name: 'MissionsPage',
		mixins: [API],
		props: ['mission', 'width', 'height', 'zoomControl', 'dragging'],
		components: {
      LMap,
      LTileLayer,
      LCircleMarker,
      LPolygon,
      LPolyline
    },
	  data () {
	    return {
				gmap_style: "width:350px;height:350px;z-index:-5;",
        newCenter: "",
        zoom: 4,
        mapType: 'hybrid',
        scrollwheel: false,
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
				mapLoaded: false,
				map: null,
				url: 'https://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        token: 'pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw'
	    }
		},
		methods: {
			setup() {
				this.gmap_style= `width:${this.width};height:${this.height};z-index:0;`
				var area = this.mission.area
				this.mission.polygons = []
				this.mission.paths = []
				var paths = []
				var avg_lat = 0
				var lat_range = {min: 200, max: -200, range: 0}
				var avg_lng = 0
				var lng_range = {min: 200, max: -200, range: 0}
				var num_coords = area.features[0].geometry.coordinates.length
				for(var i = 0; i < area.features.length; i++) {
					for (var a in area.features[i].geometry.coordinates) {
						paths.push({
						lat:area.features[i].geometry.coordinates[a][0],lng:area.features[i].geometry.coordinates[a][1]
						});
						//avg_lat
						avg_lat += area.features[i].geometry.coordinates[a][0]
						if (area.features[i].geometry.coordinates[a][0] > lat_range.max) {
							lat_range.max = area.features[i].geometry.coordinates[a][0]
						}
						if (area.features[i].geometry.coordinates[a][0] < lat_range.min) {
							lat_range.min = area.features[i].geometry.coordinates[a][0]
						}
						//avg_lng
						if (area.features[i].geometry.coordinates[a][1] > lng_range.max) {
							lng_range.max = area.features[i].geometry.coordinates[a][1]
						}
						if (area.features[i].geometry.coordinates[a][1] < lng_range.min) {
							lng_range.min = area.features[i].geometry.coordinates[a][1]
						}
						avg_lng += area.features[i].geometry.coordinates[a][1]
					}
				}
				lat_range.range = Math.abs(lat_range.max) - Math.abs(lat_range.min)
				lng_range.range = Math.abs(lng_range.max) - Math.abs(lng_range.min)
				var range = Math.max(lat_range.range, lng_range.range)
				var zoom_coefficient = 2
				this.mission.zoom = -1.420533814 * Math.log(range) + 6.8957137
				this.mission.paths = paths
				this.mission.center = {lat: avg_lat/num_coords, lng: avg_lng/num_coords}
			}
		},
		mounted() {
			setTimeout(function() { window.dispatchEvent(new Event('resize')) }, 250);
			this.$nextTick(() => {
				this.gmap_style= `width:${this.width/2};height:${this.height/2};z-index:0;`
				this.map = this.$refs.map.mapObject;
				this.map.scrollWheelZoom.disable()
				if (!this.dragging){
					this.map.dragging.disable()
				}
				this.setup()
				this.map.setView(new L.LatLng(this.mission.center.lat, this.mission.center.lng),
													this.mission.zoom)
			})
		},
		watch:{
		  mission: {
				handler(newVal, oldVal) {
					this.setup()
				},
				deep: true,
				immediate: true
			}
		}
	}
</script>
