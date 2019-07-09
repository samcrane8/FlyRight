<template>
  <v-content>
    <div
    class="map">
      <l-map
        id="map"
        ref="map"
        :zoom.sync="zoom"
        :center="center"
        v-on:click ="getLatLon($event)"
      >
        <l-tile-layer
          :url="url"
          :attribution="attribution"
          :token="token"
        >
        </l-tile-layer>
        <l-polyline
          :latLngs="points"
          color.default= "#ff0000"
        >
        </l-polyline>
        <l-polygon
          class="polygon"
          :latLngs="points"
          color.default= "#ff0000"
          fillColor.default= "#ff0000"
          v-on:drag="dragPolygon($event)"
          v-on:click="deletePolygon"
        >
        </l-polygon>
        <l-circle-marker
          v-for="(point, index) in points"
          :key="index"
          :latLng="point"
          v-on:click="points=[]"
          color.default= "#ff0000"
          v-on:mousedown="deletePolygon"
          draggable: true
        >
        </l-circle-marker>
      </l-map>
    </div>
    <div
    style="
      position:fixed;
      z-index:1000;
      x:200;
      top: 50%;
      left: 93%;
    ">
      <v-btn
        fab
        dark
        class="elevation-5"
        small
        :color="current_icon === 'edit'? 'white' : 'primary'"
        v-on:click="drawEnabled"
      >
        <v-icon
        :color="current_icon === 'edit'? 'primary' : 'white'"
        >edit</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        :color="current_icon === 'pan_tool'? 'white' : 'primary'"
        v-on:click="editEnabled"
      >
        <v-icon
        :color="current_icon === 'pan_tool'? 'primary' : 'white'"
        >pan_tool</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        :color="current_icon === 'delete'? 'white' : 'primary'"
        v-on:click="deleteEnabled"
      >
        <v-icon
        :color="current_icon === 'delete'? 'primary' : 'white'"
        >delete</v-icon>
      </v-btn>
    </div>
  </v-content>
</template>
<style>
  .map {
    width:100%;
    height:100%;
  }
  path {
    stroke: #ff0000;
  }
  .crosshair {
    cursor: crosshair !important;
  }
</style>

<script>
  import { LMap, LTileLayer, LPolygon, LPolyline, LCircleMarker} from 'vue2-leaflet';
  import L from 'leaflet';
  import 'leaflet-path-drag';

  export default {
    name: 'Map',
    props: ['value'],
    components: {
      LMap,
      LTileLayer,
      LCircleMarker,
      LPolygon,
      LPolyline
    },
    data () {
      return {
        closePoly: false,
        drawOn: false,
        editOn: true,
        deleteOn: false,
        map: null,
        points: [],
        paths: null,
        current_icon: "pan_tool",
        direction: 'top',
        fab: false,
        fling: false,
        transition: 'slide-y-reverse-transition',
        zoom: 15.4,
        center: { lat: 33.778463, lng: -84.398881 },
        url: 'https://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        token: 'pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw'
      }
    },
    methods: {
      drawEnabled () {
        if (!this.drawOn) {
          document.getElementById("map").className += " crosshair";
          this.current_icon='edit';
          this.drawOn = true;
          this.editOn = false;
          this.deleteOn = false;
        }
      },
      deleteEnabled () {
        if (!this.deleteOn) {
          document.getElementById("map").className = document.getElementById("map").className.replace(' crosshair','');
          this.drawOn = false;
          this.editOn = false;
          this.deleteOn = true;
        }
        this.current_icon='delete';
      },
      editEnabled () {
        if (!this.editOn) {
          this.current_icon= "pan_tool"
          document.getElementById("map").className = document.getElementById("map").className.replace(' crosshair','');
          this.drawOn = false;
          this.deleteOn = false;
          this.editOn = true;
        }
      },
      getLatLon (e) {
        if (this.drawOn) {
          var latLng = [e.latlng.lat, e.latlng.lng];
          this.points.push(latLng);
          var emit_points = this.points.map(x => [x.lat, x.lng])
        }
      },
      geoJsonToPolygon () {
        this.current_icon = "map";
        this.deleteOn=false;
        this.drawOn=false;
        this.editOn=false;
        var geoJson = {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [33.77917854311787, -84.39906426576435],
                  [33.77861226955116, -84.4012854091463],
                  [33.77757334846985, -84.40013728189089],
                  [33.77853646886839, -84.39833461479827]
                ]
              }
            }
          ]
        };
        this.points = geoJson.features[0].geometry.coordinates;
        this.points.splice(-1,1)
        var emit_points = this.points.map(x => [x.lat, x.lng])
        this.$emit('new_area', emit_points)
      },
      deletePolygon () {
        if (this.deleteOn) {
          // var index = this.points.indexOf(circle);
          // if (index > -1) {
          //   this.points.splice(index, 1);
          //   index = this.points.indexOf(circle);
          //   if (index > -1) {
          //     this.points.splice(index, 1);
          //   }
          // }
          // var emit_points = this.points.map(x => [x.lat, x.lng])
          this.points = []
          this.$emit('new_area', this.points)
        }
      },
      dragPolygon(e) {},
      dragCircle(circle, e) {},
      setup() {
				this.gmap_style= `width:${this.width};height:${this.height};z-index:0;`
        var area = this.value.area
				this.points = []
				this.paths = []
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
				this.zoom = -1.420533814 * Math.log(range) + 6.8957137
        this.points = paths
        this.points.splice(-1,1)
        var emit_points = this.points.map(x => [x.lat, x.lng])
        this.$emit('new_area', emit_points)
				this.center = {lat: avg_lat/num_coords, lng: avg_lng/num_coords}
			}
    },
    mounted () {
      this.setup()
      this.$nextTick(() => {
        this.map = this.$refs.map.mapObject;
      })
    },
  }
</script>