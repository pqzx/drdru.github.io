'use strict';


var STATE = {
  ASKING: 0,
  EVALUATED: 1
};


var currentState = STATE.ASKING
// game screens
var startScreen = $('#start-screen');

var gameScreen = $('#game-screen');

var playButton = $('#play');
var answerTextBox = $('#answer');

var questionField = $('#question-word');

var user_score = $('#user_score');

var currentTerm = '';
var score = 0;

$(document).ready(function() {

  show(startScreen);
  show(gameScreen);


  

  playButton.add("#options-play").click(function() {
     //show(gameScreen);
    hide(startScreen);

  });
  
  user_score.html(score);
  nextQuestion()

    // Bind the game logic to keyup/keydown handlers on the answer text field.
  answerTextBox.bind('keyup', function(e) {


    if (currentState == STATE.ASKING) {
      
      

      checkAnswer(currentTerm);
      console.log(answer);

      return true;
    }
  });

});


function nextQuestion() {
  
  answerTextBox.val(''); 
  currentTerm = food[Math.floor((Math.random() * food.length) + 1) - 1 ]
  questionField.html(currentTerm.katakana_ );

}


function show(element) {
  element
      .removeClass('hide')
      .addClass('show');
}


function hide(element) {
  element
      .removeClass('show')
      .addClass('hide');
}



function checkAnswer(answer) {

    var proposal = answerTextBox.val().replace(/\s/g, '');
    console.log('Your answer is : ' + proposal)

    if (proposal == answer.definition_) {

      score += 1;
      user_score.html(score);
console.log(score)
      nextQuestion()

    //} else {

      //console.log('Oops')

    }
}  