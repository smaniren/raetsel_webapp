
/* modalFormElement = document.getElementById('modalPasswordFrom'); */
var modalElement


function showModal(modal_id){
    modalElement = document.getElementById(modal_id);
    modalElementChild= modalElement.firstElementChild
    modalElementChild.style.animation = 'moveInRight .3s';
    modalElement.style.display = 'flex';
    modalElement.scrollIntoView()
    elementToBlur = document.getElementsByClassName('blurred_by_modal')[0];
    topNav = document.getElementsByClassName('header')[0];
    console.log(topNav)
    if(topNav){
        topNav.style.display = "none"
    };
    elementToBlur.style.filter = "blur(8px)"
    /* close modal on click outside */
    window.onclick = function(event) {
        const activeElements = document.getElementsByClassName("modal");
        for (const element of activeElements){
            if (event.target == modalElement) {
                element.style.display = 'none';
                elementToBlur.style.filter = "none"
                if(topNav){
                    topNav.style.display = "flex"
                };
            }
        }
  }
}

function closeModal(modal_id){
    modalElement = document.getElementById(modal_id);
    modalElement.style.display = 'none';
    elementToBlur = document.getElementsByClassName('blurred_by_modal')[0];
    topNav = document.getElementsByClassName('header')[0];
    console.log(topNav)
    if(topNav){
        topNav.style.display = "flex"
    };
    elementToBlur.style.filter = "none"
    /* bg.style.filter = "none" */
}



function removeAnimations(){
    /* Alle animationen entfernen */
    const activeElements = document.getElementsByClassName("moveOutLeft");
    for (const element of activeElements){
        element.classList.remove('moveOutLeft');
        element.style.display = 'flex';
    }
    const activeElements2 = document.getElementsByClassName("moveInRight");
    for (const element of activeElements2){
        element.classList.remove('moveInRight');
        element.style.display = 'none';
    }
  }
