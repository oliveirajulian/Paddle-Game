import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.caixaNome import pegarNome
import json
print("Inicializando o Jogo! Criado por Julian.")
print("Aperte enter para iniciar o jogo!")

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Paddle Game!")
icone  = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
raquete = pygame.image.load("recursos/raquete.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
bolinha = pygame.image.load("recursos/bolinha.png")
fundoGame = pygame.mixer.Sound("recursos/fundoGame.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/fundoGame.mp3")

def start():
    nomeDoJogador = pegarNome(tela)
    print("Nome do jogador:", nomeDoJogador)

    # Variáveis raquete
    posicaoXRaquete = 30
    posicaoYRaquete = 0
    limiteInferior = -15
    limiteSuperior = 560
    velocidadeRaquete = 5

    # Variáveis bolinha
    posicaoXBolinha = 950
    posicaoYBolinha = random.randint(75, 625)
    velocidadeBolinhaX = -5

    rodando = True
    perdeu = False

    # Música de fundo (se quiser tocar)
    pygame.mixer.music.play(-1)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimento da raquete
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            posicaoYRaquete -= velocidadeRaquete
        if teclas[pygame.K_DOWN]:
            posicaoYRaquete += velocidadeRaquete

        # Limitar movimento da raquete
        if posicaoYRaquete < limiteInferior:
            posicaoYRaquete = limiteInferior
        if posicaoYRaquete > limiteSuperior:
            posicaoYRaquete = limiteSuperior

        # Movimento da bolinha
        posicaoXBolinha += velocidadeBolinhaX

        # Cria retângulos para colisão
        raqueteRect = pygame.Rect(posicaoXRaquete, posicaoYRaquete, raquete.get_width(), raquete.get_height())
        bolinhaRect = pygame.Rect(posicaoXBolinha, posicaoYBolinha, bolinha.get_width(), bolinha.get_height())

        # Colisão bolinha com raquete
        if bolinhaRect.colliderect(raqueteRect):
            posicaoXBolinha = posicaoXRaquete + raquete.get_width()
            velocidadeBolinhaX *= -1.1  # Rebater e acelerar

        # Verifica se a bolinha saiu da tela (perdeu)
        if posicaoXBolinha < 0:
            perdeu = True
            rodando = False

        # Desenha tudo
        tela.fill(preto)
        tela.blit(fundoJogo, (0, 0))
        tela.blit(raquete, (posicaoXRaquete, posicaoYRaquete))
        tela.blit(bolinha, (posicaoXBolinha, posicaoYBolinha))

        pygame.display.flip()
        relogio.tick(60)

    pygame.mixer.music.stop()
    
    if perdeu:
        escreverDados(nomeDoJogador, 0)  # Aqui pode atualizar com pontos, se quiser
        dead()




def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


start()

# git add origin http....   adiciona 
# git push origin main envia para o git hub
