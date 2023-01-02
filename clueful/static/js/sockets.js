/* 00 GLOBALS */

const socket = io();
socket.connect();

/* 01 DON NOT SHOW AGAIN */
function socketGetElementInsideContainer(flashID,checkboxID) {
    checkbox = document.getElementById(checkboxID);
    if (checkbox.checked){
        data = flashID;
        /* socket = io();
        socket.connect(); */
        socket.emit('dont_show_again',data);
        
    }
}


/* 02 SAVE USER PROFILE IMAGE */
function socketSaveUserImage(){
    let gridColumns = document.querySelectorAll(".p-art-creator__image--cell");
    rgb_values_per_row = []
    image = []
    //loop through all boxes
    gridColumns.forEach((element) => {
      //store all boxes in an array
      rgb_values_per_row.push(getRGB(element.style.backgroundColor));
      if (rgb_values_per_row.length === 11){
        image.push(rgb_values_per_row);
        rgb_values_per_row = [];
      }
    });
    data = image;
    socket.emit('saveUserImage',data);
    socket.on('reload', function() {
        location.reload();
        
        return false;
    });
}

/* 03 CHECK ANSWER */
function socketCheckAnswer(game_id,input_element='none', solution='none'){
  var answer_user = document.getElementById(input_element).value
  if (answer_user == solution){
    socketRiddleDone(game_id)
    
  }
  else{
    console.log('answer wrong');
    wrongAnswerAnimation();
    
  }
}

function socketRiddleDone(game_id){
  console.log('answer correct');
  data = {
    'game_id':game_id
  }
  /* socket = io();
  socket.connect(); */
  socket.emit('correctAnswer',data);
  socket.on('redirect', function(data) {
    window.location = data.url;
    
    return false;
  });
  socket.on('riddle_data_saved', function() {
    showModal('riddle-done-modal');
    
  });

}

/* 04 PUZZLE RATING */
function socketStoreRiddleRating(rating){
  console.log(rating)
  data = {'riddle_rating':rating, 'game_id':window.location.href.split("/").pop()};
  /* socket = io();
  socket.connect(); */
  socket.emit('riddle_rating',data);
  socket.on('redirect', function(data) {
    window.location = data.url;
    
    return false;
  });
}


/* 05 UPDATE RIDDLE START TIME */
function socketUpdateTimeData(newStartDate){
  data = {
    'new_start_date':newStartDate,'game_id':window.location.href.split("/").pop()
  }
  /* socket = io();
  socket.connect(); */
  socket.emit('updateTimeData',data);
  
}


/* 06 GET HINTS */
function socketGetHint(hintNr){
  data = {
    'hint_nr':hintNr,'game_id':window.location.href.split("/").pop()
  }
  /* socket = io();
  socket.connect(); */
  socket.emit('getHint',data);
  socket.on('receiveHint', function(data) {
    create_hint(data['hint_nr'],data['hint_text'])
    
    return false;
  });

}

/* 07 GET MUSIC STATUS */
function socketGetMusicStatus(){
  /* socket = io();
  socket.connect(); */
  socket.emit('getMusicStatus');
  socket.on('receiveMusicStatus', function(data) {
    playMusic = data['music_status'];
    setMusicIcon()
    setMusic()
    
    return false;
  });
}

/* 08 SAVE MUSIC STATUS */
function socketSaveMusicStatus(status){
  data = {
    'status':status
  }
  /* socket = io();
  socket.connect(); */
  socket.emit('saveMusicStatus',data);
  
}