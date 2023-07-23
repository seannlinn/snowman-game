import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snowman Game")
ICE_BG = (153, 204, 255)
FPS = 60
VEL = 8
SNOWMAN_WIDTH, SNOWMAN_HEIGHT = 80/1.5, 95/1.5

FONT = pygame.font.SysFont('comicsans', 30)

HIT = pygame.USEREVENT + 1

SNOWMAN_IMAGE = pygame.image.load(os.path.join("assets", "snowman_s.png"))
SNOWMAN_IMAGE_SCALED = pygame.transform.scale(SNOWMAN_IMAGE, (80, 95))
FIREBALL_WIDTH, FIREBALL_HEIGHT = 20, 20
FIREBALL_IMAGE = pygame.image.load(os.path.join("assets", "fireball.png"))
FIREBALL_IMAGE_SCALED_LEFT = pygame.transform.scale(FIREBALL_IMAGE, (60, 60))
FIREBALL_IMAGE_SCALED_RIGHT = pygame.transform.rotate(FIREBALL_IMAGE_SCALED_LEFT, 180)
FIREBALL_IMAGE_SCALED_UP = pygame.transform.rotate(FIREBALL_IMAGE_SCALED_LEFT, 270)
FIREBALL_IMAGE_SCALED_DOWN = pygame.transform.rotate(FIREBALL_IMAGE_SCALED_LEFT, 90)

def handle_fireball_left(fireball_left, player):
	if fireball_left.x - 4 < -50:
		fireball_left.x = WIDTH
		fireball_left.y = random.randint(50, HEIGHT-100)
	fireball_left.x -= random.randint(4, 8)
	if player.colliderect(fireball_left):
		pygame.event.post(pygame.event.Event(HIT))


def handle_fireball_right(fireball_right, player):
	if fireball_right.x + 4 > WIDTH:
		fireball_right.x = -50
		fireball_right.y = random.randint(50, HEIGHT-100)
	fireball_right.x += random.randint(4, 8)
	if player.colliderect(fireball_right):
		pygame.event.post(pygame.event.Event(HIT))

def handle_fireball_up(fireball_up, player):
	if fireball_up.y - 4 < -50:
		fireball_up.y = HEIGHT
		fireball_up.x = random.randint(50, WIDTH-100)
	fireball_up.y -= random.randint(4, 8)
	if player.colliderect(fireball_up):
		pygame.event.post(pygame.event.Event(HIT))

def handle_fireball_down(fireball_down, player):
	if fireball_down.y + 4 > HEIGHT:
		fireball_down.y = -50
		fireball_down.x = random.randint(50, WIDTH-100)
	fireball_down.y += random.randint(4, 8)
	if player.colliderect(fireball_down):
		pygame.event.post(pygame.event.Event(HIT))

def handle_movement(keys_pressed, player):
	if keys_pressed[pygame.K_UP] and player.y - VEL > -12:
		player.y -= VEL

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_DOWN] and player.y + VEL < HEIGHT - 100:
		player.y += VEL

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_LEFT]:
		player.x -= VEL

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_RIGHT]:
		player.x += VEL


def draw_window(player, fireball_left, fireball_right, fireball_up, fireball_down, score):
	WIN.fill(ICE_BG)
	WIN.blit(SNOWMAN_IMAGE_SCALED, (player.x, player.y))
	WIN.blit(FIREBALL_IMAGE_SCALED_LEFT, (fireball_left.x, fireball_left.y))
	WIN.blit(FIREBALL_IMAGE_SCALED_RIGHT, (fireball_right.x, fireball_right.y))
	WIN.blit(FIREBALL_IMAGE_SCALED_UP, (fireball_up.x, fireball_up.y))
	WIN.blit(FIREBALL_IMAGE_SCALED_DOWN, (fireball_down.x, fireball_down.y))
	score_display = FONT.render("SCORE: " + str(round(score)), 1, (255, 255, 255))
	WIN.blit(score_display, (0, 0))
	pygame.display.update()

def draw_endscreen(text):
	draw_text = FONT.render(text, 1, (255, 255, 255))
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(4000)

def main():
	fireball_left = pygame.Rect(WIDTH, random.randint(50, HEIGHT-100), FIREBALL_WIDTH, FIREBALL_HEIGHT)
	fireball_right = pygame.Rect(-50, random.randint(50, HEIGHT-100), FIREBALL_WIDTH, FIREBALL_HEIGHT)
	fireball_up = pygame.Rect(random.randint(50, WIDTH-100), HEIGHT, FIREBALL_WIDTH, FIREBALL_HEIGHT)
	fireball_down = pygame.Rect(random.randint(50, WIDTH-100), -50, FIREBALL_WIDTH, FIREBALL_HEIGHT)
	player = pygame.Rect(230, 230, SNOWMAN_WIDTH, SNOWMAN_HEIGHT)
	score = 0
	loss_text = ""

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		score += 0.05
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == HIT:
				loss_text = "YOU LOSE"
			if loss_text != "":
				draw_endscreen(loss_text)
				pygame.quit()
			
		keys_pressed = pygame.key.get_pressed()
		handle_movement(keys_pressed, player)
		handle_fireball_left(fireball_left, player)
		handle_fireball_right(fireball_right, player)
		handle_fireball_up(fireball_up, player)
		handle_fireball_down(fireball_down, player)
		draw_window(player, fireball_left, fireball_right, fireball_up, fireball_down, score)

	pygame.quit()

if __name__ == "__main__":
	main()