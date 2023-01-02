/* Background Music */

var playMusic = socketGetMusicStatus();

const btnMusicOn = document.getElementById('music_on_svg');
const btnMusicOff = document.getElementById('music_off_svg');
const btnMusicElement = document.getElementById('btn_Music_toggle');


//
// Sounds
//

//add Sound effects every 30 sec
const numberOfSoundEffects = 7
var soundEffects = []

for (let i = 0; i< numberOfSoundEffects; i++){
  soundEffects[i] = new Audio('../static/sounds/riddle-sound-effect-'+(i+1).toString()+'.mp3')
  soundEffects[i].volume = 0.7;
}
var soundEffectInterval = window.setInterval(playRandomSoundEffect, 30000);

function playRandomSoundEffect() {
    if (playMusic){
        soundEffects[getRandomInt(0, numberOfSoundEffects)].play()
    }
}





// add Backgroudn music & ticking
const sndClockTicking = new Audio('../static/sounds/clock-ticking.mp3');
const sndRiddleBackground = new Audio('../static/sounds/riddle-background-music.mp3');
var soundArray = [sndClockTicking,sndRiddleBackground]
sndClockTicking.volume = 0.8;
sndRiddleBackground.volume = 0.2;

soundArray.forEach((sound) => {
    sound.addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
  }, false);
})

btnMusicElement.addEventListener('click', () => {
    playMusic = !playMusic;
    setMusicIcon()
    setMusic()
    socketSaveMusicStatus(playMusic)
})

function setMusicIcon(){
    if (playMusic){
        btnMusicOff.style.display = 'none';
        btnMusicOn.style.display = 'block';
    }
    else{
        btnMusicOff.style.display = 'block';
        btnMusicOn.style.display = 'none';
    }
}

function setMusic(){
    if (playMusic) {
        soundArray.forEach((sound) => {
            sound.play();
          });
    } else {
        soundArray.forEach((sound) => {
            sound.pause();
            sound.currentTime = 0;
        });
    };
}