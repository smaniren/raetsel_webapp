function editText(id) {
    TextElement = document.getElementById(id)
    InputElement = document.getElementById(id+"Input");
    
    removeAnimations()

    TextElement.classList.toggle('moveOutLeft');

    setTimeout(function() {
        TextElement.style.display = 'none';
        InputElement.style.display = 'flex';
        InputElement.classList.toggle('moveInRight');
        InputElement.style.transform = 'translateX(0rem)';
        InputElement.style.opacity = '1';
    }, 300);
}

/* modalElement = document.getElementById('modalPassword');
modalFormElement = document.getElementById('modalPasswordFrom');
var bg = document.getElementById("main-content");


function showModalPassword(){
    modalFormElement.style.animation = 'moveInRight .3s';
    modalElement.style.display = 'flex';
    modalFormElement.scrollIntoView()
}

function closeModalPassword(){
    modalElement.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modalElement) {
        modalElement.style.display = 'none';
    }
  } */
