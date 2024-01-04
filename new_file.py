import pygame
from serv import listt


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


class EnemyCommon:  # он же враг нулевого типа
    pass


class GeometryBulletHell:
    def __init__(self):
        self.choosen_lvl = 0
        self.player_type = 0
        self.gaming = False
        self.count_for_fertig_lvl = 0
        self.count_for_menu = 0
        '''self.player = тип_игрока'''

    def menu(self, event_key):
        '''главное меню'''
        self.ramka()
        font = pygame.font.Font(fontt, 13)
        # ====================================================================^
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
            if self.player_type == 0:
                pass
            self.gaming = True
            screen.fill((0, 0, 0))
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
        pygame.draw.rect(screen, (0, 0, 0), (520, 0, width, 20))
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


# ===================================================таймер====================================
class Timer:
    def __init__(self):
        self.time = pygame.time.get_ticks()

    def reset(self):
        self.time = pygame.time.get_ticks()

    def stop(self):
        serv = pygame.time.get_ticks() - self.time
        return serv


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

    fps = 40

    clock = pygame.time.Clock()
    clock.tick(fps)

    running = True
    fl = True
    flag_key = False
    screen.fill((0, 0, 0))

    bullets = []
    feinde = []
    fontt = 'C:/Windows/Fonts/bahnschrift.ttf'
    # непонятные переменнные
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

        pygame.display.flip()
    pygame.quit()
