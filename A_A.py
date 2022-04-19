# Peli on kohtuullisen haastava.
#
# Pääkohdiltaan pitäisi pelittää, mutta jotain pieniä bugeja saattoi jäädä suoritukseen.
# Sen verran kuitenkin sain bugeja ja kaatuiluja karsittua, 
# että omissa testeissä en saanut enempää kiinni.
#
# En saanut toistettua tilannetta tarpeeksi saadakseni varmuutta,
# mutta voi olla, että tietyissä olosuhteissa pelaajan ammus jää osuman jälkeen näkymättömänä
# paikoilleen, ja samaan kohtaan saapunut uusi vihollinen ottaa tästä vielä kertaalleen osuman.
# 
# Koodista tuli kenties luvattoman pitkä kaikkine if-haaroineen, ja paisui kun yhden ominaisuuden jälkeen
# täytyi aina lisätä toinen. Lisäksi, kuvien sijasta käytin pygamen piirtoa. Yritin helpottaa luettavuutta 
# lisäämällä kommentteja rivien väliin otsikoiksi.
#  
# Pääkohdiltaan peli on periaatteessa koettu jo noin 300 pisteessä. Siitä eespäin vaikeusaste lisääntyy vaiheittain.
# Vihollisesta tulee kestävämpi, asteroideja tulee useammin jne.
#
# Työmääräksi arvioisin kokonaisuudessaan 15 - 20 h.  
# 


import pygame, random

pygame.init()
vihollinen = pygame.sprite.Group()
asteroidi = pygame.sprite.Group()
ammukset =  pygame.sprite.Group()
vihollisen_ammukset = pygame.sprite.Group()
pelaaja = pygame.sprite.Group()

