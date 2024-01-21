import sys
import os
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
    def __init__(self, hp=5, speed=0.2, b_speed=0.5, bullet=1, entfernung=3, x=200, y=20):
        super().__init__(all_dudes)
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x - v, y - v), (10, 10))
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
            for i in range(-1 * self.coef_bullet - int(game.difficult),  self.coef_bullet + int(game.difficult)):
                FeindBullet(self.x + int(10 * i + random.randint(-10, 10)),
                            self.y + 15 * i * self.another_coef + 10, 4, i, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType3':
            for i in range(-2 * self.coef_bullet - int(game.difficult), 3 * self.coef_bullet - 1 + int(game.difficult)):
                FeindBullet(self.x + int(5 * i + random.randint(-30, 30)),
                            self.y - 10 * abs(i) + 10, 8, i * 0.2, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType4':
            for i in range(-2 * self.coef_bullet - 1 - int(game.difficult),
                           3 * self.coef_bullet + 1 + int(game.difficult)):
                FeindBullet(self.x + int(10 * i + random.randint(-20, 20)),
                            self.y - 10 * abs(i) + 20, 4, i, self).add(f_bullets)
        elif self.__class__.__name__ == 'EnemyType7':
            self.another_coef = self.another_coef + (-1 if self.another_coef > -3 else 5)
            for i in range(-1 * self.coef_bullet + self.another_coef - int(not game.difficult),
                           2 * self.coef_bullet + self.another_coef + int(not game.difficult)):
                FeindBullet(self.x + int(10 * i + random.randint(-20, 20)),
                            self.y - 10 * abs(i) + 20, 4, i, self).add(f_bullets)

    def xmove(self, spec):
        self.x = self.x + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))
        self.rect.x = self.x - v

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * (1 if self.acceleration else 0.5))
        self.rect.y = self.y - v

    def death(self):
        print('noo1')


class EnemyType1(EnemyCommon):
    def __init__(self, x, y, hp=20, speed=0.8, bullet=2, entfernung=1):
        super().__init__(hp=hp, speed=speed, bullet=bullet, entfernung=entfernung, x=x, y=y)
        self.walk = 3
        self.another_coef = -1

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * self.walk)
        self.walk = (self.walk - 0.2) if self.walk > 0 else 0
        self.rect.y = self.y - v


class EnemyType3(EnemyCommon):
    def __init__(self, x, y, hp=50, b_s=0.2, speed=0.2, bullet=2, entfernung=4):
        super().__init__(hp=hp, speed=speed, b_speed=b_s, bullet=bullet, entfernung=entfernung, x=x, y=y)
        self.walk = 3

    def ymove(self, spec):
        self.y = self.y + int(spec * self.coef_speed * self.walk)
        if self.y > 0:
            self.walk = (self.walk - 0.1) if self.walk > 0 else 0
        self.rect.y = self.y - v


