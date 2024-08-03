<template>
  <q-page class="flex flex-center">
    <MapComponent class="full-width" :starting_location="starting_location" :target_location="target_location"/> 
    <q-btn
      size="lg"
      round
      icon="add"
      color="primary"
      class="fixed-bottom-right"
      @click="startResearch"
    />

    <q-dialog v-model="searchDialogOpen">
      <q-card style="width:90vw; border-radius: 20px">
        <q-card-section>
          <div class="text-h6">Search for the best charging station</div>
        </q-card-section>
        <q-card-section>
          <q-input
            suffix="%"
            v-model="chargeInfo.currentBatteryLevel"
            label="Current Battery Level"
            type="number"
            lazy-rules
            :rules="[(val) => val >= 0 && val <= 100 || 'Invalid value']"
          />
          <q-input
            suffix="%"
            v-model="chargeInfo.desiredBatteryLevel"
            label="Desired Battery Level"
            type="number"
            lazy-rules
            :rules="[(val) => ((val >= 0 && val <= 100 && val > +chargeInfo.currentBatteryLevel) || !chargeInfo.currentBatteryLevel) || 'Invalid value']"
          />
          <q-input
            v-model="chargeInfo.destination"
            label="Destination"
          />
        </q-card-section>
        <q-card-actions align="right" class="q-mb-sm q-mr-sm">
          <q-btn
            rounded
            label="Cancel"
            color="primary"
            :loading="loading"
            @click="searchDialogOpen = false"
          />
          <q-btn
            rounded
            label="Search"
            color="primary"
            :loading="loading"
            :disable="!chargeInfo.currentBatteryLevel || !chargeInfo.desiredBatteryLevel || !chargeInfo.destination"
            @click="searchForChargingStations"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="chargingStationDialogOpen" >
      <q-card class="fixed-top-right" style="width: 90vw; border-radius: 20px;">
        <q-card-section>
          <div class="text-bold text-h5">Charging Stations</div>
        </q-card-section>
        <q-card-section>
          <q-list>
            <q-item v-for="(station, index) in chargingStations" :key="index">
              <q-item-section>
                <q-item-label class="text-h6">{{ station.station_id }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn
                  rounded
                  label="Details"
                  color="primary"
                  :loading="loading"
                  @click="getStationDetails(station)"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="singleStationDialogOpen" seamless>
      <q-card style="width: 90vw; border-radius: 20px;" class="fixed-top-right">
        <q-card-section>
          <div class="text-bold text-h5">{{ selectedStation.name }}</div>
        </q-card-section>
        <q-card-section>
          <div class="text-h6">Provider: {{ selectedStation.provider }}</div>
          <div class="text-h6">Distance: {{ selectedStation.distance }} km</div>
          <div class="text-h6">Charging time: {{ selectedStation.chargingTime }} mins</div>
          <div class="text-h6">Cost per hour: {{ selectedStation.costPerHour }} €</div>
          <div class="text-h6">Socket type: {{ selectedStation.socketType }}</div>
        </q-card-section>
        <q-card-actions align="right" class="q-mb-sm q-mr-sm">
          <q-btn
            rounded
            label="Navigate"
            color="primary"
            @click="navigateToStation"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';
import MapComponent from 'components/MapComponent.vue';

export default defineComponent({
  name: 'MapPage',
  data() {
    return {
      chargeInfo: {
        currentBatteryLevel: '',
        desiredBatteryLevel: '',
        destination: '',
      },
      searchDialogOpen: false,
      chargingStationDialogOpen: false,
      singleStationDialogOpen: false,
      chargingStations: [],
      selectedStation: {
        name: '',
        location: [0, 0],
        provider: '',
        distance: 0,
        chargingTime: 0,
        costPerHour: 0,
        socketType: '',
      },
      loading: false,
      starting_location: [],
      target_location: [],
    }
  },
  components: {
    MapComponent
  },
  methods: {
    async searchForChargingStations() {
      console.log('Searching for charging stations');
      this.loading = true;
      await this.$api.get('/get-location', {
        params: {
          address: this.chargeInfo.destination.replaceAll(' ', '-').replaceAll(',', ''),
        },
      })
      .then(async response => {
        if(response.data){
          this.target_location = [response.data.body[0], response.data.body[1]];
          //console.log("get-location result body: ", response.data.body);
          await this.$api.get('/get-charging-stations', {
            params: {
              latitude: response.data.body[1],
              longitude: response.data.body[0],
            },
          })
          .then(response => {
            if(response.data){
              //console.log("get-charging-stations result: ", response.data);
              this.chargingStations = response.data.body;
            }
          })
          .catch(error => {
            console.error(error);
          });
        }
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
        this.searchDialogOpen = false;
        this.chargingStationDialogOpen = true;
      });
    },
    async getStationDetails(station) {
      //console.log(`Navigating to ${station.station_id} at ${station.location[0]}, ${station.location[1]}`);
      this.loading = true;
      this.starting_location = [station.location[0], station.location[1]];
      await this.$api.get('/get-details-from-station', {
        params: {
          longitude: station.location[0],
          latitude: station.location[1],
          current_battery: this.chargeInfo.currentBatteryLevel,
          desired_battery: this.chargeInfo.desiredBatteryLevel,
          stationId: station.station_id,
        },
      }).then(response => {
        if(response.data){
          //console.log("get-details-from-station result: ", response.data);
          let body = response.data.body;
          this.selectedStation = {
            name: station.station_id,
            location: [body.location.latitude, body.location.longitude],
            provider: body.provider,
            distance: body.distance.toFixed(2),
            chargingTime: body.charging_time,
            costPerHour: body.plugs[0].cost_per_kwh,
            socketType: body.plugs[0].socket_type,
          };
        }
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
        this.chargingStationDialogOpen = false;
        this.singleStationDialogOpen = true;
      }); 
    },
    async startResearch() {
      this.searchDialogOpen = true;
      this.chargingStationDialogOpen = false;
      this.singleStationDialogOpen = false;
    },
    navigateToStation() {
      console.log(`Navigating to ${this.selectedStation.name} at ${this.selectedStation.location[0]}, ${this.selectedStation.location[1]}`);
      this.singleStationDialogOpen = false;
    },
  },
});
</script>

<style>
  .fixed-bottom-right {
    position: fixed;
    bottom: 10vh ;
    right: 16px;
  }
  .fixed-top-right {
    position: fixed;
    top: 5vh ;
    right: auto;
    left: auto;
  }
</style>