class Peli:
    def __init__(self):
        self.leveys = 600
        self.korkeus = 700
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.kello = pygame.time.Clock()

        self.tausta = Tausta(self.naytto, self.leveys, self.korkeus)
        self.player = Pelaaja(self.naytto, self.leveys, self.korkeus)
        self.vihut = Viholliset(self.naytto, self.leveys, self.korkeus)
        
        self.fontti = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("AvaruusAmmunta")

        self.game_over = False
        self.start = True
        self.paused = False
        self.silmukka()
        
    #SUORITUSLUUPPI
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.suorita()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            self.napit(tapahtuma)
            
    def napit(self, tapahtuma):
        if not self.start:
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.player.oikealle = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.player.vasemmalle = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.player.taakse = True
                if tapahtuma.key == pygame.K_UP:
                    self.player.eteen  = True
                if tapahtuma.key == pygame.K_SPACE:
                    self.player.ammu()
                if tapahtuma.key == pygame.K_ESCAPE and not self.game_over:
                    if self.paused == True:
                        self.paused = False
                    else:
                        self.paused = True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.player.oikealle = False
                if tapahtuma.key == pygame.K_LEFT:
                    self.player.vasemmalle = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.player.taakse = False
                if tapahtuma.key == pygame.K_UP:
                    self.player.eteen  = False

        if tapahtuma.type == pygame.KEYDOWN and self.game_over:
            if tapahtuma.key == pygame.K_y:
                Peli()
            if tapahtuma.key == pygame.K_n:
                exit()
        if tapahtuma.type == pygame.KEYDOWN and self.start and tapahtuma.key != pygame.K_ESCAPE:
            self.start = False
    #PÄÄOHJELMA   
    def suorita(self):

        #TAUSTA LIIKKUU TILANTEESTA RIIPPUMATTA
        self.naytto.fill((0,0,0))
        self.tausta.piirra()

        #PAUSSI/ESC
        if self.paused:
            self.pause()
            pygame.display.flip()
            self.kello.tick(60)
            return

        #ALOITUS / OHJEET, pääpelin toiminta valikon "alla"
        if self.start:
            self.valikko()

        #"ALOITUSANIMAATIO"
        elif not self.start and self.player.aloitus:
            self.player.animaatio()
            self.HUD()

        #PELIN TOIMINNALLINEN OSUUS    
        else:
            #JOS TAPPIO NIIN GAME OVER JA JOS EI TAPPIO NIIN PELAAJA VOI LIIKKUA
            if not self.game_over:
                self.player.pelaa()
                if self.player.tappio:
                    self.game_over = True
            self.vihut.invaasio(self.player)
            self.HUD()
            if self.game_over:
                self.gameover()
        
        pygame.display.flip()
        self.kello.tick(60)
    #PAUSSITEKSTI
    def pause(self):
        teksti = self.fontti.render(f"PAUSED", True, (0, 0, 250))
        self.naytto.blit(teksti, (self.leveys/2-teksti.get_width()/2, self.korkeus/4-20))
    #GAMEOVER, TEKSTI JA PELIKENTÄN TYHJENNYS        
    def gameover(self):
        ammukset.empty()
        vihollisen_ammukset.empty()
        vihollinen.empty()
        asteroidi.empty()
        pelaaja.empty()

        vari = (0,0,250)
        teksti = self.fontti.render(f"Your score: {self.player.pisteet}", True, vari)
        teksti1 = self.fontti.render(f"***GAME OVER***", True, vari)
        teksti2 = self.fontti.render("RESTART?", True, vari)
        teksti3 = self.fontti.render(f"Y / N", True, vari)
        self.naytto.blit(teksti, (self.leveys/2-teksti.get_width()/2, self.korkeus/3))
        self.naytto.blit(teksti1, (self.leveys/2-teksti1.get_width()/2, self.korkeus/3+60))
        self.naytto.blit(teksti2, (self.leveys/2-teksti2.get_width()/2, self.korkeus/3+100))
        self.naytto.blit(teksti3, (self.leveys/2-teksti3.get_width()/2, self.korkeus/3+140))

    #ALKUNÄYTTÖ
    def valikko(self):
        vari = (0,0,250)
        teksti = self.fontti.render("Instructions:", True, vari)
        teksti1 = self.fontti.render("Don't get hit by anything blue", True, vari)
        teksti2 = self.fontti.render("Shoot enemies to gain points", True, vari)
        teksti3 = self.fontti.render("MOVE: Arrow keys", True, vari)
        teksti4 = self.fontti.render("SHOOT: Space" , True, vari)
        teksti5 = self.fontti.render("PAUSE: Esc" , True, vari)
        teksti6 = self.fontti.render("Press any button to start the game" , True, vari)
        self.naytto.blit(teksti, (self.leveys/2-teksti.get_width()/2, self.korkeus/4))
        self.naytto.blit(teksti1, (self.leveys/2-teksti1.get_width()/2, self.korkeus/4+40))
        self.naytto.blit(teksti2, (self.leveys/2-teksti2.get_width()/2, self.korkeus/4+80))
        self.naytto.blit(teksti3, (self.leveys/2-teksti3.get_width()/2, self.korkeus/4+140))
        self.naytto.blit(teksti4, (self.leveys/2-teksti4.get_width()/2, self.korkeus/4+180))
        self.naytto.blit(teksti5, (self.leveys/2-teksti5.get_width()/2, self.korkeus/4+220))
        self.naytto.blit(teksti6, (self.leveys/2-teksti6.get_width()/2, self.korkeus/4+260))

    #TIEDOT PELIN AIKANA
    def HUD(self):
        fontti = pygame.font.SysFont("Arial", 20)
        vari = (75,75,255)
        o = "o "
        tikku = "|"

        teksti = fontti.render(f"Health: {o*self.player.hp}", True, vari)
        teksti2 = fontti.render(f"Weapons: {tikku*(int(self.player.heat/10)):9}|", True, vari)
        if self.player.overheated:
            teksti2 = fontti.render(f"Weapons: **OVERHEATED**", True, vari)
        teksti3 = fontti.render(f"Score: {self.player.pisteet}", True, vari)

        self.naytto.blit(teksti2, (5,self.korkeus-70))
        self.naytto.blit(teksti, (5,self.korkeus-40))
        self.naytto.blit(teksti3, (5,10))

            
