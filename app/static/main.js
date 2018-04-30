$(document).ready(function () {
  if(window.location.href.indexOf("search") > -1) {
    // window.location.href = (String(window.location.href) + "#results");
    $('html, body').animate({
      scrollTop: $('#output').offset().top
    }, {duration: 600, easing: 'swing'});
  }
});

// function selectHandler() {
//   var selected = document.getElementById("search-select").value;
//   if (selected == "bot-com") {  
//     $(".by-bot-name").addClass("inactive");
//     $(".by-user-com").addClass("inactive");
//     $(".by-bot-com").removeClass("inactive");
//   } else if (selected == "user-com") {
//     $(".by-bot-name").addClass("inactive");
//     $(".by-user-com").removeClass("inactive");
//     $(".by-bot-com").addClass("inactive");
//   } else {
//     $(".by-bot-name").removeClass("inactive");
//     $(".by-user-com").addClass("inactive");
//     $(".by-bot-com").addClass("inactive"); 
//   }
// }

function learnHandler(element) {
  console.log("hi");
}

function extractContent(s, space) {
  var span= document.createElement('span');
  span.innerHTML= s;
  if(space) {
    var children= span.querySelectorAll('*');
    for(var i = 0 ; i < children.length ; i++) {
      if(children[i].textContent)
        children[i].textContent+= ' ';
      else
        children[i].innerText+= ' ';
    }
  }
  return [span.textContent || span.innerText].toString().replace(/ +/g,' ');
};

// $('#exampleModalCenter').on('show.bs.modal', function (event) {
//   var button = $(event.relatedTarget) // Button that triggered the modal
//   var botname = button.data('botname') // Extract info from data-* attributes
//   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   var modal = $(this)
//   modal.find('.modal-title').text('{{ '+ botname +'.name }}')
//   modal.find('.modal-rank input').val(recipient)
// })

function showModal(div) {
  console.log(div);
  div.style.display = "block";
}

function closeModal(div) {
  console.log(div);
  div.style.display = "none";
}




