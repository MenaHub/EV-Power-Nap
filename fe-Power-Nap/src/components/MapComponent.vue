<template>
  <div id="map"></div>
</template>

<script>
import maplibregl from 'maplibre-gl';
import AWS from 'aws-sdk';

export default {
  name: 'MapComponent',
  mounted() {
    // Initialize AWS SDK
    AWS.config.update({
      region: 'eu-west-1',
      credentials: new AWS.Credentials(`${process.env.AWS_SECRET_KEY}`, `${process.env.AWS_SECRET_ID}`)
    });

    const locationService = new AWS.Location();

    const apiKey =`${process.env.AWS_API_KEY}`;
    const mapName = "powernap";
    const region = "eu-west-1";

    // Initialize MapLibre map
    const map = new maplibregl.Map({
      container: "map",
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`,
      center: [11.340000, 46.495000], // Center around the route
      zoom: 14,
    });
    map.addControl(new maplibregl.NavigationControl(), "top-left");

    // Define coordinates for pins
    const pins = [
      [11.324951, 46.494711],
      [11.326951, 46.495711],
      [11.328951, 46.496711],
      [11.330951, 46.497711],
      [11.332951, 46.498711]
    ];

    // Define the target destination
    const targetPosition = [11.356392, 46.495612];

    // Add pins to the map
    pins.forEach(position => {
      new maplibregl.Marker()
        .setLngLat(position)
        .addTo(map);
    });

    // Add a pin for the target destination
    new maplibregl.Marker({ color: 'red' })
      .setLngLat(targetPosition)
      .addTo(map);

    // Calculate route from the first pin to the target position
    locationService.calculateRoute({
      CalculatorName: 'powernap',
      DeparturePosition: pins[0], // Using the first pin as the starting point
      DestinationPosition: targetPosition,
      TravelMode: 'Walking',
      DistanceUnit: 'Kilometers'
    }, function(err, data) {
      if (err) {
        console.error('Error calculating route:', err);
        return;
      }

      if (!data.Legs || !data.Legs.length) {
        console.error('No route legs found in the response');
        return;
      }

      // Extract route coordinates
      var coordinates = [];
      data.Legs.forEach(leg => {
        leg.Steps.forEach(step => {
          coordinates.push(...step.StartPosition, ...step.EndPosition);
        });
      });

      // Remove duplicates and ensure proper format
      coordinates = coordinates.reduce((acc, curr, index) => {
        if (index % 2 === 1) {
          acc.push([coordinates[index - 1], curr]); // [longitude, latitude]
        }
        return acc;
      }, []);

      // Add route to the map
      map.addSource('route', {
        type: 'geojson',
        data: {
          type: 'Feature',
          geometry: {
            type: 'LineString',
            coordinates: coordinates
          }
        }
      });

      map.addLayer({
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
      map.fitBounds([
        [Math.min(...coordinates.map(c => c[0])), Math.min(...coordinates.map(c => c[1]))],
        [Math.max(...coordinates.map(c => c[0])), Math.max(...coordinates.map(c => c[1]))]
      ], { padding: 50 });

      // Calculate distance
      const totalDistance = data.Summary.Distance; // In kilometers
      console.log(`Total distance to the target: ${totalDistance.toFixed(2)} km`);
    });
  }
}
</script>

<style scoped>
#map {
  height: 100vh;
  margin: 0;
}
</style>