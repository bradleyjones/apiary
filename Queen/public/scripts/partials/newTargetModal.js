$('#btnWizardPrev').on('click', function() {
  $('#myWizard').wizard('previous');
});

$('#btnWizardNext').on('click', function() {
  var selectedItem = $('#myWizard').wizard('selectedItem').step;
  console.log(selectedItem);

  if (selectedItem == 1)  {
    $('#myWizard').wizard('next');
  } else if (selectedItem == 2) {
    $('#myWizard').wizard('next');
  } else if (selectedItem == 3) {
    // Close modal on finish
    $('#newTargetModal').modal('hide');

    //TODO Reset the form
  }
});

/*
 * populate the selectable list of agents
 */
function populateAgentsList(agents) {
  console.log(agents);

  var select = document.getElementById('select-agents');
  for (a in agents) {
    console.log(agents[a]);
    var opt = document.createElement('option');
    opt.value = agents[a].UUID;
    // use user defined name if it exists else use UUID
    opt.innerHTML = agents[a].UUID;
    select.appendChild(opt);
  }

  $('#select-agents').multiSelect();
}

/*
 * populate the selectable list of tags
 */
function populateTagsList(tags) {
  console.log(tags);

  var select = document.getElementById('select-tags');
  for (t in tags) {
    console.log(t);
    var opt = document.createElement('option');
    opt.value = t;
    opt.innerHTML = t;
    select.appendChild(opt);
  }

  $('#select-tags').multiSelect();
}
