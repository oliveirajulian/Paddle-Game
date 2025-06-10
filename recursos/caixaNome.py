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
        
