$('document').ready(function(){

  console.log('ready');
  console.log($('#armor-form-container').is(':hidden'))

  $('.toggle-armor-form-button').click(function(e){
    if ($('#armor-form-container').is(':hidden')) {
      $('#armor-form-container').removeAttr('hidden')
      $('.toggle-armor-form-button').text("Cancel Armor")
    } else {
      $('#armor-form-container').prop('hidden', true)
      $('.toggle-armor-form-button').text("Add Armor")
    }

  })

})