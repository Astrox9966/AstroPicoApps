year = 250000
yearclock = 1
pixelclock = 0
Print "Welcome to the Simulation!"

' Initialize the display
CLS   ' Clear the screen and initialize the graphics

' Year loop using DO...LOOP
DO
  year = year - 1000
  Print year
  yearclock = yearclock + 1
LOOP UNTIL yearclock >= 250

' Pixel loop using DO...LOOP
DO
  Pixel 0, 0, RGB(0, 0, 0)   ' Set pixel (0, 0) to black
  pixelclock = pixelclock + 1
LOOP UNTIL pixelclock >= 100
