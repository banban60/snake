import sys
import random
import pygame


class Jeu:
    def __init__(self):
        self.difficulte = ""
        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake")

        self.ecran_du_debut = True
        self.ecran_scoreboards = False
        self.jeu_en_cours = False
        self.game = True

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0
        self.serpent_corps = 10
        self.clock = pygame.time.Clock()
        self.clock_tick = 25

        self.positions_serpent = []
        self.taille_du_serpent = 1

        self.pomme_position_x = random.randrange(120, 680, 10)
        self.pomme_position_y = random.randrange(110, 580, 10)
        self.pomme_or_position_x = random.randrange(120, 680, 10)
        self.pomme_or_position_y = random.randrange(120, 580, 10)
        self.pomme = 10
        self.pomme_or_ou_pas = 100

        self.image_tete_du_serpent = pygame.image.load('Tete_du_serpent.png')

        self.image = pygame.image.load('snake-game.jpg')
        self.image_titre = pygame.transform.scale(self.image, (250, 200))

        self.score = 0

        self.boutton_facile = (60, 425, 200, 50)
        self.boutton_moyen = (300, 425, 200, 50)
        self.boutton_difficile = (540, 425, 200, 50)
        self.boutton_scoreboard = (20, 85, 220, 30)

        self.boutton_retour = (20, 85, 100, 30)

        self.boutton_recommencer = (257, 180, 285, 50)
        self.boutton_quitter = (257, 370, 285, 50)

        self.blanc = (255, 255, 255)

    def fonction_principale(self):

        while self.game:

            if self.ecran_du_debut:
                self.ecran.fill((0, 0, 0))

                self.ecran.blit(self.image_titre, (270, 25, 100, 50))
                self.creer_message('petite', "Le but du jeu est que le serpent se développe",
                                   (85, 200, 200, 5), self.blanc)
                self.creer_message('petite', "Pour cela, il a besoin de pommes, mangez-en autant que possible !",
                                   (10, 220, 200, 5), self.blanc)
                self.creer_message('grande', "Choissisez la difficulté du jeu",
                                   (160, 350, 200, 5), self.blanc)
                self.creer_boutton('immense', "Facile", self.boutton_facile, (100, 433), self.blanc,
                                   (0, 0, 0))
                self.creer_boutton('immense', "Moyen", self.boutton_moyen, (340, 433), self.blanc,
                                   (0, 0, 0))
                self.creer_boutton('immense', "Difficile", self.boutton_difficile, (565, 433), self.blanc,
                                   (0, 0, 0))

                self.creer_boutton('moyenne', "Meilleurs scores", self.boutton_scoreboard, (33, 89), self.blanc,
                                   (0, 0, 0))

                self.bouttons_debut_click()
                pygame.display.flip()

            if self.ecran_scoreboards:
                self.ecran.fill((0, 0, 0))

                self.creer_boutton('moyenne', "Retour", self.boutton_retour, (30, 89), self.blanc,
                                   (0, 0, 0))

                self.menu_scoreboards()
                self.bouttons_scoreboard_click()

                pygame.display.flip()

            if self.jeu_en_cours:

                self.serpent_mouvement()
                self.manger_pomme()

                la_tete_du_serpent = [self.serpent_position_x, self.serpent_position_y]
                self.positions_serpent.append(la_tete_du_serpent)

                if len(self.positions_serpent) > self.taille_du_serpent:
                    self.positions_serpent.pop(0)

                self.afficher_les_elements()

                self.se_mord(la_tete_du_serpent)

                if self.serpent_position_x <= 100 or self.serpent_position_x >= 700 \
                        or self.serpent_position_y <= 100 or self.serpent_position_y >= 600:
                    self.ecran_mort()

                self.clock.tick(self.clock_tick)
                pygame.display.flip()

    def serpent_mouvement(self):

        for evenement in pygame.event.get():

            self.gestion_evenements(evenement)

            if evenement.type == pygame.KEYDOWN:

                if evenement.key == pygame.K_RIGHT and not self.serpent_direction_x == -10:
                    self.serpent_direction_x = 10
                    self.serpent_direction_y = 0

                elif evenement.key == pygame.K_LEFT and not self.serpent_direction_x == 10:
                    self.serpent_direction_x = -10
                    self.serpent_direction_y = 0

                elif evenement.key == pygame.K_DOWN and not self.serpent_direction_y == -10:
                    self.serpent_direction_y = 10
                    self.serpent_direction_x = 0

                elif evenement.key == pygame.K_UP and not self.serpent_direction_y == 10:
                    self.serpent_direction_y = -10
                    self.serpent_direction_x = 0

        self.serpent_position_x += self.serpent_direction_x
        self.serpent_position_y += self.serpent_direction_y

    def afficher_les_elements(self):
        self.ecran.fill((0, 0, 0))

        self.creer_message('grande', "Snake Game", (320, 10, 100, 50), (20, 220, 20))
        self.creer_message('grande', str(self.score), (410, 50, 50, 50), (20, 220, 20))

        pygame.draw.rect(self.ecran, self.blanc, (100, 100, 600, 500), 3)

        pygame.draw.rect(self.ecran, (255, 0, 0), (self.pomme_position_x, self.pomme_position_y,
                                                   self.pomme, self.pomme))

        if self.pomme_or_ou_pas <= 15:
            pygame.draw.rect(self.ecran, (239, 229, 19), (self.pomme_or_position_x, self.pomme_or_position_y,
                                                          self.pomme, self.pomme))

        self.ecran.blit(self.image_tete_du_serpent, (self.serpent_position_x, self.serpent_position_y,
                                                     self.serpent_corps, self.serpent_corps))

        for partie_du_serpent in self.positions_serpent[:-1]:
            pygame.draw.rect(self.ecran, (0, 255, 0), (partie_du_serpent[0], partie_du_serpent[1],
                                                       self.serpent_corps, self.serpent_corps))

    def se_mord(self, tete_serpent):

        for partie_du_serpent in self.positions_serpent[:-1]:

            if tete_serpent == partie_du_serpent:
                self.ecran_mort()

    def creer_message(self, font, message, message_rectangle, couleur):

        if font == 'petite':
            font = pygame.font.SysFont('Lato', 25, False)

        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 35, False)

        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 40, True)

        elif font == 'immense':
            font = pygame.font.SysFont('Lato', 50, True)

        message = font.render(message, True, couleur)

        self.ecran.blit(message, message_rectangle)

    def creer_boutton(self, font, texte, boutton_rectangle, texte_rectangle, couleur_boutton, couleur_texte):
        pygame.draw.rect(self.ecran, couleur_boutton, boutton_rectangle)
        self.creer_message(font, texte, texte_rectangle, couleur_texte)

    def bouttons_debut_click(self):

        for evenement in pygame.event.get():

            self.gestion_evenements(evenement)

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                x, y = evenement.pos  # the x and y coordinates of the cursor position where the mouse was clicked

                if self.boutton_facile[0] <= x <= self.boutton_facile[0] + self.boutton_facile[2] \
                        and self.boutton_facile[1] <= y <= self.boutton_facile[1] + self.boutton_facile[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True

                    self.clock_tick = 15
                    self.difficulte = "Facile"

                elif self.boutton_moyen[0] <= x <= self.boutton_moyen[0] + self.boutton_moyen[2] \
                        and self.boutton_moyen[1] <= y <= self.boutton_moyen[1] + self.boutton_moyen[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True

                    self.clock_tick = 25
                    self.difficulte = "Moyen"

                elif self.boutton_difficile[0] <= x <= self.boutton_difficile[0] + self.boutton_difficile[2] \
                        and self.boutton_difficile[1] <= y <= self.boutton_difficile[1] + self.boutton_difficile[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True

                    self.clock_tick = 35
                    self.difficulte = "Difficile"

                elif self.boutton_scoreboard[0] <= x <= self.boutton_scoreboard[0] + self.boutton_scoreboard[2] \
                        and self.boutton_scoreboard[1] <= y <= self.boutton_scoreboard[1] + self.boutton_scoreboard[3]:

                    self.ecran_du_debut = False
                    self.ecran_scoreboards = True

    @staticmethod
    def gestion_evenements(evenement):

        if evenement.type == pygame.QUIT:
            sys.exit()

    def manger_pomme(self):

        if self.pomme_or_position_y == self.serpent_position_y and self.pomme_or_position_x == self.serpent_position_x \
                and self.pomme_or_ou_pas <= 15:
            self.pomme_or_ou_pas = 100
            self.pomme_or_position_x = random.randrange(120, 680, 10)
            self.pomme_or_position_y = random.randrange(120, 580, 10)

            self.taille_du_serpent += 2
            self.score += 2

        if self.pomme_position_y == self.serpent_position_y and self.pomme_position_x == self.serpent_position_x:
            self.pomme_or_ou_pas = random.randrange(0, 100, 1)
            print(self.pomme_or_ou_pas)

            self.pomme_position_x = random.randrange(120, 680, 10)
            self.pomme_position_y = random.randrange(120, 580, 10)

            self.taille_du_serpent += 1
            self.score += 1

    def recommencer(self):
        self.enregistrer_score()

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0

        self.positions_serpent = []
        self.taille_du_serpent = 0
        self.score = 0

        self.jeu_en_cours = False
        self.ecran_du_debut = True

    def ecran_mort(self):

        while self.jeu_en_cours:
            self.ecran.fill((0, 0, 0))
            self.creer_boutton('immense', "Recommencer", (257, 180, 285, 50), (263, 188, 200, 50), (20, 150, 20),
                               (0, 0, 0))
            self.creer_boutton('immense', "Quitter", (257, 370, 285, 50), (325, 378, 200, 50), (20, 150, 20),
                               (0, 0, 0))
            self.bouton_mort_click()
            pygame.display.flip()

    def bouton_mort_click(self):

        for evenement in pygame.event.get():
            self.gestion_evenements(evenement)

            if evenement.type == pygame.MOUSEBUTTONDOWN:

                x, y = evenement.pos

                if self.boutton_recommencer[0] <= x <= self.boutton_recommencer[0] + self.boutton_recommencer[2] \
                        and self.boutton_recommencer[1] <= y <= \
                        self.boutton_recommencer[1] + self.boutton_recommencer[3]:

                    self.recommencer()

                elif self.boutton_quitter[0] <= x <= self.boutton_quitter[0] + self.boutton_quitter[2] \
                        and self.boutton_quitter[1] <= y <= self.boutton_quitter[1] + self.boutton_quitter[3]:
                    self.enregistrer_score()
                    sys.exit()

    def enregistrer_score(self):

        with open("Scores{}.txt".format(self.difficulte), "a+") as file:
            file.write(str(self.score) + "\n")
            file.close()

    def menu_scoreboards(self):

        def scoreboard(difficulte, cases_gauche, cases_centre, nombres_gauche, scores_position):

            with open("Scores{}.txt".format(difficulte), "r+") as file:
                scores_liste = file.readlines()
                scores_liste = [int(score.strip()) for score in scores_liste]
                scores_liste.sort()
                scores_liste.reverse()
                del scores_liste[10:]
                file.close()

            if difficulte == "Facile":
                self.creer_message('petite', str(difficulte), (cases_centre[0] + 43, cases_centre[1] + 1), self.blanc)

            elif difficulte == "Moyen":
                self.creer_message('petite', str(difficulte), (cases_centre[0] + 41, cases_centre[1] + 1), self.blanc)

            elif difficulte == "Difficile":
                self.creer_message('petite', str(difficulte), (cases_centre[0] + 35, cases_centre[1] + 1), self.blanc)

            nombre_cases = 0

            while nombre_cases <= 10:
                pygame.draw.rect(self.ecran, self.blanc, cases_gauche, 2, 5)
                pygame.draw.rect(self.ecran, self.blanc, cases_centre, 2, 5)

                if nombre_cases == 10:
                    self.creer_message('petite', str(nombre_cases), (cases_gauche[0], cases_gauche[1] + 2,
                                                                     cases_gauche[2], cases_gauche[3]), self.blanc)

                elif nombre_cases == 0:
                    pass

                else:
                    self.creer_message('petite', str(nombre_cases), nombres_gauche, self.blanc)

                nombre_cases += 1
                cases_gauche[1] += cases_gauche[3]
                cases_centre[1] += cases_centre[3]
                nombres_gauche[1] += nombres_gauche[3]

            for score in scores_liste:
                self.creer_message('petite', str(score), scores_position, self.blanc)
                scores_position[1] += 20

        scoreboard("Facile", [110, 50, 20, 20], [110, 50, 120, 20], [115, 52, 20, 20], [168, 72])
        scoreboard("Moyen", [340, 50, 20, 20], [340, 50, 120, 20], [345, 52, 20, 20], [398, 72])
        scoreboard("Difficile", [570, 50, 20, 20], [570, 50, 120, 20], [575, 52, 20, 20], [628, 72])

    def bouttons_scoreboard_click(self):
        for evenement in pygame.event.get():
            self.gestion_evenements(evenement)


if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()
