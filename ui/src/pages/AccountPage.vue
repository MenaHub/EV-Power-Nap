<template>
  <q-page class="flex flex-center" >
    <div v-if="!loggedIn" class="q-gutter-y-lg" style="width:80vw;">
        <div class="text-h4">
          Account
        </div>
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
          :rules="[val => (val && val.length >= 8) || 'Invalid password']"
        />
        <div class="flex items-center justify-around q-gutter-x-sm">
          <q-btn
            style="width: 35vw;"
            rounded
            color="primary"
            label="Login"
            @click="login"
            :disable="!(this.user.email && this.user.password && /.+@.+\..+/.test(this.user.email) && this.user.password.length >= 8)"
          />
          <q-btn
            style="width: 35vw;"
            rounded
            color="primary"
            label="Register"
            @click="$router.push('/registration')"
          />
        </div>
      <q-separator />
      <q-btn
        style="width: 80vw;"
        rounded
        icon="img:src/assets/google-logo.png"
        label="Login with Google"
        @click="loginWithGoogle"
      />
    </div>

    <div v-else class="q-gutter-y-lg" style="width:80vw;"> 
      <div class="text-h4">
        Account
      </div>
      <q-input
        outlined
        disable
        label="Name"
        v-model="user.name"
      />
      <q-input
        outlined
        disable
        label="Surname"
        v-model="user.surname"
      />
      <q-input
        outlined
        disable
        label="Email"
        v-model="user.email"
      />
      <div class="q-gutter-x-sm flex justify-around">
        <q-btn
          rounded
          color="primary"
          label="Change password"
          @click="changePassword"
        />
        <q-btn
          style="width: 35vw;"
          rounded
          color="primary"
          label="Logout"
          @click="loggedIn = false"
        />
      </div>
      
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AccountPage',
  data () {
    return {
      loggedIn: false,
      user: {
        email: '',
        password: '',
        name: '',
        surname: '',
      },
    };
  },
  methods: {
    login () {
      this.user.email = 'test@test.it';
      this.user.name = 'Test';
      this.user.surname = 'Test';
      this.loggedIn = true;
    },
    loginWithGoogle () {
      console.log('loginWithGoogle');
      this.login();
    },
    changePassword () {
      console.log('changePassword');
    },
  }
});
</script>
