import random


class EscapeRoom:
    door = "closed"
    locked = True
    hammer = False
    glasses = False
    glasses_wear = False
    mirror = False
    hairpin = False  # judge hairpin visible or not
    floor = False  # judge whether player look floor or not
    pry = False
    clock = 100
    chest = "locked"  # three stutus: locked, unlocked and open
    board = "closed"  # two stutus: closed and open
    stutas = "locked"

    hairpin_get = False # judge whether get hairpin or not

    code = 0
    code_string = ""
    comma_digit_list = ""

    def start(self):
        '''This method initializes the game'''
        self.code = random.randint(0, 9999)
        self.code_string = str(self.code)
        while len(self.code_string) < 4:
            self.code_string = '0' + self.code_string  # prepend zero's (e.g., 0123)
        list1 = [digit for digit in self.code_string]
        list2 = list(set(list1))
        list2.sort()
        self.comma_digit_list = ", ".join(list2)

    def command(self, command_string):
        '''This command accepts the user's command within the game'''
        response = ""  # this is the response string
        commandParts = command_string.split(" ")
        command = commandParts[0]
        if command == "look":
            response = self.lookCommand(commandParts[1:], command_string)
        elif command == "get":
            response = self.getCommand(commandParts[1:], command_string)
        elif command == "inventory":
            response = self.inventoryCommand(commandParts[1:], command_string)
        elif command == "unlock":
            response = self.unlockCommand(commandParts[1:], command_string)
        elif command == "open":
            response = self.openCommand(commandParts[1:], command_string)
        elif command == "pry":
            response = self.pryCommand(commandParts[1:], command_string)
        elif command == "wear":
            response = self.wearCommand(commandParts[1:], command_string)
        else:
            response = "This is not an effective command."

        self.clock = self.clock - 1  # clock-1 after a command
        if(self.clock == 0):
            response = response +"\nOh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas..."
        return response

    def lookCommand(self, commandParts, command_string):
        response = ""
        if command_string == "look":
             str1 = "You are in a locked room. There is only one door \n"
             str2 = "and it has a numeric keypad. Above the door is a clock that reads "+str(self.clock)+ ".\n"
             str3 = "Across from the door is a large mirror. Below the mirror is an old chest.\n"
             str4 = "\nThe room is old and musty and the floor is creaky and warped."
             response = str1+str2+str3+str4
        elif commandParts[0] == "in":
            if command_string == "look in chest":
                if (self.hammer == False):
                    response = "Inside the chest you see: a hammer."
                else:
                    response = "Inside the chest you see: ."
            elif command_string == "look in board":
                if (self.glasses == False):
                    response = "Inside the board you see: a glasses."
                else:
                    response = "Inside the board you see: ."
            else:
                response = "You don't see that here."
        else:
            if command_string == "look door":
                if (self.glasses == False):
                    response = "The door is strong and highly secured. The door is locked and requires a 4-digit code to open."
                else:
                    string1 = "The door is strong and highly secured. The door is locked and requires a 4-digit code to open."
                    string2 = " But now you're wearing these glasses you notice something! There are smudges on the digits "
                    string3 = self.comma_digit_list + "."
                    response = string1 +string2 +string3
            elif command_string == "look mirror":
                self.mirror = True
                if (self.hairpin_get == False):
                    self.hairpin = True
                    response = "You look in the mirror and see yourself... wait, there's a hairpin in your hair. Where did that come from?"
                else:
                    response = "You look in the mirror and see yourself."
            elif command_string == "look chest":
                response = "An old chest. It looks worn, but it's still sturdy."
            elif command_string == "look floor":
                response = "The floor makes you nervous. It feels like it could fall in. One of the boards is loose."
                self.floor = True
            elif command_string == "look board":
                if (self.floor == False):
                    response = "You don't see that here."
                else:
                    if (self.pry == False):
                        response = "The board is loose, but won't come up when you pull on it. Maybe if you pried it open with something."
                    else:
                        response = "The board has been pulled open. You can look inside."
            elif command_string == "look hairpin":
                self.hairpin = True
                if (self.mirror == False):
                    response = "You don't see that here."
                else:
                    response = "You see nothing special."
            elif command_string == "look hammer":
                if (self.hammer == False):
                    response = "You don't see that here."
                else:
                    response = "You see nothing special."
            elif command_string == "look glasses":
                if (self.glasses == False):
                    response = "You see nothing special."
                else:
                    response = "These look like spy glasses. Maybe they reveal a clue!"
            elif command_string == "look clock":
                response = "You see nothing special."
            else:
                response = "You don't see that here."
        return response

    def getCommand(self, commandParts, command_string):
        response = ""
        if len(commandParts) > 1 and commandParts[1] == "from":
            if command_string == "get hammer from chest":
                if  self.chest == "locked":
                    response = "It's not open."
                else:
                    if (self.hammer == False):
                        response = "You got it."
                        self.hammer = True
                    else:
                        response = "You don't see that."
            elif command_string == "get glasses from board":
                if (self.board == "closed"):
                    response = "It's not open."
                else:
                    if (self.glasses == False):
                        response = "You got it."
                        self.glasses = True
                    else:
                        response = "You don't see that."
            else:
                if commandParts[2] != "chest" and commandParts[2] != "board":
                    response = "You can't get something out of that!"
                else:
                    response = "You don't see that."
        else:
            if command_string == "get hairpin":
                if (self.hairpin == False):
                    response = "You don't see that."
                else:
                    if (self.hairpin_get == False):
                        response = "You got it."
                        self.hairpin_get = True
                    else:
                        response = "You already have that."
            elif command_string == "get board":
                if (self.floor == False):
                    response = "You don't see that."
                else:
                    response = "You can't get that."
            elif command_string == "get door":
                response = "You can't get that."
            elif command_string == "get clock":
                response = "You can't get that."
            elif command_string == "get mirror":
                response = "You can't get that."
            elif command_string == "get chest":
                response = "You can't get that."
            elif command_string == "get floor":
                response = "You can't get that."
            elif command_string == "get hammer":
                if (self.hammer == True):
                    response = "You already have that."
                else:
                    response = "You don't see that."
            elif command_string == "get glasses":
                if (self.glasses == True):
                    response = "You already have that."
                else:
                    response = "You don't see that."
            else:
                response = "You don't see that."
        return response

    def inventoryCommand(self, commandParts, command_string):
        response = ""
        if self.hairpin_get == True:
            if self.hammer == True:
                if self.glasses == True:
                    inventoryList = ["hairpin", " a hammer", " a glasses"]
                else:
                    inventoryList = ["hairpin", " a hammer"]
            else:
                inventoryList = ["hairpin"]
        else:
            inventoryList =[]
        inventoryString = ",".join(inventoryList)
        string = "You are carrying a "
        response = string + inventoryString +"."
        return response

    def unlockCommand(self, commandParts, command_string):
        response = ""
        if len(commandParts) == 1:
            response = "with what?"
        else:
            if commandParts[0] == "chest":
                if self.chest == "open":
                    response = "It's already unlocked."
                else:
                    if commandParts[2] == "hairpin":
                        self.chest = "open"
                        response = "You hear a click! It worked!"
                    else:
                        response = "You don't have a unlocker-name"
            elif commandParts[0] == "door":
                if self.door == "open":
                    response = "It's already unlocked."
                else:
                    if commandParts[2].isdigit() == False:
                        "That's not a valid code."
                    else:
                        if len(commandParts[2]) == 4:
                            if commandParts[2] == self.code_string:
                                self.door = "open"
                                response = "You hear a click! It worked!"
                            else:
                                response = "That's not the right code!"
                        else:
                            response = "The code must be 4 digits."
            elif commandParts[0] == "hairpin":
                if self.hairpin == False:
                    response = "You don't see that here."
                else:
                    response = "You can't unlock that!"
            elif commandParts[0] == "board":
                if self.floor == False:
                    response = "You don't see that here."
                else:
                    response = "You can't unlock that!"
            elif commandParts[0] == "hammer":
                if self.hammer == False:
                    response = "You don't see that here."
                else:
                    response = "You can't unlock that!"
            elif commandParts[0] == "glasses":
                if self.glasses == False:
                    response = "You don't see that here."
                else:
                    response = "You can't unlock that!"
            elif commandParts[0] == "clock":
                response = "You can't unlock that!"
            elif commandParts[0] == "mirror":
                response = "You can't unlock that!"
            elif commandParts[0] == "floor":
                response = "You can't unlock that!"
            else:
                response = "You don't see that here."
        return  response

    def openCommand(self, commandParts, command_string):
        response = ""
        if commandParts[0] == "chest":
            if self.chest == "locked":
                response = "It's locked."
            else:
                if self.chest == "unlocked":
                    response = "It's already open!"
                else:
                    response = "You open the chest."
                    self.chest = "unlocked"
        elif commandParts[0] == "door":
            if self.door == "closed":
                response = "It's locked."
            else:
                response = "You open the door."

        elif commandParts[0] == "hairpin":
            if self.hairpin == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"
        elif commandParts[0] == "board":
            if self.floor == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"
        elif commandParts[0] == "hammer":
            if self.hammer == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"
        elif commandParts[0] == "glasses":
            if self.glasses == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"
        elif commandParts[0] == "clock":
            response = "You can't open that!"
        elif commandParts[0] == "mirror":
            response = "You can't open that!"
        elif commandParts[0] == "floor":
            response = "You can't open that!"
        else:
            response = "You don't see that."
        return response

    def pryCommand(self, commandParts, command_string):
        response = ""
        if commandParts[0] == "board":
            if (self.floor == False):  # board is invisble
                response = "You don't see that."
            else:
                if self.hammer == True:  # if player has hammer
                    if command_string == "pry board with hammer":
                        if self.board == "closed":  # board is still closed
                            self.board = "open"
                            str1 = "You use the hammer to pry open the board. It takes some work, "
                            str2 = "but with some blood and sweat, you manage to get it open."
                            response = str1 + str2
                        else:
                            response = "It's already pried open."  # board is open
                    else:
                        response = "You don't have a tool-name"
                else:
                    response = "You don't have a hammer."

        elif commandParts[0] == "hairpin":
            if self.hairpin == False:
                response = "You don't see that."
            else:
                response = "Don't be stupid! That won't work!"

        elif commandParts[0] == "hammer":
            if self.hammer == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"

        elif commandParts[0] == "glasses":
            if self.glasses == False:
                response = "You don't see that."
            else:
                response = "You can't open that!"

        elif commandParts[0] == "door":
            response = "Don't be stupid! That won't work!"
        elif commandParts[0] == "chest":
            response = "Don't be stupid! That won't work!"
        elif commandParts[0] == "clock":
            response = "Don't be stupid! That won't work!"
        elif commandParts[0] == "mirror":
            response = "Don't be stupid! That won't work!"
        elif commandParts[0] == "floor":
            response = "Don't be stupid! That won't work!"
        else:
            response = "You don't see that."
        return response

    def wearCommand(self, commandParts, command_string):
        response = ""
        if commandParts[0] == "glasses":
            if self.glasses == False:
                response = "You don't have a glasses."
            else:
                if self.glasses_wear == False:
                    response = "You are now wearing the glasses."
                    self.glasses_wear == True
                else:
                    response = "You're already wearing them!"
        else:
            response = "You don't have a object-name."
        return response

    def status(self):
        '''Reports whether the users is "dead", "locked", or "escaped"'''
        string = ""
        if (self.door == "closed"):
            if (self.clock > 0):
                self.stutas = "locked"
            else:
                self.stutas = "dead"
        else:
            if (self.clock > 0):
                self.stutas = "escaped"
            else:
                self.stutas = "dead"
        return self.stutas

