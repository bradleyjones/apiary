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
      $('#newAlertModal').modal('hide');

      //TODO Reset the form
    }
  });
