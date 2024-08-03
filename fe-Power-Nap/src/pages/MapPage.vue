<template>
  <q-page class="flex flex-center">
    <MapComponent class="full-width" /> 
<!--     <GoogleMap
      api-key="AIzaSyBLLl16JCI9xriNlT_telfQuMopJtGFV-8"
      style="width: 100%; height: 92vh"
      :center="center"
      :zoom="15"
    >
      <CustomMarker :options="{ position: center, anchorPoint: 'BOTTOM_CENTER' }">
        <div style="text-align: center">
          <img src="src/assets/pin.png" width="50" height="50" />
        </div>
      </CustomMarker>
      <Polyline :options="flightPath" />
    </GoogleMap> -->
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';
import MapComponent from 'components/MapComponent.vue';
import { GoogleMap, CustomMarker, Polyline } from 'vue3-google-map'

const flightPlanCoordinates = [
        { lat: 37.772, lng: -122.214 },
        { lat: 21.291, lng: -157.821 },
        { lat: -18.142, lng: 178.431 },
        { lat: -27.467, lng: 153.027 },
      ];

export default defineComponent({
  name: 'MapPage',
  data() {
    return {
      center: { lat: 0, lng: -180 },
      
      flightPath: {
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
      }
    }
  },
  components: {
    GoogleMap,
    CustomMarker,
    Polyline,
    MapComponent
  }
});
</script>
