import random


class EscapeRoom:
    door = "closed"
    locked = True
    hammer = False
    glasses = False
    glasses_wear = False
    mirror = False
    hairpin = False # judge hairpin visible or not
    floor = False
    pry = False
    clock = 100
    chest = "locked"  # three stutus: locked, unlocked and open
    board = "closed" # two stutus: closed and open
    stutas = "locked"

    hairpin_get = False

    code = 0

    def start(self):
        '''This method initializes the game'''
        code = random.randint(0, 9999)
        code_string = str(code)
        while len(code_string) < 4:
            code_string = '0' + code_string  # prepend zero's (e.g., 0123)
        comma_digit_list = ", ".join([digit for digit in code_string])


    def command(self, command_string):
        '''This command accepts the user's command within the game'''
        commandParts = command_string.split(" ")
        command = commandParts[0]
        if command == "look":
            EscapeRoom.lookCommand(commandParts[1:],command_string)

        elif command == "get":
            EscapeRoom.getCommand(commandParts[1:], command_string)
        elif command == "Inventory":
            EscapeRoom.inventoryCommand(commandParts[1:], command_string)
        elif command == "unlock":
            EscapeRoom.unlockCommand(commandParts[1:], command_string)
        elif command == "open":
            EscapeRoom.openCommand(commandParts[1:], command_string)
        elif command == "pry":
            EscapeRoom.pryCommand(commandParts[1:], command_string)
        elif command == "wear":
            EscapeRoom.wearCommand(commandParts[1:], command_string)

        EscapeRoom.clock = EscapeRoom.clock - 1

    def lookCommand(commandParts, command_string):
        if command_string == "look":
            print("You are in a locked room. There is only one door \n"
                  "and it has a numeric keypad. Above the door is a clock that reads <time>.\n"
                  "Across from the door is a large mirror. Below the mirror is an old chest.\n"
                  "\nThe room is old and musty and the floor is creaky and warped.")
        elif commandParts[0] == "in":
            if command_string == "look in chest":
                if(EscapeRoom.hammer == False):
                    print("Inside the chest you see: a hammer.")
                else:
                    print("Inside the chest you see: .")
            elif command_string == "look in board":
                if(EscapeRoom.glasses == False):
                    print("Inside the board you see: a glasses.")
                else:
                    print("Inside the board you see: .")
            else:
                print("You don't see that here.")
        else:
            if command_string == "look door":
                if(EscapeRoom.glasses == False):
                    print("The door is strong and highly secured. The door is locked and requires a 4-digit code to open.")
                else:
                    code_string = str(EscapeRoom.code)
                    while len(code_string) < 4:
                        code_string = '0' + code_string  # prepend zero's (e.g., 0123)
                    comma_digit_list = ", ".join([digit for digit in code_string])
                    print("The door is strong and highly secured. The door is locked and requires a 4-digit code to open."
                          " But now you're wearing these glasses you notice something! There are smudges on the digits"
                            + comma_digit_list +".")
            elif command_string == "look mirror":
                EscapeRoom.mirror = True
                if(EscapeRoom.hairpin == False):
                    EscapeRoom.hairpin = True
                    print("You look in the mirror and see yourself... wait, there's a hairpin in your hair. Where did that come from?")
                else:
                    print("You look in the mirror and see yourself.")
            elif command_string == "look chest":
                print("An old chest. It looks worn, but it's still sturdy.")
            elif command_string == "look floor":
                print("The floor makes you nervous. It feels like it could fall in. One of the boards is loose.")
                EscapeRoom.floor = True
            elif command_string == "look board":
                if(EscapeRoom.floor == False):
                    print("You don't see that here.")
                else:
                    if(EscapeRoom.pry == False):
                        print("The board is loose, but won't come up when you pull on it. Maybe if you pried it open with something.")
                    else:
                        print("The board has been pulled open. You can look inside.")
            elif command_string == "look hairpin":
                EscapeRoom.hairpin = True
                if( EscapeRoom.mirror == False):
                    print("You don't see that here.")
                else:
                    print("You see nothing special.")
            elif command_string == "look hammer":
                if(EscapeRoom.hammer == False):
                    print("You don't see that here.")
                else:
                    print("You see nothing special.")
            elif command_string == "look glasses":
                if(EscapeRoom.glasses == False):
                    print("You see nothing special.")
                else:
                    print("These look like spy glasses. Maybe they reveal a clue!")
            elif command_string == "look clock":
                print("You see nothing special.")
            else:
                print("You don't see that here.")
        return 0

    def getCommand(commandParts, command_string):
        if len(commandParts)>1 and commandParts[1] == "from":
            if command_string == "get hammer from chest":
                if(EscapeRoom.chest == "locked"):
                    print("It's not open.")
                else:
                    if(EscapeRoom.hammer == False):
                        print("You got it.")
                        EscapeRoom.hammer = True
                    else:
                        print("You don't see that.")
            elif command_string == "get glasses from board":
                if (EscapeRoom.board == "closed"):
                    print("It's not open.")
                else:
                    if (EscapeRoom.glasses == False):
                        print("You got it.")
                        EscapeRoom.glasses = True
                    else:
                        print("You don't see that.")
            else:
                if commandParts[2] != "chest" and commandParts[2] != "board":
                    print("You can't get something out of that!")
                else:
                    print("You don't see that.")
        else:
            if command_string == "get hairpin":
                if(EscapeRoom.hairpin == False):
                    print("You don't see that.")
                else:
                    if(EscapeRoom.hairpin_get == False):
                        print("You got it.")
                        EscapeRoom.hairpin_get = True
                    else:
                        print("You already have that.")
            elif command_string == "get board":
                if (EscapeRoom.floor == False):
                    print("You don't see that.")
                else:
                    print("You can't get that.")
            elif command_string == "get door":
                print("You can't get that.")
            elif command_string == "get clock":
                print("You can't get that.")
            elif command_string == "get mirror":
                print("You can't get that.")
            elif command_string == "get chest":
                print("You can't get that.")
            elif command_string == "get floor":
                print("You can't get that.")
            elif command_string == "get hammer":
                if(EscapeRoom.hammer == True):
                    print("You already have that.")
            elif command_string == "get glasses":
                if (EscapeRoom.glasses == True):
                    print("You already have that.")
            else:
                print("You don't see that.")

    def inventoryCommand(commandParts, command_string):
        string = "You are carrying."
        #", ".join([string,2,3,4])

    def unlockCommand(commandParts, command_string):
        if commandParts[0] == "chest":
            if EscapeRoom.chest == "open":
                print("It's already unlocked.")
            else:
                if commandParts[2] == "hairpin":
                    EscapeRoom.chest = "open"
                    print("You hear a click! It worked!")
                else:
                    print("You don't have a unlocker-name")
        elif commandParts[0] == "door":
            if EscapeRoom.door == "open":
                print("It's already unlocked.")
            else:
                if commandParts[2].isdigit() == False:
                    "That's not a valid code."
                else:
                    if len(commandParts[2]) == 4:
                        if commandParts[2] == EscapeRoom.code:
                            EscapeRoom.door = "open"
                            print("You hear a click! It worked!")
                        else:
                            print("That's not the right code!")
                    else:
                        print("The code must be 4 digits.")
        elif commandParts[0] == "hairpin":
            if EscapeRoom.hairpin == False:
                print("You don't see that here.")
            else:
                print("You can't unlock that!")
        elif commandParts[0] == "board":
            if EscapeRoom.floor == False:
                print("You don't see that here.")
            else:
                print("You can't unlock that!")
        elif commandParts[0] == "hammer":
            if EscapeRoom.hammer == False:
                print("You don't see that here.")
            else:
                print("You can't unlock that!")
        elif commandParts[0] == "glasses":
            if EscapeRoom.glasses == False:
                print("You don't see that here.")
            else:
                print("You can't unlock that!")
        elif commandParts[0] == "clock":
            print("You can't unlock that!")
        elif commandParts[0] == "mirror":
            print("You can't unlock that!")
        elif commandParts[0] == "floor":
            print("You can't unlock that!")
        else:
            print("You don't see that here.")

    def openCommand(commandParts, command_string):
        if commandParts[0] == "chest":
            if EscapeRoom.chest == "locked":
                print("It's locked.")
            else:
                if EscapeRoom.chest == "open":
                    print("It's already open!")
                else:
                    print("You open the chest.")
                    EscapeRoom.chest = "unlocked"
        elif commandParts[0] == "door":
            if EscapeRoom.door == "closed":
                print("It's locked.")
            else:
                print("You open the door.")

        elif commandParts[0] == "hairpin":
                if EscapeRoom.hairpin == False:
                    print("You don't see that.")
                else:
                    print("You can't open that!")
        elif commandParts[0] == "board":
            if EscapeRoom.floor == False:
                print("You don't see that.")
            else:
                print("You can't open that!")
        elif commandParts[0] == "hammer":
            if EscapeRoom.hammer == False:
                print("You don't see that.")
            else:
                print("You can't open that!")
        elif commandParts[0] == "glasses":
            if EscapeRoom.glasses == False:
                print("You don't see that.")
            else:
                print("You can't open that!")
        elif commandParts[0] == "clock":
            print("You can't open that!")
        elif commandParts[0] == "mirror":
            print("You can't open that!")
        elif commandParts[0] == "floor":
            print("You can't open that!")
        else:
            print("You don't see that.")

    def pryCommand(commandParts, command_string):
        if commandParts[0] == "board":
            if (EscapeRoom.floor == False): # board is invisble
                print("You don't see that.")
            else:
                if EscapeRoom.hammer == True: # if player has hammer
                    if command_string == "pry board with hammer":
                        if EscapeRoom.board == "closed": # board is still closed
                            EscapeRoom.board = "open"
                            print("You use the hammer to pry open the board. It takes some work, "
                                    "but with some blood and sweat, you mange to get it open.")
                        else:
                            print("It's already pried open.")  # board is open
                    else:
                        print("You don't have a tool-name")
                else:
                    print("You don't have a hammer.")

        elif commandParts[0] == "hairpin":
            if EscapeRoom.hairpin == False:
                print("You don't see that.")
            else:
                print("Don't be stupid! That won't work!")

        elif commandParts[0] == "hammer":
            if EscapeRoom.hammer == False:
                print("You don't see that.")
            else:
                print("You can't open that!")

        elif commandParts[0] == "glasses":
            if EscapeRoom.glasses == False:
                print("You don't see that.")
            else:
                print("You can't open that!")

        elif commandParts[0] == "door":
            print("Don't be stupid! That won't work!")
        elif commandParts[0] == "chest":
            print("Don't be stupid! That won't work!")
        elif commandParts[0] == "clock":
            print("Don't be stupid! That won't work!")
        elif commandParts[0] == "mirror":
            print("Don't be stupid! That won't work!")
        elif commandParts[0] == "floor":
            print("Don't be stupid! That won't work!")
        else:
            print("You don't see that.")

    def wearCommand(commandParts, command_string):
        if commandParts[0] == "glasses":
            if EscapeRoom.glasses == False:
                print("You don't have a glasses.")
            else:
                if EscapeRoom.glasses_wear == False:
                    print("You are now wearing the glasses.")
                    EscapeRoom.glasses_wear == True
                else:
                    print("You're already wearing them!")
        else:
            print("You don't have a object-name.")

    def status(self):
        '''Reports whether the users is "dead", "locked", or "escaped"'''
        if (EscapeRoom.door == "closed"):
            if(EscapeRoom.clock>0):
                EscapeRoom.stutas = "locked"
            else:
                EscapeRoom.stutas = "dead"
        else:
            if(EscapeRoom.clock>0):
                EscapeRoom.stutas = "escaped"
            else:
                EscapeRoom.stutas = "dead"
        return EscapeRoom.stutas

room = EscapeRoom()
room.start()
while(room.door == "closed"):
    command = input(">> ")
    room.command(command)

