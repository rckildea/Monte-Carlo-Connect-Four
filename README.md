# Monte Carlo Connect Four
This project implements a Monte Carlo Tree Search (MCTS) for two AI players in a game of Connect Four.  The tree allows each player to estimate their best move along each step of the way.  I wrote this program for my Introduction to Artificial Intelligence class.

## How It Works
<p>The AI will take the current board with whatever game pieces have been played, and will create a copy of that board.  On this copy, it will make a valid move, and will store the value for the position in which it placed its game piece.  From here, it will randomly simulate back-and-forth play between the two AI until the game comes to an end.  The AI then stores the value for the initial move it started with and keeps track of how many times it made each move.  Once the AI has ran through all of its simulations (the number of simulations the AI will perform is defined within its object), it will compare the relative value of each move (win = good, loss = bad, draw = okay) and the amount of times it randomly chose that move.  It will then select the best move from its possible moves.  Then, the next AI will move, and will follow the same steps.  This process repeats until a winner is found or the board is full.  It then repeats for a user-defined amount of games, and calculates the win percentages of both players.</p>
<p>For each run of the program, it also keeps track of all visited states and the calculated best move.  Because the player to make the first move is always randomized (so that no significant advantage occurs), it ensures that inverted states are also added.  So, for example, if we save the following state on the left, we will also save the state on the right, even if it was not explicitly visited.</p>
 <p align="center"> 
<img src="https://i.imgur.com/6rVO7Y1.png">
</p>
<p>Because it keeps track of visited states, it can reference them in subsequent games.  If a previously visited state was found and the best move had a win percentage greater than or equal to 50%, it will make the same move again.  If not, it will disregard the previous state, and attempt to find a better solution.</p>
<p>Below is an example printout of a trial where red ran 1000 trials per move and yellow ran 2000 trials per move.</p>
  <p align="center"> 
<img src="https://imgur.com/7c7lh2F.png">
</p>
