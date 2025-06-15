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
        self.tela = None

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
        self.img_fnt1 = pg.image.load("assets/fnt1.png").convert_alpha()
        self.img_fnt2 = pg.image.load("assets/fnt2.png").convert_alpha() # referente à lâmpada
        self.img_fft = pg.image.load("assets/fft.png").convert_alpha()
        self.img_fr = pg.image.load("assets/fr.png").convert_alpha()

        self.img_fnt1 = pg.transform.scale(self.img_fnt1, (50,50))
        self.img_fnt2 = pg.transform.scale(self.img_fnt2, (50,50))
        self.img_fft = pg.transform.scale(self.img_fft, (50,50))
        self.img_fr = pg.transform.scale(self.img_fr, (50,50))
        self.fnt1_usada = False
        self.fnt2_usada = False
        self.fft_usada = False
        self.fr_usada = False

        # Retangulo da imagem condutores
        self.rect_fnt1 = self.img_fnt1.get_rect(topleft=(largura * 0.20, altura * 0.90))
        self.rect_fnt2 = self.img_fnt2.get_rect(topleft=(largura * 0.40, altura * 0.90))
        self.rect_fft = self.img_fft.get_rect(topleft=(largura * 0.60, altura * 0.90))
        self.rect_fr =  self.img_fr.get_rect(topleft=(largura * 0.80, altura * 0.90))

        #Estado de arrasto
        self.arrastando_fnt1 = False
        self.arrastando_fnt2 = False
        self.arrastando_fft = False
        self.arrastando_fr = False

        self.fios = [] # planejando ser uma tupla de fios que ira fazer a conexao
        self.selecao = None # primeiro clique

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                from tela_inicial import TelaInicial
                return TelaInicial(pg.display.get_surface())
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

                if self.rect_fnt1.collidepoint(evento.pos):
                    self.arrastando_fnt1 = True
                elif self.rect_fnt2.collidepoint(evento.pos):
                    self.arrastando_fnt2 = True
                elif self.rect_fft.collidepoint(evento.pos):
                    self.arrastando_fft = True
                elif self.rect_fr.collidepoint(evento.pos):
                    self.arrastando_fr = True

            elif evento.type == pg.MOUSEBUTTONUP:
                # FNT1
                if self.arrastando_fnt1:
                    self.arrastando_fnt1 = False
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Centro de Carga", "Lâmpada"}:
                            if self._imagem_proxima_da_linha(self.rect_fnt1, fio):
                                if "imagens" not in fio:
                                    fio["imagens"] = []
                                if self.img_fnt1 not in fio["imagens"]:  # Evita duplicação
                                    fio["imagens"].append(self.img_fnt1)
                                    self.fnt1_usada = True
                                break
                # FNT2
                if self.arrastando_fnt2:
                    self.arrastando_fnt2 = False
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Centro de Carga", "Lâmpada"}:
                            if self._imagem_proxima_da_linha(self.rect_fnt2, fio):
                                if "imagens" not in fio:
                                    fio["imagens"] = []
                                if self.img_fnt2 not in fio["imagens"]:  # Evita duplicação
                                    fio["imagens"].append(self.img_fnt2)
                                    self.fnt2_usada = True
                                break

                # FFT
                if self.arrastando_fft:
                    self.arrastando_fft = False
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Lâmpada", "Tomada"}:
                            if self._imagem_proxima_da_linha(self.rect_fft, fio):
                                if "imagens" not in fio:
                                    fio["imagens"] = []
                                # Gira a imagem 90 graus para a esquerda antes de adicionar
                                imagem_fft_rotacionada = pg.transform.rotate(self.img_fft, 90)
                                if imagem_fft_rotacionada not in fio["imagens"]:  # Evita duplicação
                                    fio["imagens"].append(imagem_fft_rotacionada)
                                    self.fft_usada = True
                                break

                # FR
                if self.arrastando_fr:
                    self.arrastando_fr = False
                    for fio in self.fios:
                        nomes = {fio["origem"].nome, fio["destino"].nome}
                        if nomes == {"Lâmpada", "Interruptor"}:
                            if self._imagem_proxima_da_linha(self.rect_fr, fio):
                                if "imagens" not in fio:
                                    fio["imagens"] = []
                                if self.img_fr not in fio["imagens"]:  # Evita duplicação
                                    fio["imagens"].append(self.img_fr)
                                    self.fr_usada = True
                                break

            elif evento.type == pg.MOUSEMOTION:
                if self.arrastando_fnt1:
                    self.rect_fnt1.topleft = evento.pos

                if self.arrastando_fnt2:
                    self.rect_fnt2.topleft = evento.pos

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


        # Para os demais apenas uma conexao
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
        self.tela = tela

        # Preencha o fundo inteiro com uma cor clara
        tela.fill((200, 200, 200))  # Cor de fundo clara

        # Preencha a área superior com branco
        pg.draw.rect(tela, (255, 255, 255), (0, 0, self.largura, self.espaco_topo))

        # Desenhe a imagem de fundo na área útil
        tela.blit(self.imagem_fundo, (0, self.espaco_topo))

        # Nome da fase
        fonte = pg.font.SysFont(None, 36)
        texto = fonte.render("Condutores e Componentes", True, (0, 0, 0))  # Texto preto
        tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 10))

        # Linha separadora abaixo do cabeçalho
        pg.draw.line(tela, (100, 100, 100), (0, self.espaco_topo), (self.largura, self.espaco_topo), 2)

        # Bandeja inferior para condutores
        altura_bandeja = 100
        y_bandeja = self.altura - altura_bandeja
        pg.draw.rect(tela, (200, 200, 200), (0, y_bandeja, self.largura, altura_bandeja))

        # Título da área de condutores
        fonte_bandeja = pg.font.SysFont(None, 28)
        texto_bandeja = fonte_bandeja.render("Condutores", True, (0, 0, 0))
        tela.blit(texto_bandeja, (10, y_bandeja + 10))

        # Atualize o método de desenho para exibir múltiplas imagens no fio
        for fio in self.fios:
            c1 = fio["origem"]
            c2 = fio["destino"]
            centro1 = c1.ret.center
            centro2 = c2.ret.center
            pg.draw.line(tela, (0, 0, 0), centro1, centro2, 3)

            # Desenhe todas as imagens associadas ao fio
            if "imagens" in fio:
                num_imagens = len(fio["imagens"])
                for i, imagem in enumerate(fio["imagens"]):
                    # Posicione as imagens ao longo da linha
                    pos_x = centro1[0] + (centro2[0] - centro1[0]) * (i + 1) / (num_imagens + 1)
                    pos_y = centro1[1] + (centro2[1] - centro1[1]) * (i + 1) / (num_imagens + 1)
                    tela.blit(imagem, (pos_x - imagem.get_width() // 2, pos_y - imagem.get_height() // 2))

        # Destaque seleção
        if self.selecao:
            pg.draw.rect(tela, (0, 120, 255), self.selecao.ret.inflate(1, 1), 1)

        # Desenha componentes
        for comp in self.componentes:
            comp.desenhar(tela)

        if not self.fnt1_usada:
            tela.blit(self.img_fnt1, self.rect_fnt1.topleft)

        if not self.fnt2_usada:
            tela.blit(self.img_fnt2, self.rect_fnt2.topleft)

        if not self.fft_usada:
            tela.blit(self.img_fft, self.rect_fft.topleft)

        if not self.fr_usada:
            tela.blit(self.img_fr, self.rect_fr.topleft)

        fonte_voltar = pg.font.SysFont(None, 24)
        texto_voltar = fonte_voltar.render("Pressione ESC para voltar ao menu", True, (0, 0, 0))
        tela.blit(texto_voltar, (10, 10))