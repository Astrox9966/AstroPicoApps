black = rgb("0, 0, 0")
white = rgb("255, 255, 255")
lightgrey = rgb("211, 211, 211")  
darkgrey = rgb("169, 169, 169")   
grey = rgb("128, 128, 128")       

' ASTRALIXI OS Startup for PicoCalc
PRINT "ASTRALIXI OS"
PRINT "By Astrox!"
PRINT

DIM boardType$ = ""
DIM wifiFound = 0

' Setup I2C on standard Pico W pins (GPIO 4=SDA, 5=SCL)
I2C OPEN 1, 400, 100
I2C SCAN

' Check for Wi-Fi module at I2C address 0x50
FOR i = 0 TO MM.I2CDEVICES - 1
    IF MM.I2CADDRESS(i) = &H50 THEN
        wifiFound = 1
        EXIT FOR
    ENDIF
NEXT i
I2C CLOSE

' Detect board type based on PEEK memory address (may vary by firmware)
IF wifiFound THEN
    IF PEEK(&H40000000) = &H20000000 THEN
        boardType$ = "Raspberry Pi Pico W"
    ELSE
        boardType$ = "Raspberry Pi Pico 2W"
    ENDIF
ELSE
    IF PEEK(&H40000000) = &H20000000 THEN
        boardType$ = "Raspberry Pi Pico"
    ELSE
        boardType$ = "Raspberry Pi Pico 2"
    ENDIF
ENDIF

PRINT "Detected board: "; boardType$
Pause 1000
CLS

DO
    INPUT "/"; userInput$
    
    IF userInput$ <> "" THEN
        ' Dummy IF statement: check for a specific command
        IF LCASE$(userInput$) = "hello" THEN
            PRINT "Hi there!"
        ELSEIF LCASE$(userInput$) = "time" THEN
            PRINT "Current time: "; TIME$
        ELSEIF LCASE$(userInput$) = "clear" THEN
            CLS
        ELSEIF LCASE$(userInput$) = "files list" THEN
            FILES "/sdcard"
        ELSE
            PRINT "Command not recognized."
        ENDIF
    ENDIF

LOOP