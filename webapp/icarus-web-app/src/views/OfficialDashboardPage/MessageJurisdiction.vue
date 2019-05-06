<template>
  <v-content>
    <v-card>
      <div class="stat_header">
        Message Jurisdiction
      </div>
      <div
      style="padding:10px;">
        If you would like to send an email to all pilots in your jurisdiction,
        fill out the box below and hit send.
      </div>
      <v-form>
        <v-flex
        style="padding-left:15px;padding-right:15px;">
          <v-text-field
            name="input-description"
            label="message"
            v-model="message"
            multi-line
          ></v-text-field>
        </v-flex>
        <v-flex
        class="text-xs-center"
        style="padding-bottom:10px;">
          <v-btn
          color="primary"
          :disabled="message==''"
          @click="dialog=true">
            SEND
          </v-btn>
        </v-flex>
      </v-form>
    </v-card>
    <v-dialog
    v-model="dialog"
    max-width="40vw"
    >
      <v-toolbar dark color="primary">
        <v-icon>warning</v-icon>
          <v-toolbar-title>Warning</v-toolbar-title>
      </v-toolbar>
      <v-card>
        <v-card-title primary-title>
            <h1 class="headline mb-0">Are you sure?</h1>
        </v-card-title>
        <v-subheader>Are you sure you would like to send this message? This will go to every pilot in your jurisdiction.</v-subheader>
        <v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn color="primary" @click="sendMessage">Send Message</v-btn>
            <v-btn color="secondary" flat @click.stop="dialog=false">Cancel</v-btn>
            <v-spacer/>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-content>
</template>

<script>
  import API from '@/mixins/API'

  export default {
    mixins: [API],
    props: ['department_name'],
    data() {
      return {
        message: '',
        dialog:false,
      }
    },
    methods: {
      async sendMessage() {
        this.dialog = false
        const response = await this.message_pilots(
          this.message,
          this.department_name,
          this.$store.state.access_token
        );
        if (response.status == 200) {
          this.$emit('snackbar', 6000, 'Messages are successfully being sent.')
        }
      }
    }
  }
</script>

<style>
  .stat_header {
    font-weight:200;
    font-size:22px;
    padding: 10px;
  }
</style>
