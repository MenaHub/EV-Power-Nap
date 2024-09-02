<template>
  <q-layout view="hhh lpr fFf">
    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer style="height: fit-content;">
      <q-tabs
        v-model="tab"
        align="center"
        class="text-white full-height equal-width-tabs"
        active-bg-color="white"
        active-color="primary"
        indicator-color="primary"
      >
        <q-route-tab name="vehicles" label="Your Vehicles" icon="directions_car" no-caps to="/vehicles"/>
        <q-route-tab name="map" label="Map" icon="map" no-caps to="/"/>
        <q-route-tab name="account" label="Account" icon="account_circle" no-caps to="/account"/>
      </q-tabs>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainLayout',

  data () {
    return {
      tab: 'map'
    }
  }
})
</script>

<style>
.equal-width-tabs .q-tab {
  flex: 1 1 0;
  display: flex;
  justify-content: center;
}
</style>
