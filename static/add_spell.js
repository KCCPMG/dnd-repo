$('document').ready(function(){

  console.log('ready');
  console.log($('#spell-form-container').is(':hidden'))

  $('.toggle-spell-form-button').click(function(e){
    if ($('#spell-form-container').is(':hidden')) {
      $('#spell-form-container').removeAttr('hidden')
      $('.toggle-spell-form-button').text("Cancel Spell")
    } else {
      $('#spell-form-container').prop('hidden', true)
      $('.toggle-spell-form-button').text("Add Spell")
    }

  })

})