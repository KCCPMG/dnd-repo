
$('document').ready(function(){

  $('.toggle-comment-form-button').click(function(e){
    if ($('#comment-form-container').is(':hidden')) {
      $('#comment-form-container').removeAttr('hidden')
      $('.toggle-comment-form-button').text("Cancel Comment")
    } else {
      $('#comment-form-container').prop('hidden', true)
      $('.toggle-comment-form-button').text("Add Comment")
    }

  })

})

