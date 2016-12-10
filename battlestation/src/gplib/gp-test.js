var go1 = -1;
var go2 = -1;

var run = function(abt) {
  if(gp.ready) {
    window.clearInterval(go1);
    go1 = -1;
    go2 = window.setInterval(function() {
      gp.get_current(abt);
      if(!gp.ready) {
        $("#reset").click();
      }
    }, 10);
  } else {
    console.log("Waiting...")
  }
}

$(document).ready(function() {
  gp.set();
  
  go1 = window.setInterval(function() { run(); }, 50);
  
  $("#reset").click(function() {
    if(go2 != -1) {
      gp.ready = false;
      window.clearInterval(go2);
    } else {console.log("go2: "+go2+" go1: "+go1);}
    gp.set(abt);
    go1 = window.setInterval(function() { run(abt); }, 50);
  });
});