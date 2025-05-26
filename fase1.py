import pygame as pg

class Componente:
    def __init__(self, nome, imagem_path, tam_x, tam_y, pos):
        self.nome = nome
        self.pos = pos
        self.imagem = pg.image.load(imagem_path).convert_alpha()
        self.imagem = pg.transform.scale(self.imagem, (tam_x,tam_y))
        if self.nome == 'Tomada':
            self.imagem = pg.transform.rotate(self.imagem, 180)
        elif self.nome == 'Interruptor':
            self.imagem = pg.transform.rotate(self.imagem, 90)
        
        if self.nome == 'Lampada':
            self.ret = self.imagem.get_rect(center=pos)
        else:
            self.ret = self.imagem.get_rect(topleft=pos)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.ret.topleft)
        fonte = pg.font.SysFont(None, 24)
        texto = fonte.render(self.nome, True, (0, 0, 0))

        # Posição padrão do texto (centralizado abaixo da imagem)
        texto_x = self.ret.centerx - (texto.get_width() // 2)
        texto_y = self.ret.bottom + 5

        # Ajustes específicos do texto por componente
        if self.nome == 'Tomada':
            texto_x -= 80
            texto_y = self.ret.top - texto.get_height() + 40  # acima da imagem
        elif self.nome == 'Centro de Carga':
            texto_x += 70
            texto_y += 10  # mais para baixo
        elif self.nome == 'Interruptor':
            texto_x -= 20

        tela.blit(texto, (texto_x, texto_y))
        # tela.blit(texto, (self.pos[0] + 10, self.pos[1] + 80)) # abaixo da imagem 
       
class Fase1:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        # Espaços
        self.espaco_topo = int(self.altura * 0.1)
        self.altura_bandeja = 100

        # Carrega a imagem do quarto e redimensiona para o espaço útil
        altura_fundo = self.altura - self.espaco_topo - self.altura_bandeja
        self.imagem_fundo = pg.image.load("assets/quarto.png").convert_alpha()
        self.imagem_fundo = pg.transform.scale(self.imagem_fundo, (self.largura, altura_fundo))


        # Tamanhos dos componentes
        largura_carga, altura_carga = 60, 100
        largura_lamp, altura_lamp = 100, 80
        largura_int, altura_int = 90, 90
        largura_tom, altura_tom = 90, 90    


        self.componentes = [
            Componente("Centro de Carga", "assets/centro_de_cargas.png", largura_carga, altura_carga, (13, altura // 2 - altura_carga // 2)),
            Componente("Lâmpada",         "assets/lampada.png", largura_lamp, altura_lamp, (largura / 2.3, altura / 2.3)),
            Componente("Interruptor",  "assets/interruptor_simples.png", largura_int, altura_int, (largura - largura_int, altura // 2 - altura_int // 2)),
            Componente("Tomada",       "assets/tomada_intermediaria.png", largura_tom, altura_tom, (largura // 2 - largura_tom // 2, self.espaco_topo + 10)),
        ]

        # Imagens: 
        self.img_fnt = pg.image.load("assets/ffnt.png").convert_alpha()
        self.img_fft = pg.image.load("assets/fft.png").convert_alpha()
        self.img_fr = pg.image.load("assets/fr.png").convert_alpha()

        self.img_fnt = pg.transform.scale(self.img_fnt, (50,50))
        self.img_fft = pg.transform.scale(self.img_fft, (50,50))
        self.img_fr = pg.transform.scale(self.img_fr, (50,50))
        self.fnt_usada = False
        self.fft_usada = False
        self.fr_usada = False

        # Retangulo da imagem condutores
        self.rect_fnt = self.img_fnt.get_rect(topleft=(largura * 0.25, altura * 0.90))
        self.rect_fft = self.img_fft.get_rect(topleft=(largura * 0.5, altura * 0.90))
        self.rect_fr =  self.img_fr.get_rect(topleft=(largura * 0.75, altura * 0.90))

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
                                if self.conexao_valida(self.selecao, comp):
                                    self.fios.append({
                                        "origem": self.selecao,
                                        "destino": comp,
                                        "imagem": None
                                    })
                                    # print("Conexão feita:", self.selecao.nome, "→", comp.nome)
                                # else:
                                #     # print("Conexão inválida:", self.selecao.nome, "→", comp.nome)
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
    
    def conexao_valida(self, origem, destino):
        nome1 = origem.nome
        nome2 = destino.nome
        nomes = {nome1, nome2}

        # Conexão válida: Centro de Carga <-> Lâmpada (primeiro passo)
        if nomes == {"Centro de Carga", "Lâmpada"}:
            return True

        # Só permite Lâmpada -> Interruptor/Tomada se já tiver Lâmpada conectada ao Centro de Carga
        elif nomes in [{"Lâmpada", "Interruptor"}, {"Lâmpada", "Tomada"}]:
            for fio in self.fios:
                if {"Centro de Carga", "Lâmpada"} == {fio["origem"].nome, fio["destino"].nome}:
                    return True
        return False

    
    def desenhar(self, tela):     
        tela.blit(self.imagem_fundo, (0, self.espaco_topo))
        # tela.blit(self.imagem_fundo, (0, 0))

        # Nome da fase
        fonte = pg.font.SysFont(None, 36)
        texto = fonte.render("Fase x - Condutores | Componentes", True, (255,255,255))
        tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 10))

        # Linha separadora abaixo do cabeçalho
        pg.draw.line(tela, (100, 100, 100), (0, 50), (self.largura, 50), 2)

        # Bandeja inferior para condutores
        altura_bandeja = 100
        y_bandeja = self.altura - altura_bandeja
        pg.draw.rect(tela, (200, 200, 200), (0, y_bandeja, self.largura, altura_bandeja))

        # Título da área de condutores
        fonte_bandeja = pg.font.SysFont(None, 28)
        texto = fonte_bandeja.render("Condutores", True, (0, 0, 0))
        tela.blit(texto, (10, y_bandeja + 10))


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
            pg.draw.rect(tela, (0, 120, 255), self.selecao.ret.inflate(1, 1), 1)

        # Desenha componentes
        for comp in self.componentes:
            comp.desenhar(tela)
        
        if not self.fnt_usada:
            tela.blit(self.img_fnt, self.rect_fnt.topleft)
        
        if not self.fft_usada:
            tela.blit(self.img_fft, self.rect_fft.topleft)

        if not self.fr_usada:
            tela.blit(self.img_fr, self.rect_fr.topleft)