black = rgb(0, 0, 0)
white = rgb(255, 255, 255)
lightgrey = rgb(211, 211, 211)  
darkgrey = rgb(169, 169, 169)   
grey = rgb(128, 128, 128)       

' ASTRALIXI OS Startup for PicoCalc
PRINT "ASTRALIXI OS"
PRINT "By Astrox!"
PRINT

DIM boardType$ = ""
DIM wifiFound = 0

' Setup I2C on standard Pico W pins (GPIO 4=SDA, 5=SCL)
I2C OPEN 1, 400

' Scan I2C devices to find Wi-Fi module
I2C SCAN

' Check for Wi-Fi module at I2C address 0x50
wifiFound = 0
FOR i = 0 TO 127 ' There are 128 possible I2C addresses
    IF I2C READ(i, 1) >= 0 THEN ' If a response is received, device is present
        IF i = &H50 THEN
            wifiFound = 1
            EXIT FOR
        END IF
    END IF
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

' Create the Command List as an array of strings
DIM commandList$(30)
commandList$(1) = "files list = Lists all files on the SD card" ' done
commandList$(2) = "files open <filename> = Opens a file for running or viewing" ' done
commandList$(3) = "files create <filename> = Creates a new file" ' done
commandList$(4) = "files delete <filename> = Deletes a specified file"
commandList$(5) = "files rename <oldname> <newname> = Renames a file"
commandList$(6) = "app open <app_name> = Opens and runs an application from the /software directory" ' done
commandList$(7) = "app list = Lists all installed applications"
commandList$(8) = "app install <app_name> = Installs an application"
commandList$(9) = "app remove <app_name> = Removes an installed application"
commandList$(10) = "gpio set <pin> <state> = Sets a GPIO pin to HIGH (1) or LOW (0)"
commandList$(11) = "gpio read <pin> = Reads the state of a GPIO pin (returns 0 or 1)"
commandList$(12) = "gpio toggle <pin> = Toggles the state of a GPIO pin"
commandList$(13) = "wifi connect <SSID> <password> = Connects to a Wi-Fi network"
commandList$(14) = "wifi status = Shows the current Wi-Fi connection status"
commandList$(15) = "wifi scan = Scans for available Wi-Fi networks"
commandList$(16) = "time get = Displays the current time"
commandList$(17) = "time set <HH:MM:SS> = Sets the current system time"
commandList$(18) = "time format = Shows or sets the time format (12-hour/24-hour)"
commandList$(19) = "memory = Shows the current available and used memory"
commandList$(20) = "cpu usage = Displays the current CPU usage"
commandList$(21) = "shutdown = Shuts down the operating system"
commandList$(22) = "reboot = Restarts the operating system"
commandList$(23) = "clear = Clears the screen"
commandList$(24) = "cls = Clears the terminal screen"
commandList$(25) = "task list = Lists all running tasks or processes"
commandList$(26) = "task kill <task_id> = Kills a task with the given task ID"
commandList$(27) = "task pause <task_id> = Pauses a task with the given task ID"
commandList$(28) = "task resume <task_id> = Resumes a paused task"
commandList$(29) = "search <filename> = Searches for a file by name on the SD card"
commandList$(30) = "cd <directory> = Changes the current directory"

DO
    INPUT "/"; userInput$
    
    IF userInput$ <> "" THEN
        IF LCASE$(userInput$) = "hello" THEN
            PRINT "Hi there!"
        ELSEIF LCASE$(userInput$) = "time" THEN
            PRINT "Current time: "; TIME$
        ELSEIF LCASE$(userInput$) = "clear" THEN
            CLS
        ELSEIF LCASE$(userInput$) = "files list" THEN
            FILES "/sdcard"
        ELSEIF LCASE$(userInput$) = "commands list" THEN
            PRINT "Command List:"
            PRINT "----------------"
            FOR i = 1 TO 30
                PRINT commandList$(i)
            NEXT i
        ELSEIF LEFT$(LCASE$(userInput$), 11) = "files open " THEN
            fileToRun$ = MID$(userInput$, 12) 
            IF EXISTS(fileToRun$) THEN
                RUN fileToRun$
            ELSE
                PRINT "File not found."
            END IF
        ELSEIF LEFT$(LCASE$(userInput$), 13) = "files create " THEN
            fileToCreate$ = MID$(userInput$, 14) 
            IF EXISTS(fileToCreate$) THEN
                NEW 
                Save fileToCreate$
            ELSE
                PRINT "Error making file!"
            END IF
        ELSEIF LEFT$(userInput$, 9) = "app open " THEN
            appName$ = MID$(userInput$, 10)
            RUN "/software/" + appName$
        ELSE
            PRINT "Command not recognized."
        ENDIF
    ENDIF

LOOP
