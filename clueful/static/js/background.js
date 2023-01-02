var c = document.getElementById("c");
var ctx = c.getContext("2d");

//making the canvas full screen
if(c.parentElement.clientHeight > window.innerHeight-100){
    c.height =  c.parentElement.clientHeight;
}
else{
    c.height =  window.innerHeight-100;
}
c.width = c.parentElement.clientWidth;

var current_height = c.height
var current_width = c.width

//chinese characters - taken from the unicode charset
var matrix = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
//converting the string into an array of single characters
matrix = matrix.split("");

var font_size = 10;
var columns = c.parentElement.clientWidth/font_size; //number of columns for the rain

//an array of drops - one per column
var drops = [];
//x below is the x coordinate
//1 = y co-ordinate of the drop(same for every drop initially)
for(var x = 0; x < columns; x++)
    drops[x] = Math.random()*1000; 

//drawing the characters
function draw()
{   
    //Black BG for the canvas
    //translucent BG to show trail
    ctx.fillStyle = "rgba(0, 0, 0, 0.04)";
    ctx.fillRect(0, 0, c.parentElement.clientWidth, c.height);

    ctx.fillStyle = "#3daa34";//green text
    ctx.font = font_size + "px arial";
    //looping over drops
    for(var i = 0; i < drops.length; i++)
    {
        //a random chinese character to print
        var text = matrix[Math.floor(Math.random()*matrix.length)];
        //x = i*font_size, y = value of drops[i]*font_size
        ctx.fillText(text, i*font_size, drops[i]*font_size);

        //sending the drop back to the top randomly after it has crossed the screen
        //adding a randomness to the reset to make the drops scattered on the Y axis
        if(drops[i]*font_size > c.height/3 && Math.random() > 0.99)
            drops[i] = 0;

        //incrementing Y coordinate
        drops[i]++;
    }
}

function resize_bg(){
    if(c.parentElement.clientHeight > window.innerHeight-100){
        c.height =  c.parentElement.clientHeight;
    }
    else{
        c.height =  window.innerHeight-100;
    }
    c.width = c.parentElement.clientWidth;
    /* console.log(c.width); */
    
    var columns = c.parentElement.clientWidth/font_size;
    
    for(var x = 0; x < columns; x++){
        drops[x] = Math.random()*1000; 
    }
    /* ctx.fillRect(0, 0, c.parentElement.clientWidth, c.height); */
    draw()
}

window.addEventListener("resize", function(event) {
    resize_bg();
})


setInterval(draw, 35);