$('document').ready(function(){

  $('.toggle-expanded-view-button').click(function(e){
    thisButton = e.target;
    armor_container = e.target.parentElement.parentElement.parentElement;
    console.log(armor_container);

    detail = armor_container.querySelector('.expanded-detail')

    if ($(detail).is(':hidden')) {
      $(detail).removeAttr('hidden')
      $(thisButton).text("Collapse")
    } else {
      $(detail).prop('hidden', true)
      $(thisButton).text("Expand")
    }


  })


});

