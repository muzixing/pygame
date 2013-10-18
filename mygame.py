# encoding =utf-8

#1	import library
import pygame
import math
import random
from pygame.locals import *




#2	initialize the game
pygame.init()
width,height = 640,480
screen= pygame.display.set_mode((width,height))
key = [False, False, False, False]
playerpos = [100,220] 				#your hero's position
acc =[0,0]   #use for calculating 
arrows = []
speed =20
game_speed =10
#2.1 for the bad guys
bad_timer = 100
bad_timer1 = 0
badguys = [[640,100]]

healthvalue =194

permission = 1
freze_time =100

pygame.mixer.init()

#3	load the images
player = pygame.image.load("resources/images/dude2.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")

badguysimg = pygame.image.load("resources/images/badguy.png")
badguyimg1 = badguysimg

healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
#3.1  load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")

hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
#4 	keep looping
run = 1
exitcode = 0
while run:
	#4.10  about time
	bad_timer-= 1  
	freze_time -=5
	if freze_time<30:
		permission = 1
		freze_time = 100
	#5	clear the screen before draw it again
	screen.fill(0)
	#6  draw the screen elements
	for x in range(width/grass.get_width()+1):
		for y in range(height/grass.get_height()+1):
			screen.blit(grass, (x*100, y*100))
	screen.blit(castle,(0, 30))	
	screen.blit(castle,(0, 130))	
	screen.blit(castle,(0, 230))
	screen.blit(castle,(0, 330))
	#6.1  set playe position and rotation
	position = pygame.mouse.get_pos()  
	angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))	
	playerrot =pygame.transform.rotate(player,360-angle*57.29)
	playerpos_1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]- playerrot.get_rect().height/2)
	
	screen.blit(playerrot,playerpos_1)
	#6.2 	draw the arrows
	for bullet in arrows:
		index =0
		velx = speed*math.cos(bullet[0])
		vely = speed*math.sin(bullet[0])
		bullet[1]+=velx
		bullet[2]+=vely
		#6.2.5if it is go out of the screen,and delete it.
		if bullet[1]<-64 or bullet[1]>width or bullet[2]<-64 or bullet[2]>height:
			arrows.pop(index)
		index+=1
		for project in arrows:
			arrow_1 = pygame.transform.rotate(arrow, 360-project[0]*57.29)
			screen.blit(arrow_1, (project[1], project[2]))

	#6.3 draw the badguys 
	if bad_timer ==0:
		badguys.append([640, random.randint(50,430)])
		bad_timer = 100 -bad_timer1
		if bad_timer1>35:
			bad_timer1 = 35 #limit the speed
		else:
			bad_timer1+= game_speed
	index =0
	for badguy in badguys:
		if badguy[0]<-64:
			badguys.pop(index)
		badguy[0]-=6
		#6.3.1 	attcck the castle
		badrect = pygame.Rect(badguysimg.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left <64:
			healthvalue	-= random.randint(5,20)
			badguys.pop(index)
			hit.play()
		#6.3.2chevk for the collisions
		index1 =0
		for bullet in arrows:
			bullrect = pygame.Rect(arrow.get_rect())
			bullrect.left = bullet[1]
			bullrect.top = bullet[2]
			if badrect.colliderect(bullrect):
				acc[0]+=1
				badguys.pop(index)
				arrows.pop(index1)
				enemy.play()
			index1+=1
		index+=1

	for badguy in badguys:
		screen.blit(badguysimg, badguy)
	#6.4 draw the clock
	font = pygame.font.Font(None, 24)
	survivetext = font.render("Hold time: "+str((90000 - pygame.time.get_ticks())/60000)+":"+str((90000 - pygame.time.get_ticks())/1000%60).zfill(2), True, (255,0,0))
	textRect = survivetext.get_rect()
	textRect.topright = [633,5]
	screen.blit(survivetext,textRect)
	#draw health bar
	screen.blit(healthbar,(40,5))
	for helth_1 in range(healthvalue):
		screen.blit(health, (helth_1+43, 8))
	#show some imformation
	pygame.font.init()
	font =pygame.font.Font(None, 24)
	TEXT = font.render("Life", True, (0, 255, 0))
	screen.blit(TEXT,(5,5))

	pygame.font.init()
	font =pygame.font.SysFont('SimHei.ttc', 30)
	TEXT = font.render("Tower defence", True, (20, 225, 40))
	textRect= TEXT.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = 15
	screen.blit(TEXT,textRect)
	# 7 - update the screen
	pygame.display.flip()
	#8	loop through the events, and check the key
	for event in pygame.event.get(): 	#check if the event is the x button,we define the x as the key of quit.
		if event.type ==pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key==K_w:
				key[0] = True
			elif event.key == K_a:
				key[1] = True
			elif event.key == K_s:
				key[2] = True
			elif event.key ==K_d:
				key[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				key[0] = False
			elif event.key == K_a:
				key[1] = False
			elif event.key == K_s:
				key[2] = False
			elif event.key ==K_d:
				key[3] = False	
		if event.type == pygame.MOUSEBUTTONDOWN and permission:
			shoot.play()
			permission = 0
			position = pygame.mouse.get_pos()
			acc[1]+=1#Acount the arrows you have shooted
			arrows.append([math.atan2(position[1]-(playerpos_1[1]+32), position[0]- (playerpos_1[0]+26)), playerpos_1[0]+32, playerpos_1[1]+26])#angle,x,y
	#9  move the hero
	if key[0]:
		if playerpos[1]>20:
			playerpos[1]-=5
	elif key[2]:
		if playerpos[1]<height-80:
			playerpos[1]+=5
	if key[1]:
		if playerpos[0]>80:
			playerpos[0]-=5
	elif key[3]:
		if playerpos[0]<width-80:
			playerpos[0]+=5
	#10 check for the result of game.
	if healthvalue <=0:
		run = 0
		exitcode = 1  #you lose
	if pygame.time.get_ticks()>=90000:
		run = 0
		exitcode = 0  # you win
	if acc[1]!=0:#if you shoot any arrow.
		accuracy =acc[0]*1.0/acc[1]*100
	else:
		accuracy =0

#11	display the result.
if exitcode == 0:
	pygame.font.init()
	font =pygame.font.Font(None, 24)
	TEXT = font.render("Accuracy:" + str(accuracy) + "%", True, (0, 255, 0))
	textRect= TEXT.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+32
	screen.blit(TEXT,textRect)

	TEXT1 = font.render("Made by Muzi", True, (0, 255, 0))
	textRect= TEXT1.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+64
	screen.blit(TEXT1,textRect)

	screen.blit(youwin, (0,0))
else:
	pygame.font.init()
	font =pygame.font.Font(None, 24)
	TEXT = font.render("Accuracy:" + str(accuracy) + "%", True, (255, 0, 0))
	textRect= TEXT.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+32
	screen.blit(TEXT,textRect)
	
	TEXT1 = font.render("Made by Muzi", True, (255, 0, 0))
	textRect= TEXT1.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+64
	screen.blit(TEXT1,textRect)
	
	screen.blit(gameover, (0,0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()



