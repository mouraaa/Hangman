import pygame
import math
import random

#--------------------------------------------------------
#basic setup
pygame.init() 
WIDTH, HEIGHT = 800, 550
window = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("Hangman") 
FPS = 60
clock = pygame.time.Clock()

#--------------------------------------------------------
#Loading Images
images = [] 
for i in range(1,8): 
	image = pygame.image.load("images/hangman" + str(i) + ".png") 
	images.append(image) 

#--------------------------------------------------------
#Game Variables:
A = 65 #in programming, capital a = 65 and capital b = 66 etc.
x = 65
y = 400

hangman_status = 0
RADIUS = 20
GAP = 55
THICK = 3
WHITE = (255,255,255) 
BLACK = (0,0,0)

words = []
with open("words.txt") as f:
	for i in f:
		words.append(i.upper().rstrip())
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

button_font = pygame.font.SysFont('comicsans', 40) 
word_font = pygame.font.SysFont('comicsans', 60)

#--------------------------------------------------------
#METHODS
def display_message(message):
	window.fill(WHITE) 
	text = button_font.render(message, 1, BLACK)
	window.blit(text, (350, 250))	
	pygame.display.update() 
	pygame.time.delay(2000) 

#--------------------------------------------------------
#Game Loop 
run = True
while run:
	clock.tick(FPS) 
	window.fill(WHITE) 
	window.blit(images[hangman_status], (50,110)) 

	#Drawing the word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			if letter == ' ':
				display_word += '  '
				guessed.append(' ')
			else:
				display_word += "_ "
	text = word_font.render(display_word, 1, BLACK)
	window.blit(text,(400,200))

	#Drawing the Title
	text = word_font.render('DEVELOPER HANGMAN', 1, BLACK)
	window.blit(text,(160,20))

	#Drawing the buttons
	for button in buttons:
		x,y,letter,visible = button 
		if visible:
			pygame.draw.circle(window, BLACK, (x,y), RADIUS, THICK) 
			text = button_font.render(letter, 1, BLACK) 
			window.blit(text, (x - text.get_width()/2 ,y - text.get_height()/2))

	pygame.display.update() 

	#check for events
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			run = false
		if event.type == pygame.MOUSEBUTTONDOWN: 
			m_x, m_y = pygame.mouse.get_pos() 
			for button in buttons: 
				x,y,letter,visible = button
				if visible:
					distance = math.sqrt((m_x - x)**2 + (m_y - y)**2) 
					if distance < RADIUS: 
						button[3] = False
						guessed.append(button[2])
						if letter not in word:
							hangman_status += 1
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
			

pygame.quit() 
