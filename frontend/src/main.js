var Vue = require("vue")
var App = require("./components/App.vue")

var vue_apps = new Vue({
    el: '#app',
    render: f => f(App),
    components: {
        App
    }
})