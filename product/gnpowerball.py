#=================================================================================
# Assignment: Company Product Milestone 3 
# Team: GoldenNugget
# Description: Technical Functionality 1: Powerball Game Implmentation
#==================================================================================

import random

powerball_number = []
class PowerBallGenerator():
  def __init__(self):
  
  def generate(self):
  	for i in range(5):
 	 		powerball_number.append(random.randint(1,69))
  
#=================================================================================
# Class Description: Powerball Game Entrance Page
# Include: 1. Announcement Box: current $$ poll, last week winning number)
#   		   2. Option Menu (1. Start the game, 2. Rules and Prices Explained here, 
#											  3. Claim Your Prize Here! 4. Auction Your Ticket Here! )'''
#==================================================================================
 
class ClientPowerBall():
	def __init__(self):
  	self.numbers = []
    self.response = ""
    self.receipt = ""
    
  #Connect to bank and confirm the transaction id
  def check_transaction(self):
  	
  #client chooses five numbers between 1-69, they are separated by ';'
  
  def auto_generator(self):
    while True:
      for i in range(5):
      	self.numbers.append(random.randint(1,69)) 
    	if self.check_numbers:
    		break 
    	else:
        continue
    
    self.response += "All five numbers have been generated./n"
    return self.respnse;
    
    
    
  def client_numbers(self, string):
    numbers_list = stirng.split(str=";", num = 4)
    for i in range(5):
    	self.numbers.append(int(numbers_list[i]))
    if self.check_numbers():
      self.response += "\n Number has been accepted\n"
      self.genrate_receipt()
    else:
      self.response += "\n One of the numbers Are INVALID"
      self.receipt = NULL
      return self.response, self.receipt
      
  def generate_receipt(self,transaction_id):
    
  #check numbers
  def check_numbers(self):
    for i in self.numbers:
      	if i > 69 & i <= 0:
          return False
    return True

	def rules_prizes(self):
  #Option_2 is used to display rules, prizes and prices 
  	self.respomse +="""
    EACH GAME IS WORTH 10 BITPOINTS
  	1. Select five numbers from 1 to 69 or you can also choose a 'Randomly Generated Ticket' that gives you 5 randonly generated numbers 
 		2. Every Monday and Thursday the PowerBall rolls and 5 random winning numbers are displayed on our home page 
    3. If 3 or more of your ticket numbers match with the winning numbers on the PowerBall, you win according to the Prizes listed
    4. To claim your prize, go to our home page and choose the 'Claim Prize' option"""
    
    self.response += "PRIZES"
    self.response += """
+---------+------------------+
| Matches |      Prizes      |
|         |                  |
+----------------------------+
|         |                  |
|    1    | No Prize         |
|         |                  |
|         |                  |
|    2    | No Prize         |
|         |                  |
|         |                  |
|    3    | 20% of the Pool  |
|         |                  |
|         |                  |
|    4    | 30% of the Pool  |
|         |                  |
|         |                  |
|    5    | 50% of the Pool  |
|         |                  |
+---------+------------------+
"""

  def claim_prize(self):
  #Option_3 is used to Claim Your Prize
  	matches = 0
    prize = ""
    for i in range(5):
      if powerball_number.count(numbers[i]) == 1:
        matches = matches + 1    
  	if matches == 3:
      prize = "20% of the Pool"
  	elif matches == 4:
    	prize = "20% of the Pool"
    elif matches == 5:
      prize = "20% of the Pool"
    else:
      prize = "No Prize"
    return prize
    
  def main():
    
    
if "__name__" == "__main__":
  itstime = PowerBallGenerator()
  itstime.generate()