#RULLAAVA TAUSTAKUVA
class Tausta:
    def __init__(self, naytto, leveys, korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.naytto = naytto
        self.tahdet1 = []
        self.tahdet2 = []
        self.tausta = []
        self.planeetat = []

    def piirra(self):
        #TAUSTASUMU
        self.liuku()
        #TÄYTTÄÄ LISTAT JOIHIN LIIKKUVAT OSAT TALLENNETTU, RANDINT ARPOO LISÄTÄÄNKÖ VAI EI
        if random.randint(1, 50) == 1:
            self.tahdet1.append([random.randint(-1, self.leveys+1), -10])
            if random.randint(1, 2) == 1:
                self.tahdet2.append([random.randint(-1, self.leveys+1), -10])
        if random.randint(1,85) == 1:
            if len(self.planeetat) < 1:
                self.planeetat.append([random.randint(-180, self.leveys+180), -170, random.randint(100,200)])
        #PIENET TÄHDET
        for tahti in self.tahdet2:
            pygame.draw.line(self.naytto, (160, 160, 165), (tahti[0], tahti[1]), (tahti[0], tahti[1]), 2)
            tahti[1] += 0.4
            if tahti[1] > self.korkeus:
                del self.tahdet2[0]
        #PLANEETAT
        for planeetta in self.planeetat:
            planeetta_i = 1
            for n in range(15, 25):
                pygame.draw.circle(self.naytto, (0, 0, n), (planeetta[0]+n*1.9, planeetta[1]-n*1.9), planeetta[2]/planeetta_i)
                planeetta_i += 1
            planeetta[1] += 0.25
            if planeetta[1] > self.korkeus+200:
                del self.planeetat[0]
        #ROJUA LENTÄÄ
        for tahti in self.tahdet1:
            pygame.draw.line(self.naytto, (220, 220, 225), (tahti[0], tahti[1]), (tahti[0], tahti[1]+1), 2)
            tahti[1] += 2.5
            if tahti[1] > self.korkeus:
                del self.tahdet1[0]

    def liuku(self):
        #TYHJÄ LISTA
        if len(self.tausta) <= 0:
            self.tausta.append([0, -2])
        #TAUSTAN VÄRIN MUUTOS (kirkastuuko vaiko himmeneekö)
        if self.tausta[-1][0] >= 35:
            self.vaihda_vari = True
        elif self.tausta[-1][0] <= 0:
            self.vaihda_vari = False
        #LISÄÄ PIIRRETTÄVÄ RIVI
        if self.vaihda_vari == True:
            self.tausta.append([self.tausta[-1][0]-0.025, -2])
        else:
            self.tausta.append([self.tausta[-1][0]+0.025, -2])
        #PIIRRÄ RIVI
        for rivi in self.tausta:
            pygame.draw.rect(self.naytto, (0, 0, rivi[0]), (0, rivi[1], self.leveys, 1))
            rivi[1] += 0.5
            if rivi[1] > self.korkeus:
                del self.tausta[0]
                
class Pelaaja(pygame.sprite.Sprite):
    def __init__(self, naytto, leveys, korkeus):
        pygame.sprite.Sprite.__init__(self, pelaaja)
        self.naytto = naytto
        self.x = leveys*0.5
        self.y = korkeus+30
        self.leveys = leveys
        self.korkeus = korkeus
        self.tappio = False
        self.ammukset = []

        self.hp = 3
        self.heat = 0
        self.overheated = False

        self.oikealle = False
        self.vasemmalle =False
        self.eteen = False
        self.taakse = False
        self.vauhti = 5
        self.vauhti_eteen = 2
        self.rect = pygame.draw.polygon(self.naytto, (75,75,255), [(self.x-7, self.y), (self.x-3, self.y-10), (self.x, self.y-30), (self.x+3, self.y-10), (self.x+7, self.y), (self.x, self.y +5)], 3)

        self.aloitus = True
        self.pisteet = 0
        self.matka = 0

    #PISTEET KERTYVÄT HILJALLEEN EDETESSÄ
    def matkamittari(self):
        self.matka += 0.1
        if self.matka >= 7:
            self.pisteet += 1
            self.matka = 0

    #PELAAJAN ALUS LENTÄÄ KENTTÄÄN
    def animaatio(self):
        if self.y <= self.korkeus*0.80:
            self.aloitus = False
        if self.aloitus:
            self.rect = pygame.draw.polygon(self.naytto, (75,75,255), [(self.x-7, self.y), (self.x-3, self.y-10), (self.x, self.y-30), (self.x+3, self.y-10), (self.x+7, self.y), (self.x, self.y +5)], 3)
            self.y -= self.vauhti_eteen

    #SUORITTAVA OSA
    def pelaa(self):
        #LIIKU
        if self.oikealle and self.x+10 < self.leveys:
            self.x += self.vauhti
        if self.vasemmalle and self.x > 10:
            self.x -= self.vauhti
        if self.taakse and self.y < self.korkeus:
            self.y += self.vauhti
        if self.eteen and self.y > self.korkeus*0.60:
            self.y -= self.vauhti_eteen

        #PELAAJAN AMMUKSET LIIKKUU
        for ammus in self.ammukset:
            ammus.laser()
            #AMMUS OSUU VIHOLLISEEN
            if pygame.sprite.spritecollide(ammus, vihollinen, False):
                self.ammukset.remove(ammus)
            #TAI ASTEROIDIIN (ei vaikutusta, ammus katoaa)
            if pygame.sprite.spritecollide(ammus, asteroidi, None):
                ammus.kill()
                if ammus in self.ammukset:
                     self.ammukset.remove(ammus)
                
            #KENTÄN YLITYS
            if ammus.y <= 0:
                ammus.kill()
                self.ammukset.remove(ammus)

        #PELAAJA OSUU VIHOLLISEEN TAI ASTEROIDIIN
        if pygame.sprite.spritecollide(self, vihollinen, True) or pygame.sprite.spritecollide(self, asteroidi, True):
            self.hp = 0

        #TAPPIO
        if self.hp <= 0:
            self.kill()
            self.tappio = True

        #PIIRRÄ(JOS HP YLI 0)
        if self.hp > 0:
            self.rect = pygame.draw.polygon(self.naytto, (75,75,255), [(self.x-7, self.y), (self.x-3, self.y-10), (self.x, self.y-30), (self.x+3, self.y-10), (self.x+7, self.y), (self.x, self.y +5)], 3)
        
        #OSUMAN MERKKI
        if pygame.sprite.spritecollide(self, vihollisen_ammukset, True):
            self.hp -= 1
            pygame.draw.polygon(self.naytto, (250,0,0), [(self.x-7, self.y), (self.x-3, self.y-10), (self.x, self.y-30), (self.x+3, self.y-10), (self.x+7, self.y), (self.x, self.y +5)], 3)

        #ASEET JÄÄHTYY JA KUUMUU
        self.overheat()
        if self.heat > 0:
            self.heat -= 0.75
        
        #PISTEITÄ KERÄÄNTYY EDETESSÄ
        self.matkamittari()

    def ammu(self):
        if not self.overheated and not self.aloitus:
            self.ammukset.append(Ammus(self.naytto, self.x, self.y, (150,150,255), -1))
            if self.heat <= 100:
                self.heat += 20
                
    #ASEET "KUUMUVAT", EI VOI AMPUA LIIKAA SARJAA
    def overheat(self):
        if self.heat >= 100:
            self.overheated = True
        if self.heat <= 0:
            self.overheated = False

#PELAAJAN AMMUKSET       
class Ammus(pygame.sprite.Sprite):
    def __init__(self, naytto, x, y, vari, suunta):
        pygame.sprite.Sprite.__init__(self, ammukset)
        self.x = x
        self.y = y
        self.vari = vari
        self.suunta = suunta
        self.nopeus = 6 * self.suunta
        self.rect = pygame.draw.line(naytto, self.vari, (self.x, self.y-19), (self.x, self.y-25), 3)
        self.naytto = naytto
        
    def laser(self):
        self.rect = pygame.draw.line(self.naytto, self.vari, (self.x, self.y-19), (self.x, self.y-25), 3)
        self.y += self.nopeus

#LUOKKA JONKA ALLE KAIKKI VIHOLLISET KOOTTUNA + LIIKE
class Viholliset():
    def __init__(self,naytto, leveys, korkeus):
        self.naytto = naytto
        self.leveys = leveys
        self.korkeus = korkeus
        #PERUSVIHOLLISET NIIDEN PAUKUT
        self.viholliset = []
        self.ohjukset = []
        #POMON JA SEN PAUKUT
        self.sarjatuli = []
        self.pomot = []
        #KÄRPÄNEN JA SEN LASERIT
        self.karpaset = []
        self.laser = []
        #ASTEROIDIT
        self.asteroidit = []
        #LASKURI VIHOLLISIA VARTEN (kasvaa aina uuden vihollisen tultua kentälle)
        self.laskuri = 0
        

    def luo_viholliset(self, kohde):
        #UUSI VIHOLLINEN KENTÄLLE
        if len(self.viholliset) < 1:
            #JOS PISTEITÄ YLI RAJAN PERUSVIHOLLINEN KESTÄVEMPI
            if kohde.pisteet < 500:
                self.viholliset.append(Vihollinen(self.naytto, self.leveys, self.korkeus, self.ohjukset, 2))
            else:
                self.viholliset.append(Vihollinen(self.naytto, self.leveys, self.korkeus, self.ohjukset, 3))

            #LASKURI EI ETENE JOS KENTÄLLÄ POMO / KÄRPÄNEN
            if len(self.pomot) <= 0 and len(self.karpaset) <= 0:
                # JOS YLI 500 PISTETTÄ, LASKURI KIIHTYY
                if kohde.pisteet < 500:
                    self.laskuri += 1
                else:
                    self.laskuri += 2

        #KÄRPÄNEN KENTÄLLE
        if kohde.pisteet < 800:
            if self.laskuri == 10 and len(self.karpaset) <= 0 :
                self.karpaset.append(Karpanen(self.naytto, self.leveys, self.korkeus, self.laser))
                #JOS YLI 500, NIIN LASKURI 2X
                if kohde.pisteet < 500:
                    self.laskuri += 1
                else:
                    self.laskuri += 2
        #JOS YLI 800 PISTETTÄ KAKSI KÄRPÄSTÄ KERRALLA(ehto yllä)
        else:
            if self.laskuri == 10 or self.laskuri ==12 and len(self.karpaset) <= 1:
                self.karpaset.append(Karpanen(self.naytto, self.leveys, self.korkeus, self.laser))
                self.laskuri += 2

        #UUSI POMO KENTÄLLE(Pomo nollaa vihulaskurin)
        if self.laskuri >= 20 and len(self.pomot) == 0:
            self.pomot.append(Pomo(self.naytto, self.leveys, self.korkeus, self.sarjatuli))
            self.laskuri = 0

        #ASTEROIDI JOS EI POMOA(todennäköisuus kasvaa pisteiden lisääntyessä)
        if kohde.pisteet < 900:
            if len(self.pomot) <= 0 and len(self.asteroidit) < 1:
                if kohde.pisteet < 300:
                    lukema = 100
                if kohde.pisteet >= 300 and kohde.pisteet < 1000:
                    lukema = 80
                if kohde.pisteet >= 1000:
                    lukema = 60
                if random.randint(1, lukema) == 1:
                    self.asteroidit.append(Asteroidi(self.naytto, self.leveys, self.korkeus))

        #JOS YLI 900 ASTEROIDEJA TULEE POMON KANSSA
        if kohde.pisteet >= 900:
            if len(self.asteroidit) < 3:
                if random.randint(1, 50) == 1:
                    self.asteroidit.append(Asteroidi(self.naytto, self.leveys, self.korkeus))

    def liikuta_vihollisia(self, kohde):
        #ASTEROIDI LIIKKUU
        for asteroidi in self.asteroidit:
            asteroidi.syoksy()
            pygame.sprite.spritecollide(asteroidi, ammukset, None)
            if asteroidi.y > self.korkeus+40:
                asteroidi.kill()
                self.asteroidit.remove(asteroidi)

        #POMO LIIKKUU
        for pomo in self.pomot:
            pomo.ohjaa(kohde)
            #AMMUS OSUU POMOON
            if pygame.sprite.spritecollide(pomo, ammukset, True):
                pomo.add(vihollinen)
                pomo.hp -= 1
                #POMON TUHO
                if pomo.tuhoa:
                    self.pomot.pop(self.pomot.index(pomo))
                    pomo.kill()
                    kohde.pisteet += 25

        #KÄRPÄNEN LIIKKUU
        for karpanen in self.karpaset:
            karpanen.ohjaa(kohde)
            if pygame.sprite.spritecollide(karpanen, ammukset, True):
                karpanen.hp -= 1
                if karpanen.hp <= 0:
                    self.karpaset.remove(karpanen)
                    karpanen.kill()
                    kohde.pisteet += 15


        #PERUSVIHOLLINEN LIIKKUU
        for vihu in self.viholliset:
            vihu.ohjaa(kohde)
            #AMMUS OSUU VIHOLLISEEN
            if pygame.sprite.spritecollide(vihu, ammukset, True):
                vihu.hp -= 1
                #VIHUN TUHO
                if vihu.hp <= 0:
                    self.viholliset.pop(self.viholliset.index(vihu))
                    vihu.kill()
                    kohde.pisteet += 5
            #KENTÄN ULKOPUOLELLA
            if vihu.y > self.korkeus + 10:
                self.viholliset.pop(self.viholliset.index(vihu))
                vihu.kill()
    
    #VIHOLLISTEN PÄÄOHJELMA
    def invaasio(self, kohde):

        #VIHOLLISGENERAATTORI
        self.luo_viholliset(kohde)

        #VIHOLLISTEN LIIKE
        self.liikuta_vihollisia(kohde)

        #OHJUKSET LIIKKUU
        for ohjus in self.ohjukset:
            ohjus.ohjus(self.naytto, kohde)
            #OSUMA 
            if pygame.sprite.spritecollide(ohjus, pelaaja, None):
                self.ohjukset.pop(self.ohjukset.index(ohjus))
            #ULKONA
            if ohjus.y > self.korkeus:
                ohjus.kill()
                #if-haara lisätty bugin vuoksi
                if ohjus in self.ohjukset:
                    self.ohjukset.remove(ohjus)

        #SARJATULI (tallennettu listoina listaan)
        for rivi in self.sarjatuli:
            kulma = -1
            for laaki in rivi:
                laaki.sarjatuli(self.naytto, kulma)
                kulma += 0.5
                if pygame.sprite.spritecollide(laaki, pelaaja, None):
                    rivi.remove(laaki)
                    
                if laaki.y > self.korkeus:
                    laaki.kill()
                    #if-haara, bugi
                    if laaki in rivi:
                        rivi.remove(laaki)

        #KÄRPÄSEN LASER
        for laser in self.laser:
            laser.laser()
            if pygame.sprite.spritecollide(laser, pelaaja, None):
                self.laser.remove(laser)
            if laser.y > self.korkeus:
                laser.kill()
                #if-haara, bugi
                if laser in self.laser:
                    self.laser.remove(laser)

class Vihollinen(pygame.sprite.Sprite):
    def __init__(self, naytto, leveys, korkeus, ammukset, hp):
        pygame.sprite.Sprite.__init__(self, vihollinen)
        self.leveys = leveys
        self.korkeus = korkeus
        self.naytto = naytto
        #ALOITUSKOHTA
        self.x = random.randint(13,self.leveys-13)
        self.y = -40
        #AMMUNNAN LASKURI/TAUOTUS
        self.laskuri = 2.2
        self.ammukset = ammukset
        #OSUMAPISTEET
        self.hp = hp

        self.nopeus = 0.8
        self.kulmat = [(self.x-12, self.y), (self.x-5, self.y - 2), (self.x-1, self.y-5), (self.x +1, self.y-5), (self.x+5, self.y-2), (self.x +12, self.y), (self.x+12, self.y +40), (self.x+7, self.y+15), (self.x-7, self.y + 15), (self.x-12, self.y+40)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,150), self.kulmat, 3)
       
    def ohjaa(self, kohde):
        self.kulmat = [(self.x-12, self.y), (self.x-5, self.y - 2), (self.x-1, self.y-5), (self.x +1, self.y-5), (self.x+5, self.y-2), (self.x +12, self.y), (self.x+12, self.y +40), (self.x+7, self.y+15), (self.x-7, self.y + 15), (self.x-12, self.y+40)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,150), self.kulmat, 3)
        
        #OSUMAN MERKKI
        if pygame.sprite.spritecollide(self, ammukset, None):
            pygame.draw.polygon(self.naytto, (150,0,0), self.kulmat, 3)
        
        #LIIKE
        if self.y < self.korkeus:
            self.y += self.nopeus
        if self.x < kohde.x:
            self.x += 3
        if self.x > kohde.x:
            self.x -= 3
        #OHITUS
        if self.y > kohde.y:
            self.y += 8
        #AMMUSTEN VIIVE         
        if self.laskuri == 0.16:
            self.ammu()
        if self.laskuri >= 3:
            self.ammu()
            self.laskuri = 0
        #LATAA VIIVE
        self.laskuri += 0.02

    def ammu(self):
        if self.laskuri == 0.16:
            self.ammukset.append(VihollisenAmmukset(self.naytto, self.x , self.y + 10, (0, 0, 240), 1))
        else:
            self.ammukset.append(VihollisenAmmukset(self.naytto, self.x , self.y + 10, (0, 0, 180), 1))
        
