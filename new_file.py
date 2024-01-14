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


class EnemyCommon(pygame.sprite.Sprite):  # он же враг нулевого типа
    def __init__(self, hp=5, speed=0.4, b_speed=0.5, bullet=1, entfernung=3, x=200, y=20):
        super().__init__(all_dudes)
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x - 5, y - 5), (10, 10))
        self.hp = hp
        self.bullet_speed = b_speed
        self.coef_speed = speed
        self.coef_bullet = bullet
        self.entfernung = entfernung
        self.acceleration = True

    def render(self):
        if self.hp != 0:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)

    def shot(self):  # цыганские фокусы с числами
        if self.__class__.__name__.startswith('Player'):
            self._bullet_pattern()

        elif self.__class__.__name__ == 'EnemyCommon':
            FeindBullet(self.x + int(10 + random.randint(-10, 10)),
                        self.y + 10, 6, 0, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType1':
            for i in range(-1 * self.coef_bullet, 2 * self.coef_bullet):
                FeindBullet(self.x + int(10 * i + random.randint(-10, 10)),
                            self.y + 15 * i * self.another_coef + 10, 4, i, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType3':
            for i in range(-2 * self.coef_bullet, 3 * self.coef_bullet - 1):
                FeindBullet(self.x + int(5 * i + random.randint(-20, 20)),
                            self.y - 10 * abs(i) + 10, 8, i * 0.2, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType4':
            pass
        elif self.__class__.__name__ == 'EnemyType7':
            pass

    def xmove(self, spec):
        self.x = self.x + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))

    def death(self):
        print('noo')


class EnemyType1(EnemyCommon):
    def __init__(self, x, y, hp=20, speed=0.8, bullet=2, entfernung=1):
        super().__init__(hp=hp, speed=speed, bullet=bullet, entfernung=entfernung, x=x, y=y)
        self.walk = 3
        self.another_coef = -1

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * self.walk)
        self.walk = (self.walk - 0.2) if self.walk > 0 else 0


class EnemyType3(EnemyCommon):
    def __init__(self, x, y, hp=50, b_s=0.2, speed=0.2, bullet=2, entfernung=4):
        super().__init__(hp=hp, speed=speed, b_speed=b_s, bullet=bullet, entfernung=entfernung, x=x, y=y)
        self.walk = 3

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * self.walk)
        if self.y > 0:
            self.walk = (self.walk - 0.1) if self.walk > 0 else 0


