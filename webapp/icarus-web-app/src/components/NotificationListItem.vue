<template>
  <div :style="unread_style"
  @click="clicked()">
    {{data.actor_object_username}} {{data.verb}}
  </div>
</template>

<script>
  import router from '@/router'
  import API from '@/mixins/API'

  export default {
    mixins: [API],
    data() {
        return {
            
        }
    },
    props: ['data'],
    methods: {
      async clicked() {
        const response = await this.read(
          this.$store.state.access_token,
          this.data.id
        );
        this.$emit('update_notifications')
        if (!this.data.action_object_object_id) {
          this.$emit('snackbar', 6000, 'Error with notification routing.')
          return;
        }
        router.push(`/flightdetails?id=${this.data.action_object_object_id}`)
        //location.reload();
      }
    },
    computed: {
      unread_style() {
        if (this.data.unread) {
          return "font-weight:500;cursor:pointer;"
        } else {
          return "font-weight:300;cursor:pointer;"
        }
      }
    }
  }
</script>

<style>

</style>
