var min=6,max=30;
function decreaseFontSize() {
  var s,s1,s2;
  var p = document.getElementsByTagName('p');
  for (i = 0; i < p.length; i++) {
    if (p[i].style.fontSize) s = parseInt(p[i].style.fontSize.replace("px", ""));
    else s = 12;
    if (s != min) s -= 1;
    p[i].style.fontSize = s + "px";
  }
  var sapan = document.getElementsByTagName('span');
  for (i = 0; i < sapan.length; i++) {
    if (sapan[i].style.fontSize) s = parseInt(sapan[i].style.fontSize.replace("px", ""));
    else s = 12;
    if (s != min) s -= 1;
    sapan[i].style.fontSize = s + "px";
  }
  var div = document.getElementsByTagName('div');
  for (i = 0; i < div.length; i++) {
    if (div[i].style.fontSize) s1 = parseInt(div[i].style.fontSize.replace("px", ""));
    else  s1 = 12;
    if (s1 != min)  s1 -= 1;
    div[i].style.fontSize = s + "px";
  }
    var a = document.getElementsByTagName('a');
    for (i = 0; i < a.length; i++) {
      if (a[i].style.fontSize) s2 = parseInt(a[i].style.fontSize.replace("px", ""));
      else  s2 = 12;
      if (s2 != min) s2 -= 1;
      a[i].style.fontSize = s2 + "px";
  }
  document.getElementById("Ainc").style.fontSize="15px";
  document.getElementById("Arest").style.fontSize="16px";
  document.getElementById("Adec").style.fontSize="14px";
}
function increaseFontSize() {
  var s,s1,s2;
  var p = document.getElementsByTagName('p');
  for (i = 0; i < p.length; i++) {
    if (p[i].style.fontSize) s = parseInt(p[i].style.fontSize.replace("px", ""));
    else s = 14;
    if (s <= max) s += 3;
    p[i].style.fontSize = s + "px";
    document.body.style.fontSize = s + "px";
  }
  var span = document.getElementsByTagName('span');
  for (i = 0; i < span.length; i++) {
    if (span[i].style.fontSize) s = parseInt(span[i].style.fontSize.replace("px", ""));
    else  s = 14;
    if (s <= max)  s += 3;
    span[i].style.fontSize = s + "px";
    document.body.style.fontSize = s + "px";
  }
  var div = document.getElementsByTagName('div');
  for (i = 0; i < div.length; i++) {
    if (div[i].style.fontSize)
      s1 = parseInt(div[i].style.fontSize.replace("px", ""));
    else s1 = 14;
    if (s1 <= max) s1 += 3;
    div[i].style.fontSize = s1 + "px";
  }
  var a = document.getElementsByTagName('a');
  for (i = 0; i < a.length; i++) {
    if (a[i].style.fontSize)
      s2 = parseInt(a[i].style.fontSize.replace("px", ""));
    else s2 = 14;
    if (s2 <= max) s2 += 3;
    a[i].style.fontSize = s2 + "px";
  }
  document.getElementById("Ainc").style.fontSize="15px";
  document.getElementById("Arest").style.fontSize="16px";
  document.getElementById("Adec").style.fontSize="14px";
}
function resetFontSize(){
    var s=14;
    var p = document.getElementsByTagName('p');
    for (i = 0; i < p.length; i++) {
      p[i].style.fontSize = s + "px";
      document.body.style.fontSize = s + "px";
    }
    var span = document.getElementsByTagName('p');
    for (i = 0; i <span.length; i++) {
      span[i].style.fontSize = s + "px";
      document.body.style.fontSize = s + "px";
    }
    var div = document.getElementsByTagName('div');
    for (i = 0; i < div.length; i++)
      div[i].style.fontSize = s + "px";
    var a = document.getElementsByTagName('a');
    for (i = 0; i < a.length; i++)
      a[i].style.fontSize = s + "px";
    document.body.style.fontSize = s + "px";
    document.getElementById("Ainc").style.fontSize="15px";
    document.getElementById("Arest").style.fontSize="16px";
    document.getElementById("Adec").style.fontSize="14px";
}