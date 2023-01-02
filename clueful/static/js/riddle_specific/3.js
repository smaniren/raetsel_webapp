function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

var arrowContainer = document.getElementById("arrow-container");
var userInput = document.getElementById("answer");
var secret = [];
var numberOfSecrets = 6;

do {
    secretNumber = getRandomInt(0, 9);
    if (!secret.includes(secretNumber)) {
        secret.push(secretNumber);
    }
} while (secret.length <= numberOfSecrets);

var key = {
    0: "&#8592; &#8593; &#8593; &#8594; &#8595; &#8595",
    1: "&#8593; &#8593;",
    2: "&#8592; &#8593; &#8594; &#8593; &#8592;",
    3: "&#8594; &#8593; &#8592; &#8594; &#8593; &#8592;",
    4: "&#8593; &#8593; &#8595; &#8592; &#8593;",
    5: "&#8594; &#8593; &#8592; &#8593; &#8594;",
    6: "&#8594; &#8595; &#8592; &#8593; &#8593; &#8594;",
    7: "&#8594; &#8595; &#8595;",
    8: "&#8592; &#8593; &#8594; &#8593; &#8592; &#8595; &#8594; &#8595;",
    9: "&#8594; &#8593; &#8593; &#8592; &#8595; &#8594;"
};

for (var i = 0; i < secret.length; i++) {
    var arrow = document.createElement("div");
    arrow.className = "arrow";
    arrow.innerHTML = key[secret[i]];
    arrowContainer.append(arrow);
}

function checkAnswer() {
    var answerCorrect = true;
    if (secret.length !== userInput.value.length) {
        answerCorrect = false;
    }
    for (var i = 0; i < secret.length; i++) {
        if (String(secret[i]) !== userInput.value[i]) {
            answerCorrect = false;
        }
    }
    if (answerCorrect) {
        socketRiddleDone(3)
    } else {
        wrongAnswerAnimation();
    }
}
