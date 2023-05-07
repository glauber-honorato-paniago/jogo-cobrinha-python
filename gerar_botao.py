import pygame

# Definir constantes
COR_DO_BOTAO = (0, 255, 0)  # Verde
COR_DO_TEXTO = (0, 0, 0)  # Branco

# Função para desenhar botão


def desenhar_botao(window, x, y, largura, altura, texto, acao, cor_botao=COR_DO_BOTAO, cor_texto=COR_DO_TEXTO):
    pygame.draw.rect(window, cor_botao, (x, y, largura, altura))
    fonte = pygame.font.Font(None, 36)
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x + largura / 2, y + altura / 2)
    window.blit(texto_surface, texto_rect)
    # Verificar se o botão foi clicado
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if x < mouse_pos[0] < x + largura and y < mouse_pos[1] < y + altura:
            acao()
