<script setup>
import { ref } from 'vue'

const valid = ref(false)
const firstname = ref('')
const lastname = ref('')
const email = ref('')

const nameRules = [
  (value) => !!value || 'Name is required.',
  (value) => (value && value.length <= 10) || 'Name must be less than 10 characters.',
]

const emailRules = [
  (value) => !!value || 'E-mail is required.',
  (value) => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
]

function submit (){
    if (valid.value) {
        // Handle form submission
        console.log("Form is valid! Sending data:", {
        first: firstname.value,
        last: lastname.value,
        email: email.value
        })
        alert("Success! Check the console.")
    } else {
        console.log('Form is invalid. Please correct the errors.');
    }
}

</script>

<template>
  <v-form v-model="valid", @submit.prevent="submit">
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="firstname"
            :counter="10"
            :rules="nameRules"
            label="First name"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="lastname"
            :counter="10"
            :rules="nameRules"
            label="Last name"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-btn type="submit" color="primary" :disabled="!valid">
            Register Store
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>
