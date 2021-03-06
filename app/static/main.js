$(document).ready(function () {
  if(window.location.href.indexOf("search") > -1) {
    // window.location.href = (String(window.location.href) + "#results");

    var filter = window.location.href.substring(window.location.href.lastIndexOf("=")+1,window.location.href.length);
    var preprocess_1 = window.location.href.substring(0,window.location.href.lastIndexOf("="));
    var type = preprocess_1.substring(preprocess_1.lastIndexOf("=")+1,preprocess_1.lastIndexOf("&"));
    var preprocess_2 = preprocess_1.substring(0,preprocess_1.lastIndexOf("="));
    var input = preprocess_2.substring(preprocess_2.lastIndexOf("=")+1,preprocess_2.lastIndexOf("&")).replace("+"," ");        
    document.getElementById("input").value = input;
    document.getElementById("search-select").value = type;
    document.getElementById("search-filter").value = filter;
    $('html, body').animate({
      scrollTop: $('#output').offset().top
    }, {duration: 600, easing: 'swing'});
  } else {
    document.getElementById("output").innerHTML = "";
  }
  $('[data-toggle="tooltip"]').tooltip(); 
});

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
  var id = div.getAttribute('id');
  div.style.display = "block";
  var modal_content_div = document.getElementById(id).getElementsByClassName("modal-content")[0];
  var modal_body_div = modal_content_div.getElementsByClassName("modal-body")[0];
  var modal_comment_div = modal_body_div.getElementsByClassName("modal-comment")[0];

  modal_comment_div.innerHTML = extractContent(modal_comment_div.innerText, true);

  window.onclick = function(event) {
    if (event.target == div) {
        div.style.display = "none";
    }
  }
}

function closeModal(div) {
  console.log(div);
  div.style.display = "none";
}


// var msg = window.location.href.match(/\?search=(.*)/);
// document.getElementById("input").value = msg[1];
// var msg = window.location.href.match(/\?search-type=(.*)/);
// document.getElementById("search-select").value = msg[1];
