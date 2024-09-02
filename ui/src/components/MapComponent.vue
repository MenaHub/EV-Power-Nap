<template>
  <!-- id="map" is used to inject the Maplibre map -->
  <div 
    id="map"
  ></div>
</template>

<script>
import maplibregl from 'maplibre-gl';
import { LocationClient, CalculateRouteCommand } from '@aws-sdk/client-location';

export default {
  name: 'MapComponent',
  data() {
    return {
      map: null,
      locationClient: null,
    };
  },
  mounted() {
    const credentials = {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    };
    
    this.locationClient = new LocationClient({
      region: 'eu-west-1',
      credentials: credentials,
    });

    const apiKey = `${process.env.AWS_API_KEY}`;
    const mapName = "powernap";
    const region = "eu-west-1";

    // Initialize MapLibre map
    this.map = new maplibregl.Map({
      container: "map",
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`,
      center: [11.340000, 46.495000], // centered in Bolzano area for NOI techpark APIs reachability
      zoom: 14,
    });
  },
  methods: {
    updateRoute() {
      if (this.starting_location.length === 0 || this.target_location.length === 0) {
        console.error("Starting or target location not provided");
        return;
      }
      
      this.clearExistingRoutesIfAny();

      const input = {
        CalculatorName: 'powernap',
        DeparturePosition: this.starting_location,
        DestinationPosition: this.target_location,
        TravelMode: 'Walking',
        DistanceUnit: 'Kilometers'
      };
      const calculateRouteCommand = new CalculateRouteCommand(input);
      
      this.locationClient.send(calculateRouteCommand)
      .then((data) => {
        if (!data.Legs || !data.Legs.length) {
          console.error('No route legs found in the response');
          return;
        }

        // Extract route coordinates
        let coordinates = [];
        data.Legs.forEach(leg => {
          leg.Steps.forEach(step => {
            coordinates.push([step.StartPosition[0], step.StartPosition[1]]);
            coordinates.push([step.EndPosition[0], step.EndPosition[1]]);
          });
        });

        // Add route to the map
        this.map.addSource('route', {
          type: 'geojson',
          data: {
            type: 'Feature',
            geometry: {
              type: 'LineString',
              coordinates: coordinates
            }
          }
        });

        this.map.addLayer({
          id: 'route',
          type: 'line',
          source: 'route',
          layout: {},
          paint: {
            'line-color': '#FF5733',
            'line-width': 5
          }
        });

        this.map.fitBounds([
          [Math.min(...coordinates.map(c => c[0])), Math.min(...coordinates.map(c => c[1]))],
          [Math.max(...coordinates.map(c => c[0])), Math.max(...coordinates.map(c => c[1]))]
        ], 
          {
            padding: {
              top: 250,
              bottom: 100,
              left: 100,
              right: 100
            }, 
            maxZoom: this.$q.screen.lt.sm ? 15 : 14
          }
        );

        const totalDistance = data.Summary.Distance; // In kilometers
        //console.log(`Total distance to the target: ${totalDistance.toFixed(2)} km`);
        this.$emit('totalDistance', totalDistance);
      })
      .catch((err) => {
        console.error('Error calculating route:', err);
      });
    },
    clearExistingRoutesIfAny(){
      if (this.map.getSource('route')) {
        this.map.removeLayer('route');
        this.map.removeSource('route');
      }
    }
  },
  watch: {
    starting_location(newVal) {
      if (newVal && this.target_location.length > 0) {
        this.updateRoute();
      } else {
        this.clearExistingRoutesIfAny();
      }
    },
    target_location(newVal) {
      if (newVal && this.starting_location.length > 0) {
        this.updateRoute();
      } else {
        this.clearExistingRoutesIfAny();
      }
    },
    cleanMap(newVal, oldVal) {
      if (newVal && newVal !== oldVal) {
        this.clearExistingRoutesIfAny();
      }
    }
  },
  props: {
    starting_location: {
      type: Array,
      default: () => [11.340000, 46.495000]
    },
    target_location: {
      type: Array,
      default: () => [11.356392, 46.49561]
    },
    cleanMap: {
      type: Boolean,
      default: false
    },
  },
  // computed: {
  //   mapStyle() {
  //     return {
  //       position: 'absolute',
  //       top: '0',
  //       bottom: `0`,
  //       left: '0',
  //       right: '0'
  //     };
  //   }
  // },
}

</script>

<style scoped>
#map {
  position: relative;
  inset: 0;
}
</style>