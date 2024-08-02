<template>
  <q-page class="flex items-start justify-center">
    <div class="q-gutter-y-lg q-py-lg" style="width:80vw;">
      <div class="text-h4">Vehicles</div>
      <div v-for="(vehicle, index) in vehicles" :key="index">
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ vehicle.name }}</div>
          </q-card-section>
          <q-card-section>
            <q-img :src="vehicle.image" />
          </q-card-section>
          <q-card-section>
            <div class="text-h6 q-mb-md">Socket type: <strong> {{ vehicle.socketType }}</strong> </div>
            <div class="flex justify-end">
              <q-btn
                rounded
                label="Charge this vehicle"
                color="primary"
                to="/map"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
      <q-btn
        size="lg"
        round
        icon="add"
        color="primary"
        class="fixed-bottom-right"
        @click="addVehicle"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'VehiclePage',
  methods: {
    addVehicle() {
      this.vehicles.push({
        name: 'New Vehicle',
        image: 'src/assets/tesla.png',
        socketType: 'Type X'
      });
    }
  },
  data () {
    return {
      vehicles: [
        {
          name: 'Tesla Cybertruck',
          image: 'src/assets/tesla.png',
          socketType: 'Type 1'
        },
        {
          name: 'Tesla Model S',
          image: 'src/assets/tesla.png',
          socketType: 'Type 2'
        },
        {
          name: 'Tesla Model 3',
          image: 'src/assets/tesla.png',
          socketType: 'Type 2'
        },
        {
          name: 'Tesla Model X',
          image: 'src/assets/tesla.png',
          socketType: 'Type 2'
        },
      ]
    }
  }
});
</script>

<style>
.fixed-bottom-right {
  position: fixed;
  bottom: 10vh ;
  right: 16px;
}
</style>
