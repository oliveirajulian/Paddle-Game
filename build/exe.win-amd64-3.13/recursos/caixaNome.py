import pygame, json



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

def mostrarUltimosRegistros(n=5):
    try:
        with open("log.data", "r") as banco:
            dados = json.load(banco)
    except:
        return []

    todos = dados.get("todos", [])
    return todos[-n:][::-1]              
        
def telaDead(tela, fonteMenu, fundoDead, branco, preto, relogio, nomeDoJogador):
    botaoReiniciar = pygame.Rect(300, 550, 180, 40)
    botaoSair = pygame.Rect(520, 550, 180, 40)

    ultimos_5 = mostrarUltimosRegistros(5)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoReiniciar.collidepoint(evento.pos):
                    return "reiniciar"
                elif botaoSair.collidepoint(evento.pos):
                    return "sair"

        tela.blit(fundoDead, (0, 0))
        subtitulo = fonteMenu.render("Últimas partidas", True, branco)
        tela.blit(subtitulo, (20, 20))

        for i, registro in enumerate(ultimos_5):
            texto = f"{registro['data']} {registro['hora']} - {registro['nome']}: {registro['pontos']} pts"
            linha = fonteMenu.render(texto, True, branco)
            tela.blit(linha, (40, 40 + i * 30))

        pygame.draw.rect(tela, branco, botaoReiniciar, border_radius=10)
        pygame.draw.rect(tela, branco, botaoSair, border_radius=10)

        textoReiniciar = fonteMenu.render("Reiniciar", True, preto)
        textoSair = fonteMenu.render("Sair", True, preto)

        tela.blit(textoReiniciar, (botaoReiniciar.x + 45, botaoReiniciar.y + 10))
        tela.blit(textoSair, (botaoSair.x + 65, botaoSair.y + 10))

        pygame.display.update()
        relogio.tick(60)


