import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sky shooting!")
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
RED=(255, 0, 0)
YELLOW=(255, 255, 0)

BORDER=pygame.Rect(WIDTH//2 - 5, 0, 0, HEIGHT)

BULLET_HIT_SOUND=pygame.mixer.Sound('assets/grenadesound.mp3')
BULLET_FIRE_SOUND=pygame.mixer.Sound('assets/firesound.mp3')

HEALTH_FONT=pygame.font.SysFont('comicsans', 40)
WINNER_FONT=pygame.font.SysFont('comicsans', 100)

FPS=60
VEL=4
BULLET_VEL=20
MAX_BULLETS= 30

MAN_WIDTH, MAN_HEIGHT=70,55

YELLOW_HIT= pygame.USEREVENT+1
WHITE_HIT=pygame.USEREVENT+2

YELLOW_IMAGE=pygame.image.load('assets/leftship1.png')
YELLOWSHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(YELLOW_IMAGE, (MAN_WIDTH, MAN_HEIGHT)),270)
WHITE_IMAGE=pygame.image.load('assets/rightship1.png')
WHITESHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(WHITE_IMAGE, (MAN_WIDTH, MAN_HEIGHT)),90)

SPACE=pygame.transform.scale(pygame.image.load(os.path.join('assets', 'skyy.png')), (WIDTH,HEIGHT+100))


def draw_window(white, yellow, white_bullets, yellow_bullets, white_health, yellow_health):
    WIN.blit(SPACE,(0, 0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    white_health_text = HEALTH_FONT.render("HP: " + str(white_health), 1,RED)
    yellow_health_text = HEALTH_FONT.render("HP: " + str(yellow_health), 1, RED)
    WIN.blit(white_health_text,(WIDTH - white_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOWSHIP_IMAGE,(yellow.x,yellow.y))
    WIN.blit(WHITESHIP_IMAGE,(white.x,white.y))

    for bullet in white_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL>0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL+yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL>0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y +VEL+ yellow.height < HEIGHT-15:  # down
        yellow.y += VEL


def white_handle_movement(keys_pressed,white):
    if keys_pressed[pygame.K_LEFT]  and white.x - VEL>BORDER.x+BORDER.width:  # left
        white.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and white.x + VEL+white.width < WIDTH:  # right
        white.x += VEL
    if keys_pressed[pygame.K_UP] and white.y - VEL>0:  # up
        white.y -= VEL
    if keys_pressed[pygame.K_DOWN] and white.y +VEL+ white.height < HEIGHT-15:  # down
        white.y += VEL


def handle_bullets(yellow_bullets, white_bullets, yellow,white):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in white_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            white_bullets.remove(bullet)
        elif bullet.x < 0:
            white_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1 ,RED)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2,HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    white = pygame.Rect(700,300,MAN_WIDTH,MAN_HEIGHT)
    yellow = pygame.Rect(100,300,MAN_WIDTH,MAN_HEIGHT)

    white_bullets = []
    yellow_bullets = []

    white_health = 10
    yellow_health = 10

    clock=pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 - 2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(white_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(white.x , white.y + white.height//2 - 2, 10, 5)
                    white_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == WHITE_HIT:
                white_health -=1
                BULLET_HIT_SOUND.play()

            if event.type==YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if white_health <=0:
            winner_text= "YELLOW WINS!"

        if yellow_health <=0:
            winner_text="WHITE WINS!"

        if winner_text !="":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        white_handle_movement(keys_pressed, white)

        handle_bullets(yellow_bullets,white_bullets,yellow,white)

        draw_window(white, yellow, white_bullets, yellow_bullets, white_health, yellow_health)
    main()



if __name__ == "__main__":
    main()

