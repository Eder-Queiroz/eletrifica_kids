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

        # Imagens: 
        self.img_fnt = pg.image.load("assets/fnt.png").convert_alpha()
        self.img_fft = pg.image.load("assets/fft.png").convert_alpha()
        self.img_fr = pg.image.load("assets/fr.png").convert_alpha()

        self.img_fnt = pg.transform.scale(self.img_fnt, (50,50))
        self.img_fft = pg.transform.scale(self.img_fft, (50,50))
        self.img_fr = pg.transform.scale(self.img_fr, (50,50))
        self.fnt_usada = False

        # Fazer ainda
        self.fft_usada = False
        self.fr_usada = False

        # Retangulo da imagem
        self.rect_fnt = self.img_fnt.get_rect(topleft=(700, 100))


        self.rect_fft = self.img_fft.get_rect(topleft=(500, 100))
        self.rect_fr =  self.img_fr.get_rect(topleft=(300, 100))

        #Estado de arrasto
        self.arrastando_fnt = False


        self.arrastando_fft = False
        self.arrastando_fr = False

        self.fios = [] # planejando ser uma tupla de fios que ira fazer a conexao

        self.selecao = None # primeiro clique

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for comp in self.componentes:
                    if comp.ret.collidepoint(pos):
                        if self.selecao is None:
                            self.selecao = comp
                        else:
                            # Criar ligação entre os 2
                            if self.selecao != comp and not self.fio_ja_existe(self.selecao, comp):
                                self.fios.append({
                                    "origem": comp,
                                    "destino": self.selecao,
                                    "imagem": None
                                    })
                                print(self.fios)
                            self.selecao = None
            
                if self.rect_fnt.collidepoint(evento.pos):
                    self.arrastando_fnt = True
                elif self.rect_fft.collidepoint(evento.pos):
                    self.arrastando_fft = True
                elif self.rect_fr.collidepoint(evento.pos):
                    self.arrastando_fr = True
                    
            elif evento.type == pg.MOUSEBUTTONUP:
                # FNT
                if self.arrastando_fnt:
                    self.arrastando_fnt = False 
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Centro de Carga", "Lâmpada"} and fio["imagem"] is None:
                            if self._imagem_proxima_da_linha(self.rect_fnt, fio):
                                fio["imagem"] = self.img_fnt
                                self.fnt_usada = True
                                break
                
                # FFT
                if self.arrastando_fft:
                    self.arrastando_fft = False 
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Lâmpada", "Tomada"} and fio["imagem"] is None:
                            if self._imagem_proxima_da_linha(self.rect_fft, fio):
                                fio["imagem"] = self.img_fft
                                self.fft_usada = True
                                break

                # FR
                if self.arrastando_fr:
                    self.arrastando_fr = False 
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Lâmpada", "Interruptor"} and fio["imagem"] is None:
                            if self._imagem_proxima_da_linha(self.rect_fr, fio):
                                fio["imagem"] = self.img_fr
                                self.fr_usada = True
                                break


                # # ponto_solto = self.rect_fnt.center

                # for fio in self.fios:
                #     nomes = {fio["origem"].nome, fio["destino"].nome}
                    
                #     # Só permitir colocar a imagem entre Lâmpada e Interruptor
                #     if nomes == {"Lâmpada", "Interruptor"}:
                #         origem = fio["origem"]
                #         destino = fio["destino"]
                #         centro1 = origem.ret.center
                #         centro2 = destino.ret.center

                #         # Calcular a distancia do centro da imagem até o meio do fio
                #         meio = ((centro1[0] + centro2[0]) // 2, (centro1[1] + centro2[1]) // 2)
                #         dx = self.rect_fnt.centerx - meio[0]
                #         dy = self.rect_fnt.centery - meio[1]
                #         distancia = (dx ** 2 + dy ** 2) ** 0.5

                #         if distancia < 50 and fio["imagem"] is None: # tolerancia de 50px
                #             fio["imagem"] = self.img_fnt  # Salva imagem no fio
                #             self.fnt_usada = True
                #             break

            elif evento.type == pg.MOUSEMOTION:
                if self.arrastando_fnt:
                    self.rect_fnt.topleft = evento.pos
                
                if self.arrastando_fft:
                    self.rect_fft.topleft = evento.pos

                if self.arrastando_fr:
                    self.rect_fr.topleft = evento.pos

    def _imagem_proxima_da_linha(self, rect_imagem, fio, tolerancia=50):
        centro1 = fio["origem"].ret.center
        centro2 = fio["destino"].ret.center
        meio = ((centro1[0] + centro2[0]) // 2, (centro1[1] + centro2[1]) // 2)
        dx = rect_imagem.centerx - meio[0]
        dy = rect_imagem.centery - meio[1]
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        return distancia < tolerancia


    def fio_ja_existe(self, c1, c2):
        return any((fio["origem"] == c1 and fio["destino"] == c2) or 
                   (fio["origem"] == c2 and fio["destino"] == c1) 
                   for fio in self.fios
        )
    
    def desenhar(self, tela):
        tela.fill((240, 240, 240)) # Fundo branco

        for fio in self.fios:
            c1 = fio["origem"]
            c2 = fio["destino"]
            centro1 = c1.ret.center
            centro2 = c2.ret.center
            pg.draw.line(tela, (0,0,0), centro1, centro2, 3)

            # Se tiver imagem nesse fio, desenha no meio da linha
            if fio.get("imagem"):
                meio = ((centro1[0] + centro2[0]) // 2, (centro1[1] + centro2[1]) // 2)
                tela.blit(fio["imagem"], meio)

        # Destaque seleção
        if self.selecao:
            pg.draw.rect(tela, (0,0,0), self.selecao.ret, 3)

        # Desenha componentes
        for comp in self.componentes:
            comp.desenhar(tela)
        
        if not self.fnt_usada:
            tela.blit(self.img_fnt, self.rect_fnt.topleft)
        
        if not self.fft_usada:
            tela.blit(self.img_fft, self.rect_fft.topleft)

        if not self.fr_usada:
            tela.blit(self.img_fr, self.rect_fr.topleft)