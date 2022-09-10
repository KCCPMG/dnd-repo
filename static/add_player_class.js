$('document').ready(function(){

  console.log('ready');
  console.log($('#player-class-form-container').is(':hidden'))

  $('.toggle-player-class-form-button').click(function(e){
    if ($('#player-class-form-container').is(':hidden')) {
      $('#player-class-form-container').removeAttr('hidden')
      $('.toggle-player-class-form-button').text("Cancel Class")
    } else {
      $('#player-class-form-container').prop('hidden', true)
      $('.toggle-player-class-form-button').text("Add Class")
    }

  })

})