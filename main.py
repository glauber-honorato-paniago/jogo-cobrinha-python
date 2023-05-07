import random

import pygame
import pygame.locals as pyl

import gerar_botao
pygame.init()


class Game:
    def __init__(self) -> None:
        self.altura = 500
        self.largura = 700
        self.window = pygame.display.set_mode((self.largura, self.altura))
        self.background_img = pygame.image.load('img/bg.png')

        # importando as fontes e os efeitos sonoros
        self.fonte_contador_pontos = pygame.font.SysFont('calibri', 30, True, False)
        self.sonoro_colisao_maca = pygame.mixer.Sound('sfx/colisao_maca.wav')

        # importando a imagem da cabeça da cobra e formatando a mesma
        cabeca_cobra_img = pygame.image.load('img/cobra.png').convert_alpha()
        # Defina a cor do fundo como transparente
        self.cabeca_cobra = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        self.cabeca_cobra.convert_alpha()
        self.cabeca_cobra.blit(cabeca_cobra_img, (0, 0))
        self.cabeca_cobra_rotacao_original = self.cabeca_cobra.copy()

        # importando o texto de game over e formatando o mesmo
        texto_gamer_over = pygame.image.load('img/game over.png').convert_alpha()
        self.texto_game_over = pygame.Surface((800, 500), pygame.SRCALPHA, 32)
        self.texto_game_over.convert_alpha()
        self.texto_game_over.blit(texto_gamer_over, (350, 200))

        # importando a maca e formatando o mesmo
        maca = pygame.image.load('img/maca.png').convert_alpha()
        self.maca = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        self.maca.convert_alpha()
        self.maca.blit(maca, (0, 0))

        self.relogio = pygame.time.Clock()
        self.resetar_jogo('init')
        self.iniciar_loop_game()

    def menu_inicial(self):
        # desenando widgets do menu inicial
        # funcao do comando  botao de iniciar jogo
        def iniciar_jogo():
            self.status = 1
        gerar_botao.desenhar_botao(self.window, 190, 240, 300, 50,
                                   'Iniciar Jogo', iniciar_jogo, (81, 119, 249))

    def resetar_jogo(self, chamada='game'):
        # resetando as variaveis de ambiente do jogo
        # 0 = menus, 1 = jogando, 2 = game over
        if chamada == 'game':
            self.status = 1
        else:
            self.status = 0

        self.pontuacao = 0
        self.direcao_movimento = 'direita'
        # rotacionando a cobra para o valor padrao
        self.cabeca_cobra = pygame.transform.rotate(
            self.cabeca_cobra_rotacao_original.copy(), 270)

        self.posicao_cabeca_cobra = [200, 40]
        self.tamanho_cobra = 2
        self.historico_posicao_cobra = [[160, 40], [180, 40], [200, 40]]
        self.posicao_maca = [200, 200]

    def comer_maca(self):
        # gerando posicoes aleatorias para a maça multiplos de 20
        self.pontuacao += 1
        self.tamanho_cobra += 1

        x = random.randint(40, 660)
        y = random.randint(40, 460)

        self.posicao_maca = [(x // 20) * 20, (y // 20) * 20]
        self.sonoro_colisao_maca.play()

    def atualizar_historico_posica_cobra(self):
        self.historico_posicao_cobra.append(self.posicao_cabeca_cobra.copy())
        if len(self.historico_posicao_cobra) > self.tamanho_cobra + 1:
            self.historico_posicao_cobra.pop(0)

    def tela_game_over(self):
        # geranto tela de game over
        superficie_preta = pygame.Surface((self.largura, self.altura))
        superficie_preta.fill((0, 0, 0))
        superficie_preta.set_alpha(128)
        self.window.blit(superficie_preta, (0, 0))
        self.window.blit(self.texto_game_over, (-210, -70))
        gerar_botao.desenhar_botao(self.window, 210, 250, 250, 50,
                                   'Reiniciar Jogo', self.resetar_jogo)

    def checar_fim_de_jogo(self):
        if self.posicao_cabeca_cobra[0] < 0 or self.posicao_cabeca_cobra[0] > self.largura - 20:
            self.status = 2

        elif self.posicao_cabeca_cobra[1] < 40 or self.posicao_cabeca_cobra[1] > self.altura - 20:
            self.status = 2

        elif self.posicao_cabeca_cobra in self.historico_posicao_cobra[:-1]:
            self.status = 2

        if self.status == 2:
            self.tela_game_over()

    def movimentar_cobra(self):
        if self.direcao_movimento == 'cima':
            self.posicao_cabeca_cobra[1] -= 20

        elif self.direcao_movimento == 'baixo':
            self.posicao_cabeca_cobra[1] += 20

        elif self.direcao_movimento == 'direita':
            self.posicao_cabeca_cobra[0] += 20

        elif self.direcao_movimento == 'esquerda':
            self.posicao_cabeca_cobra[0] -= 20

        self.atualizar_historico_posica_cobra()

    def rotacionar_cobra(self):
        if self.status == 0 or self.status == 2:
            return

        self.cabeca_cobra = self.cabeca_cobra_rotacao_original.copy()

        if self.direcao_movimento == 'baixo':
            self.cabeca_cobra = pygame.transform.rotate(self.cabeca_cobra, 180)

        elif self.direcao_movimento == 'direita':
            self.cabeca_cobra = pygame.transform.rotate(self.cabeca_cobra, 270)

        elif self.direcao_movimento == 'esquerda':
            self.cabeca_cobra = pygame.transform.rotate(self.cabeca_cobra, 90)

    def iniciar_loop_game(self):
        while True:
            # setando o fps
            self.relogio.tick(10)
            # contruindo o background
            self.window.blit(self.background_img, (0, 0))
            # contruindo cabeca da cobra caso o status seja jogando
            if self.status == 1 or self.status == 2:
                self.window.blit(self.cabeca_cobra,
                                 (self.posicao_cabeca_cobra[0], self.posicao_cabeca_cobra[1]))

           # bind de teclas
            for event in pygame.event.get():
                if event.type == pyl.QUIT:
                    pygame.quit()
                    exit()

                if self.status == 1 or self.status == 2:
                    # bind das teclas
                    if event.type == pyl.KEYDOWN:
                        if (event.key == pyl.K_d or event.key == pyl.K_RIGHT) and self.direcao_movimento != 'esquerda':
                            self.direcao_movimento = 'direita'
                            self.rotacionar_cobra()

                        if (event.key == pyl.K_a or event.key == pyl.K_LEFT) and self.direcao_movimento != 'direita':
                            self.direcao_movimento = 'esquerda'
                            self.rotacionar_cobra()

                        if (event.key == pyl.K_w or event.key == pyl.K_UP) and self.direcao_movimento != 'baixo':
                            self.direcao_movimento = 'cima'
                            self.rotacionar_cobra()

                        if (event.key == pyl.K_s or event.key == pyl.K_DOWN) and self.direcao_movimento != 'cima':
                            self.direcao_movimento = 'baixo'
                            self.rotacionar_cobra()

                        if event.key == pyl.K_ESCAPE or event.key == pyl.K_SPACE:
                            if not self.jogo_pausado and not self.game_over:
                                self.pausar_jogo()
                            elif self.jogo_pausado and not self.game_over:
                                self.despausar_jogo()

            #  contruindo o menu inicial caso o status seja do mesmo
            if self.status == 0:
                self.menu_inicial()

            else:
                maca = self.window.blit(
                    self.maca, (self.posicao_maca[0], self.posicao_maca[1], 20, 20))
                # desenhando widgets da cobra
                for indice in range(self.tamanho_cobra):
                    indice = (indice * -1) - 2
                    pygame.draw.rect(self.window, (66, 104, 249), (self.historico_posicao_cobra[indice][0],
                                                                   self.historico_posicao_cobra[indice][1],
                                                                   20, 20))

                # verificando se a cobra colidiu com a maça e gerando uma nova posição para a maça
                if pygame.Rect(self.posicao_cabeca_cobra[0], self.posicao_cabeca_cobra[1], 20, 20).colliderect(maca):
                    self.comer_maca()

                # movimentando a cobra caso o status do jogo nao seja gamer over caso contrario exibir tela de game over.
                if self.status == 1:
                    self.movimentar_cobra()

                # obtendo a pontuação do jogador e desenhando o texto na tela
                texto_pontuacao = self.fonte_contador_pontos.render(
                    f'{self.pontuacao}', False, (255, 255, 255))
                self.window.blit(texto_pontuacao, (620, 5))

                # checando se ouve fim de jogo
                self.checar_fim_de_jogo()

            pygame.display.flip()


game = Game()