class VihollisenAmmukset(pygame.sprite.Sprite):
    def __init__(self,naytto, x, y, vari, suunta):
        pygame.sprite.Sprite.__init__(self, vihollisen_ammukset)
        self.x = x
        self.y = y
        self.vari = vari
        self.suunta = suunta
        self.nopeus = 8 * self.suunta
        self.rect = pygame.draw.circle(naytto, self.vari, (self.x, self.y), 5)
        self.naytto = naytto

    #PERUSVIHOLLISEN AMMUS
    def ohjus(self, naytto, kohde):
        self.rect = pygame.draw.circle(naytto, self.vari, (self.x, self.y), 5)
        self.y += self.nopeus-1.5
        if self.x < kohde.x:
            self.x += 1.5
        if self.x > kohde.x:
            self.x -= 1.5

    #POMON AMMUS
    def sarjatuli(self, naytto, kulma):
        self.rect = pygame.draw.circle(naytto, self.vari, (self.x, self.y), 5)
        self.y += self.nopeus-6
        self.x += kulma

    #KÄRPÄSEN AMMUS
    def laser(self):
        self.rect = pygame.draw.line(self.naytto, self.vari, (self.x, self.y), (self.x, self.y+10), 4)
        self.y += self.nopeus

class Pomo(pygame.sprite.Sprite):
    def __init__(self, naytto, leveys, korkeus, sarjatuli):
        pygame.sprite.Sprite.__init__(self, vihollinen)
        self.leveys = leveys
        self.korkeus = korkeus
        self.naytto = naytto
        self.x = random.randint(13,self.leveys-13)
        self.y = -97
        self.laskuri = 0
        self.sarjatuli = sarjatuli
        self.hp = 20
        self.tuhoa = False

        self.kulmat = [(self.x-40, self.y), (self.x - 30, self.y-10), (self.x - 20, self.y -20), (self.x -10, self.y -30), (self.x +10, self.y -30), (self.x + 20, self.y -20), (self.x +30, self.y - 10), (self.x + 40, self.y), (self.x + 30, self.y +70), (self.x, self.y + 100), (self.x - 30, self.y + 70)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,100), self.kulmat, 4)

        
    def ohjaa(self, kohde):
        self.kulmat = [(self.x-40, self.y), (self.x - 30, self.y-10), (self.x - 20, self.y -20), (self.x -10, self.y -30), (self.x +10, self.y -30), (self.x + 20, self.y -20), (self.x +30, self.y - 10), (self.x + 40, self.y), (self.x + 30, self.y +70), (self.x, self.y + 100), (self.x - 30, self.y + 70)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,100), self.kulmat, 4)
        #OSUMAN MERKKI
        if pygame.sprite.spritecollide(self, ammukset, None):
            pygame.draw.polygon(self.naytto, (150,0,0), self.kulmat, 4)

        #LIIKE
        if self.y < self.korkeus*0.08:
            self.y += 0.2
        if self.x < kohde.x:
            self.x += 1
        if self.x > kohde.x:
            self.x -= 1
        
        #SARJATULEN JAKSOTUS
        kohdat = [10, 15, 20, 25, 30, 35, 40]
        self.laskuri += 0.25
        if self.laskuri >= 70:
            self.laskuri = 0
        for n in kohdat:
            if self.laskuri == n:
                self.ammu()

        #TUHOUTUU
        if self.hp <= 0:
            self.tuhoa = True

    def ammu(self):
        #SARJATULILISTAAN LADATAAN VIIDEN AMMUKSEN LISTA, JOKA KÄYDÄÄN LÄPI VIHOLLISET/INVAASIO
        self.sarjatuli.append([VihollisenAmmukset(self.naytto, self.x , self.y + 99, (0, 0, 240), 1), VihollisenAmmukset(self.naytto, self.x , self.y + 99, (0, 0, 140), 1), VihollisenAmmukset(self.naytto, self.x , self.y + 99, (0, 0, 240), 1), VihollisenAmmukset(self.naytto, self.x , self.y + 99, (0, 0, 140), 1), VihollisenAmmukset(self.naytto, self.x , self.y + 99, (0, 0, 240), 1)])

