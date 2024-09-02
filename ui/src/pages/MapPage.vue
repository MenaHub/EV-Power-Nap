<template>
  <q-page 
    :style-fn="pageStyle"
  >
    <MapComponent
      class="full-width"
      :starting_location="starting_location" 
      :target_location="target_location"
      :cleanMap="cleanMap"
      @totalDistance="setTotalDistance"
    /> 
    <q-btn
      size="lg"
      round
      icon="add"
      color="primary"
      :style="buttonStyle"
      @click="startResearch"
    />

    <q-dialog v-model="searchDialogOpen">
      <q-card style="width:90vw; border-radius: 10px">
        <q-card-section>
          <div class="text-h6">Search for the best charging station</div>
        </q-card-section>
        <q-card-section>
          <q-input
            suffix="%"
            v-model="chargeInfo.currentBatteryLevel"
            label="Current Battery Level"
            type="number"
            :disable="loading"
            lazy-rules
            :rules="[(val) => val >= 0 && val <= 100 || 'Invalid value']"
          />
          <q-input
            suffix="%"
            v-model="chargeInfo.desiredBatteryLevel"
            label="Desired Battery Level"
            type="number"
            :disable="loading"
            lazy-rules
            :rules="[(val) => ((val >= 0 && val <= 100 && val > +chargeInfo.currentBatteryLevel) || !chargeInfo.currentBatteryLevel) || 'Invalid value']"
          />
          <q-input
            v-model="chargeInfo.destination"
            clearable
            label="Destination"
            error-message="Enter a valid address or city"
            :error="destinationError"
            :disable="loading"
          />
        </q-card-section>
        <q-card-actions align="right" class="q-mb-sm q-mr-sm">
          <q-btn
            flat
            rounded
            label="Cancel"
            color="primary"
            :disable="loading"
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

    <q-dialog v-model="chargingStationDialogOpen">
      <q-card class="fixed-top">
        <q-card-section class="q-gutter-y-md">
          <div class="text-bold" style="font-size: 1.5rem;">Charging Stations</div>
          <div class="q-gutter-y-md">
            <div class="row" v-for="(station, index) in chargingStations" :key="index">
              <div class="col text-h6">{{ station.station_id }}</div>
              <q-btn
                flat
                rounded
                icon="arrow_forward"
                color="primary"
                :loading="loadingStation === station.station_id"
                :disable="loadingStation !== null && loadingStation !== station.station_id"
                @click="getStationDetails(station)"
              />     
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="singleStationDialogOpen" seamless>
      <q-card class="fixed-top">
        <q-card-section class="row flex items-center justify-between q-gutter-sm card-section">
          <div class="col text-bold" align="center" style="font-size: 1.5rem;">{{ selectedStation.name }}</div>
          <div class="col card-details flex justify-center">
            <div>
              <div>Provider: {{ selectedStation.provider }}</div>
              <div>Distance: {{ selectedStation.distance }} km</div>
              <div>Charging time: {{ selectedStation.chargingTime }} mins</div>
              <div>Cost per hour: {{ selectedStation.costPerHour }} €</div>
              <div>Socket type: {{ selectedStation.socketType }}</div>
            </div>
          </div>
          <div class="col" align="center" style="row-gap: 0.5rem;">
            <div class="row q-gutter-sm justify-center">
              <q-btn 
                class="col"
                rounded
                label="go back"
                color="red"
                @click="goBack"
                style="min-width: fit-content"
              />
              <q-btn
                class="col"
                rounded
                label="Navigate"
                color="primary"
                @click="navigateToStation"
                style="min-width: fit-content"
              />
              </div>
          </div>
        </q-card-section>
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
      destinationError: false,
      cleanMap: false,
      offset: 0,
      chargeInfo: {
        currentBatteryLevel: '',
        desiredBatteryLevel: '',
        destination: '',
      },
      searchDialogOpen: false,
      chargingStationDialogOpen: false,
      singleStationDialogOpen: false,
      loadingStation: null,
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
  mounted() {
    this.searchDialogOpen = false;
    this.chargingStationDialogOpen = false;
    this.singleStationDialogOpen = false;
    this.starting_location = [];
    this.target_location = [];
  },
  methods: {
    pageStyle(offset) {
      this.offset = offset;
      return {
        minHeight: `none`,
        position: 'relative',
        top: '0',
        right: '0',
        left: '0',
        bottom: `${this.offset}px`,
      };
    },
    async searchForChargingStations() {
      //console.log('Searching for charging stations');
      this.loading = true;
      this.destinationError = false;
      this.starting_location = [];
      this.target_location = [];
      await this.$api.post('/get-location', {
        address: this.chargeInfo.destination.replaceAll(' ', '-').replaceAll(',', '')
      })
      .then(async response => {
        if(response.data){
          this.target_location = [response.data.body[0], response.data.body[1]];
          //console.log("get-location result body: ", response.data.body);
          await this.$api.get('/get-charging-stations', {
            params: {
              latitude: response.data.body[1],
              longitude: response.data.body[0],
              current_battery: this.chargeInfo.currentBatteryLevel,
              desired_battery: this.chargeInfo.desiredBatteryLevel,
            },
          })
          .then(response => {
            if(response.data){
              //console.log("get-charging-stations result: ", response.data);
              this.chargingStations = response.data;
              this.searchDialogOpen = false;
              this.chargingStationDialogOpen = true;
            }
          })
          .catch(error => {
            this.destinationError = true;
            console.error(error);
          });
        }
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
    async getStationDetails(station) {
      //console.log(`Navigating to ${station.station_id} at ${station.location[0]}, ${station.location[1]}`);
      this.loading = true;
      this.loadingStation = station.station_id;
      await this.$api.get('/get-details-from-station', {
        params: {
          longitude: station.location[0],
          latitude: station.location[1],
          current_battery: this.chargeInfo.currentBatteryLevel,
          desired_battery: this.chargeInfo.desiredBatteryLevel,
          station_id: station.station_id,
        },
      }).then(response => {
        if(response.data){
          //console.log("get-details-from-station result: ", response.data);
          this.chargingStationDialogOpen = false;
          var response = response.data;

          this.selectedStation.name = station.station_id,
          this.selectedStation.location = [response.location.latitude, response.location.longitude],
          this.selectedStation.provider = response.provider,
          //distance: response.distance.toFixed(2),
          this.selectedStation.chargingTime = response.charging_time.toFixed(0),
          this.selectedStation.costPerHour = response.plugs[0].cost_per_kwh,
          this.selectedStation.socketType = response.plugs[0].socket_type,
          
          this.starting_location = [station.location[0], station.location[1]];
          this.singleStationDialogOpen = true;
        }
      })
      .catch(error => {
        console.error(error);
        this.$q.notify({
          color: 'negative',
          message: 'Error while fetching station details',
          position: 'top',
          timeout: 3000,
        });
      })
      .finally(() => {
        this.loading = false;
        this.chargingStationDialogOpen = false;
        this.loadingStation = null; 
      }); 
    },
    startResearch() {
      this.searchDialogOpen = true;
      this.chargingStationDialogOpen = false;
      this.singleStationDialogOpen = false;
    },
    navigateToStation() {
      const url = `https://www.google.com/maps/dir/${this.starting_location[1]},${this.starting_location[0]}/${this.target_location[1]},${this.target_location[0]}`;
      window.open(url, '_blank');
    },
    setTotalDistance(totalDistance) {
      this.selectedStation.distance = totalDistance.toFixed(2);
    },
    goBack(){
      this.singleStationDialogOpen = false;
      this.chargingStationDialogOpen = true;
      this.cleanMap = true;
    },
  },
  computed: {
    // pageStyle() {
    //   return {
    //     position: 'absolute',
    //     top: '0',
    //     right: '0',
    //     left: '0',
    //     bottom: `${this.offset}px`,
    //   }
    // },
    buttonStyle(){
      return {
        bottom: `calc(${this.offset}px + 16px)`,
        right: '16px',
        position: 'fixed',
      }
    }
  }
});
</script>

<style scoped>
.fixed-top {
    position: fixed;
    top: 5vh ;
    right: auto;
    left: auto;
    height: fit-content;
    border-radius: 10px;
    width: 90vw;
  }

.card-details div {
  font-size: 1rem;
  font-weight: 500;
}
.card-section > div {
  min-width: fit-content;
}
</style>