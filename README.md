# a1_hw2
About the minimax search algorithm, alpha-beta pruning.  

Making the ai agent of the 6x7 connect four game with depth 4.

The structure of game is made by the TA.

I only build 3 agents.
## Minimax agent
The normal vision using minimax. 

It runs very slow, the time complexity is O(7^4). 

## Minimax with Alpha-beta pruing agent
Not only the > or < break the search, also the = .

The speed of this agent is 4 times faster than last one. 
## Own
Using the alpha-beta pruing algorithm, but without = .

And change the value function.

The original value funtion is counting the number of 2 nodes  and 3 nodes connected, from different player. 

Then get the value from computing the number with weight from big to small.

I rewrite it become counting the number of (one side empty)2 nodes connected, (two sides empty) 2 nodes connected, 

(one side empty) 3 nodes connected, (two sides empty) 3 nodes connected.

It can think more detail.

The speed of this agent is between the first one and the second one.
