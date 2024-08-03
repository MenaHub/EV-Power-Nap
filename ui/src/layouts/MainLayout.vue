<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer style="height: 8vh;">
      <q-tabs
        v-model="tab"
        align="center"
        class="text-white full-height"
        active-bg-color="white"
        active-color="primary"
        indicator-color="primary"
      >
        <q-route-tab name="vehicles" label="Your Vehicles" icon="directions_car" no-caps to="/vehicles"/>
        <q-route-tab name="map" label="Map" icon="map" no-caps to="/map"/>
        <q-route-tab name="account" label="Account" icon="account_circle" no-caps to="/account"/>
      </q-tabs>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  data () {
    return {
      tab: 'map' // Default selected tab
    }
  },

  methods: {
  }
})
</script>
