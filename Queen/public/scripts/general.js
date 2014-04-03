/*
 * Multi-purpose functions
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

// Add an new alert
function addAlert(type, msg) {
  var div = document.createElement("div");
  var content = document.createTextNode(msg);
  div.appendChild(content);

  var classes = "alert alert-dismissable ";
  switch(type){
    case "success":
      classes += "alert-success";
      break;
    case "info":
      classes += "alert-info";
      break;
    case "warning":
      classes += "alert-warning";
      break;
    case "danger":
      classes += "alert-danger";
      break;
    default:
      classes += "alert-info";
      break;
  }
  div.className = classes;

  //Give alert unique id for timeout
  var uniqid = Date.now();
  div.id = uniqid;

  var btn = document.createElement("button");
  btn.innerText = "×";
  btn.setAttribute("class", "close");
  btn.setAttribute("type", "button");
  btn.setAttribute("data-dismiss", "alert");
  btn.setAttribute("aria-hidden", "true");
  div.appendChild(btn);

  var navbar = document.getElementById("main-navbar");
  document.body.insertBefore(div, navbar);

  //Set timeout for alerts for all other than danger
  if (msg != "danger"){
    window.setTimeout(function() { $("#"+uniqid).alert('close'); }, 5000);
  }
}
