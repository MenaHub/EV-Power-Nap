<template>
  <div id="map"></div>
</template>

<script>
import maplibregl from 'maplibre-gl';
import AWS from 'aws-sdk';

export default {
  name: 'MapComponent',
  data() {
    return {
      map: null,
      locationService: null,
    };
  },
  mounted() {
    // Initialize AWS SDK
    AWS.config.update({
      region: 'eu-west-1',
      credentials: new AWS.Credentials(`${process.env.AWS_SECRET_ACCESS_KEY}`, `${process.env.AWS_SECRET_ACCESS_ID}`)
    });

    this.locationService = new AWS.Location();

    const apiKey = `${process.env.AWS_API_KEY}`;
    const mapName = "powernap";
    const region = "eu-west-1";

    // Initialize MapLibre map
    this.map = new maplibregl.Map({
      container: "map",
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`,
      center: [11.340000, 46.495000], // Center around the route
      zoom: 14,
    });
    this.map.addControl(new maplibregl.NavigationControl(), "top-left");
  },
  methods: {
    updateRoute() {
      if (this.starting_location.length === 0 || this.target_location.length === 0) {
        console.error("Starting or target location not provided");
        return;
      }

      // Clear existing markers and route
      if (this.map.getSource('route')) {
        this.map.removeLayer('route');
        this.map.removeSource('route');
      }

      // Define coordinates for pins
      console.log("starting_point: ", this.starting_location);
      const pins = [this.starting_location];

      // Define the target destination
      const targetPosition = this.target_location;

      // Add pins to the map
      pins.forEach(position => {
        new maplibregl.Marker()
          .setLngLat(position)
          .addTo(this.map);
      });

      // Add a pin for the target destination
      new maplibregl.Marker({ color: 'red' })
        .setLngLat(targetPosition)
        .addTo(this.map);

      // Calculate route from the first pin to the target position
      this.locationService.calculateRoute({
        CalculatorName: 'powernap',
        DeparturePosition: pins[0], // Using the first pin as the starting point
        DestinationPosition: targetPosition,
        TravelMode: 'Walking',
        DistanceUnit: 'Kilometers'
      }, (err, data) => {
        if (err) {
          console.error('Error calculating route:', err);
          return;
        }

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

        // Fit the map view to the route
        this.map.fitBounds([
          [Math.min(...coordinates.map(c => c[0])), Math.min(...coordinates.map(c => c[1]))],
          [Math.max(...coordinates.map(c => c[0])), Math.max(...coordinates.map(c => c[1]))]
        ], { padding: 50 });

        // Calculate distance
        const totalDistance = data.Summary.Distance; // In kilometers
        console.log(`Total distance to the target: ${totalDistance.toFixed(2)} km`);
      });
    }
  },
  watch: {
    starting_location(newVal) {
      if (newVal && this.target_location.length > 0) {
        this.updateRoute();
      }
    },
    target_location(newVal) {
      if (newVal && this.starting_location.length > 0) {
        this.updateRoute();
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
    }
  }
}
</script>

<style scoped>
#map {
  height: 100vh;
  margin: 0;
}
</style>
