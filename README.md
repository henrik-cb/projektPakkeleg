# projektPakkeleg
This project is a simple random timer for a Raspberry Pi connected to LEDs, a flip switch and a speaker. The control is entirely headless using the flip switch. If the script is run at boot, then no connection to the Pi is needed.

The project is intended for the Danish game 'Pakkeleg' where a random timer determines when the game ends.
The controls is as follows:

- Start the timer by flipping the switch on (with default time window 10-15 minutes).

- Stop the timer by flipping off the switch.

- Set the time window by flipping the switch on and off fast. This enters the set mode. 

  - First, the minimum time is set by turning the switch on and off quickly, with each increasing the minimum time by 2 minutes. This is indicated by a LED turning on for each 2 minutes. When the required minimum time is reached, flip the switch on.
  - Second, the maximum time is set by turning the switch off and on quickly, with each increasing the maximum time by 2 minutes. The LED also indicate this. When finished, turn the switch off.
  - The time window is now set untill changed or the script is restarted.


This is a simple code for my own amusement, so output is in Danish and comments are few. Feel free to contact me with questions or comments.


