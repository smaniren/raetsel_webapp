/* Background Music */

var playMusic = socketGetMusicStatus();

const btnMusicOn = document.getElementById('music_on_svg');
const btnMusicOff = document.getElementById('music_off_svg');
const btnMusicElement = document.getElementById('btn_Music_toggle');

const sndMenuBackground = new Audio('../static/sounds/menu-background.mp3');
sndMenuBackground.volume = 0.4;
sndMenuBackground.addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
});

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
        sndMenuBackground.play();
    } else {
        sndMenuBackground.pause();
        sndMenuBackground.currentTime = 0;
    };
}