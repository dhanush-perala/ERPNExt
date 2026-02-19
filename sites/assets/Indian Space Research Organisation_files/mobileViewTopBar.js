 function mobileView() {
	 
                                                var x = document.getElementById("myMob");
                                                x.style.display = "block";
                                               // var y = document.getElementById("dotsID");
                                               // y.style.display = "none";

                                            }


                                            function mobileViewClose() {
                                           
                                                var x = document.getElementById("myMob");
                                                x.style.display = "none";
                                                var y = document.getElementById("dotsID");
                                                y.style.display = "block";
                                            }
                                            
 function mobileViewAutoClose(x) {
  if (x.matches) { // If media query matches
    document.getElementById("myMob").style.display = "none";
  }
}

var x = window.matchMedia("(min-width: 768px)")
mobileViewAutoClose(x) // Call listener function at run time
x.addListener(mobileViewAutoClose) // Attach listener function on state changes


