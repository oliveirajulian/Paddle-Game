import pygame
import random
import threading
import speech_recognition as sr
from datetime import datetime
from recursos.funcoes import inicializarBancoDeDados, escreverDados  # você vai ajustar escreverDados depois
from recursos.caixaNome import pegarNome, telaDead  # vai substituir telaDead depois

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
passarinho = pygame.image.load("recursos/passarinho.png")

fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)

pausado = False  # variável global para pausar

def ouvir_comando():
    global pausado
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source, timeout=5)
                texto = r.recognize_google(audio, language="pt-BR").lower()
                print(f"Você disse: {texto}")
                if "pause" in texto or "pausa" in texto:
                    pausado = not pausado
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Erro na API de reconhecimento de voz")

# Iniciar thread da voz
threading.Thread(target=ouvir_comando, daemon=True).start()

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
                            telaBoasVindas(nomeDoJogador)
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
        
def telaBoasVindas(nomeDoJogador):
    larguraBotao = 200
    alturaBotao = 50
    botaoComecar = pygame.Rect((tamanho[0] - larguraBotao) // 2, 500, larguraBotao, alturaBotao)

    explicacao = [
        "Bem-vindo ao Paddle Game!",
        "Você controla a raquete com as setas para cima e para baixo.",
        "Rebata a bolinha o máximo que conseguir.",
        "Cada rebatida vale 1 ponto.",
        "Boa sorte!"
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoComecar.collidepoint(evento.pos):
                    return  # sai da função e começa o jogo

        tela.fill(preto)

        titulo = fonteMorte.render(f"Olá, {nomeDoJogador}!", True, branco)
        tela.blit(titulo, ((tamanho[0] - titulo.get_width()) // 2, 100))

        for i, linha in enumerate(explicacao):
            texto = fonteMenu.render(linha, True, branco)
            tela.blit(texto, ((tamanho[0] - texto.get_width()) // 2, 250 + i * 30))

        pygame.draw.rect(tela, branco, botaoComecar, border_radius=12)
        textoBotao = fonteMenu.render("Começar Partida", True, preto)
        tela.blit(textoBotao, (botaoComecar.x + 30, botaoComecar.y + 15))

        pygame.display.flip()
        relogio.tick(60)

def jogar(nomeDoJogador):
    global pausado

    posicaoXRaquete = 30
    posicaoYRaquete = 300
    limiteInferior = 0
    limiteSuperior = tamanho[1] - raquete.get_height()
    velocidadeRaquete = 6

    posicaoXBolinha = 500
    posicaoYBolinha = random.randint(75, 625)
    velocidadeBolinhaX = -5
    velocidadeBolinhaY = random.choice([-3, -2, 2, 3])
    
    passarinho_x = random.randint(50, tamanho[0] - 100)
    passarinho_y = tamanho[1] + passarinho.get_height()
    velocidade_passarinho = random.uniform(1.5, 3.0)

    pontos = 0
    rodando = True
    colidiu_raquete = False

    pygame.mixer.music.play(-1)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if pausado:
            texto_pause = fonteMorte.render("PAUSE", True, branco)
            tela.blit(fundoJogo, (0, 0))
            tela.blit(texto_pause, (tamanho[0] // 2 - texto_pause.get_width() // 2,
                                    tamanho[1] // 2 - texto_pause.get_height() // 2))
            pygame.display.update()
            relogio.tick(60)
            continue

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
            if not colidiu_raquete:
                posicaoXBolinha = posicaoXRaquete + raquete.get_width() + 1

                max_velocidade = 28
                fator_aceleracao = 1.1

                nova_velocidadeX = -velocidadeBolinhaX * fator_aceleracao

                min_velocidade = 5
                if abs(nova_velocidadeX) < min_velocidade:
                    nova_velocidadeX = min_velocidade if nova_velocidadeX > 0 else -min_velocidade

                if abs(nova_velocidadeX) > max_velocidade:
                    nova_velocidadeX = max_velocidade if nova_velocidadeX > 0 else -max_velocidade

                velocidadeBolinhaX = nova_velocidadeX

                pontos += 1
                velocidadeBolinhaY = random.choice([-4, -3, -2, 2, 3, 4])
                somBolinha.play()

                colidiu_raquete = True
        else:
            colidiu_raquete = False

        if posicaoXBolinha >= tamanho[0] - bolinha_img.get_width():
            posicaoXBolinha = tamanho[0] - bolinha_img.get_width()
            velocidadeBolinhaX *= -1.1
            velocidadeBolinhaY = random.choice([-4, -3, -2, 2, 3, 4])

        if posicaoXBolinha < 0:
            pygame.mixer.music.stop()
            escreverDados(nomeDoJogador, pontos)  # substituir pela sua função atualizada

            # Substituir telaDead para a nova versão sem Tkinter e com log no Pygame
            resultado = telaDead(tela, fonteMenu, fundoDead, branco, preto, relogio) 

            if resultado == "reiniciar":
                start()
            else:
                pygame.quit()
                exit()
            return

        # Passarinho voando de baixo para cima
        passarinho_y -= velocidade_passarinho
        if passarinho_y < -passarinho.get_height():
            passarinho_y = tamanho[1] + passarinho.get_height()
            passarinho_x = random.randint(50, tamanho[0] - 100)
            velocidade_passarinho = random.uniform(1.5, 3.0)

        tela.blit(fundoJogo, (0, 0))
        tela.blit(passarinho, (passarinho_x, passarinho_y))
        tela.blit(raquete, (posicaoXRaquete, posicaoYRaquete))
        tela.blit(bolinha_img, (posicaoXBolinha, posicaoYBolinha))

        pontosTexto = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(pontosTexto, (10, 10))

        pygame.display.update()
        relogio.tick(60)

start()
