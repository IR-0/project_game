import pygame
# from serv import listt


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 40
clock = pygame.time.Clock()
clock.tick(fps)


class EnemyCommon:  # он же враг нулевого типа
    def __init__(self, hp=5, speed=0.8, bullet=0.6, entfernung=2.0, x=200, y=20):
        self.x = x
        self.y = y
        self.hp = hp
        self.coef_speed = speed
        self.coef_bullet = bullet
        self.entfernung = entfernung

    def render(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)
        pass

    def shot(self):
        pass

    def xmove(self, spec, acceleration=1):
        self.x = self.x + int(spec * self.coef_speed * acceleration)

    def ymove(self, spec, acceleration=1):
        self.y = self.y + int(spec * self.coef_speed * acceleration)

    def death(self):
        pass


class EnemyType1(EnemyCommon):
    def __init__(self):
        super().__init__(20, 1, 1, 1)


class EnemyType3(EnemyCommon):
    def __init__(self):
        super().__init__(50, 1, 1.5, 0.9)


class EnemyType4(EnemyCommon):
    def __init__(self, hp=50, speed=2, bullet=1, entfernung=0.8):
        super().__init__(hp, speed, bullet, entfernung)
        self.anticipation = 40

    def ruck(self, coef=1):  # уклон
        pass


class EnemyType7(EnemyType4):
    def __init__(self):
        super().__init__(100, 2, 2, 0.7)
        self.anticipation = 20

    def ruck(self):
        super().ruck(coef=2)


class Player0(EnemyCommon):  # h. Общий класс для всех играбельных персонажей
    def __init__(self, hp=1, speed=1, bullet=1, ent=1.0, x=400, y=400):
        super().__init__(hp=hp, speed=speed, bullet=bullet, entfernung=ent, x=x, y=y)

    def graze(self):
        pass

    def bomb(self):
        pass


class Player1(Player0):  # d
    def __init__(self):
        super().__init__(speed=1.3, bullet=0.9, ent=0.8)


class Player2(Player0):  # s
    def __init__(self):
        super().__init__(speed=0.9, bullet=1.3, ent=1.3)


class Player3(Player0):  # j
    def __init__(self):
        super().__init__(speed=0.8, bullet=1.1, ent=1.4)


class GeometryBulletHell:
    def __init__(self):
        self.choosen_lvl = 0
        self.player_type = 0
        self.gaming = False
        self.count_for_fertig_lvl = 0
        self.count_for_menu = 0
        self.player = Player0

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
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 20))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 20, height))
        pygame.draw.rect(screen, (0, 0, 0), (0, 580, width, height))
        pygame.draw.rect(screen, (0, 0, 0), (520, 0, width, height))
        pygame.draw.rect(screen, (255, 255, 255), (20, 20, 500, 560), 2)

    def lvl0(self):
        pass

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


class Timer:
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
    screen.fill((0, 0, 0))

    bullets = []
    feinde = []
    fontt = 'C:/Windows/Fonts/bahnschrift.ttf'
    # TOD непонятные переменнные (потом переназову)
    n = 40
    k = 540
    m = 20
    step = 4
    record_score = [0, 0, 0, 1, 0, 10, 0, 0]
    lvl_description = ["""Нулевой уровень. Обучение. Показываются 
    основы игры""", "Первый уровень", "Второй уровень",
                       "Третий уровень", "Четвертый уровень", "Пятый уровень", "Шестой уровень. Финальный",
                       "Седьмой уровень. Секретный"]
    players = ['H', 'D', 'S', 'J']
    player_desc = ['Аш. Стандарт во всех смыслах', "Ди. Быстрый, но разброс больше", "Эс. Медленный, но разбрас меньше",
                   "Джей. Еще медленнее. Больше разброс, пули самонаводящиеся"]
    count = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if fl:  # титульняк
                if timer_title.stop() >= 1000:
                    font = pygame.font.Font(fontt, 50)
                    text = font.render(listt[2], False, (255, 255, 255))
                    screen.blit(text, (200 if sprites_not_exist else 300, 250))

            if event.type == pygame.KEYDOWN:  # ИГРА
                fl = False
                flag_key = True

                game.menu(event.key)
            elif event.type == pygame.KEYUP:
                flag_key = False

            if game.gaming:
                if event.type == pygame.KEYDOWN:
                    if flag_key:
                        if event.key == pygame.K_UP:
                            game.player.ymove(-step)
                            print('ok')
                        elif event.key == pygame.K_DOWN:
                            game.player.ymove(step)
                        elif event.key == pygame.K_RIGHT:
                            game.player.xmove(step)
                        elif event.key == pygame.K_LEFT:
                            game.player.xmove(-step)
                        screen.fill((0, 0, 0))
                        game.player.render()
                        game.extended_ramka()

        pygame.display.flip()
    pygame.quit()
