<template>
    <div id="app">
        <div id="navbar">
            <Navbar title="Purdue ROV - BattleStation"></Navbar>
        </div>
        <div id="main-container">
            <Card class="camera-width full-height">
                <CameraView></CameraView>
            </Card>
            <div style="width: calc(100% - 800px); height: 100%; float: left">
                <Card class="half-width half-height">
                    <IMU :data="packet.IMU"></IMU>
                </Card>
                <Card class="half-width half-height">
                    <Pres_Temp :data="packet.Pressure"></Pres_Temp>
                </Card>
                <Card class="half-width half-height">
                    <DataView title="Pressure:" :data="packet.Pressure"></DataView>
                </Card>
                <Card class="half-width half-height">
                    <IMU :data="packet.IMU"></IMU>
                </Card>
            </div>
        </div>
    </div>
</template>

<script>
var Navbar = require("./Navbar.vue")
var CameraView = require("./CameraView.vue")
var IMU = require("./IMU.vue")
var DataView = require("./DataView.vue")
var Card = require("./Card.vue")
var Pres_Temp = require("./Pressure.vue")


export default {
    components: {
        Navbar,
        CameraView,
        IMU,
        Card,
        DataView,
        Pres_Temp
    },
    data: function() {
        return {
            packet: {
                IMU: {
                  x: 8,
                  y: 0,
                  z: 8,
                  pitch: 8,
                  roll: 0,
                  yaw: 8
                },
                Pressure: {
                  pressure: 0,
                  temperature: 0
                },
                Thrusters: {
                  t0: { power: "0"},
                  t1: { power: "0"},
                  t2: { power: "0"},
                  t3: { power: "0"},
                  t4: { power: "0"},
                  t5: { power: "0"},
                  t6: { power: "0"},
                  t7: { power: "0"}
                }
            }
        };
    },
    mounted: function() {
        var vm = this;
        
        gp.vue = vm;
        
        var go1 = -1;
        var go2 = -1;
        gp.set();
        go1 = window.setInterval(function() {
            if(gp.ready) {
                window.clearInterval(go1);
                go1 = -1;
                bind.activate();
                go2 = window.setInterval(function() {
                  gp.get_current();
                });
            }
        });

        var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('connect', function () {
            console.log("connected")
        });
        
        var app_refresh = setInterval(function() {
            socket.emit("dearflask", JSON.stringify(controls));
        }, 50);

        socket.on("dearclient", function(status) {
            Object.keys(status).forEach(function(key, i) {
                vm.packet[key] = status[key];
            });
            //setTimeout(function() {
                //console.log(vm.packet);
            //}, 10);
        });
        
        socket.emit("helpme", controls);
        
        console.log(vm.packet);
    }
}
</script>

<style scoped>
#app {
    font-family: 'Roboto', Helvetica, Arial, sans-serif;
    width: 100%;
    height: 100%;
    background-color: #1a1a1a;
    font-weight: 100;
}

#navbar {
    height: 50px;
}

#main-container {
    position: fixed;
    top: 70px;
    left: 6px;
    right: 6px;
    bottom: 6px;
    margin: 0;
}

.half-width {
    width: 50%;
    float: left;
}

.half-height {
    height: 50%;
    float: left;
}

.full-height {
    height: 100%;
    float: left;
}

.camera-width {
    width: 800px;
}
</style>
