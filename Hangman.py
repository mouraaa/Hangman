import pygame
import math
import random

#--------------------------------------------------------
#basic setup
pygame.init() #ALWAYS initialize pygame to use it (basically setting it up)
WIDTH, HEIGHT = 800, 550
window = pygame.display.set_mode((WIDTH,HEIGHT)) #setting up the game window (pygame only accepts a tuple for set_mode so you have to add the extra pair of paranthesis
pygame.display.set_caption("Hangman") #setting up the label on top of the game
FPS = 60
clock = pygame.time.Clock() #makes sure the loop runs at a specific speed

#--------------------------------------------------------
#Loading Images
images = [] 
for i in range(1,8): #range(inclusive, exlusive) --> check comment on line 15 to see why we chose (1,8) 
	image = pygame.image.load("hangman" + str(i) + ".png") #this is how you load an image from pygame (it only accepts the name of the image)
	images.append(image) #add the image to the list

#--------------------------------------------------------
#Game Variables:
A = 65 #in programming, capital a = 65 and capital b = 66 etc.
x = 65
y = 400

hangman_status = 0
RADIUS = 20
GAP = 55
THICK = 3
WHITE = (255,255,255) #these need to be in paranthesis because drawing functions only accepts tuples
BLACK = (0,0,0)

words = [] #has to be all uppercase bc of line 45 when we use chr(A + i), we are starting off at Capital A and ending at Capital Z and
#were compare if those capital letters in the list match the letters in the word. They will never match if its capital a and lowercase a
with open("words.txt") as f:
	for i in f:
		words.append(i.rstrip())
word = random.choice(words)
guessed = []

#--------------------------------------------------------
#GAME BUTTONS
buttons = []
for i in range(26):
	if x < 740:
		buttons.append([x,y,chr(A + i),True]) #chr(A+i) will add the capital letter representation of A-Z of the number given each iteration
		x += GAP
	else:
		x = 65
		y = 460
		buttons.append([x,y,chr(A + i),True]) #char(A+i) will add the number representation of each capital letter A-Z 
		x += GAP

button_font = pygame.font.SysFont('comicsans', 40) #PARAMETERS ---> font name, font size
word_font = pygame.font.SysFont('comicsans', 60)

#--------------------------------------------------------
#METHODS
def display_message(message):
	window.fill(WHITE) #overrides the entire screen with white
	text = button_font.render(message, 1, BLACK) #text needs to be rendered first --> Paramers: what you want to render, 1, color of text
	window.blit(text, (350, 250))	
	pygame.display.update() #you need to update the display everytime if you change anything in the display
	pygame.time.delay(2000) #delays for 2 seconds

#--------------------------------------------------------
#Game Loop 
#whenever you create a pygame program, you need a loop to constantly check for collisions/ see if you clicked something, see if time runs out, etc.
run = True
while run:
	clock.tick(FPS) #necessary to make sure the while loops runs at the speed we set up on line 9-10
	window.fill(WHITE) #fills the window with a specific color --> only takes RGB values within a tuple (the two extra paranthesis)
	window.blit(images[hangman_status], (50,110)) #blit stands for draw (PARAMETERS: (what you want to draw, x,y position of where you want to draw it)

	#Drawing the word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			display_word += "_ "
	text = word_font.render(display_word, 1, BLACK)
	window.blit(text,(400,200))

	#Drawing the Title
	text = word_font.render('DEVELOPER HANGMAN', 1, BLACK)
	window.blit(text,(160,20))

	#Drawing the buttons
	for button in buttons:
		x,y,letter,visible = button #since the list is in triples, EX(50,70,'B',TRUE) --> x = 50 and y = 70, letter = B, visible = TRUE
		if visible:
			pygame.draw.circle(window, BLACK, (x,y), RADIUS, THICK) #PARAMTERS (where you want to draw it, color, where its drawn (the center of the button), radius, witdth of the button)
			text = button_font.render(letter, 1, BLACK) #text needs to be rendered first --> Paramers: what you want to render, 1, color of text
			window.blit(text, (x - text.get_width()/2 ,y - text.get_height()/2)) #cant use second paramter as (x,y) because it will start to draw the letter from the upper left corner of the text AT x,y
																																					 #using text.get_width()/2 and text.get_height/2 will return where the middle of that specific letter is because each letter has a different midpoint		
	pygame.display.update() #you need to update the display everytime if you change anything in the display

	#necessary to check for events (clicking a keyboard/mouse etc..)
	for event in pygame.event.get(): #any event that happens will be stored here
		if event.type == pygame.QUIT: #if the user clicks the close button
			run = false
		if event.type == pygame.MOUSEBUTTONDOWN: #if the user clicks the mouse
			m_x, m_y = pygame.mouse.get_pos() #returns the (x,y) position of the mouse 
			for button in buttons: #loop to every button to see what button was clicked
				x,y,letter,visible = button
				if visible:
					distance = math.sqrt((m_x - x)**2 + (m_y - y)**2) #(x,y) refer to the center of each specific circle/letter
																														#distance formula is used to see how far the click was from the center of that circle/letter
					if distance < RADIUS: #if the distance is less than the radius, that means button click was on that circle
						button[3] = False
						guessed.append(button[2])
						if letter not in word:
							hangman_status += 1
						# print(letter) #prints that specific letter
						break

	pygame.display.update()
	won = True
	for letter in word:
		if letter not in guessed:
			won = False
			break

	if won:
		display_message("You WON!")
		check = True
		while check:
			answer = input("Do you want to play again? (y/n): ")
			if answer == 'y' or answer == 'Y':
				word = random.choice(words)
				hangman_status = 0
				guessed = []
				for button in buttons:
					button[3] = True
				check = False	
				continue 
			elif answer == 'n' or answer == 'N':
				run = False
				break
			else:
				print("Invalid answer")

	if hangman_status == 6:
		display_message("You lost...")
		answer = input("Do you want to play again? (y/n): ")
		if answer == 'y' or answer == 'Y':
				word = random.choice(words)
				hangman_status = 0
				guessed = []
				for button in buttons:
					button[3] = True
				check = False	
		elif answer == 'n' or answer == 'N':
			break
			

pygame.quit() #closes the window 


"""
UNDERSTANDING THE COORDINATE SYSTEM IN PYGAME:
Unlike the coordinate system in math where the center is (0,0), the top left corner of pygame is (0,0).
This means that as you move right, the x value increases and when you move left the x value decreases BUT
as you move down the y value increases and as you move up the y value decreases.

When you draw items in pygame, you start drawing it from the top left corner.
"""