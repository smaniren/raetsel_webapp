
/////////////////////////////////////////////////////////////////////////
// RIDDLE-SPECIFIC
/////////////////////////////////////////////////////////////////////////

//Riddle 02
var rangeRed = document.getElementById("riddle__2__range_red");
var rangeGreen = document.getElementById("riddle__2__range_green");
var rangeBlue = document.getElementById("riddle__2__range_blue");
var background = document.getElementById("riddle");
background.style.background =
  "linear-gradient(90deg, rgb(0 ,0 ,0 ) 50%, rgb(255 , 255, 255) 50%";
var counter = 0;
var game_running = true;

var numberOfLeds = 5;
var ledArray = []

for (var i = 0; i < numberOfLeds; i++) {
  ledArray.push(get_led('r2_led_red_' + (i + 1).toString()))
}

var colorDict = {
  0: "32",
  1: "64",
  2: "96",
  3: "128",
  4: "160",
  5: "192",
  6: "224",
  7: "255"
};
var colorDictLength = Object.keys(colorDict).length;

var solution = [
  ["7", "7", "7"],
  [
    String(getRandomInt(0, colorDictLength - 1)),
    String(getRandomInt(0, colorDictLength - 1)),
    String(getRandomInt(0, colorDictLength - 1))
  ],
  [String(getRandomInt(0, colorDictLength - 1)), String(getRandomInt(0, colorDictLength - 1)), String(getRandomInt(0, colorDictLength - 1))],
  [String(getRandomInt(0, colorDictLength - 1)), String(getRandomInt(0, colorDictLength - 1)), String(getRandomInt(0, colorDictLength - 1))],
  ["1", "4", "5"]
];

document.querySelectorAll(".riddle__2__color-range").forEach((item) => {
  item.addEventListener("input", function () {
    if (game_running) {
      var red = colorDict[rangeRed.value];
      var green = colorDict[rangeGreen.value];
      var blue = colorDict[rangeBlue.value];
      console.log(counter);
      if (colorSame(rangeRed.value, rangeGreen.value, rangeBlue.value)) {
        toggle_led(ledArray[counter]);
        counter += 1;
        if (counter < solution.length) {
          changeBackground(red, green, blue, solution[counter]);
        } else {
          changeBackground(red, green, blue, solution[solution.length - 1]);
          game_running = false;
          socketRiddleDone(2)
        }
      } else {
        changeBackground(red, green, blue, solution[counter]);
      }
    }
  });
});

function changeBackground(red, green, blue, solution) {
  background.style.background =
    "linear-gradient(90deg, rgb(" +
    red +
    "," +
    green +
    "," +
    blue +
    ") 50%, rgb(" +
    colorDict[solution[0]] +
    "," +
    colorDict[solution[1]] +
    "," +
    colorDict[solution[2]] +
    ") 50%";
}

function colorSame(r, g, b) {
  var correct_values = solution[counter];
  //console.log([r, g, b]);
  //console.log(correct_values);
  var is_same =
    [r, g, b].length == correct_values.length &&
    [r, g, b].every(function (element, index) {
      return element === correct_values[index];
    });
  if (is_same) {
    return true;
  }
}