class EnemyType4(EnemyCommon):
    def __init__(self, x, y, hp=80, speed=2, b_s=0.6, bullet=1, entfernung=1, anti=20):
        super().__init__(hp=hp, speed=speed, b_speed=b_s, bullet=bullet, entfernung=entfernung, x=x, y=y)
        self.anticipation = anti
        self.graze = HitBox(self.x - self.anticipation // 2, self.y - self.anticipation // 2, self.anticipation)
        self.walk = 3
        self.stop = 0
        self.to_x = 0

    def ymove(self, spec):
        serv = up_border + 40
        if self.y > serv and not self.stop:
            self.stop = 1
        elif self.y > serv and self.stop == 1:
            self.stop = 2
        elif self.y < serv and self.stop == 2:
            self.stop = 3

        self.y = self.y + int(spec * self.coef_speed * self.walk) + (-1 if self.stop == 2 else 0)
        self.walk = (self.walk - 0.1) if self.walk > 0 else 0
        self.rect.y = self.y - v
        self.graze.rect.y = self.y - self.anticipation // 2

    def xmove(self, spec):
        if self.to_x != 0:
            self.x = self.x + int(spec * self.coef_speed * self.to_x * 4)
        self.rect.x = self.x - v
        self.graze.rect.x = self.x - self.anticipation // 2

    def ruck(self):  # уклон от пуль врагом
        if pygame.sprite.spritecollideany(self.graze, bullets):
            if count % (1000 // self.anticipation) == 0:
                self.to_x = -1 if self.to_x == 1 else 1


class EnemyType7(EnemyType4):
    def __init__(self, x, y, b_s=1.0, speed=2, bullet=1, entfernung=1):
        super().__init__(x, y, speed=speed, b_s=b_s, bullet=bullet, entfernung=entfernung)
        self.another_coef = -1
        self.anticipation = 50

    def ruck(self):
        super().ruck()


class Player0(EnemyCommon):  # h. Общий класс для всех играбельных персонажей
    def __init__(self, hp=5, speed=1, b_s=1, bullet=2, ent=2, x=400, y=400):
        super().__init__(hp=hp, speed=speed, b_speed=b_s, bullet=bullet, entfernung=ent, x=x, y=y)
        self.x, self.y = x, y  # почемуто программа не видит координаты
        self.r, self.r_x, self.r_y = 0, 0, 0
        self.graze_rect = HitBox(self.x - 20, self.y - 20, 40)
        self.bombing = None
        self.gr_bomb = pygame.sprite.Group()
        self.count_b = 3

    def xmove(self, spec):
        super().xmove(spec)
        self.graze_rect.rect.x = self.x - 10

    def ymove(self, spec):
        super().ymove(spec)
        self.graze_rect.rect.y = self.y - 10

    def _bullet_pattern(self):
        for i in range(-1 * self.coef_bullet, self.coef_bullet + 1):
            Bullet(self.x + 10 * i, self.y - 10, 2, i, self).add(bullets)

    def bomb(self):
        global keys
        if self.count_b == 0:
            return
        if self.r_x == 0 or self.r_y == 0:
            self.r_x, self.r_y = self.x, self.y
        if self.r < 600:
            pygame.draw.circle(screen, (100, 100, 100), (self.r_x, self.r_y), self.r)
            if self.bombing is not None:
                self.bombing.kill()
            self.bombing = HitBox(self.r_x - (self.r // 2), self.r_y - (self.r // 2), self.r)
            self.bombing.add(self.gr_bomb)
            self.r += 2
        else:
            keys[4] = 0
            self.count_b -= 1
            self.bombing.kill()
            self.bombing = None
            self.r, self.r_x, self.r_y = 0, 0, 0

    def shift(self, off):  # выключить ускорение и замедлить персонажа
        self.acceleration = False if off else True

    def graze(self):  # начисления очков, если персонаж проходит рядом с пулей
        # print(self.x, self.graze_rect.rect.x)
        if pygame.sprite.spritecollideany(self.graze_rect, f_bullets):
            if count % 10 == 0:
                game.graze += 1


class Player1(Player0):  # d
    def __init__(self, x, y):
        super().__init__(speed=2, bullet=1, ent=1, x=x, y=y)


class Player2(Player0):  # s
    def __init__(self, x, y):
        super().__init__(speed=0.9, bullet=1, ent=3, x=x, y=y)

    def _bullet_pattern(self):
        for i in range(-2 * self.coef_bullet, 3 * self.coef_bullet, 2):
            Bullet(self.x + int(5 * i + random.randint(-30, 30)),
                   self.y - 20 * abs(i) + 10, 2, i, self).add(bullets)


class HitBox(pygame.sprite.Sprite):
    def __init__(self, x, y, a):
        super().__init__()
        self.rect = pygame.Rect((x, y), (a, a))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, typee, num, owner):
        super().__init__(bullets if self.__class__.__name__ == 'Bullet' else f_bullets)
        self.x, self.y, self.type, self.num = x, y, typee, num
        self.rect = pygame.Rect((x - (typee // 2), y - (typee // 2)), (typee, typee))
        self.owner = owner

    def move(self):
        self.y -= int(10 * self.owner.bullet_speed)
        self.x += self.owner.entfernung * self.num - self.num * random.randint(1, 2)
        self.rect.x = self.x - v
        self.rect.y = self.y - v

    def render(self):
        if self.__class__.__name__.startswith('F'):
            color = (0, 255, 255)
        else:
            color = (255, 255, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.type)


class FeindBullet(Bullet):
    def __init__(self, x, y, typee, num, owner):
        super().__init__(x, y, typee, num, owner)

    def move(self):
        self.y += int(10 * self.owner.bullet_speed)
        self.x += self.owner.entfernung * self.num
        self.rect.x = self.x - v
        self.rect.y = self.y - v


class GeometryBulletHell:
    def __init__(self):
        self.choosen_lvl = 0
        self.player_type = 0
        self.gaming = False
        self.count = 0
        self.count_for_fertig_lvl = 0
        self.count_for_menu = 0
        self.difficult = False

        self.graze = 0
        self.count_killed = 0
        self.player = Player0

        self.var_lvl0 = 0  # служебные переменные уровней
        self.var_lvl1 = 0
        self.var_lvl2 = 0
        self.var_lvl3 = 0
        self.var_lvl4 = 0
        self.var_lvl5 = 0
        self.var_lvl6 = 0
        self.var_lvl7 = 0

    def menu(self, eventt):
        '''главное меню'''
        global arrow
        self.ramka()
        font = pygame.font.Font(fontt, 13)
        text = font.render('sum of record score: ' + str(sum(record_score)), False, (140, 140, 140))
        screen.blit(text, (k, m))
        self.choosen_lvl = abs(self.choosen_lvl) % 8

        # перемещение курсорными клавишами по уровням
        if eventt.type == pygame.KEYDOWN:
            eventt = eventt.key
            if eventt == pygame.K_LEFT:
                self.choosen_lvl = (self.choosen_lvl - 1) % 8
            elif eventt == pygame.K_RIGHT:
                self.choosen_lvl = (self.choosen_lvl + 1) % 8
            elif eventt == pygame.K_UP:
                self.player_type = (self.player_type - 1) % 3
            elif eventt == pygame.K_DOWN:
                self.player_type = (self.player_type + 1) % 3

            elif eventt == pygame.K_z:  # ================================ КНОПКА СУДЬБЫ =========================
                global count
                if self.choosen_lvl == 7 and sum(record_score) < 500_000:
                    font = pygame.font.Font(None, 40)
                    text = font.render('играйте, чтобы открыть уровень', False, (100, 100, 100))
                    screen.blit(text, (40, 300))
                    return
                elif self.choosen_lvl == 7 and sum(record_score) >= 500_000:
                    print('accesss')
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
        else:
            x, y = eventt.pos
            if event.type == pygame.MOUSEMOTION:
                arrow.rect.x = x
                arrow.rect.y = y

            if eventt.type == pygame.MOUSEBUTTONDOWN:
                if eventt.pos:
                    if (400 < x < 430) and (40 < y < 70):
                        self.difficult = not self.difficult

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

        # размещение уровней и игрока в меню. Описание уровней
        for j in range(2):
            for i in range(4):
                font = pygame.font.Font(None, 50)
                text = font.render(str(self.count_for_menu), False, (100, 100, 100))
                screen.blit(text, (40 + 50 * i + 10, 40 + 50 * j + 5))
                pygame.draw.rect(screen, (255, 255, 255), (40 + 50 * i, 40 + 50 * j, n, n), 1)

                if self.count_for_menu == self.choosen_lvl:
                    pygame.draw.circle(screen, (255, 255, 255), ((20 + 50 * i) + 20, (48 + 50 * j) + 20), 5)

                    font = pygame.font.Font(fontt, 20)
                    text = font.render(lvl_description[self.count_for_menu], False, (255, 255, 255))
                    screen.blit(text, (30, 300))

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
            font = pygame.font.Font(fontt, 20)
            text = font.render(player_desc[self.player_type], False, (255, 255, 255))
            screen.blit(text, (30, 200))

        # сложность
        font = pygame.font.Font(fontt, 13)
        text = font.render('hard' if self.difficult else 'easy', False, (100, 100, 100))
        screen.blit(text, (402, 47))
        pygame.draw.rect(screen, (200, 200, 200), (400, 40, n - 10, n - 10), 1)

        arrow_group.draw(screen)

    def menu_in_game(self, key):
        global game_menu
        if key != 'NaN':
            if key == pygame.K_z:
                self.end_lvl(0)
                game_menu = not game_menu

        serv = (190, 300, 145, 40)
        font = pygame.font.Font(fontt, 30)
        text = font.render('ПАУЗА', False, (100, 100, 100))
        screen.blit(text, (220, 170, 60, 40))
        pygame.draw.rect(screen, (0, 0, 0), serv)
        pygame.draw.rect(screen, (200, 200, 200), serv, 1)
        font = pygame.font.Font(fontt, 15)
        text = font.render('выйти в меню', False, (100, 100, 100))
        screen.blit(text, (215, 310, 60, 40))

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
        global another
        if 40 < count < 99:
            another = True
        elif self.var_lvl0 == 0 and count > 100:
            another = False
            self.var_lvl0 += 1

        elif self.var_lvl0 == 1 and count > 160:
            EnemyCommon(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl0 += 1

        elif self.var_lvl0 == 2 and count > 350:
            EnemyCommon(x=l_border + 100, y=up_border - 10).add(feinde)
            self.var_lvl0 += 1

        elif self.var_lvl0 == 3 and count > 500:
            for i in range(3):
                EnemyCommon(x=l_border + 100 * i + 100, y=up_border - 10).add(feinde)
            self.var_lvl0 += 1

        elif self.var_lvl0 == 4:
            if all([h.hp < 1 or h.y > height for h in feinde]):
                self.var_lvl0 += 1

        elif self.var_lvl0 == 5:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl1(self):
        if self.var_lvl1 == 0 and count > 40:
            if self.difficult:
                for j in range(4):
                    EnemyCommon(x=l_border + 100 * j + 90, y=up_border - 10).add(feinde)
            else:
                EnemyCommon(x=l_border + 200, y=up_border - 10).add(feinde)
                EnemyCommon(x=l_border + 300, y=up_border - 10).add(feinde)
            self.var_lvl1 += 1

        elif self.var_lvl1 == 1 and count > 240:
            for i in range(5):
                EnemyCommon(x=l_border + 80 * i + 100, y=up_border - 10).add(feinde)
            self.var_lvl1 += 1

        elif self.var_lvl1 == 2 and count > 400:
            EnemyType1(x=l_border + 140, y=up_border - 10).add(feinde)
            EnemyType1(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl1 += 1

        elif self.var_lvl1 == 3:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl1 += 1

        elif self.var_lvl1 == 4:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl2(self):
        if self.var_lvl2 == 0 and count > 100:
            for i in range(-5, game.difficult):
                EnemyCommon(x=l_border + 50 * abs(i) + 20, y=up_border + 50 * i).add(feinde)
            self.var_lvl2 += 1

        elif self.var_lvl2 == 1 and count > 300:
            for i in range(-5, game.difficult):
                EnemyCommon(x=r_border + 50 * i - 20, y=up_border + 50 * i).add(feinde)
            self.var_lvl2 += 1

        elif self.var_lvl2 == 2 and count > 600:
            for i in range(1, 5):
                feind = EnemyType1(x=l_border + 120 * i - 20, y=up_border - 20)
                if i % 2 != 0:
                    feind.another_coef = 1
                feind.add(feinde)
            self.var_lvl2 += 1

        elif self.var_lvl2 == 3 and count > 1000:
            for i in range(-5, 0):
                EnemyCommon(x=l_border + 90 * abs(i), y=up_border - 20).add(feinde)
            EnemyType3(x=l_border + 280, y=up_border - 20).add(feinde)
            EnemyType3(x=l_border + 220, y=up_border - 200).add(feinde)
            if game.difficult:
                EnemyType3(x=l_border + 340, y=up_border - 80).add(feinde)
                EnemyType3(x=l_border + 160, y=up_border - 100).add(feinde)
            self.var_lvl2 += 1

        elif self.var_lvl2 == 4:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl2 += 1

        elif count > 2000:
            self.var_lvl2 = 5

        elif self.var_lvl2 == 5:
            self.end_lvl(1)
            return

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl3(self):
        if self.var_lvl3 == 0 and count > 20:
            EnemyType4(x=l_border + 180, y=up_border - 20).add(feinde)
            self.var_lvl3 += 1

        elif self.var_lvl3 == 1 and count > 260:
            for i in range(-5, 0):
                EnemyCommon(x=l_border + 90 * abs(i), y=up_border - 20).add(feinde)
            for j in range(0, 3):
                EnemyType3(x=l_border + 150 * abs(j) + 100, y=up_border - 20).add(feinde)
            self.var_lvl3 += 1

        elif self.var_lvl3 == 2 and count > 700:
            EnemyType1(x=l_border + 140, y=up_border - 10).add(feinde)
            EnemyType1(x=l_border + 400, y=up_border - 10).add(feinde)
            EnemyType3(x=l_border + 250, y=up_border - 20).add(feinde)
            self.var_lvl3 += 1

        elif self.var_lvl3 == 3:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl3 += 1

        elif self.var_lvl3 == 4:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl4(self):
        if self.var_lvl4 == 0 and count > 30:
            EnemyType3(x=l_border + 200, y=up_border - 10).add(feinde)
            EnemyType3(x=l_border + 300, y=up_border - 10).add(feinde)
            self.var_lvl4 += 1

        elif self.var_lvl4 == 1 and count > 190:
            EnemyType1(x=l_border + 250, y=up_border - 10).add(feinde)
            self.var_lvl4 += 1

        elif self.var_lvl4 == 2 and count > 300:
            EnemyType1(x=l_border + 100, y=up_border - 10).add(feinde)
            self.var_lvl4 += 1

        elif self.var_lvl4 == 3 and count > 400:
            EnemyType1(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl4 += 1

        elif self.var_lvl4 == 4 and count > 500:
            EnemyType4(x=l_border + 250, y=up_border - 10).add(feinde)
            self.var_lvl4 += 1

        elif self.var_lvl4 == 5:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl4 += 1

        elif self.var_lvl4 == 6:
            self.end_lvl(1)

        print(self.var_lvl4)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl5(self):
        if self.var_lvl5 == 0 and count > 30:
            EnemyType7(x=l_border + 150, y=up_border - 20).add(feinde)
            self.var_lvl5 += 1

        elif self.var_lvl5 == 1 and count > 200:
            EnemyType3(x=l_border + 100, y=up_border - 10).add(feinde)
            self.var_lvl5 += 1

        elif self.var_lvl5 == 2 and count > 250:
            EnemyType3(x=l_border + 250, y=up_border - 10).add(feinde)
            self.var_lvl5 += 1

        elif self.var_lvl5 == 3 and count > 300:
            EnemyType3(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl5 += 1

        elif self.var_lvl5 == 4 and count > 500:
            EnemyType7(x=l_border + 150, y=up_border - 10).add(feinde)
            EnemyType7(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl5 += 1

        elif self.var_lvl5 == 5:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl5 += 1

        elif self.var_lvl5 == 6:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl6(self):
        if self.var_lvl6 == 0 and count > 40:
            for i in range(-3, game.difficult):
                EnemyType4(x=l_border + 100 * abs(i) + 20, y=up_border + 50 * i).add(feinde)
            self.var_lvl6 += 1

        elif self.var_lvl6 == 1 and count > 400:
            EnemyType1(x=l_border + 220, y=up_border - 10).add(feinde)
            EnemyType1(x=l_border + 270, y=up_border - 10).add(feinde)
            EnemyType3(x=l_border + 100, y=up_border - 10).add(feinde)
            EnemyType3(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl6 += 1

        elif self.var_lvl6 == 2 and count > 900:
            for i in range(-5, int(game.difficult)):
                EnemyType1(x=l_border + 80 * abs(i) + 20, y=up_border - 10).add(feinde)
            self.var_lvl6 += 1

        elif self.var_lvl6 == 3:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl6 += 1

        if self.var_lvl6 == 4:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def lvl7(self):
        print(self.var_lvl7, count)
        if self.var_lvl7 == 0 and count > 40:
            EnemyType7(x=l_border + 100, y=up_border - 10).add(feinde)
            EnemyType7(x=l_border + 400, y=up_border - 10).add(feinde)
            EnemyType3(x=l_border + 250, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 1 and count > 200:
            for i in range(-5, int(game.difficult)):
                EnemyType1(x=l_border + 80 * abs(i) + 20, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 2 and count > 500:
            EnemyType7(x=l_border + 100, y=up_border - 10).add(feinde)
            EnemyType7(x=l_border + 150, y=up_border - 10).add(feinde)
            EnemyType7(x=l_border + 300, y=up_border - 10).add(feinde)
            EnemyType7(x=l_border + 350, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 3 and count > 900:
            EnemyType3(x=l_border + 100, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 4 and count > 1000:
            EnemyType1(x=l_border + 100, y=up_border - 10).add(feinde)
            EnemyType1(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 5 and count > 1100:
            EnemyType3(x=l_border + 250, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 6 and count > 1200:
            EnemyType1(x=l_border + 210, y=up_border - 10).add(feinde)
            EnemyType1(x=l_border + 270, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 7 and count > 1300:
            EnemyType3(x=l_border + 400, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 8 and count > 1400:
            for i in range(-6, int(game.difficult)):
                EnemyType1(x=l_border + 80 * abs(i) + 20, y=up_border - 10).add(feinde)
            self.var_lvl7 += 1

        elif self.var_lvl7 == 9:
            if all([(h.hp < 1 or h.y > height) for h in feinde]):
                self.var_lvl7 += 1

        elif self.var_lvl7 == 10:
            self.end_lvl(1)

        sc = self.score(0)
        self.score_render(var=sc)

    def end_lvl(self, on_off):
        global feinde, f_bullets, bullets, keys, another
        feinde = pygame.sprite.Group()
        f_bullets = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        keys = [0, 0, 0, 0, 0]
        another = False
        # это прискорбно сообщать, но через eval и цикл не работает
        self.var_lvl0 = 0
        self.var_lvl1 = 0
        self.var_lvl2 = 0
        self.var_lvl3 = 0
        self.var_lvl4 = 0
        self.var_lvl5 = 0
        self.var_lvl6 = 0
        self.var_lvl7 = 0

        self.score(on_off)
        self.graze, self.count_killed = 0, 0
        game.gaming = False
        return

    def score(self, on_off):  # подчет итогов
        score = int((self.graze * 100 + self.count_killed * 10) * self.player.hp *
                    (self.player.count_b if self.player.count_b != 0 else 0.5))
        if self.difficult:
            score = score * 2

        if score > record_score[self.choosen_lvl] and on_off:
            record_score[self.choosen_lvl] = score
        return score

    def score_render(self, var=0):
        font = pygame.font.Font(fontt, 20)
        text = font.render(str(var), False, (100, 100, 100))
        screen.blit(text, (k, m + 20))

        font = pygame.font.Font(fontt, 20)
        text = font.render('lifes: ' + str(self.player.hp), False, (100, 100, 100))
        screen.blit(text, (k, m + 50))

        font = pygame.font.Font(fontt, 20)
        text = font.render('bombs: ' + str(self.player.count_b), False, (100, 100, 100))
        screen.blit(text, (k, m + 80))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


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
        listt = ['GEOMETRY HELL', 'image.png', '']

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
    # TODO непонятные переменнные (потом переназову)
    n = 40
    k = 540
    m = 20
    v = 5
    running = True
    fl = True
    flag_key = False
    fire = False
    game_menu = False
    another = False
    step = 5

    with open('save.txt', 'r') as save:
        record_score = [int(sc.strip()) for sc in save.readlines()]

    lvl_description = ["""Нулевой уровень. Обучение""", "Первый уровень", "Второй уровень",
                       "Третий уровень", "Четвертый уровень", "Пятый уровень", "Шестой уровень. Финальный",
                       "Седьмой уровень. Секретный"]
    players = ['H', 'D', 'S']
    player_desc = ['Аш. Стандарт во всех смыслах', "Ди. Быстрый, разброс меньше", "Эс. Медленный, разброс больше"]
    count = 0

    keys = [0, 0, 0, 0, 0]

    r = iter(range(0, 10000))  # sekret
    sekret = 0

    arrow_group = pygame.sprite.Group()
    arrow = pygame.sprite.Sprite(arrow_group)
    arrow.image = load_image('katze.png')
    arrow.rect = arrow.image.get_rect()

    while running:

        count += 1  # костыль на коем всё держится
        if game.gaming:
            eval(f'game.lvl{game.choosen_lvl}()')

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                with open('save.txt', 'w') as save:
                    for elem in record_score:
                        save.write(str(elem) + '\n')
                sys.exit()
            if fl:  # титульняк
                if count > 1000:
                    font = pygame.font.Font(fontt, 50)
                    text = font.render(listt[2], False, (255, 255, 255))
                    screen.blit(text, (200 if sprites_not_exist else 300, 250))

# ===============================================================================================================

            if event.type == pygame.KEYUP and game.gaming:
                if not pygame.key.get_pressed():
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

            if event.type == pygame.KEYDOWN:
                fl = False
                flag_key = True

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

            if not game.gaming and (event.type == pygame.KEYDOWN or
                                    event.type == pygame.MOUSEMOTION) or \
                    (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                game.menu(event)

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
                    spice = enemy.__class__.__name__
                    if spice == 'Player0':
                        print(0)
                        continue
                    if pygame.sprite.spritecollideany(enemy, bullets):
                        enemy.hp -= 1
                        if enemy.hp == 0:
                            game.count_killed += 1
                            continue
                    if pygame.sprite.spritecollideany(enemy, game.player.gr_bomb):
                        enemy.hp = -1
                        continue
                    if enemy.hp > 0:
                        enemy.ymove(step)
                        enemy.render()
                        if enemy.y > 22:
                            if count % 40 == 0 and spice == 'EnemyCommon':
                                enemy.shot()
                            if count % 20 == 0 and spice == 'EnemyType1':
                                enemy.another_coef = - enemy.another_coef
                                enemy.shot()
                            if count % 50 == 0 and spice == 'EnemyType3':
                                enemy.shot()
                            if count % 10 == 0 and spice == 'EnemyType4':
                                enemy.shot()
                                enemy.ruck()
                                enemy.xmove(2)
                                if count % 10 == 0:
                                    enemy.to_x = 0
                            if spice == 'EnemyType7':
                                if game.difficult:
                                    if count % 10 == 0:
                                        enemy.shot()
                                        enemy.ruck()
                                        enemy.xmove(2)
                                else:
                                    if count % 20 == 0:
                                        enemy.shot()
                                        enemy.ruck()
                                        enemy.xmove(2)
                                if count % 100 == 0:
                                    enemy.to_x = 0

                for obj in bullets:  # пули игрока
                    if obj.y > 0:
                        obj.move()
                        obj.render()
                    else:
                        obj.kill()

                game.player.graze()
                if pygame.sprite.spritecollideany(game.player, f_bullets) and count % 3 == 0:
                    game.player.hp -= 1
                    if game.player.hp == 0:
                        game.end_lvl(0)
                        font = pygame.font.Font(fontt, 70)
                        text = font.render('GAME OVER', False, (100, 100, 100))
                        screen.blit(text, (l_border + 80, up_border + 200))

                for ob in f_bullets:  # пули врага
                    if ob.y < height:
                        if not pygame.sprite.spritecollideany(ob, game.player.gr_bomb):
                            ob.move()
                            ob.render()
                        else:
                            ob.kill()
                    elif ob.y > height:
                        ob.kill()
            else:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        game.menu_in_game(event.key)
                    else:
                        game.menu_in_game('NaN')

            game.player.render()
            game.extended_ramka()
            sc = game.score(0)
            game.score_render(var=sc)
            pygame.draw.polygon(screen, (255, 255, 255), ((game.player.x - 13, down_border + 14),
                                                          (game.player.x, down_border + 6),
                                                          (game.player.x + 13, down_border + 14)))
            if another:
                font = pygame.font.Font(fontt, 15)
                text0 = font.render('передвижение по стрелочкам', False, (255, 255, 255))
                text1 = font.render('стрельба на клавишу "я"', False, (255, 255, 255))
                text2 = font.render('активирование бомбы на клавишу "ч"', False, (255, 255, 255))
                text3 = font.render('замедлиться на левый shift', False, (255, 255, 255))
                text = [text0, text1, text2, text3]
                for i in range(4):
                    screen.blit(text[i], (40, 350 + i * 20, 60, 40))

            if not sekret:
                pygame.time.delay(20)

        pygame.display.flip()
    pygame.quit()
