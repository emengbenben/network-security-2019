#====================================================================================================
# Assignment: Company Product Milestone 3 
# Team: GoldenNugget
# Description: Technical Functionality: GoldenNugget Home page and selections
# Include: 1. Welcome narratives
#          2. Option Menu (1. Powerball, 2. Roulette, 3. Deal or no Deal, 4. About us 5. Careers)
#======================================================================================================
from gnpowerball import ClientPowerBall #from (project folder name)

class GoldenNugget():
  def __init__(self):
  
  def welcome_narratives(self):
    	output = ""
  		output += """
      Welcome to the Golden Nugget Casino!
  		WHERE FRIENDSHIP IS THE LARGEST JACKPOT!
      
      May we all be winners -> complete assignemnts, pass this course, get straight As, and an internship & job.
      
      Speaking of internships and jobs, we have an expert team here at Golden Nugget to assist with your career needs: 
      		-10 Bitpoints for resume review or cover letter review
          -100 bitpoints for writing your cover letter
          -250 bitpoints for internship/job referral
          
  		Casino Services Menu:
      		1. Powerball
          2. Roulette
          3. Deal or No Deal
          4. Career Assisstance # direct transfer with memo
          5. About Us
          6. Career with Golden Nugget Casino
          
  		Note: You can choose the menu by enter a single digit that is corresponding to the menu."
      """
      return output 
  
  def choose_game(self, userInput):
  	if userInput == "1":
  			ClientPowerBall.main() 
  	else:
  		output  = "Please enter a single digit of your choice."
	  return output

if "__name__" == "__main__"
	


















