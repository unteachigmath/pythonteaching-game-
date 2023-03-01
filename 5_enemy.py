import pygame
import os
import random
pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 750, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # 보여지는 윈도우(화면)을 셋팅한다. 클라스
pygame.display.set_caption("Mygame")


# 이미지 로드
ENEMY_RED = pygame.image.load(
    os.path.join("image and sound", "enemy_red.png"))
ENEMY_YELLOW = pygame.image.load(
    os.path.join("image and sound", "enemy_green.png"))
ENEMY_PUPPLE = pygame.image.load(
    os.path.join("image and sound", "enemy_purple.png"))

# 플레이어 캐릭터
PLAYER_CHARACTER = pygame.image.load(
    os.path.join("image and sound", "player1.png"))
PLAYER_CHARACTER_1 = pygame.image.load(
    os.path.join("image and sound", "player1.png"))
PLAYER_CHARACTER_2 = pygame.image.load(
    os.path.join("image and sound", "player2.png"))
PLAYER_CHARACTER_3 = pygame.image.load(
    os.path.join("image and sound", "player3.png"))

# 레이져 이미지 로드
MISSILE_RED = pygame.image.load(
    os.path.join("image and sound", "enemy_red_missile.png"))
MISSILE_YELLOW = pygame.image.load(
    os.path.join("image and sound", "enemy_green_missile.png"))
MISSILE_PUPPLE = pygame.image.load(
    os.path.join("image and sound", "enemy_purple_missile.png"))

MISSILE_PLAYER = pygame.image.load(
    os.path.join("image and sound", "player1_missile.png"))
MISSILE_PLAYER_1 = pygame.image.load(
    os.path.join("image and sound", "player1_missile.png"))
MISSILE_PLAYER_2 = pygame.image.load(
    os.path.join("image and sound", "player2_missile.png"))
MISSILE_PLAYER_3 = pygame.image.load(
    os.path.join("image and sound", "player3_missile.png"))

# 배경
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("image and sound", "background_forest.png")), (WIDTH, HEIGHT))

bg_music = pygame.mixer.music.load(
    os.path.join("image and sound", "background_music.mp3"))
# pygame.mixer.music.play(-1)

missile_sound = pygame.mixer.Sound(
    os.path.join("image and sound", "missile_sound.wav"))

##############


class Missile:
    def __init__(self, x_pos, y_pos, img):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, missile_vel):
        self.y_pos += missile_vel

    def draw(self, window):
        window.blit(self.img, (self.x_pos, self.y_pos))

    def off_screen(self, height):
        return not (self.y_pos <= height and self.y_pos >= 0)

    def collision(self, obj):
        return collision_dect(self, obj)


def collision_dect(obj_1, obj_2):
    x_offset = obj_2.x_pos - obj_1.x_pos
    y_offset = obj_2.y_pos - obj_1.y_pos
    return obj_1.mask.overlap(obj_2.mask, (x_offset, y_offset)) != None


class Player:
    def __init__(self, x_pos, y_pos, hp):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.hp = hp
        self.player_img = PLAYER_CHARACTER
        self.missile_img = MISSILE_PLAYER
        self.missile_list = []
        self.mask = pygame.mask.from_surface(self.player_img)
        self.cooldown_counter = 0
        self.full_hp = 5

    def fire(self):
        if self.cooldown_counter == 0:
            missile = Missile(self.x_pos, self.y_pos, self.missile_img)
            self.missile_list.append(missile)
            self.cooldown_counter = 1

    def draw(self, window):
        self.cooldown()
        window.blit(self.player_img, (self.x_pos, self.y_pos))
        for missile in self.missile_list:
            missile.draw(window)

        pygame.draw.rect(window, (255, 0, 0),
                         (50, 35, 100, 20))
        pygame.draw.rect(window, (0, 0, 255), (50, 35,
                         100*(1-(self.full_hp-self.hp)/self.full_hp), 20))
        hp_title = pygame.font.SysFont("comicsans", 30).render(
            "HP", 1, (255, 255, 255))
        WINDOW.blit(hp_title, (0, 25))

    def get_width(self):
        return self.player_img.get_width()

    def get_height(self):
        return self.player_img.get_height()

    def hit_by_missile(self, missile):
        self.hp -= 1
        self.missile_list.remove(missile)

    def cooldown(self):
        if self.cooldown_counter >= 10:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
# 5_enemy강의내용


enemy_missile_list = []
class Enemy:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enemy_img, self.missile_img = random.choice(
            [(ENEMY_RED, MISSILE_RED), (ENEMY_YELLOW, MISSILE_YELLOW), (ENEMY_PUPPLE, MISSILE_PUPPLE)])
        self.mask = pygame.mask.from_surface(self.enemy_img)

    def fire(self):
        global enemy_missie_list
        missile = Missile(self.x_pos+self.enemy_img.get_width() /
                          2-MISSILE_RED.get_width()/2, self.y_pos+self.enemy_img.get_height(), self.missile_img)
        enemy_missile_list.append(missile)

    def draw(self, window):
        window.blit(self.enemy_img, (self.x_pos, self.y_pos))
        

    def get_width(self):
        return self.enemy_img.get_width()

    def get_height(self):
        return self.enemy_img.get_height()

    def move(self, enemy_vel):
        self.y_pos += enemy_vel

def main():
    global enemy_missile_list
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    level = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    kill_score = 0

    player_vel = 7
    missile_vel = 6

    player = Player(300, 630, 5)

    enemies = []  # 5_enemy강의내용
    wave_length = 10
    enemy_vel = 4

    while run:
        clock.tick(FPS)
        WINDOW.blit(BG, (0, 0))

        level_label = main_font.render(f"LEVEL : {level}", 1, (255, 255, 255))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width()-10, 10))
        kill_label = main_font.render(
            f"KILL : {kill_score}", 1, (255, 255, 255))
        WINDOW.blit(kill_label, (kill_label.get_width()+40, 10))

        for missile in player.missile_list:
            missile.move(-missile_vel)
            if missile.y_pos < 0:
                player.missile_list.remove(missile)

        # 5_enemy강의내용
        for enemy in enemies:
            enemy.draw(WINDOW)
        for missile in enemy_missile_list:
            missile.draw(WINDOW)

        player.draw(WINDOW)

        pygame.display.update()

        # 5_enemy강의내용
        if len(enemies) == 0:
            level += 1
            wave_length += 7
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH - 100), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x_pos - player_vel > 0:
            player.x_pos -= player_vel
        if keys[pygame.K_RIGHT] and player.x_pos + player_vel + player.get_width() < WIDTH:
            player.x_pos += player_vel
        if keys[pygame.K_UP] and player.y_pos-player_vel > 0:
            player.y_pos -= player_vel
        if keys[pygame.K_DOWN] and player.y_pos+player_vel + player.get_height() + 15 < HEIGHT:
            player.y_pos += player_vel

        if keys[pygame.K_SPACE]:
            player.fire()
            missile_sound.play()

        # 5_enemy강의내용
        for enemy in enemies:
            enemy.move(enemy_vel)
            
            if random.randrange(0, 1*60) == 1 and enemy.y_pos > 0:  # FPS를 고려한 설정
                enemy.fire()

            if collision_dect(enemy, player):
                player.hp -= 1
                enemies.remove(enemy)
                kill_score += 1
            elif enemy.y_pos + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)
        for missile in enemy_missile_list:
            missile.move(missile_vel)

            if missile.collision(player):
                player.hp -= 1
                enemy_missile_list.remove(missile)
            if missile in enemy_missile_list and missile.y_pos > HEIGHT:
                enemy_missile_list.remove(missile)

main()
