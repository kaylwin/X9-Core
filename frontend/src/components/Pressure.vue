<template>
    <div>
        <h1>Pressure:</h1>
        <hr>
        <ul v-for="(value, key) in data">
            <li>{{key}}: {{value.pressure}}</li>
            <hr>
        </ul>
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
</style>