<template>
  <v-content>
    <div
    class="map">
      <l-map
        id="map"
        ref="map"
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
          v-on:click="deletePolygon(points)"
        >
        </l-polygon>
        <l-circle-marker
          v-for="(point, index) in points"
          :key="index"
          :latLng="point"
          v-on:click="clickOnVertex(point, $event)"
          color.default= "#ff0000"
          v-on:mousedown="dragCircle(index, $event)"
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
  import { LMap, LTileLayer, LGeoJson, LPolygon, LPolyline, LCircleMarker} from 'vue2-leaflet';
  import L from 'leaflet';
  import 'leaflet-path-drag';

  export default {
    name: 'Map',
    props: ['area', 'departments'],
    components: {
      LMap,
      LTileLayer,
      LCircleMarker,
      LPolygon,
      LPolyline,
      LGeoJson
    },
    data () {
      return {
        closePoly: false,
        drawOn: false,
        editOn: true,
        deleteOn: false,
        map: null,
        points: [],
        current_icon: "pan_tool",
        direction: 'top',
        fab: false,
        fling: false,
        transition: 'slide-y-reverse-transition',
        zoom: 15.4,
        center: { lat: 33.778463, lng: -84.398881 },
        url: 'https://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        token: 'pk.eyJ1IjoiaWNhcnVzbWFwIiwiYSI6ImNqbXh1bmRsMTFiZ2Iza24xbG91OHVtcG8ifQ.7tZmv96qIkPogIuR60hHWw',
      }
    },
    mounted () {
      this.$nextTick(() => {
        this.map = this.$refs.map.mapObject;
        this.map.locate({setView: true, maxView: 9})
        this.departments.forEach(department => {
          L.polygon(department.area.features[0].geometry.coordinates)
            .setStyle({fillColor: '#000000', color: '#ffffff', opacity: 0.2,
            fillOpacity:0.07, weight: 1})
            .addTo(this.map);
        });
        
        ///.setStyle({fillColor: '#0000FF'});
      })
    },
    methods: {
      drawEnabled () {
        if (!this.drawOn) {
          document.getElementById("map").className += " crosshair";
          this.current_icon='edit';
          this.drawOn = true;
          this.editOn = false;
          this.deleteOn = false;
          if (this.points.length!=0) {
            this.points = [];
          }
        }
      },
      deleteEnabled () {
        if (!this.deleteOn) {
          document.getElementById("map").className = document.getElementById("map").className.replace(' crosshair','');
          this.drawOn = false;
          this.editOn = false;
          this.deleteOn = true;
        }
        if (this.points.length==0) {
          this.points = this.points;
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
          this.points = this.points;
        }
      },
      getLatLon (e) {
        if (this.drawOn) {
          if (this.closePoly) {
            this.points = this.points;
            this.$emit('input', this.points)
            this.points = [];
            this.closePoly = false;
          } else {
            var latLng = [e.latlng.lat, e.latlng.lng];
            this.points.push(latLng);
          }
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
        this.$emit('input', this.points)
      },
      clickOnVertex (circle, e) {
        if (this.deleteOn) {
          // var index = this.points.indexOf(circle);
          // if (index > -1) {
          //   this.points.splice(index, 1);
          //   index = this.points.indexOf(circle);
          //   if (index > -1) {
          //     this.points.splice(index, 1);
          //   }
          // }
          this.points = []
          this.$emit('input', this.points)
        }
      },
      dragPolygon(e) {},
      dragCircle(circle, e) {},
      deletePolygon(poly) {
        if (this.deleteOn) {
          this.points = [];
          this.points = [];
          this.$emit('input', this.points)
        }
      }
    },
    watch: {
      points: {
        handler(newVal, oldVal) {
          this.$emit('input', this.points)
        }
      }
    }
  }
</script>