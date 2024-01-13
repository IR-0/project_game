import sys
import random
import pygame
# from serv import listt


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 40
clock = pygame.time.Clock()
clock.tick(fps)

LVLONE = pygame.USEREVENT + 2


class EnemyCommon:  # он же враг нулевого типа
    def __init__(self, hp=5, speed=1, b_speed=0.3, bullet=1, entfernung=4, x=200, y=20):
        self.x = x
        self.y = y
        self.hp = hp
        self.bullet_speed = b_speed
        self.coef_speed = speed
        self.coef_bullet = bullet
        self.entfernung = entfernung
        self.acceleration = True

    def render(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)

    def shot(self):
        if self.__class__.__name__.startswith('Player'):
            self._bullet_pattern()
        else:
            for i in range(-1 * self.coef_bullet, 2 * self.coef_bullet):
                f_bullets.append(FeindBullet(self.x + 10 * i, self.y + 10, 6, i, self))

    def xmove(self, spec):
        self.x = self.x + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))

    def death(self):
        pass


class EnemyType1(EnemyCommon):
    def __init__(self):
        super().__init__(hp=20, speed=1, bullet=1, entfernung=1)


class EnemyType3(EnemyCommon):
    def __init__(self):
        super().__init__(50, 1, 1.5, 6)


class EnemyType4(EnemyCommon):
    def __init__(self, hp=50, speed=2, bullet=1, entfernung=1):
        super().__init__(hp=hp, speed=speed, bullet=bullet, entfernung=entfernung)
        self.anticipation = 40

    def ruck(self, coef=1):  # уклон
        pass


class EnemyType7(EnemyType4):
    def __init__(self, speed=2, bullet=2, entfernung=1):
        super().__init__(speed=speed, bullet=bullet, entfernung=entfernung)
        self.anticipation = 20

    def ruck(self):
        super().ruck(coef=2)


class Player0(EnemyCommon):  # h. Общий класс для всех играбельных персонажей
    def __init__(self, hp=1, speed=1, b_s=1, bullet=1, ent=2, x=400, y=400):
        super().__init__(hp=hp, speed=speed, b_speed=b_s, bullet=bullet, entfernung=ent, x=x, y=y)
        self.r, self.r_x, self.r_y, self.alpha = 0, 0, 0, 255

    def _bullet_pattern(self):
        for i in range(-2 * self.coef_bullet, 4 * self.coef_bullet - 1):
            bullets.append(Bullet(self.x + 10 * i, self.y + 10, 2, i, self))

    def bomb(self):
        if self.r_x == 0 or self.r_y == 0:
            self.r_x, self.r_y = self.x, self.y
        if self.r < 300:
            pygame.draw.circle(screen, (100, 100, 100, abs(self.alpha % 255)), (self.r_x, self.y), self.r)
            self.alpha -= 1
            self.r += 1

    def shift(self, off):  # выключить ускорение и замедлить персонажа
        self.acceleration = False if off else True

    def graze(self):
        pass


class Player1(Player0):  # d
    def __init__(self, x, y):
        print(1)
        super().__init__(speed=2, bullet=1, ent=1, x=x, y=y)


class Player2(Player0):  # s
    def __init__(self, x, y):
        print(2)
        super().__init__(speed=0.9, bullet=1.3, ent=1.3, x=x, y=y)


class Player3(Player0):  # j
    def __init__(self, x, y):
        super().__init__(speed=0.8, bullet=1.1, ent=1.4, x=x, y=y)


class Bullet:
    def __init__(self, x, y, type, num, owner):
        self.x, self.y, self.type, self.num = x, y, type, num
        self.owner = owner

    def move(self):
        self.y -= int(10 * self.owner.bullet_speed)

    def entfer(self, cl):
        self.x += cl.entfernung * self.num

    def render(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.type)


class FeindBullet(Bullet):
    def __init__(self, x, y, type, num, owner):
        super().__init__(x, y, type, num, owner)
        self.owner = owner

    def move(self):
        self.y += int(10 * self.owner.bullet_speed)