class Asteroidi(pygame.sprite.Sprite):
    def __init__(self, naytto, leveys, korkeus):
        pygame.sprite.Sprite.__init__(self, asteroidi)
        self.naytto = naytto
        self.leveys = leveys
        self.korkeus = korkeus

        #GENEROIDAAN ASTEROIDIN KOKO JA LIIKKEEN SUUNTA + VAUHTI
        self.x = random.randint(-40, self.leveys + 40)
        self.y = -100
        self.halkaisija = random.randint(20, 40)
        self.rect = pygame.draw.circle(self.naytto, (0, 0, 130), (self.x, self.y), self.halkaisija, 8)
        self.pos = [x for x in range(-8,-1)] 
        self.neg = [y for y in range(1,8)]
        self.suunta = random.choice(self.pos + self.neg)

    #ASTEROIDIN LIIKE
    def syoksy(self):
        self.rect = pygame.draw.circle(self.naytto, (0, 0, 130), (self.x, self.y), self.halkaisija, 8)

        #ASTEROIDIN KUVA RIIPPUEN ONKO SUUNTA + VAI -
        if self.suunta < 0:
            pygame.draw.circle(self.naytto, (0, 0, 100), (self.x+3, self.y-5), self.halkaisija, 3)
            pygame.draw.circle(self.naytto, (0, 0, 100), (self.x+6, self.y-10), self.halkaisija, 1)
        else:
            pygame.draw.circle(self.naytto, (0, 0, 100), (self.x-3, self.y-5), self.halkaisija, 3)
            pygame.draw.circle(self.naytto, (0, 0, 100), (self.x-6, self.y-10), self.halkaisija, 1)
        self.y += 8
        self.x += self.suunta

