$('document').ready(function(){

  console.log('ready');
  console.log($('#weapon-form-container').is(':hidden'))

  $('.toggle-weapon-form-button').click(function(e){
    if ($('#weapon-form-container').is(':hidden')) {
      $('#weapon-form-container').removeAttr('hidden')
      $('.toggle-weapon-form-button').text("Cancel Weapon")
    } else {
      $('#weapon-form-container').prop('hidden', true)
      $('.toggle-weapon-form-button').text("Add Weapon")
    }

  })

})