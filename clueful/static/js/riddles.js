/////////////////////////////////////////////////////////////////////////
// GLOBALS
/////////////////////////////////////////////////////////////////////////

//Todays date
var now

//Date of starting a riddle
var start





//
// LEDs
//
document.querySelectorAll('[class^="led_"]').forEach(function (ledElement) {
  if (ledElement.classList.contains("led_red")) {
    ledElement.getElementsByClassName("led__diode")[0].style.background =
      " radial-gradient(rgba(255, 255, 255, 0) 40%, #373737), linear-gradient(-45deg, #ffa5a5 0%, #fccfcf 100%)";
    ledElement.getElementsByClassName("led__diode__on")[0].style.background =
      "radial-gradient(rgba(255, 255, 255, 0) 40%, #373737), linear-gradient(-45deg, #ff1818 0%, #fa0000 100%)";
    ledElement.getElementsByClassName("led__diode__on")[0].style.opacity = 0;
  }
});

function get_led(id) {
  return document
    .getElementById(id)
    .getElementsByClassName("led__diode__on")[0];
}

function toggle_led(led) {
  if (led.style.opacity == "0") {
    led.style.opacity = "0.8";
  } else {
    led.style.opacity = "0";
  }
}




/////////////////////////////////////////////////////////////////////////
// GENERAL
/////////////////////////////////////////////////////////////////////////

//COMPARE ARRAYS IF SAME
function compareArrays(a, b) {
  return a.every((val, idx) => val === b[idx]);
}

//RANDOM INT
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

//WRONG ANSWER
var wrongAnswerCounter = 0;
const wrongAnimationParent = document.getElementById("answer__wrong__container");
var timeoutHandle = window.setTimeout(function () {
  document.querySelectorAll("[id^=wrongAnimation]").forEach(function (element) {
    console.log(element);
    element.remove();
  });
}, 2000);


function wrongAnswerAnimation() {
  wrongAnswerCounter += 1;
  var wrongAnimation = document.createElement("div");
  wrongAnimation.innerHTML = "WRONG!";
  wrongAnimation.id = "wrongAnimation" + wrongAnswerCounter;

  wrongAnimation.className = "answer__wrong";
  wrongAnimationParent.appendChild(wrongAnimation);
  window.clearTimeout(timeoutHandle);
  timeoutHandle = window.setTimeout(function () {
    document.querySelectorAll("[id^=wrongAnimation]").forEach(function (element) {
      element.remove();
    });
  }, 1900);
};

//
//DIFFICULTY RATING
//
var chosen_difficulty = 0;
var svgArray = [];
var elements = document.getElementsByClassName("riddle-rating__star");
var ratingTextElement = document.getElementById("riddle-rating__text");

var ratingTexts = ['rate your experience!', 'eeeasy!', 'meh...', 'it was ok', 'pretty hard', 'almost unsolveable!']


for (let i = 0; i < elements.length; i++) {
  svgArray.push(elements[i].children[0].children[0]);
  elements[i].onmouseover = function () {
    elementHovered(elements[i]);
  };
  elements[i].onmouseout = function () {
    elementMouseout(elements[i]);
  };
  elements[i].onclick = function () {
    elementClicked(elements[i]);
  };
}

function elementHovered(element) {
  var numOfStars = parseInt(String(element.id).slice(-1));
  setStars(element, numOfStars);
}

//WHEN CLICKED GET VALUE, STORE VALUE AND REDIRECT VIA SOCKET
function elementClicked(element) {
  btnRiddleRating.style.display = 'flex';
  chosen_difficulty = parseInt(String(element.id).slice(-1));
  Array.from(elements).forEach((element) =>
    element.classList.remove("riddle-rating__animation")
  );
  element.classList.add("riddle-rating__animation");
}

//WHEN DIV LEFT: SET RATING TO SORED VALUE
function elementMouseout(element) {
  setStars(element, chosen_difficulty);
}

function setStars(element, numOfStars) {
  svgArray.forEach(
    (element) => (
      (element.style.fill = "#faf9f9"),
      (element.style.transform = "scale(1.0) translate(0px, 0px)"),
      (element.style.filter = "drop-shadow(0px 0px 0px transparent)")
    )
  );
  for (let i = 0; i < numOfStars; i++) {
    svgArray[i].style.fill = "#ffbe47";
    svgArray[i].style.transform = "scale(1.10) translate(-1px, -1px)";
    svgArray[i].style.filter = "drop-shadow(0px 0px 1px orange)";
  }
  ratingTextElement.innerHTML = ratingTexts[numOfStars]
}


