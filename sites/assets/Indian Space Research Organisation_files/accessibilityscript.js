(function () {


  document.getElementById('noContrast').onclick = function () {
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "invert(1)";
    }
    var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '#fff', 'important');
      elements[i].style.setProperty('background', '#000', 'important');
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("contrastInvert").style.border = "1px solid #098cff";
    document.getElementById("contrastInvert").style.borderRadius = "0px";
    document.getElementById("noContrast").style.display = "none";
    document.getElementById("contrastInvert").style.display = "block";
  };

  document.getElementById("noContrast").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      
        var elements1 = document.querySelectorAll('img,video,section');
        for (var i = 0; i < elements1.length; i++) {
          elements1[i].style.filter = "invert(1)";
        }
        var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
        for (var i = 0; i < elements.length; i++) {
          elements[i].style.setProperty('color', '#fff', 'important');
          elements[i].style.setProperty('background', '#000', 'important');
        }
        document.getElementById("closeButton").style.background = "#024d64";
        document.getElementById("contrastInvert").style.border = "1px solid #098cff";
        document.getElementById("contrastInvert").style.borderRadius = "0px";
        document.getElementById("noContrast").style.display = "none";
        document.getElementById("contrastInvert").style.display = "block";
        document.getElementById("contrastInvert").tabIndex = "0";
    }
  });

  document.getElementById('contrastInvert').onclick = function () {
    var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe,footer');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '#000', 'important');
      elements[i].style.setProperty('background', '#fff', 'important');
    }
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "grayscale(50%)";
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("contrastLight").style.border = "1px solid #098cff";
    document.getElementById("contrastLight").style.borderRadius = "0px";
    document.getElementById("contrastInvert").style.display = "none";
    document.getElementById("contrastLight").style.display = "block";
  };


  document.getElementById("contrastInvert").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe,footer');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '#000', 'important');
      elements[i].style.setProperty('background', '#fff', 'important');
    }
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "grayscale(50%)";
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("contrastLight").style.border = "1px solid #098cff";
    document.getElementById("contrastLight").style.borderRadius = "0px";
    document.getElementById("contrastInvert").style.display = "none";
    document.getElementById("contrastLight").style.display = "block";
    document.getElementById("contrastLight").tabIndex = "0";
    }
  });


  document.getElementById('contrastLight').onclick = function () {
    var elements = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.filter = "grayscale(0%)";
    }
    var elements1 = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe,footer');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.setProperty('color', '#fff', 'important');
      elements1[i].style.setProperty('background', '#000', 'important');
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("accessibilityIcon").style.color = "";
    document.getElementById("contrastDark").style.border = "1px solid #098cff";
    document.getElementById("contrastDark").style.borderRadius = "0px";
    document.getElementById("contrastLight").style.display = "none";
    document.getElementById("contrastDark").style.display = "block";
  };


  document.getElementById("contrastLight").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements = document.querySelectorAll('img,video,section');
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.filter = "grayscale(0%)";
      }
      var elements1 = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe,footer');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.setProperty('color', '#fff', 'important');
        elements1[i].style.setProperty('background', '#000', 'important');
      }
      document.getElementById("closeButton").style.background = "#024d64";
      document.getElementById("accessibilityIcon").style.color = "";
      document.getElementById("contrastDark").style.border = "1px solid #098cff";
      document.getElementById("contrastDark").style.borderRadius = "0px";
      document.getElementById("contrastLight").style.display = "none";
      document.getElementById("contrastDark").style.display = "block";
      document.getElementById("contrastDark").tabIndex = "0";
    }
  });  


  document.getElementById('contrastDark').onclick = function () {
    var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '#000', 'important');
      elements[i].style.color = "#000";
      elements[i].style.setProperty('background', '#fff', 'important');
    }
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "grayscale(100%)";
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("contrastDesaturate").style.border = "1px solid #098cff";
    document.getElementById("contrastDesaturate").style.borderRadius = "0px";
    document.getElementById("contrastDark").style.display = "none";
    document.getElementById("contrastDesaturate").style.display = "block";
  };


  document.getElementById("contrastDark").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.setProperty('color', '#000', 'important');
        elements[i].style.color = "#000";
        elements[i].style.setProperty('background', '#fff', 'important');
      }
      var elements1 = document.querySelectorAll('img,video,section');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.filter = "grayscale(100%)";
      }
      document.getElementById("closeButton").style.background = "#024d64";
      document.getElementById("contrastDesaturate").style.border = "1px solid #098cff";
      document.getElementById("contrastDesaturate").style.borderRadius = "0px";
      document.getElementById("contrastDark").style.display = "none";
      document.getElementById("contrastDesaturate").style.display = "block";
      document.getElementById("contrastDesaturate").tabIndex = "0";
    }
    });

  document.getElementById('contrastDesaturate').onclick = function () {
    var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '', 'important');
      elements[i].style.background = "";
    }
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "";
    }
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("noContrast").style.border = "";
    document.getElementById("noContrast").style.borderRadius = "";
    document.getElementById("contrastDesaturate").style.display = "none";
    document.getElementById("noContrast").style.display = "block";
  };


  document.getElementById("contrastDesaturate").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.setProperty('color', '', 'important');
        elements[i].style.background = "";
      }
      var elements1 = document.querySelectorAll('img,video,section');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.filter = "";
      }
      document.getElementById("closeButton").style.background = "#024d64";
      document.getElementById("noContrast").style.border = "";
      document.getElementById("noContrast").style.borderRadius = "";
      document.getElementById("contrastDesaturate").style.display = "none";
      document.getElementById("noContrast").style.display = "block";
      document.getElementById("noContrast").tabIndex = "0";
    }
  });  

  document.getElementById('normalFontAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.fontSize = "large";

    }
    document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
    document.getElementById("accessibilityFont").style.fontSize = "26px;";
    document.getElementById("bigFontAccessibility").style.border = "1px solid #098cff";
    document.getElementById("bigFontAccessibility").style.borderRadius = "0px";
    document.getElementById("normalFontAccessibility").style.display = "none";
    document.getElementById("bigFontAccessibility").style.display = "block";
  };


  document.getElementById("normalFontAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.fontSize = "large";
  
      }
      document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
      document.getElementById("accessibilityFont").style.fontSize = "26px;";
      document.getElementById("bigFontAccessibility").style.border = "1px solid #098cff";
      document.getElementById("bigFontAccessibility").style.borderRadius = "0px";
      document.getElementById("normalFontAccessibility").style.display = "none";
      document.getElementById("bigFontAccessibility").style.display = "block";
      document.getElementById("bigFontAccessibility").tabIndex = "0";
    }
  });

  document.getElementById('bigFontAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.fontSize = "x-large";
    }
    document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
    document.getElementById("accessibilityFont").style.fontSize = "27px;";
    document.getElementById("biggerFontAccessibility").style.border = "1px solid #098cff";
    document.getElementById("biggerFontAccessibility").style.borderRadius = "0px";
    document.getElementById("bigFontAccessibility").style.display = "none";
    document.getElementById("biggerFontAccessibility").style.display = "block";
  };


  document.getElementById("bigFontAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.fontSize = "x-large";
      }
      document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
      document.getElementById("accessibilityFont").style.fontSize = "27px;";
      document.getElementById("biggerFontAccessibility").style.border = "1px solid #098cff";
      document.getElementById("biggerFontAccessibility").style.borderRadius = "0px";
      document.getElementById("bigFontAccessibility").style.display = "none";
      document.getElementById("biggerFontAccessibility").style.display = "block";
      document.getElementById("biggerFontAccessibility").tabIndex = "0";
    }
  }); 

  document.getElementById('biggerFontAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.fontSize = "xx-large";
    }
    document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
    document.getElementById("accessibilityFont").style.fontSize = "28px;";
    document.getElementById("biggestFontAccessibility").style.border = "1px solid #098cff";
    document.getElementById("biggestFontAccessibility").style.borderRadius = "0px";
    document.getElementById("biggerFontAccessibility").style.display = "none";
    document.getElementById("biggestFontAccessibility").style.display = "block";
  };


  document.getElementById("biggerFontAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.fontSize = "xx-large";
      }
      document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
      document.getElementById("accessibilityFont").style.fontSize = "28px;";
      document.getElementById("biggestFontAccessibility").style.border = "1px solid #098cff";
      document.getElementById("biggestFontAccessibility").style.borderRadius = "0px";
      document.getElementById("biggerFontAccessibility").style.display = "none";
      document.getElementById("biggestFontAccessibility").style.display = "block";
      document.getElementById("biggestFontAccessibility").tabIndex = "0";
    }
  });  

  document.getElementById('biggestFontAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.fontSize = "";
    }
    document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
    document.getElementById("accessibilityFont").style.fontSize = "30px;";
    document.getElementById("normalFontAccessibility").style.border = "";
    document.getElementById("normalFontAccessibility").style.borderRadius = "";
    document.getElementById("biggestFontAccessibility").style.display = "none";
    document.getElementById("normalFontAccessibility").style.display = "block";
  };

  document.getElementById("biggestFontAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.fontSize = "";
      }
      document.getElementById("closeButton").style.setProperty('font-size', '15px', 'important');
      document.getElementById("accessibilityFont").style.fontSize = "30px;";
      document.getElementById("normalFontAccessibility").style.border = "";
      document.getElementById("normalFontAccessibility").style.borderRadius = "";
      document.getElementById("biggestFontAccessibility").style.display = "none";
      document.getElementById("normalFontAccessibility").style.display = "block";
      document.getElementById("normalFontAccessibility").tabIndex = "0";
    }
  });   


  document.getElementById('normalCursor').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.cursor = "url('cursorBigger.png'), auto";
    }
    document.getElementById("biggerCursor").style.border = "thin solid #098cff";
    document.getElementById("biggerCursor").style.borderRadius = "0px";
    document.getElementById("normalCursor").style.display = "none";
    document.getElementById("biggerCursor").style.display = "block";
  };


  document.getElementById("normalCursor").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.cursor = "url('cursorBigger.png'), auto";
      }
      document.getElementById("biggerCursor").style.border = "thin solid #098cff";
      document.getElementById("biggerCursor").style.borderRadius = "0px";
      document.getElementById("normalCursor").style.display = "none";
      document.getElementById("biggerCursor").style.display = "block";
      document.getElementById("biggerCursor").tabIndex = "0";
    }
  });  


  document.getElementById('biggerCursor').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body');
    elementToChange1[0].onmousemove = function (e) {
      var x = e.clientX;
      var y = e.clientY;
      let height = screen.height;
      let hei = height - y - 100;
      //var coor = "Coordinates: (" + x + "," + y + ")";
      //document.getElementById("demo").innerHTML = coor;
      document.getElementById("maskmain").style.display = "block";
      document.getElementById("maskmain").style.position = "fixed";
      document.getElementById("mask1").style.height = y - 50 + "px";
      document.getElementById("mask2").style.height = hei + "px";
    };
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.cursor = "";
    }
    document.getElementById("readMaskAccessibility").style.border = "thin solid #098cff";
    document.getElementById("readMaskAccessibility").style.borderRadius = "0px";
    document.getElementById("biggerCursor").style.display = "none";
    document.getElementById("readMaskAccessibility").style.display = "block";
  };



  document.getElementById("biggerCursor").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body');
      elementToChange1[0].onmousemove = function (e) {
        var x = e.clientX;
        var y = e.clientY;
        let height = screen.height;
        let hei = height - y - 100;
        //var coor = "Coordinates: (" + x + "," + y + ")";
        //document.getElementById("demo").innerHTML = coor;
        document.getElementById("maskmain").style.display = "block";
        document.getElementById("maskmain").style.position = "fixed";
        document.getElementById("mask1").style.height = y - 50 + "px";
        document.getElementById("mask2").style.height = hei + "px";
      };
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.cursor = "";
      }
      document.getElementById("readMaskAccessibility").style.border = "thin solid #098cff";
      document.getElementById("readMaskAccessibility").style.borderRadius = "0px";
      document.getElementById("biggerCursor").style.display = "none";
      document.getElementById("readMaskAccessibility").style.display = "block";
      document.getElementById("readMaskAccessibility").tabIndex = "0";

}
  });

  document.getElementById('readMaskAccessibility').onclick = function () {
    document.getElementById("maskmain").style.display = "none";
    var elementToChange = document.querySelectorAll('body');
    elementToChange[0].onmousemove = function (e) {
      document.getElementById("maskmain").style.display = "none";
      document.getElementById("maskmain").style.position = "";
      document.getElementById("mask1").style.height = "0";
      document.getElementById("mask2").style.height = "0";

      var x = e.clientX;
      var y = e.clientY;
      let height = screen.height;
      let hei = height - y - 100;
      let width = screen.width;
      let maskreadwidth = width * 50 / 100;
      maskreadMarginL = x - maskreadwidth / 2;
      maskreadMarginR = width * 25 / 100;
      document.getElementById("maskmainread").style.display = "block";
      document.getElementById("maskmainread").style.position = "fixed";
      document.getElementById("maskread").style.height = y - 50 + "px";
      if (maskreadMarginL <= 0) {
        document.getElementById("maskreadLine").style.marginLeft = "0px";
      }
      else if (maskreadMarginR >= width - x) {
        document.getElementById("maskreadLine").style.marginLeft = width * 50 / 100 + "px";
      } else {
        document.getElementById("maskreadLine").style.marginLeft = maskreadMarginL + "px";
      }
      document.getElementById("maskarrow-down").style.marginLeft = x + "px";
    };
    document.getElementById("readLineAccessibility").style.border = "thin solid #098cff";
    document.getElementById("readLineAccessibility").style.borderRadius = "0px";
    document.getElementById("readMaskAccessibility").style.display = "none";
    document.getElementById("readLineAccessibility").style.display = "block";
  };


  document.getElementById("readMaskAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      document.getElementById("maskmain").style.display = "none";
      var elementToChange = document.querySelectorAll('body');
      elementToChange[0].onmousemove = function (e) {
        document.getElementById("maskmain").style.display = "none";
        document.getElementById("maskmain").style.position = "";
        document.getElementById("mask1").style.height = "0";
        document.getElementById("mask2").style.height = "0";
  
        var x = e.clientX;
        var y = e.clientY;
        let height = screen.height;
        let hei = height - y - 100;
        let width = screen.width;
        let maskreadwidth = width * 50 / 100;
        maskreadMarginL = x - maskreadwidth / 2;
        maskreadMarginR = width * 25 / 100;
        document.getElementById("maskmainread").style.display = "block";
        document.getElementById("maskmainread").style.position = "fixed";
        document.getElementById("maskread").style.height = y - 50 + "px";
        if (maskreadMarginL <= 0) {
          document.getElementById("maskreadLine").style.marginLeft = "0px";
        }
        else if (maskreadMarginR >= width - x) {
          document.getElementById("maskreadLine").style.marginLeft = width * 50 / 100 + "px";
        } else {
          document.getElementById("maskreadLine").style.marginLeft = maskreadMarginL + "px";
        }
        document.getElementById("maskarrow-down").style.marginLeft = x + "px";
      };
      document.getElementById("readLineAccessibility").style.border = "thin solid #098cff";
      document.getElementById("readLineAccessibility").style.borderRadius = "0px";
      document.getElementById("readMaskAccessibility").style.display = "none";
      document.getElementById("readLineAccessibility").style.display = "block";
      document.getElementById("readLineAccessibility").tabIndex = "0";

}
  });


  document.getElementById('readLineAccessibility').onclick = function () {
    document.getElementById("maskmainread").style.display = "none";
    var elementToChange1 = document.querySelectorAll('body');
    elementToChange1[0].onmousemove = function (e) {
      document.getElementById("maskmainread").style.display = "none";
      document.getElementById("maskmainread").style.position = "";
    };
    document.getElementById("normalCursor").style.border = "";
    document.getElementById("normalCursor").style.borderRadius = "";
    document.getElementById("readLineAccessibility").style.display = "none";
    document.getElementById("normalCursor").style.display = "block";
  };


  document.getElementById("readLineAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      document.getElementById("maskmainread").style.display = "none";
      var elementToChange1 = document.querySelectorAll('body');
      elementToChange1[0].onmousemove = function (e) {
        document.getElementById("maskmainread").style.display = "none";
        document.getElementById("maskmainread").style.position = "";
      };
      document.getElementById("normalCursor").style.border = "";
      document.getElementById("normalCursor").style.borderRadius = "";
      document.getElementById("readLineAccessibility").style.display = "none";
      document.getElementById("normalCursor").style.display = "block";
      document.getElementById("normalCursor").tabIndex = "0";

    }
  });

  document.getElementById('linkAccessibility').onclick = function () {
    let link = document.getElementsByTagName('a');
    for (let i = 0; i < link.length; i++) {
      link[i].style.setProperty('color', '#FFFF00', 'important');
      link[i].style.backgroundColor = "#000";
      link[i].style.fontWeight = "bold";
    }
    let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
    for (let i = 0; i < links.length; i++) {
      links[i].style.color = "inherit";
    }
    document.getElementById("highlightLinkAccessibility").style.border = "1px solid #098cff";
    document.getElementById("highlightLinkAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("closeButton").style.fontWeight = "normal";
    document.getElementById("linkAccessibility").style.display = "none";
    document.getElementById("highlightLinkAccessibility").style.display = "block";
  };


  document.getElementById("linkAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      let link = document.getElementsByTagName('a');
      for (let i = 0; i < link.length; i++) {
        link[i].style.setProperty('color', '#FFFF00', 'important');
        link[i].style.backgroundColor = "#000";
        link[i].style.fontWeight = "bold";
      }
      let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
      for (let i = 0; i < links.length; i++) {
        links[i].style.color = "inherit";
      }
      document.getElementById("highlightLinkAccessibility").style.border = "1px solid #098cff";
      document.getElementById("highlightLinkAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.background = "#024d64";
      document.getElementById("closeButton").style.fontWeight = "normal";
      document.getElementById("linkAccessibility").style.display = "none";
      document.getElementById("highlightLinkAccessibility").style.display = "block";
      document.getElementById("highlightLinkAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('highlightLinkAccessibility').onclick = function () {
    let link = document.getElementsByTagName('a');
    for (let i = 0; i < link.length; i++) {
      link[i].style.setProperty('color', '', 'important');
      link[i].style.backgroundColor = "";
      link[i].style.fontWeight = "";
    }
    let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
    for (let i = 0; i < links.length; i++) {
      links[i].style.color = "";
    }
    document.getElementById("linkAccessibility").style.border = "";
    document.getElementById("linkAccessibility").style.borderRadius = "";
    document.getElementById("closeButton").style.background = "#024d64";
    document.getElementById("closeButton").style.fontWeight = "normal";
    document.getElementById("highlightLinkAccessibility").style.display = "none";
    document.getElementById("linkAccessibility").style.display = "block";
  };

  document.getElementById("highlightLinkAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      let link = document.getElementsByTagName('a');
      for (let i = 0; i < link.length; i++) {
        link[i].style.setProperty('color', '', 'important');
        link[i].style.backgroundColor = "";
        link[i].style.fontWeight = "";
      }
      let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
      for (let i = 0; i < links.length; i++) {
        links[i].style.color = "";
      }
      document.getElementById("linkAccessibility").style.border = "";
      document.getElementById("linkAccessibility").style.borderRadius = "";
      document.getElementById("closeButton").style.background = "#024d64";
      document.getElementById("closeButton").style.fontWeight = "normal";
      document.getElementById("highlightLinkAccessibility").style.display = "none";
      document.getElementById("linkAccessibility").style.display = "block";
      document.getElementById("linkAccessibility").tabIndex = "0";
    }
  });  


  document.getElementById('normalTextSpace').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('letter-spacing', '.12em', 'important');
      elementToChange1[i].style.setProperty('word-spacing', '.16em', 'important');
    }
    document.getElementById("bigTextSpace").style.border = "1px solid #098cff";
    document.getElementById("bigTextSpace").style.borderRadius = "0px";
    document.getElementById("bigTextSpace").style.setProperty('letter-spacing', '', 'important');
    document.getElementById("bigTextSpace").style.setProperty('word-spacing', '', 'important');
    document.getElementById("normalTextSpace").style.display = "none";
    document.getElementById("bigTextSpace").style.display = "block";
  };

  document.getElementById("normalTextSpace").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('letter-spacing', '.12em', 'important');
        elementToChange1[i].style.setProperty('word-spacing', '.16em', 'important');
      }
      document.getElementById("bigTextSpace").style.border = "1px solid #098cff";
      document.getElementById("bigTextSpace").style.borderRadius = "0px";
      document.getElementById("bigTextSpace").style.setProperty('letter-spacing', '', 'important');
      document.getElementById("bigTextSpace").style.setProperty('word-spacing', '', 'important');
      document.getElementById("normalTextSpace").style.display = "none";
      document.getElementById("bigTextSpace").style.display = "block";
      document.getElementById("bigTextSpace").tabIndex = "0";
    }
  }); 


  document.getElementById('bigTextSpace').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('letter-spacing', '.24em', 'important');
      elementToChange1[i].style.setProperty('word-spacing', '.32em', 'important');
    }
    document.getElementById("biggerTextSpace").style.border = "1px solid #098cff";
    document.getElementById("biggerTextSpace").style.borderRadius = "0px";
    document.getElementById("biggerTextSpace").style.setProperty('letter-spacing', '', 'important');
    document.getElementById("biggerTextSpace").style.setProperty('word-spacing', '', 'important');
    document.getElementById("bigTextSpace").style.display = "none";
    document.getElementById("biggerTextSpace").style.display = "block";
  };


  document.getElementById("bigTextSpace").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('letter-spacing', '.24em', 'important');
        elementToChange1[i].style.setProperty('word-spacing', '.32em', 'important');
      }
      document.getElementById("biggerTextSpace").style.border = "1px solid #098cff";
      document.getElementById("biggerTextSpace").style.borderRadius = "0px";
      document.getElementById("biggerTextSpace").style.setProperty('letter-spacing', '', 'important');
      document.getElementById("biggerTextSpace").style.setProperty('word-spacing', '', 'important');
      document.getElementById("bigTextSpace").style.display = "none";
      document.getElementById("biggerTextSpace").style.display = "block";
      document.getElementById("biggerTextSpace").tabIndex = "0";

    }
  });


  document.getElementById('biggerTextSpace').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('letter-spacing', '.36em', 'important');
      elementToChange1[i].style.setProperty('word-spacing', '.48em', 'important');
    }
    document.getElementById("biggestTextSpace").style.border = "1px solid #098cff";
    document.getElementById("biggestTextSpace").style.borderRadius = "0px";
    document.getElementById("biggestTextSpace").style.setProperty('letter-spacing', '', 'important');
    document.getElementById("biggestTextSpace").style.setProperty('word-spacing', '', 'important');
    document.getElementById("biggerTextSpace").style.display = "none";
    document.getElementById("biggestTextSpace").style.display = "block";
  };


  document.getElementById("biggerTextSpace").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('letter-spacing', '.36em', 'important');
        elementToChange1[i].style.setProperty('word-spacing', '.48em', 'important');
      }
      document.getElementById("biggestTextSpace").style.border = "1px solid #098cff";
      document.getElementById("biggestTextSpace").style.borderRadius = "0px";
      document.getElementById("biggestTextSpace").style.setProperty('letter-spacing', '', 'important');
      document.getElementById("biggestTextSpace").style.setProperty('word-spacing', '', 'important');
      document.getElementById("biggerTextSpace").style.display = "none";
      document.getElementById("biggestTextSpace").style.display = "block";
      document.getElementById("biggestTextSpace").tabIndex = "0";
    }
  });


  document.getElementById('biggestTextSpace').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('letter-spacing', '', 'important');
      elementToChange1[i].style.setProperty('word-spacing', '', 'important');
    }
    document.getElementById("normalTextSpace").style.border = "";
    document.getElementById("normalTextSpace").style.borderRadius = "";
    document.getElementById("normalTextSpace").style.setProperty('letter-spacing', '', 'important');
    document.getElementById("normalTextSpace").style.setProperty('word-spacing', '', 'important');
    document.getElementById("biggestTextSpace").style.display = "none";
    document.getElementById("normalTextSpace").style.display = "block";
  };

  document.getElementById("biggestTextSpace").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('letter-spacing', '', 'important');
        elementToChange1[i].style.setProperty('word-spacing', '', 'important');
      }
      document.getElementById("normalTextSpace").style.border = "";
      document.getElementById("normalTextSpace").style.borderRadius = "";
      document.getElementById("normalTextSpace").style.setProperty('letter-spacing', '', 'important');
      document.getElementById("normalTextSpace").style.setProperty('word-spacing', '', 'important');
      document.getElementById("biggestTextSpace").style.display = "none";
      document.getElementById("normalTextSpace").style.display = "block";
      document.getElementById("normalTextSpace").tabIndex = "0";
    }
  });


  document.getElementById('nonDyslexiaAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('font-family', 'comic sans MS, sans serif', 'important');
    }
    document.getElementById("closeButton").style.setProperty('font-family', 'Open Sans, sans-serif', 'important');
    document.getElementById("dyslexiaAccessibility").style.border = "1px solid #098cff";
    document.getElementById("dyslexiaAccessibility").style.borderRadius = "0px";
    document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
    document.getElementById("nonDyslexiaAccessibility").style.display = "none";
    document.getElementById("dyslexiaAccessibility").style.display = "block";
  };


  document.getElementById("nonDyslexiaAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('font-family', 'comic sans MS, sans serif', 'important');
      }
      document.getElementById("closeButton").style.setProperty('font-family', 'Open Sans, sans-serif', 'important');
      document.getElementById("dyslexiaAccessibility").style.border = "1px solid #098cff";
      document.getElementById("dyslexiaAccessibility").style.borderRadius = "0px";
      document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
      document.getElementById("nonDyslexiaAccessibility").style.display = "none";
      document.getElementById("dyslexiaAccessibility").style.display = "block";
      document.getElementById("dyslexiaAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('dyslexiaAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('font-family', 'arial, serif', 'important');
    }
    document.getElementById("legibleAccessibility").style.border = "1px solid #098cff";
    document.getElementById("legibleAccessibility").style.borderRadius = "0px";
    document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
    document.getElementById("dyslexiaAccessibility").style.display = "none";
    document.getElementById("legibleAccessibility").style.display = "block";
  };


  document.getElementById("dyslexiaAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('font-family', 'arial, serif', 'important');
      }
      document.getElementById("legibleAccessibility").style.border = "1px solid #098cff";
      document.getElementById("legibleAccessibility").style.borderRadius = "0px";
      document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
      document.getElementById("dyslexiaAccessibility").style.display = "none";
      document.getElementById("legibleAccessibility").style.display = "block";
      document.getElementById("legibleAccessibility").tabIndex = "0";
    }
  }); 

  document.getElementById('legibleAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('font-family', '', 'important');
    }
    document.getElementById("nonDyslexiaAccessibility").style.border = "";
    document.getElementById("nonDyslexiaAccessibility").style.borderRadius = "";
    document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
    document.getElementById("legibleAccessibility").style.display = "none";
    document.getElementById("nonDyslexiaAccessibility").style.display = "block";
  };


  document.getElementById("legibleAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('font-family', '', 'important');
      }
      document.getElementById("nonDyslexiaAccessibility").style.border = "";
      document.getElementById("nonDyslexiaAccessibility").style.borderRadius = "";
      document.getElementById('accessibilityFont').style.setProperty('font-family', '', 'important');
      document.getElementById("legibleAccessibility").style.display = "none";
      document.getElementById("nonDyslexiaAccessibility").style.display = "block";
      document.getElementById("nonDyslexiaAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('normalLineHeight').onclick = function () {
    var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.lineHeight = '';
      elementToChange1[i].style.setProperty('line-height', '1.75', 'important');
    }
    document.getElementById("lineHeight175x").style.border = "1px solid #098cff";
    document.getElementById("lineHeight175x").style.borderRadius = "0px";
    document.getElementById("closeButton").style.lineHeight = "";
    document.getElementById("normalLineHeight").style.display = "none";
    document.getElementById("lineHeight175x").style.display = "block";
  };

  document.getElementById("normalLineHeight").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.lineHeight = '';
        elementToChange1[i].style.setProperty('line-height', '1.75', 'important');
      }
      document.getElementById("lineHeight175x").style.border = "1px solid #098cff";
      document.getElementById("lineHeight175x").style.borderRadius = "0px";
      document.getElementById("closeButton").style.lineHeight = "";
      document.getElementById("normalLineHeight").style.display = "none";
      document.getElementById("lineHeight175x").style.display = "block";
      document.getElementById("lineHeight175x").tabIndex = "0";
    }
  });


  document.getElementById('lineHeight175x').onclick = function () {
    var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.lineHeight = '';
      elementToChange1[i].style.setProperty('line-height', '2', 'important');
    }
    document.getElementById("lineHeight200x").style.border = "1px solid #098cff";
    document.getElementById("lineHeight200x").style.borderRadius = "0px";
    document.getElementById("closeButton").style.lineHeight = "";
    document.getElementById("lineHeight175x").style.display = "none";
    document.getElementById("lineHeight200x").style.display = "block";
  };

  document.getElementById("lineHeight175x").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.lineHeight = '';
        elementToChange1[i].style.setProperty('line-height', '2', 'important');
      }
      document.getElementById("lineHeight200x").style.border = "1px solid #098cff";
      document.getElementById("lineHeight200x").style.borderRadius = "0px";
      document.getElementById("closeButton").style.lineHeight = "";
      document.getElementById("lineHeight175x").style.display = "none";
      document.getElementById("lineHeight200x").style.display = "block";
      document.getElementById("lineHeight200x").tabIndex = "0";
    }
  });


  document.getElementById('lineHeight200x').onclick = function () {
    var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.lineHeight = '';
      elementToChange1[i].style.setProperty('line-height', '2.5', 'important');
    }
    document.getElementById("lineHeight250x").style.border = "1px solid #098cff";
    document.getElementById("lineHeight250x").style.borderRadius = "0px";
    document.getElementById("closeButton").style.lineHeight = "";
    document.getElementById("lineHeight200x").style.display = "none";
    document.getElementById("lineHeight250x").style.display = "block";
  };

  document.getElementById("lineHeight200x").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.lineHeight = '';
        elementToChange1[i].style.setProperty('line-height', '2.5', 'important');
      }
      document.getElementById("lineHeight250x").style.border = "1px solid #098cff";
      document.getElementById("lineHeight250x").style.borderRadius = "0px";
      document.getElementById("closeButton").style.lineHeight = "";
      document.getElementById("lineHeight200x").style.display = "none";
      document.getElementById("lineHeight250x").style.display = "block";
      document.getElementById("lineHeight250x").tabIndex = "0";
    }
  });


  document.getElementById('lineHeight250x').onclick = function () {
    var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.lineHeight = '';
    }
    document.getElementById("normalLineHeight").style.border = "";
    document.getElementById("normalLineHeight").style.borderRadius = "";
    document.getElementById("closeButton").style.lineHeight = "";
    document.getElementById("lineHeight250x").style.display = "none";
    document.getElementById("normalLineHeight").style.display = "block";
  };

  document.getElementById("lineHeight250x").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.lineHeight = '';
      }
      document.getElementById("normalLineHeight").style.border = "";
      document.getElementById("normalLineHeight").style.borderRadius = "";
      document.getElementById("closeButton").style.lineHeight = "";
      document.getElementById("lineHeight250x").style.display = "none";
      document.getElementById("normalLineHeight").style.display = "block";
      document.getElementById("normalLineHeight").tabIndex = "0";
    }
  });


  document.getElementById('noAlignAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "right";
    }
    document.getElementById("rightAlignAccessibility").style.border = "1px solid #098cff";
    document.getElementById("rightAlignAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("noAlignAccessibility").style.display = "none";
    document.getElementById("rightAlignAccessibility").style.display = "block";
  };

  document.getElementById("noAlignAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "right";
      }
      document.getElementById("rightAlignAccessibility").style.border = "1px solid #098cff";
      document.getElementById("rightAlignAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("noAlignAccessibility").style.display = "none";
      document.getElementById("rightAlignAccessibility").style.display = "block";
      document.getElementById("rightAlignAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('rightAlignAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "center";
    }
    document.getElementById("centerAlignAccessibility").style.border = "1px solid #098cff";
    document.getElementById("centerAlignAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("rightAlignAccessibility").style.display = "none";
    document.getElementById("centerAlignAccessibility").style.display = "block";
  };

  document.getElementById("rightAlignAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "center";
      }
      document.getElementById("centerAlignAccessibility").style.border = "1px solid #098cff";
      document.getElementById("centerAlignAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("rightAlignAccessibility").style.display = "none";
      document.getElementById("centerAlignAccessibility").style.display = "block";
      document.getElementById("centerAlignAccessibility").tabIndex = "0";
    }
  });

  document.getElementById('centerAlignAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "left";
    }
    document.getElementById("leftAlignAccessibility").style.border = "1px solid #098cff";
    document.getElementById("leftAlignAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("centerAlignAccessibility").style.display = "none";
    document.getElementById("leftAlignAccessibility").style.display = "block";
  };

  document.getElementById("centerAlignAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "left";
      }
      document.getElementById("leftAlignAccessibility").style.border = "1px solid #098cff";
      document.getElementById("leftAlignAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("centerAlignAccessibility").style.display = "none";
      document.getElementById("leftAlignAccessibility").style.display = "block";
      document.getElementById("leftAlignAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('leftAlignAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "justify";
    }
    document.getElementById("justifyAlignAccessibility").style.border = "1px solid #098cff";
    document.getElementById("justifyAlignAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("leftAlignAccessibility").style.display = "none";
    document.getElementById("justifyAlignAccessibility").style.display = "block";
  };

  document.getElementById("leftAlignAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "justify";
      }
      document.getElementById("justifyAlignAccessibility").style.border = "1px solid #098cff";
      document.getElementById("justifyAlignAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("leftAlignAccessibility").style.display = "none";
      document.getElementById("justifyAlignAccessibility").style.display = "block";
      document.getElementById("justifyAlignAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('justifyAlignAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "";
    }
    document.getElementById("noAlignAccessibility").style.border = "";
    document.getElementById("noAlignAccessibility").style.borderRadius = "";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("justifyAlignAccessibility").style.display = "none";
    document.getElementById("noAlignAccessibility").style.display = "block";
  };


  document.getElementById("justifyAlignAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "";
      }
      document.getElementById("noAlignAccessibility").style.border = "";
      document.getElementById("noAlignAccessibility").style.borderRadius = "";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("justifyAlignAccessibility").style.display = "none";
      document.getElementById("noAlignAccessibility").style.display = "block";
      document.getElementById("noAlignAccessibility").tabIndex = "0";
    }
  });


  document.getElementById('toggleVideoAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        var iframeSrc = elementToChange1[i].src;
        elementToChange1[i].src = iframeSrc;
      }
    }
    var elementToChange1 = document.querySelectorAll('video');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        elementToChange1[i].pause();
      }
    }
    var elementToChange1 = document.querySelectorAll('img');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        elementToChange1[i].style.setProperty('animation-play-state', 'paused', 'important');
        elementToChange1[i].style.setProperty('-moz-animation-play-state', 'paused', 'important');
        elementToChange1[i].style.setProperty('-webkit-animation-play-state', 'paused', 'important');
        elementToChange1[i].style.setProperty('-o-animation-play-state', 'paused', 'important');
      }
    }
    document.getElementById("pauseVideoAccessibility").style.border = "1px solid #098cff";
    document.getElementById("pauseVideoAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("toggleVideoAccessibility").style.display = "none";
    document.getElementById("pauseVideoAccessibility").style.display = "block";
  };


  document.getElementById("toggleVideoAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          var iframeSrc = elementToChange1[i].src;
          elementToChange1[i].src = iframeSrc;
        }
      }
      var elementToChange1 = document.querySelectorAll('video');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          elementToChange1[i].pause();
        }
      }
      var elementToChange1 = document.querySelectorAll('img');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          elementToChange1[i].style.setProperty('animation-play-state', 'paused', 'important');
          elementToChange1[i].style.setProperty('-moz-animation-play-state', 'paused', 'important');
          elementToChange1[i].style.setProperty('-webkit-animation-play-state', 'paused', 'important');
          elementToChange1[i].style.setProperty('-o-animation-play-state', 'paused', 'important');
        }
      }
      document.getElementById("pauseVideoAccessibility").style.border = "1px solid #098cff";
      document.getElementById("pauseVideoAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("toggleVideoAccessibility").style.display = "none";
      document.getElementById("pauseVideoAccessibility").style.display = "block";
      document.getElementById("pauseVideoAccessibility").tabIndex = "0";
    }
  }); 


  document.getElementById('pauseVideoAccessibility').onclick = function () {
    var elementToChange1 = document.querySelectorAll('iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        var iframeSrc = elementToChange1[i].src;
        //alert(iframeSrc);
        elementToChange1[i].src += "&autoplay=1";
        //alert(elementToChange1[i].src);

      }
    }
    var elementToChange1 = document.querySelectorAll('video');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {

        elementToChange1[i].play();
      }
    }
    var elementToChange1 = document.querySelectorAll('img');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        elementToChange1[i].style.setProperty('animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-moz-animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-webkit-animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-o-animation-play-state', '', 'important');
      }
    }
    document.getElementById("toggleVideoAccessibility").style.border = "";
    document.getElementById("toggleVideoAccessibility").style.borderRadius = "";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("pauseVideoAccessibility").style.display = "none";
    document.getElementById("toggleVideoAccessibility").style.display = "block";
  };


  document.getElementById("pauseVideoAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elementToChange1 = document.querySelectorAll('iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          var iframeSrc = elementToChange1[i].src;
          //alert(iframeSrc);
          elementToChange1[i].src += "&autoplay=1";
          //alert(elementToChange1[i].src);
  
        }
      }
      var elementToChange1 = document.querySelectorAll('video');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
  
          elementToChange1[i].play();
        }
      }
      var elementToChange1 = document.querySelectorAll('img');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          elementToChange1[i].style.setProperty('animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-moz-animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-webkit-animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-o-animation-play-state', '', 'important');
        }
      }
      document.getElementById("toggleVideoAccessibility").style.border = "";
      document.getElementById("toggleVideoAccessibility").style.borderRadius = "";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("pauseVideoAccessibility").style.display = "none";
      document.getElementById("toggleVideoAccessibility").style.display = "block";
      document.getElementById("toggleVideoAccessibility").tabIndex = "0";
    }
  }); 


  document.getElementById('toggleTooltipAccessibility').onclick = function () {
    var elements1 = document.querySelectorAll('a,p,div,span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].classList.toggle("show");
    }
    var elements1 = document.querySelectorAll('span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.visibility = "visible";
    }
    document.getElementById("showTooltipAccessibility").style.border = "1px solid #098cff";
    document.getElementById("showTooltipAccessibility").style.borderRadius = "0px";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("toggleTooltipAccessibility").style.display = "none";
    document.getElementById("showTooltipAccessibility").style.display = "block";
  };

  document.getElementById("toggleTooltipAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements1 = document.querySelectorAll('a,p,div,span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].classList.toggle("show");
      }
      var elements1 = document.querySelectorAll('span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.visibility = "visible";
      }
      document.getElementById("showTooltipAccessibility").style.border = "1px solid #098cff";
      document.getElementById("showTooltipAccessibility").style.borderRadius = "0px";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("toggleTooltipAccessibility").style.display = "none";
      document.getElementById("showTooltipAccessibility").style.display = "block";
      document.getElementById("showTooltipAccessibility").tabIndex = "0";
    }
  }); 


  document.getElementById('showTooltipAccessibility').onclick = function () {
    var elements1 = document.querySelectorAll('a,p,div,span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].classList.toggle("show");
    }
    var elements1 = document.querySelectorAll('span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.visibility = "";
    }
    document.getElementById("toggleTooltipAccessibility").style.border = "";
    document.getElementById("toggleTooltipAccessibility").style.borderRadius = "";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("showTooltipAccessibility").style.display = "none";
    document.getElementById("toggleTooltipAccessibility").style.display = "block";
  };

  document.getElementById("showTooltipAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){

      var elements1 = document.querySelectorAll('a,p,div,span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].classList.toggle("show");
      }
      var elements1 = document.querySelectorAll('span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.visibility = "";
      }
      document.getElementById("toggleTooltipAccessibility").style.border = "";
      document.getElementById("toggleTooltipAccessibility").style.borderRadius = "";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("showTooltipAccessibility").style.display = "none";
      document.getElementById("toggleTooltipAccessibility").style.display = "block";
      document.getElementById("toggleTooltipAccessibility").tabIndex = "0";
}
  });

  document.getElementById('resetAccessibility').onclick = function () {
    var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.setProperty('color', '', 'important');
      elements[i].style.background = "";
    }
    var elements1 = document.querySelectorAll('img,video,section');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.filter = "";
    }
    var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.fontSize = "";
    }
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.cursor = "";
    }

    var elementToChange = document.querySelectorAll('body');
    document.getElementById("maskmain").style.display = "none";
    document.getElementById("maskmainread").style.display = "none";
    elementToChange[0].onmousemove = function (e) {
      document.getElementById("maskmain").style.display = "none";
      document.getElementById("maskmain").style.position = "";
      document.getElementById("mask1").style.height = "0";
      document.getElementById("mask2").style.height = "0";
      document.getElementById("maskmainread").style.display = "none";
      document.getElementById("maskmainread").style.position = "";
    };

    let link = document.getElementsByTagName('a');
    for (let i = 0; i < link.length; i++) {
      link[i].style.setProperty('color', '', 'important');
      link[i].style.backgroundColor = "";
      link[i].style.fontWeight = "";
    }
    let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
    for (let i = 0; i < links.length; i++) {
      links[i].style.color = "";
    }

    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('letter-spacing', '', 'important');
      elementToChange1[i].style.setProperty('word-spacing', '', 'important');
    }

    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.setProperty('font-family', '', 'important');
    }
    var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.lineHeight = '';
    }
    var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      elementToChange1[i].style.textAlign = "";
    }

    var elementToChange1 = document.querySelectorAll('iframe');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        var iframeSrc = elementToChange1[i].src;
        elementToChange1[i].src += "&autoplay=1";
      }
    }
    var elementToChange1 = document.querySelectorAll('video');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {

        elementToChange1[i].play();
      }
    }
    var elementToChange1 = document.querySelectorAll('img');
    for (var i = 0; i < elementToChange1.length; i++) {
      if (elementToChange1[i]) {
        elementToChange1[i].style.setProperty('animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-moz-animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-webkit-animation-play-state', '', 'important');
        elementToChange1[i].style.setProperty('-o-animation-play-state', '', 'important');
      }
    }

    var elements1 = document.querySelectorAll('a,p,div,span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].classList.remove("show");
    }
    var elements1 = document.querySelectorAll('span');
    for (var i = 0; i < elements1.length; i++) {
      elements1[i].style.visibility = "none";
    }

    document.getElementById('contrastInvert').style.display = "none";
    document.getElementById('contrastLight').style.display = "none";
    document.getElementById('contrastDark').style.display = "none";
    document.getElementById('contrastDesaturate').style.display = "none";
    document.getElementById('noContrast').style.display = "block";
    document.getElementById('noContrast').style.border = "";


    document.getElementById('bigFontAccessibility').style.display = "none";
    document.getElementById('biggerFontAccessibility').style.display = "none";
    document.getElementById('biggestFontAccessibility').style.display = "none";
    document.getElementById('normalFontAccessibility').style.display = "block";
    document.getElementById('normalFontAccessibility').style.border = "";


    document.getElementById('biggerCursor').style.display = "none";
    document.getElementById('normalCursor').style.display = "block";
    document.getElementById('normalCursor').style.border = "";
    document.getElementById("readLineAccessibility").style.display = "none";
    document.getElementById("readMaskAccessibility").style.display = "none";


    document.getElementById('bigTextSpace').style.display = "none";
    document.getElementById('biggerTextSpace').style.display = "none";
    document.getElementById('biggestTextSpace').style.display = "none";
    document.getElementById('normalTextSpace').style.display = "block";
    document.getElementById('normalTextSpace').style.border = "";


    document.getElementById('highlightLinkAccessibility').style.display = "none";
    document.getElementById('linkAccessibility').style.display = "block";
    document.getElementById('linkAccessibility').style.border = "";


    document.getElementById('dyslexiaAccessibility').style.display = "none";
    document.getElementById('legibleAccessibility').style.display = "none";
    document.getElementById('nonDyslexiaAccessibility').style.display = "block";
    document.getElementById('nonDyslexiaAccessibility').style.border = "";


    document.getElementById('lineHeight175x').style.display = "none";
    document.getElementById('lineHeight200x').style.display = "none";
    document.getElementById('lineHeight250x').style.display = "none";
    document.getElementById('normalLineHeight').style.display = "block";
    document.getElementById('normalLineHeight').style.border = "";


    document.getElementById('rightAlignAccessibility').style.display = "none";
    document.getElementById('centerAlignAccessibility').style.display = "none";
    document.getElementById('leftAlignAccessibility').style.display = "none";
    document.getElementById('justifyAlignAccessibility').style.display = "none";
    document.getElementById('noAlignAccessibility').style.display = "block";
    document.getElementById('noAlignAccessibility').style.border = "";


    document.getElementById("toggleVideoAccessibility").style.border = "";
    document.getElementById("toggleVideoAccessibility").style.borderRadius = "";
    document.getElementById("closeButton").style.textAlign = "";
    document.getElementById("pauseVideoAccessibility").style.display = "none";
    document.getElementById("toggleVideoAccessibility").style.display = "block";


    document.getElementById("toggleTooltipAccessibility").style.border = "";
    document.getElementById("toggleTooltipAccessibility").style.borderRadius = "";
    document.getElementById("showTooltipAccessibility").style.display = "none";
    document.getElementById("toggleTooltipAccessibility").style.display = "block";

    document.querySelector('.skiptomain').style.color = "#f5e6ba";
  };


  document.getElementById("resetAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      var elements = document.querySelectorAll('a,p,li,body,button,input,span,h1,h2,h3,h4,h5,h6,iframe');
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.setProperty('color', '', 'important');
        elements[i].style.background = "";
      }
      var elements1 = document.querySelectorAll('img,video,section');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.filter = "";
      }
      var elementToChange1 = document.querySelectorAll('body,a,p,li,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.fontSize = "";
      }
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.cursor = "";
      }
  
      var elementToChange = document.querySelectorAll('body');
      document.getElementById("maskmain").style.display = "none";
      document.getElementById("maskmainread").style.display = "none";
      elementToChange[0].onmousemove = function (e) {
        document.getElementById("maskmain").style.display = "none";
        document.getElementById("maskmain").style.position = "";
        document.getElementById("mask1").style.height = "0";
        document.getElementById("mask2").style.height = "0";
        document.getElementById("maskmainread").style.display = "none";
        document.getElementById("maskmainread").style.position = "";
      };
  
      let link = document.getElementsByTagName('a');
      for (let i = 0; i < link.length; i++) {
        link[i].style.setProperty('color', '', 'important');
        link[i].style.backgroundColor = "";
        link[i].style.fontWeight = "";
      }
      let links = document.querySelectorAll('button,p,li,span,i,h1,h2,h3,h4,h5,h6');
      for (let i = 0; i < links.length; i++) {
        links[i].style.color = "";
      }
  
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('letter-spacing', '', 'important');
        elementToChange1[i].style.setProperty('word-spacing', '', 'important');
      }
  
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.setProperty('font-family', '', 'important');
      }
      var elementToChange1 = document.querySelectorAll('a,p,li,div,button,input,span');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.lineHeight = '';
      }
      var elementToChange1 = document.querySelectorAll('body,a,p,li,div,button,input,span,iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        elementToChange1[i].style.textAlign = "";
      }
  
      var elementToChange1 = document.querySelectorAll('iframe');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          var iframeSrc = elementToChange1[i].src;
          elementToChange1[i].src += "&autoplay=1";
        }
      }
      var elementToChange1 = document.querySelectorAll('video');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
  
          elementToChange1[i].play();
        }
      }
      var elementToChange1 = document.querySelectorAll('img');
      for (var i = 0; i < elementToChange1.length; i++) {
        if (elementToChange1[i]) {
          elementToChange1[i].style.setProperty('animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-moz-animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-webkit-animation-play-state', '', 'important');
          elementToChange1[i].style.setProperty('-o-animation-play-state', '', 'important');
        }
      }
  
      var elements1 = document.querySelectorAll('a,p,div,span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].classList.remove("show");
      }
      var elements1 = document.querySelectorAll('span');
      for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.visibility = "none";
      }
  
      document.getElementById('contrastInvert').style.display = "none";
      document.getElementById('contrastLight').style.display = "none";
      document.getElementById('contrastDark').style.display = "none";
      document.getElementById('contrastDesaturate').style.display = "none";
      document.getElementById('noContrast').style.display = "block";
      document.getElementById('noContrast').style.border = "";
  
  
      document.getElementById('bigFontAccessibility').style.display = "none";
      document.getElementById('biggerFontAccessibility').style.display = "none";
      document.getElementById('biggestFontAccessibility').style.display = "none";
      document.getElementById('normalFontAccessibility').style.display = "block";
      document.getElementById('normalFontAccessibility').style.border = "";
  
  
      document.getElementById('biggerCursor').style.display = "none";
      document.getElementById('normalCursor').style.display = "block";
      document.getElementById('normalCursor').style.border = "";
      document.getElementById("readLineAccessibility").style.display = "none";
      document.getElementById("readMaskAccessibility").style.display = "none";
  
  
      document.getElementById('bigTextSpace').style.display = "none";
      document.getElementById('biggerTextSpace').style.display = "none";
      document.getElementById('biggestTextSpace').style.display = "none";
      document.getElementById('normalTextSpace').style.display = "block";
      document.getElementById('normalTextSpace').style.border = "";
  
  
      document.getElementById('highlightLinkAccessibility').style.display = "none";
      document.getElementById('linkAccessibility').style.display = "block";
      document.getElementById('linkAccessibility').style.border = "";
  
  
      document.getElementById('dyslexiaAccessibility').style.display = "none";
      document.getElementById('legibleAccessibility').style.display = "none";
      document.getElementById('nonDyslexiaAccessibility').style.display = "block";
      document.getElementById('nonDyslexiaAccessibility').style.border = "";
  
  
      document.getElementById('lineHeight175x').style.display = "none";
      document.getElementById('lineHeight200x').style.display = "none";
      document.getElementById('lineHeight250x').style.display = "none";
      document.getElementById('normalLineHeight').style.display = "block";
      document.getElementById('normalLineHeight').style.border = "";
  
  
      document.getElementById('rightAlignAccessibility').style.display = "none";
      document.getElementById('centerAlignAccessibility').style.display = "none";
      document.getElementById('leftAlignAccessibility').style.display = "none";
      document.getElementById('justifyAlignAccessibility').style.display = "none";
      document.getElementById('noAlignAccessibility').style.display = "block";
      document.getElementById('noAlignAccessibility').style.border = "";
  
  
      document.getElementById("toggleVideoAccessibility").style.border = "";
      document.getElementById("toggleVideoAccessibility").style.borderRadius = "";
      document.getElementById("closeButton").style.textAlign = "";
      document.getElementById("pauseVideoAccessibility").style.display = "none";
      document.getElementById("toggleVideoAccessibility").style.display = "block";
  
  
      document.getElementById("toggleTooltipAccessibility").style.border = "";
      document.getElementById("toggleTooltipAccessibility").style.borderRadius = "";
      document.getElementById("showTooltipAccessibility").style.display = "none";
      document.getElementById("toggleTooltipAccessibility").style.display = "block";
  
      document.querySelector('.skiptomain').style.color = "#f5e6ba";

    }
  });  

  document.getElementById("refreshAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
window.location.reload();
    }
});

  document.getElementById('openbtnAccessibility').onclick = function () {
    document.getElementById("mySidepanel").style.display = "inline";
  };

  document.getElementById("openbtnAccessibility").addEventListener("keyup", function(event) {    
    if(event.keyCode === 13){
      document.getElementById("mySidepanel").style.display = "inline";
      document.getElementById("mySidepanel").tabIndex = "0";
    }
});

  document.getElementById('closeButton').onclick = function () {
    document.getElementById("mySidepanel").style.display = "none";
  };

})();
function openNav() {
  //document.getElementById("mySidepanel").style.width = "250px";
  document.getElementById("mySidepanel").style.display = "inline";
  //alert("hiii");
}

function closeNav() {
  //document.getElementById("mySidepanel").style.width = "0";
  document.getElementById("mySidepanel").style.display = "none";
}