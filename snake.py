#importeren van de bibliotheken
import pygame
import time
import random
import RPi.GPIO as GPIO

#GPIO setup
GPIO.setmode(GPIO.BCM)
#PIN 29 boven
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#PIN 31 rechts
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#PIN 33 links
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#PIN 32 onder
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#initialiseren van pygame
pygame.init()

#kleuren creëren
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

#variable window grootte
display_width = 794
display_height = 410

#window grote met gameDisplay
gameDisplay = pygame.display.set_mode((display_width,display_height))

#titel window
pygame.display.set_caption('Dries Snake')

#icon
icon = pygame.image.load('/pictures/Appel2.png')
pygame.display.set_icon(icon)

img = pygame.image.load('/pictures/SnakeHead.png')
appleimg = pygame.image.load('/pictures/Appel2.png')

clock = pygame.time.Clock()

AppleThickness = 30

block_size = 20

FPS = 15

#lettertype
smallfont = pygame.font.SysFont("comicsansms", 25)#size small
medfont = pygame.font.SysFont("comicsansms", 50)#size meduim
largefont = pygame.font.SysFont("comicsansms", 80)#size large

def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0

    return randAppleX,randAppleY

def game_intro():
    
    intro = True

    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if(GPIO.input(13) == 1):
            intro = False

            Leftflag = True
            Rightflag = False
            Upflag   = False
            Downflag = False
        elif(GPIO.input(6) == 1):
            intro = False

            Leftflag = False
            Rightflag = True
            Upflag   = False
            Downflag = False
        elif(GPIO.input(5) == 1):
            intro = False

            Leftflag = False
            Rightflag = False
            Upflag   = True
            Downflag = False
        elif(GPIO.input(12) == 1):
            intro = False

            Leftflag = False
            Rightflag = False
            Upflag   = False
            Downflag = True
        
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake", green, -100, size="large")
        message_to_screen("The objective of the game is to eat apples", black, -30)
        message_to_screen("The more apples you eat, the longer you get", black, 10)
        message_to_screen("If you run into yourself, or the edges, you die!", black, 50)
        message_to_screen("Press any key to play", black, 180)

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):
    #snakehead roteren in de juiste richting
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])#(slang) tekenen

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
        
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
def gameLoop():
    global direction

    direction ='right'

    #richtingsindicatie
    Leftflag = False
    Rightfag = False
    Upflag   = False
    Downflag = False
    
    #variable voor het eindigen van het spel
    gameExit = False
    #variable voor als je dood bent (het spel wordt niet geëindigd!)
    gameOver = False

    #1ste blok en laatste blok van de slang
    lead_x = display_width/2
    lead_y = display_height/2
    
    lead_x_change = 15 #de variable voor een verandering van richting op de x-as
    lead_y_change = 0 #de variable voor een verandering van richting op de y-as

    snakeList = []
    snakeLength = 1
    
    #X en Y waarde van de appel random
    randAppleX,randAppleY = randAppleGen()
    
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game Over", red, y_displace = -50, size = "large")
            message_to_screen("Press any key to play again", black, y_displace = 50, size = "medium")
            pygame.display.update()
        
        while gameOver == True:
            #gameDisplay.fill(white)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                    
            if(GPIO.input(13) == 1):
                gameLoop()#herstarten

                Leftflag = True
                Rightflag = False
                Upflag   = False
                Downflag = False
            elif(GPIO.input(6) == 1):
                gameLoop()#herstarten

                Leftflag = False
                Rightflag = True
                Upflag   = False
                Downflag = False
            elif(GPIO.input(5) == 1):
                gameLoop()#herstarten

                Leftflag = False
                Rightflag = False
                Upflag   = True
                Downflag = False
            elif(GPIO.input(12) == 1):
                gameLoop()#herstarten

                Leftflag = False
                Rightflag = False
                Upflag   = False
                Downflag = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        if(GPIO.input(13) == 1 and Rightflag == False):
            direction = "left"
            lead_x_change = -block_size#snelheid links
            lead_y_change = 0

            Leftflag = True
            Rightflag = False
            Upflag   = False
            Downflag = False
        elif(GPIO.input(6) == 1 and Leftflag == False):
            direction = "right"
            lead_x_change = block_size#snelheid rechts
            lead_y_change = 0

            Leftflag = False
            Rightflag = True
            Upflag   = False
            Downflag = False
        elif(GPIO.input(5) == 1 and Downflag == False):
            direction = "up"
            lead_y_change = -block_size#snelheid boven
            lead_x_change = 0

            Leftflag = False
            Rightflag = False
            Upflag   = True
            Downflag = False
        elif(GPIO.input(12) == 1 and Upflag == False):
            direction = "down"
            lead_y_change = block_size#snelheid onder
            lead_x_change = 0

            Leftflag = False
            Rightflag = False
            Upflag   = False
            Downflag = True
            

        if lead_x > display_width or lead_x < 0 or lead_y > display_height or lead_y < 0:#boundaries
            gameOver = True
                            

                    
        lead_x += lead_x_change #de richting veranderen constant x-as
        lead_y += lead_y_change #de richting veranderen constant y-as

        gameDisplay.fill(white)

        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])#appel tekenen

        gameDisplay.blit(appleimg, (randAppleX,randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:#alle coordinaten van de slang(snakeList) zonder snakeHead
            if eachSegment == snakeHead:#is de coordinaten van de snakeHead = ...
                gameOver = True
            
        snake(block_size, snakeList)#snake functie oproepen

        score(snakeLength-1)#score functie oproepen
        
        pygame.display.update()

        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
                #niewe X en Y waarde van de appel random na het opeten
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y +block_size < randAppleY + AppleThickness:
                #niewe X en Y waarde van de appel random na het opeten
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    GPIO.cleanup()

    #tegengestelde van init
    pygame.quit()

    #het scherm afsluiten
    quit()

game_intro()
gameLoop()