class Karpanen(pygame.sprite.Sprite):
    def __init__(self, naytto, leveys, korkeus, laser):
        pygame.sprite.Sprite.__init__(self, vihollinen)
        self.naytto = naytto
        self.leveys = leveys
        self.korkeus = korkeus

        self.x = random.randint(35,self.leveys-35)
        self.y = - 40
        self.kulmat = [(self.x-30, self.y), (self.x+30, self.y), (self.x+15, self.y+15), (self.x+23, self.y+23), (self.x +7, self.y +7), (self.x, self.y+30), (self.x -7, self.y +7), (self.x-23, self.y+23), (self.x-15, self.y+15)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,200), self.kulmat, 4)
        self.vasemmalle = random.choice([False, True])
        if not self.vasemmalle:
            self.oikealle = True
        else:
            self.oikealle = False

        self.laser = laser
        self.laskuri = 0
        self.hp = 5

    def ohjaa(self, kohde):
        self.kulmat = [(self.x-30, self.y), (self.x+30, self.y), (self.x+15, self.y+15), (self.x+23, self.y+23), (self.x +7, self.y +7), (self.x, self.y+30), (self.x -7, self.y +7), (self.x-23, self.y+23), (self.x-15, self.y+15)]
        self.rect = pygame.draw.polygon(self.naytto, (0,0,200), self.kulmat, 4)

        if pygame.sprite.spritecollide(self, ammukset, None):
            pygame.draw.polygon(self.naytto, (200,0,0), self.kulmat, 4)

        if self.y < 0:
            self.y += 1

        if self.x <= 15:
            self.oikealle = True
            self.vasemmalle = False
        if self.x >= self.leveys -15:
            self.vasemmalle = True
            self.oikealle = False

        if self.vasemmalle:
            self.x -= 3
        if self.oikealle:
            self.x += 3

        self.ammu()

    def ammu(self):
        kohdat = [n for n in range(8, 41, 8)]
        for n in kohdat:
            if self.laskuri == n:
                self.laser.append(VihollisenAmmukset(self.naytto, self.x, self.y + 30, (30, 30, 255-n*2), 1))
        #AMMUSTEN TAUOTUS
        self.laskuri += 1
        if self.laskuri >= 80:
            self.laskuri = 0
            
    
Peli()