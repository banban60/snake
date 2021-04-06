import sys
import random
import pygame


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeu Snake")
        self.jeu_en_cours = True
        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0
        self.serpent_corps = 10
        self.clock = pygame.time.Clock()

        self.positions_serpent = []
        self.taille_du_serpent = 1

        self.pomme_position_x = random.randrange(110, 690, 10)
        self.pomme_position_y = random.randrange(110, 590, 10)
        self.pomme = 10

        self.ecran_du_debut = True

        self.image_tete_du_serpent = pygame.image.load('Tete_du_serpent.png')

        self.image = pygame.image.load('snake-game.jpg')
        self.image_titre = pygame.transform.scale(self.image, (200, 100))

        self.score = 0

    def fonction_principale(self):

        while self.ecran_du_debut:

            for evenement in pygame.event.get():

                if evenement.type == pygame.QUIT:
                    sys.exit()

                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RETURN:

                        self.ecran_du_debut = False

                self.ecran.fill((0, 0, 0))

                self.ecran.blit(self.image_titre, (300, 50, 100, 50))
                self.creer_message('petite', "Le but du jeu est que le serpent se développe",
                                   (250, 200, 200, 5), (240, 240, 240))
                self.creer_message('petite', "Pour cela, il a besoin de pommes, mangez-en autant que possible !",
                                   (190, 220, 200, 5), (240, 240, 240))
                self.creer_message('moyenne', "Appuyer sur Enter pour commencer",
                                   (200, 450, 200, 5), (255, 255, 255))

                pygame.display.flip()

        while self.jeu_en_cours:

            for evenement in pygame.event.get():

                if evenement.type == pygame.QUIT:
                    sys.exit()

                if evenement.type == pygame.KEYDOWN:

                    if evenement.key == pygame.K_RIGHT:
                        self.serpent_direction_x = 10
                        self.serpent_direction_y = 0

                    if evenement.key == pygame.K_LEFT:
                        self.serpent_direction_x = -10
                        self.serpent_direction_y = 0

                    if evenement.key == pygame.K_DOWN:
                        self.serpent_direction_y = 10
                        self.serpent_direction_x = 0

                    if evenement.key == pygame.K_UP:
                        self.serpent_direction_y = -10
                        self.serpent_direction_x = 0

            if self.serpent_position_x <= 100 or self.serpent_position_x >= 700 \
                    or self.serpent_position_y <= 100 or self.serpent_position_y >= 600:
                sys.exit()

            self.serpent_mouvement()

            if self.pomme_position_y == self.serpent_position_y and self.pomme_position_x == self.serpent_position_x:

                print("ok")
                self.pomme_position_x = random.randrange(110, 690, 10)
                self.pomme_position_y = random.randrange(110, 590, 10)
                self.taille_du_serpent += 1

                self.score += 1

            la_tete_du_serpent = [self.serpent_position_x, self.serpent_position_y]

            self.positions_serpent.append(la_tete_du_serpent)

            if len(self.positions_serpent) > self.taille_du_serpent:

                self.positions_serpent.pop(0)
                print(self.positions_serpent)

            self.afficher_les_elements()
            self.se_mord(la_tete_du_serpent)

            self.creer_message('grande', "Snake Game", (320, 10, 100, 50), (20, 220, 20))
            self.creer_message('grande', str(self.score), (410, 50, 50, 50), (20, 220, 20))

            self.creer_limite()
            self.clock.tick(25)

            pygame.display.flip()

    def creer_limite(self):

        pygame.draw.rect(self.ecran, (255, 255, 255), (100, 100, 600, 500), 3)

    def serpent_mouvement(self):
        self.serpent_position_x += self.serpent_direction_x
        self.serpent_position_y += self.serpent_direction_y
        # print(self.serpent_position_x, self.serpent_position_y)

    def afficher_les_elements(self):
        self.ecran.fill((0, 0, 0))

        self.ecran.blit(self.image_tete_du_serpent, (self.serpent_position_x, self.serpent_position_y,
                                                     self.serpent_corps, self.serpent_corps))

        pygame.draw.rect(self.ecran, (255, 0, 0), (self.pomme_position_x, self.pomme_position_y,
                                                   self.pomme, self.pomme))

        for partie_du_serpent in self.positions_serpent[:-1]:
            pygame.draw.rect(self.ecran, (0, 255, 0), (partie_du_serpent[0], partie_du_serpent[1],
                                                       self.serpent_corps, self.serpent_corps))

    def se_mord(self, tete_serpent):

        for partie_du_serpent in self.positions_serpent[:-1]:

            if tete_serpent == partie_du_serpent:
                sys.exit()

    def creer_message(self, font, message, message_rectangle, couleur):

        if font == 'petite':
            font = pygame.font.SysFont('Lato', 20, False)

        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 30, False)

        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 40, True)

        message = font.render(message, True, couleur)

        self.ecran.blit(message, message_rectangle)


if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()