// STORE PUZZLE-RATING
var btnRiddleRating = document.getElementById('riddle-rating__save-rating')
btnRiddleRating.addEventListener('click', () => {
  var rating = chosen_difficulty;
  socketStoreRiddleRating(rating);
});


//
// POINTS COUNT-DOWN
//
function interval(data) {
  const hundredsElement = document.getElementById("countdown--hundreds");
  const tensElement = document.getElementById("countdown--tens");
  const unitsElement = document.getElementById("countdown--units");
  const digitElements = [hundredsElement, tensElement, unitsElement];


  var oldPoints = getDigits(545);

  start = new Date(data['start_time']);
  now = new Date();

  interval = setInterval(function () {
    var newPoints = getDigits(getPoints());
    if (oldPoints[0] !== newPoints[0]) {
      addPulseOut(digitElements);
    } else if (oldPoints[1] !== newPoints[1]) {
      addPulseOut([digitElements[1], digitElements[2]]);
    } else if (oldPoints[2] !== newPoints[2]) {
      addPulseOut([digitElements[2]]);
    }
    setTimeout(function () {
      var pulse_elements = document.querySelectorAll(".pulse_out");
      setDigitElements(newPoints);
      for (var i = 0; i < pulse_elements.length; ++i) {
        pulse_elements[i].classList.remove("pulse_out");
        pulse_elements[i].classList.add("pulse_in");
      }
    }, 600);
    oldPoints = newPoints;
    var pulse_elements = document.querySelectorAll(".pulse_in");
    for (var i = 0; i < pulse_elements.length; ++i) {
      pulse_elements[i].classList.remove("pulse_in");
    }
  }, 1000);

  function getPoints() {
    now = new Date();
    var duration = Math.round((now.getTime() - start.getTime()) / 1000);
    var points = Math.round(1000 * 0.985 ** (duration / 60));
    if (points >= 1000) {
      return 999;
    } else if (points <= 1) {
      return 1;
    } else {
      return points;
    }
  }

  function getDigits(fullNumber) {
    var digits = [];
    var digitHundreds = Math.floor(fullNumber / 100);
    var digitTens = Math.floor((fullNumber - digitHundreds * 100) / 10);
    var currentUnits = fullNumber - (digitHundreds * 100 + digitTens * 10);
    return [digitHundreds, digitTens, currentUnits];
  }

  function setDigitElements(points) {
    digitElements.forEach((element, index) => {
      element.innerHTML = points[index];
    });
  }

  function addPulseOut(elements) {
    elements.forEach((element) => {
      element.classList.add("pulse_out");
    });
  }

}


//
// Get Hints
//

//find first hint-button and add click-eventlistener
var hint1_btn = document.getElementById("hint-1-btn");
var hint2_btn = document.getElementById("hint-2-btn");
var hint3_btn = document.getElementById("hint-3-btn");
//var hint1_text = document.getElementById("hint-1-text");
if (hint1_btn) { hint1_btn.onclick = function () { socketGetHint(1); calculate_new_start_date() } }
if (hint2_btn) { hint2_btn.onclick = function () { socketGetHint(2); calculate_new_start_date() } }
if (hint3_btn) { hint3_btn.onclick = function () { socketGetHint(3); calculate_new_start_date() } }

function create_hint(hint_nr, hint_text) {
  text_element = document.getElementById("hint-" + hint_nr + "-text")
  btn_element = document.getElementById("hint-" + hint_nr + "-btn")
  if (text_element) {
    btn_element.style.display = "none";
    text_element.style.display = "block";
    text_element.innerHTML = hint_text;
    hint_nr = hint_nr + 1
    next_btn = document.getElementById("hint-" + hint_nr + "-btn")
    if (next_btn) {
      next_btn.style.display = "block";
    }
  }
}


//
// Update Start-Time when hint is used
//

function calculate_new_start_date() {
  newStartDate = new Date(start.getTime() - 1800000)
  socketUpdateTimeData(newStartDate)
  //Update global Variable
  start = newStartDate
}
