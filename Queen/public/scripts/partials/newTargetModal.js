/*
 * Code related to the modal dialog / wizard step by step dialog for setting new
 * targets to agents
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var selectedAgents = [];
var selectedTags = [];

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
    // push new target
    var files = $('#filepath').val();
    console.log(files);
    newtarget(files, selectedTags, selectedAgents);


    // Close modal on finish
    $('#newTargetModal').modal('hide');

    //TODO Reset the form
    $('#myWizard').wizard('previous');
    $('#myWizard').wizard('previous');
    selectedAgents = [];
    selectedTags = [];
  }
});

/*
 * Add new tag to tag list
 */
$('#newtagbtn').on('click', function (){
  console.log("adding new tag")
  var value = $('#newtag').val();
  $('#select-tags').multiSelect('addOption', {
    value: value,
    text: value,
    index: 0
  });
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

  $('#select-agents').multiSelect({
    afterSelect: function (value) {
      console.log(value[0]);
      selectedAgents.push(value[0]);
      console.log(selectedAgents);
    },

    afterDeselect: function (value) {
      var index = selectedAgents.indexOf(value[0]);
      if (index > -1 ) {
        selectedAgents.splice(index, 1);
      }
    }
  });
}

/*
 * populate the selectable list of tags
 */
function populateTagsList(tags) {
  console.log(tags);

  var select = document.getElementById('select-tags');
  for (t in tags) {
    var x = tags[t];
    console.log(x);
    var opt = document.createElement('option');
    opt.value = x.NAME;
    opt.innerHTML = x.NAME;
    select.appendChild(opt);
  }

  $('#select-tags').multiSelect({
    afterSelect: function (value) {
      selectedTags.push(value);
    },

    afterDeselect: function (value) {
      var index = selectedAgents.indexOf(value);
      if (index > -1 ) {
        selectedTags.splice(index, 1);
      }
    }
  });
}
