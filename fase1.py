import pygame as pg

class Componente:
    def __init__(self, nome, cor, pos):
        self.nome = nome
        self.cor = cor
        self.pos = pos
        self.ret = pg.Rect(pos[0], pos[1], 100, 60)

    def desenhar(self, tela):
        pg.draw.rect(tela, self.cor, self.ret)
        fonte = pg.font.SysFont(None, 24)
        texto = fonte.render(self.nome, True, (0, 0, 0))
        # copiando um conteudo grafico para a tela e ajustando sua posicao, no caso a posicao do texto
        tela.blit(texto, (self.pos[0] + 10, self.pos[1] + 20)) 
       
class Fase1:
    def __init__(self):
        self.componentes = [
            Componente("Centro de Carga", (255, 100, 100), (0, 300)),
            Componente("Lâmpada",         (255, 100, 100), (350, 250)),
            Componente("Interruptor",     (255, 100, 100), (700, 300)),
            Componente("Tomada",          (255, 100, 100), (150, 0)),
        ]

        # Imagens
        self.img_fase = pg.image.load("assets/f.png").convert_alpha()
        self.img_fase = pg.transform.scale(self.img_fase, (50,50))
        # Retangulo da imagem
        self.rect_fase = self.img_fase.get_rect(topleft=(700, 100))
        #Estado de arrasto
        self.arrastando_fase = False


        self.fios = [] # planejando ser uma tupla de fios que ira fazer a conexao

        self.selecao = None # primeiro clique


    # Colocar quaquer interação do usuario com o jogo aqui para ser carregado na tela
    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for comp in self.componentes:
                    # collidepoint é um metodo do retangulo para identificar se o ponto esta dentro dele
                    if comp.ret.collidepoint(pos):
                        if self.selecao is None:
                            self.selecao = comp
                        else:
                            # Criar ligação entre os 2
                            if self.selecao != comp and not self.fio_ja_existe(self.selecao, comp):
                                self.fios.append((self.selecao, comp))
                            self.selecao = None
            
                if self.rect_fase.collidepoint(evento.pos):
                    self.arrastando_fase = True
            elif evento.type == pg.MOUSEBUTTONUP:
                self.arrastando_fase = False
            elif evento.type == pg.MOUSEMOTION:
                if self.arrastando_fase:
                    self.rect_fase.topleft = evento.pos


    def fio_ja_existe(self, c1, c2):
        return any((a == c1 and b == c2) or (a == c2 and b == c1) for a,b in self.fios)
    
    def desenhar(self, tela):
        tela.fill((240, 240, 240)) # Fundo branco

        # Desenha linhas
        for c1, c2 in self.fios:
            centro1 = c1.ret.center
            centro2 = c2.ret.center
            pg.draw.line(tela, (0,0,0), centro1, centro2, 3)

        # Destaque seleção
        if self.selecao:
            pg.draw.rect(tela, (0,0,0), self.selecao.ret, 3)

        # Desenha componentes
        for comp in self.componentes:
            comp.desenhar(tela)
        
        tela.blit(self.img_fase, self.rect_fase.topleft)


