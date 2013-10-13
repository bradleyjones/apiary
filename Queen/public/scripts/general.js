// Add an new alert
function addAlert(type, msg) {
  var div = document.createElement("div");
  var content = document.createTextNode(msg);
  div.appendChild(content);

  var classes = "alert alert-dismissable ";
  switch(type){
    case "success":
      classes += "alert-success alert-timeout";
      break;
    case "info":
      classes += "alert-info alert-timeout";
      break;
    case "warning":
      classes += "alert-warning alert-timeout";
      break;
    case "danger":
      classes += "alert-danger";
      break;
    default:
      classes += "alert-info alert-timeout";
      break;
  }
  div.className = classes;

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
    window.setTimeout(function() { $(".alert-timeout").alert('close'); }, 2500);
  }
}
