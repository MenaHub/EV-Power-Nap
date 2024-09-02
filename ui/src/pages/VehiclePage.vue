<template>
  <q-page 
    :style-fn="pageStyle"
    class="flex items-start justify-center"
  >
    <div class="q-gutter-y-lg q-py-lg" style="width:80vw;">
      <div class="text-h4">Vehicles</div>
      <div v-for="(vehicle, index) in vehicles" :key="index">
        <q-card style="border-radius: 10px;">
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
                to="/"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>  
    </div>
    <q-btn
      size="lg"
      round
      icon="add"
      color="primary"
      :style="{ 'bottom' : `calc(${offset}px + 16px)`, 'right' : '16px', 'position' : 'fixed'}"
      @click="addVehicle"
    />
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'VehiclePage',
  methods: {
    pageStyle(offset) {
      this.offset = offset;
      return {
        minHeight: 'none',
        position: 'relative',
        top: '0',
        right: '0',
        left: '0',
        bottom: `${offset}px`,
      };
    },
    addVehicle() {
      this.vehicles.push({
        name: 'New Vehicle',
        image: 'assets/tesla.png',
        socketType: 'Type X'
      });

      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    scrollToBottom() {
      const element = document.documentElement;
      const bottom = element.scrollHeight - element.clientHeight;
      window.scrollTo({ top: bottom, behavior: 'smooth' });
    }
  },
  computed: {
    // pageStyle() {
    //   return {
    //     position: 'relative',
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
  },
  data () {
    return {
      offset: 0,
      vehicles: [
        {
          name: 'Tesla Cybertruck',
          image: 'assets/tesla.png',
          socketType: 'Type 1'
        },
        {
          name: 'Tesla Model S',
          image: 'assets/tesla.png',
          socketType: 'Type 2'
        },
        {
          name: 'Tesla Model 3',
          image: 'assets/tesla.png',
          socketType: 'Type 2'
        },
        {
          name: 'Tesla Model X',
          image: 'assets/tesla.png',
          socketType: 'Type 2'
        },
      ]
    }
  }
});
</script>
