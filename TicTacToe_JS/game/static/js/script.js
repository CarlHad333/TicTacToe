selbtn = document.getElementById('sel');

selbtn.addEventListener('click', function(){

  let originalBoard;
  let p1 = document.getElementById('player1').selectedOptions[0];
  let p2 = document.getElementById('player2').selectedOptions[0];
  p1.selected = true;
  p2.selected = true;
  const xplayer = p1.value;
  const oplayer = p2.value;
  selbtn.disabled = true;
  

  const winCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [6, 4, 2]
  ]
  
  let btns = document.querySelectorAll('.button-option');

  let count = 0;

  function disableButtons() {
      btns.forEach((element) => (element.disabled = true));
  }

  function draw() {
    disableButtons();
    alert("It's a Draw!");
  }

  const winChecker = () => {
    for(let i of winCombos) {
      let [element1, element2, element3] = [
          btns[i[0]].className,
          btns[i[1]].className,
          btns[i[2]].className,
      ];

      if (element1 != "button-option" && (element2 != "button-option") && (element3 != "button-option")) {
          if (element1 == element2 && element1 == element3) {
              disableButtons();
              while (count != 9) {

                if (element1 == "X") {
                    alert("X wins!");
                    return true;
                }
                else if(element1 === 'O') {
                    alert("O wins!");
                    return true;
                }
                else {
                  return false;
                }
              }
            }
          }
      }
  }

  startGame();


  function startGame() {
    originalBoard = Array.from(Array(9).keys());
    let xTurn = true;

    for (let i = 0; i < btns.length; ++i) {
      if (oplayer === 'H') {
        btns[i].addEventListener("click", function() {
          if (xTurn) {
              xTurn = false;
              btns[i].setAttribute("class", "X");
              btns[i].disabled = true;
          } else {
              xTurn = true;
              btns[i].setAttribute("class", "O");
              btns[i].disabled = true;
          }

          count++;
          if (count === 9 && !winChecker()) {
              draw();
          }

          winChecker();
              
        })
      }
      else {
        btns[i].addEventListener('click', turnClick, false);
        let gameWon = checkWin(originalBoard, xplayer);
        if (gameWon) gameOver(gameWon);
      }
    }
    
  }

  
  function turnClick(square) {
    if (xplayer === 'H' && oplayer === 'M'){
      turn(square.target.id, xplayer);
      if (!checkTie() && !checkWin(originalBoard, xplayer)) turn(bestSpot(), oplayer);
    }
    else if (xplayer === 'H' && oplayer === 'R'){
      turn(square.target.id, xplayer);
      if (!checkTie() && !checkWin(originalBoard, xplayer)) turn(randomPlayer(), oplayer);
    }
  }

   
  function turn(squareId, player) {
    originalBoard[squareId] = player;
    if (player === xplayer){
      document.getElementById(squareId).className = 'X';
      document.getElementById(squareId).disabled = true;
    } else {
      document.getElementById(squareId).className = 'O';
      document.getElementById(squareId).disabled = true;
    }
    let gameWon = checkWin(originalBoard, player)
    if (gameWon) gameOver(gameWon)
  }

  function checkWin(board, player) {
    let plays = board.reduce((a, e, i) =>
      (e === player) ? a.concat(i) : a, []);
    let gameWon = null;
    for (let [index, win] of winCombos.entries()) {
      if (win.every(elem => plays.indexOf(elem) > -1)) {
        gameWon = {index: index, player: player};
        break;
      }
    }
    return gameWon;
  }

  function gameOver(gameWon) {
    for (var i = 0; i < btns.length; i++) {
      btns[i].removeEventListener('click', turnClick, false);
    }
    declareWinner(gameWon.player == xplayer ? "You win!" : "You lose.");
  }


  function declareWinner(who) {
    alert(who);
  }

  function emptySquares() {
    return originalBoard.filter(s => typeof s == 'number');
  }

  function bestSpot() {
    return minimax(originalBoard, oplayer, -1000, 1000).index;
  }

  function checkTie() {
    if (emptySquares().length == 0) {
      for (var i = 0; i < btns.length; i++) {
        btns[i].removeEventListener('click', turnClick, false);
      }
      declareWinner("Tie Game!")
      return true;
    }
    return false;
  }

  
  function minimax(newBoard, player, alpha, beta) {
    var availSpots = emptySquares();

    if (checkWin(newBoard, oplayer)) {
      return {score: -10};
    } else if (checkWin(newBoard, xplayer)) {
      return {score: 10};
    } else if (availSpots.length === 0) {
      return {score: 0};
    }
    var moves = [];
    for (var i = 0; i < availSpots.length; i++) {
      var move = {};
      move.index = newBoard[availSpots[i]];
      newBoard[availSpots[i]] = player;

      if (player == xplayer) {
        var result = minimax(newBoard, oplayer, alpha, beta);
        move.score = result.score;
      } else {
        var result = minimax(newBoard, xplayer, alpha, beta);
        move.score = result.score;
      }

      newBoard[availSpots[i]] = move.index;

      moves.push(move);
    }

    var bestMove;
    if(player === xplayer) {   
      var bestScore = -10000;
      for(var i = 0; i < moves.length; i++) {
        if (moves[i].score > bestScore) {
          bestScore = moves[i].score;
          bestMove = i;
          alpha = Math.max(alpha, bestScore);
          if(beta <= alpha) break;
        }
      }
    } else {  
      var bestScore = 10000;
      for(var i = 0; i < moves.length; i++) {
        if (moves[i].score < bestScore) {
          bestScore = moves[i].score;
          bestMove = i;
          beta = Math.min(beta, bestScore);
          if (beta <= alpha) break;
        }
      }
    }

    return moves[bestMove];
  }
  

  function randomPlayer(player) {
    var square = emptySquares()[Math.floor(Math.random() * emptySquares().length)];
    return square;
  }

})