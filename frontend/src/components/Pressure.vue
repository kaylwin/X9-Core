template>
    <div>
        <h1>Pressure:</h1>
        <hr>
        <div class="pressurebox">
            <p>Pressure: {{data.pressure}}</p>
        </div>
        <div class="pressurebox">
            <p>Temprature: {{data.temprature}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['data'],
      
        mounted: function() {
            console.log(this.data);
        }
    }
</script>

<style scoped>
h1 {
    font-weight: 400;
}

.pressurebox {
  border: 1px black solid;
  padding: 4px;
}
</style>