class GeometryBulletHell:
    def __init__(self):
        self.choosen_lvl = 0
        self.player_type = 0
        self.gaming = False
        self.count_for_fertig_lvl = 0
        self.count_for_menu = 0
        self.player = Player0
        self.var_lvl0 = True

    def menu(self, event_key):
        '''главное меню'''
        self.ramka()
        font = pygame.font.Font(fontt, 13)
        text = font.render('sum of record score: ' + str(sum(record_score)), False, (140, 140, 140))
        screen.blit(text, (k, m))
        self.choosen_lvl = abs(self.choosen_lvl) % 8

        # перемещение курсорными клавишами по уровням
        if event_key == pygame.K_LEFT:
            self.choosen_lvl = (self.choosen_lvl - 1) % 8
        elif event_key == pygame.K_RIGHT:
            self.choosen_lvl = (self.choosen_lvl + 1) % 8
        elif event_key == pygame.K_UP:
            self.player_type = (self.player_type - 1) % 4
        elif event_key == pygame.K_DOWN:
            self.player_type = (self.player_type + 1) % 4

        elif event_key == pygame.K_z:  # ================================ КНОПКА СУДЬБЫ =========================
            x, y = 270, 550
            if self.player_type == 0:
                self.player = Player0(x=x, y=y)
            elif self.player_type == 1:
                self.player = Player1(x=x, y=y)  # странно, раньше не подсвечивало
            elif self.player_type == 2:
                self.player = Player2(x=x, y=y)
            elif self.player_type == 3:
                self.player = Player3(x=x, y=y)
            self.gaming = True
            screen.fill((0, 0, 0))
            self.player.render()
            self.extended_ramka()
            return

        # размещение уровней и игрока в меню. Описание уровней
        for j in range(2):
            for i in range(4):
                font = pygame.font.Font(None, 50)
                text = font.render(str(self.count_for_menu), False, (100, 100, 100))
                screen.blit(text, (40 + 50 * i + 10, 40 + 50 * j + 5))
                pygame.draw.rect(screen, (255, 255, 255), (40 + 50 * i, 40 + 50 * j, n, n), 1)

                if self.count_for_menu == self.choosen_lvl:
                    pygame.draw.circle(screen, (255, 255, 255), ((40 + 50 * i) + 20, (40 + 50 * j) + 20), 5)

                    font = pygame.font.Font(fontt, 20)
                    text = font.render(lvl_description[self.count_for_menu], False, (255, 255, 255))
                    screen.blit(text, (30, 150))

                    font = pygame.font.Font(fontt, 20)
                    text = font.render('''record score: ''' + str(record_score[self.count_for_menu]), False, (140, 140, 140))
                    screen.blit(text, (k, m + 20))
                self.count_for_menu = (self.count_for_menu + 1) % 8

        for j in range(4):  # персонажи
            font = pygame.font.Font(fontt, 10)
            text = font.render(players[j], False, (100, 100, 100))
            screen.blit(text, (476, 40 + 50 * j + 5))
            pygame.draw.rect(screen, (200, 200, 200), (470, 40 + 50 * j, n - 10, n - 10), 1)

            if self.count_for_fertig_lvl == self.player_type:
                pygame.draw.circle(screen, (255, 255, 255), (470, 60 + 50 * j), 5)
            self.count_for_fertig_lvl = (self.count_for_fertig_lvl + 1) % 4

    def ramka(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (20, 20, 500, 560), 2)

    def extended_ramka(self):
        '''идея в том, что до вызова функции прорисовывается поле и пули на нем, а после вызовва
        поле ограничивается рамкой, в итоге пули существуют и за пределами рамки, но закрываются ею'''
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, up_border))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, l_border, height))
        pygame.draw.rect(screen, (0, 0, 0), (0, down_border, width, height))
        pygame.draw.rect(screen, (0, 0, 0), (r_border, 0, width, height))
        pygame.draw.rect(screen, (255, 255, 255), (up_border, l_border, r_border - 20, down_border - 20), 2)

    def lvl0(self):
        if self.var_lvl0:
            for i in range(-5, 0):
                feinde.append(EnemyCommon(x=l_border + 20 * abs(i), y=up_border + 20 * i))
            self.var_lvl0 = False

    def lvl1(self):
        pass

    def lvl2(self):
        pass

    def lvl3(self):
        pass

    def lvl4(self):
        pass

    def lvl5(self):
        pass

    def lvl6(self):
        pass

    def lvl7(self):
        pass


class Timer:  # КОСТЫЛЬ КОТОРЫЙ НЕАДЕКВАТНО РАЮОТАЕТ
    def __init__(self):
        self.time = pygame.time.get_ticks()

    def reset(self):
        self.time = pygame.time.get_ticks()

    def stop(self):
        serv = pygame.time.get_ticks() - self.time
        return serv

# ===================================================ПРОГРАММА===============================================


