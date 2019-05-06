<script>
  import { Line, mixins } from 'vue-chartjs'
  const { reactiveProp } = mixins

  export default {
    extends: Line,
    mixins: [reactiveProp],
    props: ['options', 'chartData'],
    data() {
      return {
        gradient: null,
      }
    },
    methods: {
      render_chart() {
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        
        this.gradient = this.$refs.canvas
          .getContext('2d')
          .createLinearGradient(0, 0, 0, 450)
        
        this.gradient.addColorStop(0, 'rgba(100, 100,100, 0.5)')
        this.gradient.addColorStop(0.5, 'rgba(100, 100, 100, 0.25)');
        this.gradient.addColorStop(1, 'rgba(100, 100, 100, 0)');

        this.chartData.datasets.backgroundColor = this.gradient
        this.renderChart(this.chartData, this.options)
        }
      },
      mounted () {
      this.render_chart()
      
    }
  }
</script>
