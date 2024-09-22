import pyxel
from random import  randint
from PIL import Image
from playsound import playsound


class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Sniper Wish")
        pyxel.load("Music.pyxres")


        #new
        self.col_liste = [(0, 0, 0),
                          (43, 51, 91),
                          (126, 32, 114),
                          (25, 149, 156),
                          (139, 72, 82),
                          (52, 92, 152),
                          (169, 193, 255),
                          (238, 238, 238),
                          (212, 24, 108),
                          (211, 132, 65),
                          (233, 195, 91),
                          (112, 198, 169),
                          (118, 150, 222),
                          (163, 163, 163),
                          (255, 151, 152),
                          (237, 199, 176)]
        self.game = 0
        self.image = []
        self.back = []
        self.enemi = []
        self.img = [Image.open('Image/dragunov2.png'), Image.open('Image/scope.png'),
                    Image.open('Image/back_1.png'), Image.open('Image/back_2.png'),
                    Image.open('Image/enemy.png'), Image.open('Image/enemy2.png'),
                    Image.open('Image/dragunov3.png'), Image.open('Image/back.png')]

        self.co_im = [[55, 65], [0, 0],
                      [0, 0], [57, 59], [0, 15]]

        self.rgb_img = [self.img[0].convert('RGB'), self.img[1].convert('RGB'),
                        self.img[2].convert('RGB'), self.img[3].convert('RGB'),
                        self.img[4].convert('RGB'), self.img[5].convert('RGB'),
                        self.img[6].convert('RGB'), self.img[7].convert('RGB')]

        self.cool_down = 10
        self.mouse_co = [pyxel.mouse_x, pyxel.mouse_y]
        self.ammo = 15
        self.nb_enemi = 5
        self.position = [[(64, 72), (96, 104), True], [(48, 56), (48, 56), True],
                         [(104, 112), (80, 88), True], [(96, 104), (24, 32), True],
                         [(16, 24), (112, 120), True]]
        self.cd_end = 0
        self.was = True
        self.start_music = True
        self.scope = False
        self.aim = False
        self.victory = False
        self.defeat = False


        pyxel.run(self.update, self.draw)

    def aim_on_off(self):


        if self.scope:
            self.scope = False
            playsound('Son/scope.mp3')

        if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and self.cool_down == 10:

            if self.aim:
                self.image.clear()
                self.enemi.clear()
                self.back.clear()
                self.Image_load_back(0, 0, 128, 128, self.rgb_img[2], self.co_im[2])
                self.Image_load(self.img[0], self.rgb_img[0], self.co_im[0])
                self.aim = False
                self.cool_down = 0
            else:
                self.back.clear()


                taille_case = 8
                multiple = 128//taille_case
                ecx = self.encadre(self.mouse_co[0], taille_case)
                ecy = self.encadre(self.mouse_co[1], taille_case)
                self.Image_load_back(ecx[0]*multiple, ecy[0]*multiple, ecx[1]*multiple, ecy[1]*multiple,
                                     self.rgb_img[3], [-ecx[0]*multiple, -ecy[0]*multiple])

                self.image.clear()

                self.Image_load(self.img[1], self.rgb_img[1], self.co_im[1])
                self.scope = True
                self.aim = True
                self.cool_down = 0
                self.enemi.clear()
                for i1 in range(len(self.position)):
                    self.enemy(i1)

    def shoot(self):
        if self.aim and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.ammo > 0:
            self.ammo -= 1
            for i, e in enumerate(self.position):
                if type(e) != type(True) and self.encadre(self.mouse_co[0], 8) == e[0] and self.encadre(self.mouse_co[1], 8) == e[1] and self.position[i][2]:
                    self.position[i][2] = False
                    self.enemi.clear()
                    for i1 in range(len(self.position)):
                        self.enemy(i1)
                    self.nb_enemi -= 1

            playsound('Son/shoot.mp3')

    def enemy(self, i):

        if self.aim and self.encadre(self.mouse_co[0], 8) == self.position[i][0] and self.encadre(self.mouse_co[1], 8) == self.position[i][1]:

            if self.position[i][2]:
                self.Image_load_enemi(self.img[4], self.rgb_img[4], self.co_im[3])
            else:
                self.Image_load_enemi(self.img[5], self.rgb_img[5], self.co_im[3])





    def encadre(self, x, t):
        a = x // t
        return (a * t, a * t + t)

    def Image_load_enemi(self, img, rgb_img, co):
        if self.enemi == []:
            for iy in range(img.height):
                for ix in range(img.width):
                    rgb = rgb_img.getpixel((ix, iy))
                    if rgb != (0, 255, 0):
                        mini = [(elt[0] - rgb[0], elt[1] - rgb[1], elt[2] - rgb[2]) for elt in self.col_liste]
                        for i, coul in enumerate(mini):
                            coul = [e if e > 0 else e * -1 for e in coul]
                            mini[i] = sum(coul)
                        vmin = min(mini)

                        self.enemi.append((co[0], co[1], ix, iy, mini.index(vmin)))

    def Image_load(self, img, rgb_img, co):
        if self.image == []:
            for iy in range(img.height):
                for ix in range(img.width):
                    rgb = rgb_img.getpixel((ix, iy))
                    if rgb != (0, 255, 0):
                        mini = [(elt[0] - rgb[0], elt[1] - rgb[1], elt[2] - rgb[2]) for elt in self.col_liste]
                        for i, coul in enumerate(mini):
                            coul = [e if e > 0 else e * -1 for e in coul]
                            mini[i] = sum(coul)
                        vmin = min(mini)

                        self.image.append((co[0], co[1], ix, iy, mini.index(vmin)))

    def Image_load_back(self, sx, sy, ex, ey, rgb_img, co):
        if self.back == []:

            for iy in range(sy, ey):
                for ix in range(sx, ex):
                    rgb = rgb_img.getpixel((ix, iy))
                    if rgb != (0, 255, 0):
                        mini = [(elt[0] - rgb[0], elt[1] - rgb[1], elt[2] - rgb[2]) for elt in self.col_liste]
                        for i, coul in enumerate(mini):
                            coul = [e if e > 0 else e * -1 for e in coul]
                            mini[i] = sum(coul)
                        vmin = min(mini)

                        self.back.append((co[0], co[1], ix, iy, mini.index(vmin)))

    def menu(self):
        if self.mouse_co[1] > 70 and self.mouse_co[1] > 90 and\
            self.mouse_co[1] < 110 and self.mouse_co[0] > 30 and\
                self.mouse_co[0] < 100 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):

            self.image.clear()
            self.back.clear()
            self.game = 1

    def music(self):
        pyxel.playm(0, 1, True)
        self.start_music = False

    def win(self):

        if pyxel.btn(pyxel.KEY_SPACE):
            self.ammo = 0

        if self.nb_enemi == 0:
            if self.cd_end == 250:
                self.cd_end = 0

                self.victory = False
                self.image.clear()
                self.back.clear()
                self.ammo = 15
                self.nb_enemi = 5
                self.game = 0
                return

            self.cd_end += 1
            self.victory = True

        if self.ammo == 0 and self.nb_enemi != 0 and not self.victory:
            if self.cd_end == 250:
                self.cd_end = 0
                self.defeat = False

                self.image.clear()
                self.back.clear()
                self.ammo = 15
                self.nb_enemi = 5
                self.game = 0
                return

            self.cd_end += 1
            self.defeat = True












    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""
        if self.start_music:
            self.music()
        if self.game == 1:
            self.was = True
            self.win()
            pyxel.mouse(False)
            if not self.aim:
                self.Image_load(self.img[0], self.rgb_img[0], self.co_im[0])
                self.mouse_co = [pyxel.mouse_x, pyxel.mouse_y]
            if self.cool_down < 10:
                self.cool_down += 1
            self.Image_load_back(0, 0, 128, 128, self.rgb_img[2], self.co_im[2])
            self.shoot()
            #print(self.mouse_co)
            self.aim_on_off()

        elif self.game == 0:
            if self.was:
                self.enemi.clear()
                self.image.clear()
                for i in range(len(self.position)):
                    self.position[i][2] = True
                self.was = False
            pyxel.mouse(True)
            self.mouse_co = [pyxel.mouse_x, pyxel.mouse_y]
            self.Image_load(self.img[6], self.rgb_img[6], self.co_im[4])
            self.Image_load_back(0, 0, 128, 128, self.rgb_img[7], self.co_im[1])
            self.menu()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
        if self.game  == 1:
            for pi in self.back:
                pyxel.rect(pi[0] + pi[2], pi[1] + pi[3], 1, 1, pi[4])

            for pi in self.enemi:
                pyxel.rect(pi[0] + pi[2], pi[1] + pi[3], 1, 1, pi[4])


            for pi in self.image:
                pyxel.rect(pi[0] + pi[2], pi[1] + pi[3], 1, 1, pi[4])

            if self.enemi != []:
                pyxel.text(25, 15, '/!\ Enemy Detected', 8)

            if self.nb_enemi >= 0 and not self.aim:
                pyxel.text(5, 5, 'Remain enemy', 7)
                pyxel.text(60, 5, str(str(self.nb_enemi)), 8)
                pyxel.text(65, 5, '/5', 7)

            pyxel.text(5, 120, str(self.ammo), 7)
            pyxel.text(15, 120, '/15', 7)




            if not self.aim:
                pyxel.line(75, 100, self.mouse_co[0], self.mouse_co[1], 8)

            if self.victory:
                pyxel.text(30, 50, 'Mission Complete,', 11)
                pyxel.text(30, 55, 'Good Job.', 11)

            if self.defeat:
                pyxel.text(20, 50, 'Mission Fail,', 8)
                pyxel.text(20, 55, 'we ll get em next time.', 8)


        elif self.game == 0:
            """for pi in self.back:
                pyxel.rect(pi[0] + pi[2], pi[1] + pi[3], 1, 1, pi[4])"""

            for pi in self.image:
                pyxel.rect(pi[0] + pi[2], pi[1] + pi[3], 1, 1, pi[4])

            pyxel.elli(30, 3, 70, 12, 13)
            pyxel.text(43, 6, 'Sniper Wish', 8)
            pyxel.elli(24, 90, 80, 17, 8)
            pyxel.elli(29, 91, 70, 15, 13)
            pyxel.text(58, 95, 'PLAY', 7)
            pyxel.rect(18, 98, 30, 2, 8)
            pyxel.rect(82, 98, 30, 2, 8)
            pyxel.rect(64, 79, 2, 15, 8)
            pyxel.rect(64, 103, 2, 15, 8)


Jeu()