try:
    foo = open('sprites/is_exist.txt', 'r')
    foo.close()
except Exception as e:
    print(e)
    sprites_not_exist = True
else:
    print('ok')
    sprites_not_exist = False


if __name__ == '__main__':
    if sprites_not_exist:
        listt = ['TEST GAME', 'image.png', 'test lol апрол']

    pygame.display.set_caption(listt[0])
    im = pygame.image.load(listt[1])
    pygame.display.set_icon(im)
    screen.fill((0, 0, 0))

    timer_title = Timer()

    game = GeometryBulletHell()

    running = True
    fl = True
    flag_key = False
    fire = False
    screen.fill((0, 0, 0))

    up_border = 20
    down_border = 580
    l_border = 20
    r_border = 520

    bullets = []
    f_bullets = []
    feinde = []
    fontt = 'C:/Windows/Fonts/bahnschrift.ttf'
    # TOD непонятные переменнные (потом переназову)
    n = 40
    k = 540
    m = 20
    step = 5
    record_score = [0, 0, 0, 1, 0, 10, 0, 0]
    lvl_description = ["""Нулевой уровень. Обучение. Показываются 
    основы игры""", "Первый уровень", "Второй уровень",
                       "Третий уровень", "Четвертый уровень", "Пятый уровень", "Шестой уровень. Финальный",
                       "Седьмой уровень. Секретный"]
    players = ['H', 'D', 'S', 'J']
    player_desc = ['Аш. Стандарт во всех смыслах', "Ди. Быстрый, но разброс больше", "Эс. Медленный, но разбрас меньше",
                   "Джей. Еще медленнее. Больше разброс, пули самонаводящиеся"]
    count = 0

    keys = [0, 0, 0, 0, 0]

    r = iter(range(0, 10000))

    while running:

        count += 1

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if fl:  # титульняк
                if timer_title.stop() >= 1000:
                    font = pygame.font.Font(fontt, 50)
                    text = font.render(listt[2], False, (255, 255, 255))
                    screen.blit(text, (200 if sprites_not_exist else 300, 250))

# ===============================================================================================================

            if event.type == pygame.KEYUP and game.gaming:
                flag_key = False

                if event.key == pygame.K_z:
                    fire = False
                if event.key == pygame.K_x:
                    keys[4] = 1
                if event.key == pygame.K_LSHIFT:
                    game.player.shift(0)

                if event.key == pygame.K_UP:
                    keys[0] = 0
                elif event.key == pygame.K_DOWN:
                    keys[1] = 0
                elif event.key == pygame.K_RIGHT:
                    keys[2] = 0
                elif event.key == pygame.K_LEFT:
                    keys[3] = 0

            if event.type == pygame.KEYDOWN:  # здесь притаилось меню
                fl = False
                flag_key = True

                if not game.gaming:
                    game.menu(event.key)
                else:
                    game.lvl0()
                    if event.key == pygame.K_z:
                        fire = True
                    if event.key == pygame.K_LSHIFT:
                        game.player.shift(1)

                    if event.key == pygame.K_UP:
                        keys[0] = 1
                    if event.key == pygame.K_DOWN:
                        keys[1] = 1
                    if event.key == pygame.K_RIGHT:
                        keys[2] = 1
                        keys[3] = 0
                    if event.key == pygame.K_LEFT:
                        keys[3] = 1
                        keys[2] = 0

        if game.gaming:
            if fire:
                game.player.shot()

            if flag_key:
                if keys[0] and game.player.y > up_border + 7:
                    game.player.ymove(-step)
                if keys[1] and game.player.y < down_border - 7:
                    game.player.ymove(step)
                if keys[2] and (not keys[3]) and game.player.x < r_border - 7:
                    game.player.xmove(step)
                if keys[3] and (not keys[2]) and game.player.x > l_border + 7:
                    game.player.xmove(-step)

            screen.fill((0, 0, 0))
            if keys[4]:
                game.player.bomb()
            for enemy in feinde:
                enemy.ymove(1)
                enemy.render()
                if enemy.y > 22 and count % 30 == 0:
                    enemy.shot()
            for obj in bullets:
                if obj.y > 0:
                    obj.move()
                    obj.entfer(game.player)
                    obj.render()
            for ob in f_bullets:
                if ob.y < height:
                    ob.move()
                    ob.entfer(game.player)
                    ob.render()
            game.player.render()
            game.extended_ramka()

            pygame.time.delay(20)

        pygame.display.flip()
    pygame.quit()
