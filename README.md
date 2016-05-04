# smashBros
Cory Jbara and Madelyn Nelson

Multiplayer game using PyGame and Twisted 

Server must be running on student00 with the following command: 
python2.6 server.py 

To start the game, use the following command: python2.6 play.py <playerNumber>
<playerNumber> must be either 1 or 2, and the two players playing must choose who is who.


This game simulates the most basic of all Smash Bros games. In order to play,
you have to connect to the server. Once you connnect, you can move either
direction with the left and right keys and jump with the space bar. The
objective of the game is to get the other player off the screen. In order to do
this, you use the 's' key to shoot fireballs/arrows (for Mario and Link
respectively), and once youre opponent dies three times, you win! 

We implemented gravity and friction in the game, and your % damage is
proportional to your knockback. Your damage and number of lives are displayed
in the top corner of the screen.


