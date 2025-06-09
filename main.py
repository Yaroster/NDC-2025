import pyxel
import random

# Constants
FPS = 30
HEIGHT = 128
WIDTH = 128


class App:
    def __init__(self):
        # Initialisation de l'Etat du Jeu
        self.gamestate = 0

        # Variables des Joueurs
        self.player_x = 64
        self.player_y = 96
        self.player_state = 0
        self.player_sprite_1, self.player_sprite_2 = 0, 72
        self.player_charges = 3

        # Score
        self.score = 0

        # NB: On appelle ici Canard ("Duck") les ennemis du jeu en reference a Duck Hunt
        self.ducks1 = []  # spawn left
        self.ducks2 = []  # spawn right
        self.ducks3 = []  # spawn left
        self.ducks4 = []  # spawn right
        self.ducks5 = []  # spawn left
        self.ducks = [self.ducks1, self.ducks2, self.ducks3, self.ducks4, self.ducks5]
        self.duck1delay = self.duck2delay = self.duck3delay = self.duck4delay = self.duck5delay = 3
        self.duckdelays = [self.duck1delay, self.duck2delay, self.duck3delay, self.duck4delay, self.duck5delay]

        # Etats des Canards
        self.duckstate = 0
        self.duck_sprite_x = 0
        self.duck_sprite_y = 88

        # Minuteur
        self.timer = 60 * FPS

        # Missiles
        self.bullets = []

        # Initialisations diverses
        pyxel.init(WIDTH, HEIGHT, fps=FPS, title="Monster Hunter")
        pyxel.load("./theme.pyxres")
        pyxel.stop()
        pyxel.playm(4, loop=True)
        pyxel.run(self.update, self.draw)

    # Methode permettant de jouer de la musique
    def sound_player_start(self):
        pyxel.playm(3, loop=True)

    # Verfie l'Etat de Jeu Initial
    def check_start(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.gamestate == 0:
            self.sound_player_start()
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.gamestate = 1
                self.sound_player_bgm()

        if self.gamestate == 1 and self.score >= 1500:
            self.gamestate = 2
            self.timer = 60 * FPS
            print("Level 2 start")

    # Methode permettant de jouer le SFX de mort
    def sound_player_death(self):
        pyxel.playm(3, loop=True)

    # Methode de gestion du mouvement du joueur
    def player_motion(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < 120:
            self.player_x += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 1:
            self.player_x -= 1

    # Methode de gestion de animations du joueur
    def animate_player_state(self):
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_LEFT):
            self.player_state = 1
        else:
            self.player_state = 0

        if self.player_state == 0:
            self.player_sprite_1 = 0
            self.player_sprite_2 = 72
        else:
            self.player_sprite_1 = 8
            self.player_sprite_2 = 72

    # Methode de gestion des tirs des joueurs
    def player_shoot(self):
        if self.gamestate in [1, 2] and pyxel.btnp(pyxel.KEY_SPACE) and self.player_charges > 0:
            self.bullets.append([self.player_x, self.player_y - 10])
            self.player_charges -= 1
            pyxel.playm(5)

    # Methode permettant la generation aleatoire de Canards
    def spawn_ducks(self):
        if random.random() < 0.05:
            row_num = random.randint(1, 5)
            if row_num == 1 and self.duck1delay == 0:
                self.ducks1.append([-5, 25])
                self.duck1delay += 25
            elif row_num == 2 and self.duck2delay == 0:
                self.ducks2.append([135, 40])
                self.duck2delay += 25
            elif row_num == 3 and self.duck3delay == 0:
                self.ducks3.append([-5, 55])
                self.duck3delay += 25
            elif row_num == 4 and self.duck4delay == 0:
                self.ducks4.append([135, 70])
                self.duck4delay += 25
            elif row_num == 5 and self.duck5delay == 0:
                self.ducks5.append([-5, 85])
                self.duck5delay += 25

    # Methode de gestion de l'Animation des Canards
    def animate_ducks(self):
        if self.timer % 3 == 0:
            self.duckstate = (self.duckstate + 1) % 4
            self.duck_sprite_x = self.duckstate * 8

    # Methode de gestion des "overlaps" (superpositions) de Canards
    def rects_overlap(self, r1, r2):
        return (
            r1[0] < r2[0] + r2[2]
            and r1[0] + r1[2] > r2[0]
            and r1[1] < r2[1] + r2[3]
            and r1[1] + r1[3] > r2[1]
        )

    # Methode de gestion des collisions entre les canards les autres entites du jeu.
    def collision_ducks(self):
        to_remove = []
        for row in self.ducks:
            for duck in row:
                duck_rect = (duck[0], duck[1], 8, 8)
                for bullet in self.bullets:
                    bullet_rect = (bullet[0], bullet[1], 8, 8)
                    if self.rects_overlap(duck_rect, bullet_rect):
                        to_remove.append((row, duck, bullet))
                        if self.gamestate == 1:
                            pyxel.playm(6)
                        if self.gamestate == 2:
                            pyxel.playm(7)
                        break

        for row, duck, bullet in to_remove:
            if duck in row:
                row.remove(duck)
            if bullet in self.bullets:
                self.bullets.remove(bullet)
            if self.gamestate == 1:
                self.score += 100
            elif self.gamestate == 2:
                self.score += 150


    # Methode de gestion du theme musical de base
    def sound_player_bgm(self):
        pyxel.playm(0, loop=True)


    # Methode Update, qui se joue constamment
    def update(self):
        if self.duck1delay > 0:
            self.duck1delay -= 1
        if self.duck2delay > 0:
            self.duck2delay -= 1
        if self.duck3delay > 0:
            self.duck3delay -= 1
        if self.duck4delay > 0:
            self.duck4delay -= 1
        if self.duck5delay > 0:
            self.duck5delay -= 1

        match self.gamestate:
            case -3:
                if pyxel.btnp(pyxel.KEY_P):
                    self.gamestate = 1
            case -1:
                if pyxel.btnp(pyxel.KEY_RETURN):
                    self.__init__()  # Reset game
            case 0:
                self.check_start()
            case 1 | 2:
                if pyxel.btnp(pyxel.KEY_P):
                    self.gamestate = -3
                if self.timer == 0 and self.score < 4000:
                    self.gamestate = -1
                    #self.sound_player_death()
                if self.timer == 0 and self.score >= 4000:
                    self.gamestate = -2
                if self.player_charges < 3 and self.timer % 60 == 0:
                    self.player_charges += 1
                self.timer -= 1
                self.player_motion()
                self.animate_player_state()
                self.player_shoot()
                self.spawn_ducks()
                self.animate_ducks()
                self.collision_ducks()
                self.check_start()

        self.player_state = 0

    # Methode Draw, qui dessine les elements par Etat de Jeu
    def draw(self):
        match self.gamestate:
            case -3: #Etat de Jeu de Pause
                pyxel.cls(0)
                pyxel.text((WIDTH // 2)-8, HEIGHT * 0.1, "Pause", 7)
            case -2: #Etat de Jeu de Victoire
                pyxel.cls(0)
                pyxel.text(WIDTH * 0.38, HEIGHT *0.1, "CONGRATS!", 7)
                pyxel.text(WIDTH*0.15, HEIGHT*0.35, f'Your final score was {self.score}', 7)
                pyxel.text((WIDTH // 2) - 22, HEIGHT * 0.5, f'Score: {self.score}/4000', 8)
                pyxel.text(20, HEIGHT - 30, "Press Enter to try again", 8)
                pyxel.text(20, HEIGHT - 20, "Press1 Q to exit the game", 8)
            case -1: #Etat de Jeu du Game Over
                #pyxel.playm(3)
                pyxel.cls(0)
                pyxel.text((WIDTH // 2) - 22, HEIGHT * 0.1, "Game Over", 7)
                pyxel.text((WIDTH // 2) - 22, HEIGHT * 0.5, f'Score: {self.score}/1500', 8)
                pyxel.text(15, HEIGHT - 30, "  Entrer               ", 3)
                pyxel.text(15, HEIGHT - 30, "-         pour recommencer", 7)
                pyxel.text(15, HEIGHT - 20, "  Q                    ", 8)
                pyxel.text(15, HEIGHT - 20, "-   pour quitter le jeu", 7)
            case 0: #Etat de Jeu de la Page d'Acceuil
                #pyxel.playm(4)
                pyxel.cls(0)
                pyxel.text((WIDTH // 2) - 22, HEIGHT * 0.1, "Monster Hunter", 7)
                pyxel.text(15, HEIGHT - 30, "  Entrer               ", 3)
                pyxel.text(15, HEIGHT - 30, "-         pour commencer", 7)
                pyxel.text(15, HEIGHT - 0, " - Espace pour tirer", 7)
                pyxel.text(15, HEIGHT - 20, "  Q                    ", 8)
                pyxel.text(15, HEIGHT - 20, "-   pour quitter le jeu", 7)
            case 1 | 2: #Etat de Jeu lors de la Partie
                #pyxel.playm(0)
                bank = 0 if self.gamestate == 1 else 1
                pyxel.bltm(0, 0, bank, 0, 0, 256, 256)
                pyxel.text(5, 5, "Timer: " + str(self.timer // FPS), 6)
                score_goal = "1500" if self.gamestate == 1 else "4000"
                pyxel.text(WIDTH - 70, 5, "Score: " + str(self.score) + "/" + score_goal, 6)
                level_text = "Niveau 1" if self.gamestate == 1 else "Niveau 2"
                pyxel.text((WIDTH // 2) - 22, HEIGHT * 0.1, level_text, 7)
                pyxel.blt(
                    self.player_x,
                    self.player_y,
                    bank,
                    self.player_sprite_1,
                    self.player_sprite_2,
                    8,
                    8,
                )
                pyxel.text(1, HEIGHT - 5, "Charges remaining: ", 7)
                for i in range(self.player_charges):
                    pyxel.text(WIDTH - 10 * (i + 1), HEIGHT - 5, "X", 7)

                for bullet in self.bullets:
                    pyxel.blt(bullet[0], bullet[1], bank, 32, 88, 8, 8)
                    bullet[1] -= 1.5 if self.gamestate == 1 else 1.85

                for row in self.ducks:
                    for duck in row:
                        duck_x, duck_y = duck
                        direction = self.ducks.index(row) % 2
                        speed = 1.25 if self.gamestate == 1 else 1.55
                        if direction == 1:
                            duck[0] -= speed
                            if self.gamestate == 2:
                                pyxel.blt(duck_x, duck_y, bank, self.duck_sprite_x, self.duck_sprite_y, -8, 8)
                            else:
                                pyxel.blt(duck_x, duck_y, bank, self.duck_sprite_x, self.duck_sprite_y, 8, 8)
                        else:
                            duck[0] += speed
                            if self.gamestate == 2:
                                pyxel.blt(duck_x, duck_y, bank, self.duck_sprite_x, self.duck_sprite_y, 8, 8)
                            else:
                                pyxel.blt(duck_x, duck_y, bank, self.duck_sprite_x, self.duck_sprite_y, -8, 8)

App()