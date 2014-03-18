$('#btnWizardPrev').on('click', function() {
  $('#myWizard').wizard('previous');
});

$('#btnWizardNext').on('click', function() {
  var selectedItem = $('#myWizard').wizard('selectedItem').step;

  $('#myWizard').wizard('next');

  if (selectedItem == 2) {
    $('#btnWizardNext').html("FINISH HIM!!");
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
  $('#select-tags').multiSelect();
}