class EnemyType4(EnemyCommon):
    def __init__(self, x, y, hp=50, speed=2, bullet=1, entfernung=1):
        super().__init__(hp=hp, speed=speed, bullet=bullet, entfernung=entfernung, x=x, y=y)
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
            Bullet(self.x + 10 * i, self.y + 10, 2, i, self).add(bullets)

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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, typee, num, owner):
        super().__init__(bullets if type(self) == 'Bullet' else f_bullets)
        self.x, self.y, self.type, self.num = x, y, typee, num
        self.rect = pygame.Rect((x - (typee // 2), y - (typee // 2)), (typee, typee))
        self.owner = owner

    def move(self):
        self.y -= int(10 * self.owner.bullet_speed)
        self.x += self.owner.entfernung * self.num - self.num * random.randint(1, 2)

    def render(self):
        if self.__class__.__name__.startswith('F'):
            color = (0, 255, 255)
        else:
            color = (255, 255, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.type)


class FeindBullet(Bullet):
    def __init__(self, x, y, typee, num, owner):
        super().__init__(x, y, typee, num, owner)
        self.owner = owner

    def move(self):
        self.y += int(10 * self.owner.bullet_speed)
        self.x += self.owner.entfernung * self.num


class GeometryBulletHell:
    def __init__(self):
        self.choosen_lvl = 0
        self.player_type = 0
        self.gaming = False
        self.count_for_fertig_lvl = 0
        self.count_for_menu = 0
        self.player = Player0

        self.var_lvl0 = 0  # переменные уровней
        self.var_lvl1 = 0
        self.var_lvl2 = 0
        self.var_lvl3 = 0
        self.var_lvl4 = 0
        self.var_lvl5 = 0
        self.var_lvl6 = 0
        self.var_lvl7 = 0

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
            self.player_type = (self.player_type - 1) % 3
        elif event_key == pygame.K_DOWN:
            self.player_type = (self.player_type + 1) % 3

        elif event_key == pygame.K_z:  # ================================ КНОПКА СУДЬБЫ =========================
            global count
            x, y = 270, 550
            if self.player_type == 0:
                self.player = Player0(x=x, y=y)
            elif self.player_type == 1:
                self.player = Player1(x=x, y=y)
            elif self.player_type == 2:
                self.player = Player2(x=x, y=y)
            self.gaming = True
            screen.fill((0, 0, 0))
            self.player.render()
            self.extended_ramka()
            count = 0
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

        for j in range(3):  # персонажи
            font = pygame.font.Font(fontt, 10)
            text = font.render(players[j], False, (100, 100, 100))
            screen.blit(text, (476, 40 + 50 * j + 5))
            pygame.draw.rect(screen, (200, 200, 200), (470, 40 + 50 * j, n - 10, n - 10), 1)

            if self.count_for_fertig_lvl == self.player_type:
                pygame.draw.circle(screen, (255, 255, 255), (470, 60 + 50 * j), 5)
            self.count_for_fertig_lvl = (self.count_for_fertig_lvl + 1) % 3

    def menu_in_game(self):
        for j in range(3):
            font = pygame.font.Font(fontt, 10)
            text = font.render(players[j], False, (100, 100, 100))
            screen.blit(text, (476, 40 + 50 * j + 5))
            pygame.draw.rect(screen, (200, 200, 200), (470, 40 + 50 * j, n - 10, n - 10), 1)

            if self.count_for_fertig_lvl == self.player_type:
                pygame.draw.circle(screen, (255, 255, 255), (470, 60 + 50 * j), 5)
            self.count_for_fertig_lvl = (self.count_for_fertig_lvl + 1) % 3

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

    def score_render(self):   # TODO
        font = pygame.font.Font(fontt, 20)
        text = font.render('000000000000000', False, (100, 100, 100))
        screen.blit(text, (k, m + 20))

    def lvl0(self):
        pass

    def lvl1(self):
        if self.var_lvl1 == 0 and count > 100:
            for i in range(-5, 0):
                EnemyCommon(x=l_border + 50 * abs(i), y=up_border + 50 * i).add(feinde)
            self.var_lvl1 += 1  # потом.....,

        elif self.var_lvl1 == 1 and count > 300:
            for i in range(-5, 0):
                EnemyCommon(x=r_border + 50 * i, y=up_border + 50 * i).add(feinde)
            self.var_lvl1 += 1

        elif self.var_lvl1 == 2 and count > 600:
            for i in range(1, 5):
                feind = EnemyType1(x=l_border + 120 * i - 20, y=up_border - 20)
                if i % 2 != 0:
                    feind.another_coef = 1
                feind.add(feinde)
            self.var_lvl1 += 1

        elif self.var_lvl1 == 3 and count > 1000:
            for i in range(-5, 0):
                EnemyCommon(x=l_border + 90 * abs(i), y=up_border - 20).add(feinde)
            EnemyType3(x=l_border + 280, y=up_border - 20).add(feinde)
            EnemyType3(x=l_border + 220, y=up_border - 200).add(feinde)
            self.var_lvl1 += 1

    def lvl2(self):
        pass

    def lvl3(self):  # атавизм кода
        if self.var_lvl1 == 3 and count > 1000:
            for i in range(-5, 0):
                EnemyCommon(x=l_border + 90 * abs(i), y=up_border - 20).add(feinde)
            for j in range(-1, 3):
                EnemyType3(x=l_border + 150 * abs(j) + 100, y=up_border - 20).add(feinde)
            self.var_lvl1 += 1

    def lvl4(self):
        pass

    def lvl5(self):
        pass

    def lvl6(self):
        pass

    def lvl7(self):
        pass

# ===================================================ПРОГРАММА===============================================


try:
    foo = open('sprites/is_exist.txt', 'r')
    foo.close()
except Exception as e:
    print(e)
    sprites_not_exist = True
else:
    print('file exist')
    sprites_not_exist = False


if __name__ == '__main__':
    if sprites_not_exist:
        listt = ['TEST GAME', 'image.png', 'test lol апрол']

    pygame.display.set_caption(listt[0])
    im = pygame.image.load(listt[1])
    pygame.display.set_icon(im)
    screen.fill((0, 0, 0))
    game = GeometryBulletHell()

    up_border = 20
    down_border = 580
    l_border = 20
    r_border = 520
    all_dudes = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    f_bullets = pygame.sprite.Group()
    feinde = pygame.sprite.Group()
    fontt = 'C:/Windows/Fonts/bahnschrift.ttf'
    # TOD непонятные переменнные (потом переназову)
    n = 40
    k = 540
    m = 20
    running = True
    fl = True
    flag_key = False
    fire = False
    game_menu = False
    step = 5
    record_score = [0, 0, 0, 1, 0, 10, 0, 0]
    lvl_description = ["""Нулевой уровень. Обучение. Показываются 
    основы игры""", "Первый уровень", "Второй уровень",
                       "Третий уровень", "Четвертый уровень", "Пятый уровень", "Шестой уровень. Финальный",
                       "Седьмой уровень. Секретный"]
    players = ['H', 'D', 'S']
    player_desc = ['Аш. Стандарт во всех смыслах', "Ди. Быстрый, но разброс больше", "Эс. Медленный, но разбрас меньше"]
    count = 0

    keys = [0, 0, 0, 0, 0]

    r = iter(range(0, 10000))  # sekret
    sekret = 0

    while running:

        count += 1  # костыль на коем всё держится
        if game.gaming:
            eval(f'game.lvl{game.choosen_lvl}()')

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if fl:  # титульняк
                if count > 1000:
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
                if event.key == pygame.K_s:
                    sekret = 0

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
                    if event.key == pygame.K_z:
                        fire = True
                    if event.key == pygame.K_LSHIFT:
                        game.player.shift(1)
                    if event.key == pygame.K_ESCAPE:
                        game_menu = not game_menu
                    if event.key == pygame.K_s:
                        sekret = 1

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
            if not game_menu:
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
                    if pygame.sprite.spritecollideany(enemy, bullets):
                        print('why.')
                        enemy.hp -= 1
                    if enemy.hp != 0:
                        enemy.ymove(step)
                        enemy.render()
                        if enemy.y > 22:
                            spice = type(enemy).__name__
                            if count % 40 == 0 and spice == 'EnemyCommon':
                                enemy.shot()
                            if count % 20 == 0 and spice == 'EnemyType1':
                                enemy.shot()
                            if count % 50 == 0 and spice == 'EnemyType3':
                                enemy.shot()

                for obj in bullets:  # пули игрока
                    if obj.y > 0:
                        obj.move()
                        obj.render()

                if pygame.sprite.spritecollide(game.player, f_bullets, False):
                    print('noo')

                for ob in f_bullets:  # пули врага
                    # print(1, len(f_bullets))
                    if ob.y < height:
                        ob.move()
                        ob.render()
                    else:
                        ob.remove(f_bullets)  # ? почему ничего не удаляется из списка
                    # print(2, len(f_bullets))
            else:
                game.menu_in_game()

            game.player.render()
            game.extended_ramka()
            pygame.draw.polygon(screen, (255, 255, 255), ((game.player.x - 13, down_border + 14),
                                                          (game.player.x, down_border + 6),
                                                          (game.player.x + 13, down_border + 14)))
            game.score_render()

            if not sekret:
                pygame.time.delay(20)

        pygame.display.flip()
    pygame.quit()
