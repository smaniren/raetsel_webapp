
//Initial references
let container = document.querySelector(".p-art-creator__image--container");
let clearGridButton = document.getElementById("btnDeletePicture");
let colorButton = document.getElementById("btnColor");
let createRandomButton = document.getElementById("btnCreateRandom");
let saveImageButton = document.getElementById("btnSaveImage");


let color = '#000000'



let colorArray = user_image_values

colorArray=colorArray.flat(1)

//Events object
let events = {
  mouse: {
    down: "mousedown",
    move: "mousemove",
    up: "mouseup",
  },
  touch: {
    down: "touchstart",
    move: "touchmove",
    up: "touchend",
  },
};
let deviceType = "";
//Initially draw_color ande would be false
let draw_color = false;
let erase = false;
let getColor = false;
//Detect touch device
const isTouchDevice = () => {
  try {
    //We try to create TouchEvent(it would fail for desktops and throw error)
    document.createEvent("TouchEvent");
    deviceType = "touch";
    return true;
  } catch (e) {
    deviceType = "mouse";
    return false;
  }
};
isTouchDevice()


let count_cell = 0;
let count_row = 0;
for (let i = 0; i < 11; i++) {
  //incrementing count_cell by 2
  count_row += 1;
  //Create row div
  let div = document.createElement("div");
  div.classList.add("p-art-creator__image--row");
  //Create Columns
  for (let j = 0; j < 11; j++) {
    let col = document.createElement("div");
    col.classList.add("p-art-creator__image--cell");
    /* We need unique ids for all columns (for touch screen specifically) */
    col.setAttribute("id", `gridCol${count_cell}`);
    col.style.background = "rgb("+colorArray[count_cell][0]+","+colorArray[count_cell][1]+","+colorArray[count_cell][2]+")";
    count_cell += 1;
    /*
      For eg if deviceType = "mouse"
      the statement for the event would be events[mouse].down which equals to mousedown
      if deviceType="touch"
      the statement for event would be events[touch].down which equals to touchstart
       */
    col.addEventListener(events[deviceType].down, () => {
      //user starts draw_coloring
      draw_color = true;
      //if erase = true then background = transparent else color
      if (erase) {
        col.style.backgroundColor = "rgb(255,255,255)";
      } else if (getColor) {
        console.log(convertRgb(col.style.backgroundColor));
        colorButton.defaultValue = convertRgb(col.style.backgroundColor);}
       else {
        col.style.backgroundColor = color;
      }
    });
    col.addEventListener(events[deviceType].move, (e) => {
      /* elementFromPoint returns the element at x,y position of mouse */
      e.preventDefault();
      let elementId = document.elementFromPoint(
        !isTouchDevice() ? e.clientX : e.touches[0].clientX,
        !isTouchDevice() ? e.clientY : e.touches[0].clientY
      ).id;
      //checker
      checker(elementId);
    });
    //Stop draw_coloring
    col.addEventListener(events[deviceType].up, () => {
      draw_color = false;
    });
    //append columns
    div.appendChild(col);
  }
  //append grid to container
  container.appendChild(div);
}
function checker(elementId) {
  let gridColumns = document.querySelectorAll(".p-art-creator__image--cell");
  //loop through all boxes
  gridColumns.forEach((element) => {
    //if id matches then color
    if (elementId == element.id) {
      if (draw_color && !erase && !getColor) {
        element.style.backgroundColor = color;
      } else if (draw_color && erase) {
        element.style.backgroundColor = "rgb(255,255,255)";
      }
    }
  });
}

//Clear Grid
clearGridButton.addEventListener("click", () => {
    let gridColumns = document.querySelectorAll(".p-art-creator__image--cell");
  //loop through all boxes
  gridColumns.forEach((element) => {
    //if id matches then color
        element.style.backgroundColor = "rgb(255,255,255)";
  });
});

function convertRgb(rgb) {
  // This will choose the correct separator, if there is a "," in your value it will use a comma, otherwise, a separator will not be used.
  var separator = rgb.indexOf(",") > -1 ? "," : " ";


  // This will convert "rgb(r,g,b)" into [r,g,b] so we can use the "+" to convert them back to numbers before using toString 
  rgb = rgb.substr(4).split(")")[0].split(separator);

  // Here we will convert the decimal values to hexadecimal using toString(16)
  var r = (+rgb[0]).toString(16),
    g = (+rgb[1]).toString(16),
    b = (+rgb[2]).toString(16);

  if (r.length == 1)
    r = "0" + r;
  if (g.length == 1)
    g = "0" + g;
  if (b.length == 1)
    b = "0" + b;

  // The return value is a concatenation of "#" plus the rgb values which will give you your hex
  return "#" + r + g + b;
}

function setColor(element){
  color = element.style.backgroundColor
  let colors = document.querySelectorAll(".color-picker__colors");
  //loop through all boxes
  colors.forEach((element) => {
    element.classList.remove('active')
  });
  element.classList.add('active')
  console.log(color)
}


Object.defineProperty(Array.prototype, 'flat', {
    value: function(depth = 1) {
      return this.reduce(function (flat, toFlatten) {
        return flat.concat((Array.isArray(toFlatten) && (depth>1)) ? toFlatten.flat(depth-1) : toFlatten);
      }, []);
    }
});


function getRGB(str){
  var match = str.match(/rgba?\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})\)?(?:, ?(\d(?:\.\d?))\))?/);
  return [parseInt(match[1]),parseInt(match[2]),parseInt(match[3])];
}


function getRandomImage(){
    $.ajax({
      url: "/createRandomImage",
      type: "get",
      success: function(result) {
        colorArray=result.flat(1)
        count_cell = 0;
        for (let i = 0; i < 11; i++) {
          for (let j = 0; j < 11; j++) {
            current_element = document.getElementById('gridCol'+count_cell)
            current_element.style.background = "rgb("+colorArray[count_cell][0]+","+colorArray[count_cell][1]+","+colorArray[count_cell][2]+")";
            count_cell += 1;
          }
        }
       },
      error: function(xhr) {
          //Handel error
      }
    }); 
};



