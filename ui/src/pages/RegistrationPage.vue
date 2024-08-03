<template>
  <q-page class="flex flex-center">
    <div class="q-gutter-y-lg">
      <div class="q-gutter-y-md">
        <div class="text-h4">
          Account information
        </div>
        <q-input
          v-model="user.name"
          outlined
          label="First name"
          lazy-rules
          :rules="[val => val && val.length > 0 || 'First name is required']"
        />
        <q-input
          v-model="user.surname"
          outlined
          label="Last name"
          lazy-rules
          :rules="[val => val && val.length > 0 || 'Last name is required']"
        />
        <q-input
          v-model="user.email"
          outlined
          label="Email"
          type="email"
          lazy-rules
          :rules="[val => /.+@.+\..+/.test(val) || 'Invalid email']"
        />
        <q-input
          v-model="user.password"
          outlined
          label="Password"
          type="password"
          lazy-rules
          :rules="[val => (val && val.length >= 8) || 'Password must be present and at least 8 characters long']"
        />
        <q-input
          v-model="user.passwordConfirmation"
          outlined
          label="Confirm password"
          type="password"
          lazy-rules
          :rules="[val => val === user.password || 'Passwords do not match']"
        />
      </div>

      <div class="q-gutter-y-md">
        <div class="text-h4">
          Vehicle information
        </div>
        <q-input
          v-model="vehicle.name"
          outlined
          label="Vehicle name"
          lazy-rules
          :rules="[val => val && val.length > 0 || 'Vehicle name is required']"
        />
        <q-select
          v-model="vehicle.socketType"
          outlined
          required
          label="Vehicle type"
          :options="socketType"
        />
      
      </div>
      
      <div class="flex items-center justify-end">
        <q-btn
          rounded
          color="primary"
          label="Register"
          :disabled="!registrationEnabled"
          @click="$router.push('/account')"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'RegistrationPage',
  data () {
    return {
      user: {
        name: '',
        surname: '',
        email: '',
        password: '',
        passwordConfirmation: '',
      },
      vehicle: {
        name: '',
        socketType: '',
      },
      socketType: [
        'Type 1',
        'Type 2',
        'Type 3',
        'Type 4',
      ]
    }
  },
  computed: {
    registrationEnabled() {
      return this.user.name && this.user.surname && this.user.email && this.user.password && this.user.passwordConfirmation && this.vehicle.name && this.vehicle.socketType;
    }
  }
});
</script>
