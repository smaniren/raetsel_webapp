const pushButtons = document.querySelectorAll(".push-button__button");
pushButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        currentSelection.unshift(index);
        currentSelection.splice(7, 1);
        checkAnswer();
    })
})

var currentSelection = []

const secret = [3, 0, 2, 0, 1, 4, 4].reverse()


function checkAnswer() {
    if (compareArrays(secret, currentSelection) == true) {
        socketRiddleDone(4)
    }
}

