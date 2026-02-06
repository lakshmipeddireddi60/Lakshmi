import pygame
import random

pygame.init()
pygame.mixer.init()

shoot_sound = pygame.mixer.Sound("shoot.wav")

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite System Demo")

# -------- BACKGROUND --------
background = pygame.image.load("space1.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Two background positions (IMPORTANT)
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 3

start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 60)
clock = pygame.time.Clock()

# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# ================= BULLET =================
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((8, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 7
        if self.rect.bottom < 0:
            self.kill()

# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ulka1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 90))

        x = random.randint(40, WIDTH - 40)
        self.rect = self.image.get_rect(center=(x, -50))

    def update(self):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.kill()

# ================= GROUPS =================
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

# ================= GAME LOOP =================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

        if event.type == SPAWN_EVENT:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # -------- UPDATE --------
    all_sprites.update()

    pygame.sprite.groupcollide(bullets, enemies, True, True)
    pygame.sprite.spritecollide(player, enemies, True)
    
    # -------- BACKGROUND MOVE --------
    bg_y1 += bg_speed
    bg_y2 += bg_speed

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT
        
    # -------- DRAW --------
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))

    # Timer
    seconds = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Time: {seconds}s", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

