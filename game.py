import pygame
from PIL import Image
import random
import socket
import time

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("soundtracklegends-intro-futuristic-467811.mp3")
pygame.mixer.music.set_volume(1)  # 50% volume
pygame.mixer.music.play(-1)  

running = True

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("KINETIX")

image = pygame.image.load("player.png").convert_alpha()
gif = Image.open("background_image.gif")

obstacle_image = pygame.image.load("obstacle.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (300, 300))

frames = []

for i in range(gif.n_frames):
    gif.seek(i)

    frame = gif.convert("RGBA")

    surface = pygame.image.frombytes(
        frame.tobytes(),
        frame.size,
        "RGBA"
    )

    frames.append(surface)

image = pygame.transform.scale(image, (100, 100))

x_survivor = 500
y_obstacle = 90
x_obstacle = 500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8080))
s.listen(10)

frame_idx = 0

font1 = pygame.font.Font(None, 100)
font2 = pygame.font.Font(None, 50)

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if ((x_obstacle - x_survivor) ** 2 + (y_obstacle - 700) ** 2) ** 0.5 <= 80:
     crash_image = font1.render('CRASH!!', True, (225, 0, 0))
     score_image = font2.render(f'score - {score}', True, (0, 0, 255))

     crash_rect = crash_image.get_rect(center = (500, 500))
     score_rect = score_image.get_rect(center = (570, 570))

     screen.blit(crash_image, crash_rect)
     screen.blit(score_image, score_rect)

     pygame.display.flip()

     time.sleep(3)

     score = 0
    
    background_image = pygame.transform.scale(frames[frame_idx], (1000, 1000))
    
    image_rect = obstacle_image.get_rect(center = (x_obstacle, y_obstacle))

    screen.blit(background_image, (0, 0))
    screen.blit(obstacle_image, image_rect)
                
    image_rect = image.get_rect(center = (x_survivor, 700))
    screen.blit(image, image_rect)

    pygame.display.flip()

    c, addr = s.accept() 
    data = c.recv(5).decode()

    if data == 'right' and x_survivor != 900:
     x_survivor += 100
    
    if data == 'left' and x_survivor != 100:
     x_survivor -= 100
    
    if x_obstacle - 50 < 850:
     x_obstacle += 30

    x_obstacle += random.choice(range(-100, 100, 75))

    if y_obstacle > 1000:
     y_obstacle = 90
     x_obstacle = 500
     score += 1
   
    else:
     y_obstacle += 30

    frame_idx = (frame_idx + 1) % len(frames)

