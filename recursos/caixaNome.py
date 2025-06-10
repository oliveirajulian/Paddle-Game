import pygame


def pegarNome(tela):
    pygame.font.init()
    fonte = pygame.font.Font(None, 50)
    texto = ""
    clock = pygame.time.Clock()
    ativo = True
    
    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and texto.strip():
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += evento.unicode
        
        
        tela.fill((0, 0, 0))
        tela.blit(fonte.render("Digite seu nome:", True, (255, 255 ,255)), (200, 180))
        pygame.draw.rect(tela, (50, 50, 50), (200, 240, 240, 50))
        tela.blit(fonte.render(texto, True, (255, 255, 255)), (210, 250))
        pygame.display.flip()
        clock.tick(30)
    return texto                            
        
def telaDead(tela, fonteMenu, fundoDead, branco, preto, relogio):
    larguraButtonRestart = 150
    alturaButtonRestart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if restartButton.collidepoint(evento.pos):
                    return "reiniciar"
                elif quitButton.collidepoint(evento.pos):
                    return "sair"

        tela.blit(fundoDead, (0, 0))

        restartButton = pygame.Rect(400, 400, larguraButtonRestart, alturaButtonRestart)
        pygame.draw.rect(tela, branco, restartButton, border_radius=15)
        restartTexto = fonteMenu.render("Reiniciar", True, preto)
        tela.blit(restartTexto, (restartButton.x + 20, restartButton.y + 10))

        quitButton = pygame.Rect(400, 460, larguraButtonQuit, alturaButtonQuit)
        pygame.draw.rect(tela, branco, quitButton, border_radius=15)
        quitTexto = fonteMenu.render("Sair do Jogo", True, preto)
        tela.blit(quitTexto, (quitButton.x + 20, quitButton.y + 10))

        pygame.display.update()
        relogio.tick(60)

