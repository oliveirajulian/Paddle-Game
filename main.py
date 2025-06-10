import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, escreverDados
from recursos.caixaNome import pegarNome, telaDead

pygame.init()
inicializarBancoDeDados()

# Configurações da tela
tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Paddle Game!")
icone = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Imagens e sons
raquete = pygame.image.load("recursos/raquete.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
bolinha_img = pygame.image.load("recursos/bolinha.png")
fundoGame = pygame.mixer.music.load("recursos/fundoGame.mp3")
somBolinha = pygame.mixer.Sound("recursos/somBolinha.mp3")


fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)

def start():
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40

    pedindoNome = False
    user_text = ""
    input_box = pygame.Rect(350, 10, 300, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

            if not pedindoNome:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if startButton.collidepoint(evento.pos):
                        pedindoNome = True
                        user_text = ""
                        active = True
                        color = color_active
                    elif quitButton.collidepoint(evento.pos):
                        quit()
            else:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(evento.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

                if evento.type == pygame.KEYDOWN and active:
                    if evento.key == pygame.K_RETURN:
                        nomeDoJogador = user_text.strip()
                        if nomeDoJogador != "":
                            jogar(nomeDoJogador)
                            return
                    elif evento.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 20:
                            user_text += evento.unicode

        tela.blit(fundoStart, (0, 0))

        if not pedindoNome:
            startButton = pygame.Rect(10, 60, larguraButtonStart, alturaButtonStart)
            pygame.draw.rect(tela, branco, startButton, border_radius=15)
            startTexto = fonteMenu.render("Iniciar Game", True, preto)
            tela.blit(startTexto, (startButton.x + 20, startButton.y + 10))

            quitButton = pygame.Rect(10, 110, larguraButtonQuit, alturaButtonQuit)
            pygame.draw.rect(tela, branco, quitButton, border_radius=15)
            quitTexto = fonteMenu.render("Sair do Game", True, preto)
            tela.blit(quitTexto, (quitButton.x + 30, quitButton.y + 10))
        else:
            pygame.draw.rect(tela, color, input_box, 2)
            text_surface = fonteMenu.render(user_text, True, preto)
            tela.blit(text_surface, (input_box.x + 5, input_box.y + 8))
            instrucao = fonteMenu.render("Digite seu nome e pressione Enter", True, branco)
            tela.blit(instrucao, (input_box.x, input_box.y - 25))

        pygame.display.update()
        relogio.tick(60)

def jogar(nomeDoJogador):
    posicaoXRaquete = 30
    posicaoYRaquete = 300
    limiteInferior = 0
    limiteSuperior = tamanho[1] - raquete.get_height()
    velocidadeRaquete = 6

    posicaoXBolinha = 500
    posicaoYBolinha = random.randint(75, 625)
    velocidadeBolinhaX = -5
    velocidadeBolinhaY = random.choice([-3, -2, 2, 3])

    pontos = 0
    rodando = True

    pygame.mixer.music.play(-1)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            posicaoYRaquete -= velocidadeRaquete
        if teclas[pygame.K_DOWN]:
            posicaoYRaquete += velocidadeRaquete

        posicaoYRaquete = max(min(posicaoYRaquete, limiteSuperior), limiteInferior)

        posicaoXBolinha += velocidadeBolinhaX
        posicaoYBolinha += velocidadeBolinhaY

        if posicaoYBolinha <= 0 or posicaoYBolinha >= tamanho[1] - bolinha_img.get_height():
            velocidadeBolinhaY *= -1

        raqueteRect = pygame.Rect(posicaoXRaquete, posicaoYRaquete, raquete.get_width(), raquete.get_height())
        bolinhaRect = pygame.Rect(posicaoXBolinha, posicaoYBolinha, bolinha_img.get_width(), bolinha_img.get_height())

        if bolinhaRect.colliderect(raqueteRect):
            posicaoXBolinha = posicaoXRaquete + raquete.get_width()
            velocidadeBolinhaX *= -1.1
            pontos += 1
            velocidadeBolinhaY = random.choice([-4, -3, -2, 2, 3, 4])
            
            somBolinha.play()

        if posicaoXBolinha >= tamanho[0] - bolinha_img.get_width():
            posicaoXBolinha = tamanho[0] - bolinha_img.get_width()
            velocidadeBolinhaX *= -1.1
            velocidadeBolinhaY = random.choice([-4, -3, -2, 2, 3, 4])

        # 👉 Se a bolinha sair pela esquerda (perdeu)
        if posicaoXBolinha < 0:
            pygame.mixer.music.stop()
            escreverDados(nomeDoJogador, pontos)
            resultado = telaDead(tela, fonteMenu, fundoDead, branco, preto, relogio)

            if resultado == "reiniciar":
                start()
            else:
                pygame.quit()
                exit()
            return  # encerra a função jogar

        # Desenho na tela
        tela.blit(fundoJogo, (0, 0))
        tela.blit(raquete, (posicaoXRaquete, posicaoYRaquete))
        tela.blit(bolinha_img, (posicaoXBolinha, posicaoYBolinha))

        texto_pontos = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_pontos, (tamanho[0] - 150, 10))

        pygame.display.flip()
        relogio.tick(60)

    pygame.mixer.music.stop()


start()
