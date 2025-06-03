import pygame
import time
import random
import os

class Simbologia:
    def __init__(self, nome, img_path, img_center, text_center, fonte):
        self.nome = nome
        # carrega e escala a imagem
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (80, 80))
        # retângulo com base no centro
        self.rect_img = self.img.get_rect(center=img_center)

        # prepara o texto com fonte menor (20px)
        self.text_surf = fonte.render(nome, True, (0,0,0))
        self.rect_text = self.text_surf.get_rect(center=text_center)

        self.matched = False

    def draw(self, tela):
        # sempre desenha imagem e texto, mesmo quando matched=True
        tela.blit(self.img, self.rect_img)
        tela.blit(self.text_surf, self.rect_text)


class Fase3:
    def __init__(self):
        # Fonte reduzida para 20px em vez de 28px
        fonte = pygame.font.SysFont(None, 20)

        # lista de (nome, caminho_absoluto_para_imagem)
        base = os.path.dirname(__file__)
        lista = [
            ("Int. intermediário", os.path.join(base, "images", "interruptor-intermediario.jpg")),
            ("Int. paralelo",      os.path.join(base, "images", "interruptor-paralelo.jpg")),
            ("Int. simples",       os.path.join(base, "images", "interruptor-simples.jpg")),
            ("Tomada alta",               os.path.join(base, "images", "tomada-alta.jpg")),
            ("Tomada baixa",              os.path.join(base, "images", "tomada-baixa.jpg")),
            ("Tomada média",              os.path.join(base, "images", "tomada-media.jpg")),
            ("Lâmpada",                   os.path.join(base, "images", "lampada.jpg")),
        ]

        # pega dimensões da tela atual
        screen = pygame.display.get_surface()
        W, H = screen.get_size()

        n = len(lista)

        # ——————— 1) Calcular margem para imagens ———————
        half_img = 80 / 2
        margem_img = int(half_img + 20)
        # (40px de metade da imagem + 20px de folga extra)

        # ——————— 2) Calcular margem para textos (com fonte menor) ———————
        # mede cada texto para definir margem mínima
        label_widths = [fonte.size(nome)[0] for nome,_ in lista]
        half_label_max = max(label_widths) / 2
        margem_txt = int(half_label_max + 20)
        # (metade do maior texto + 20px de folga extra)

        # ——————— 3) Gerar steps / positions para IMAGENS e TEXTOS ———————
        if n > 1:
            step_imgs  = (W - 2*margem_img) / (n - 1)
            step_texts = (W - 2*margem_txt) / (n - 1)

            pos_x_imgs  = [margem_img + i*step_imgs for i in range(n)]
            pos_x_texts = [margem_txt + i*step_texts for i in range(n)]
        else:
            # se só tiver 1 item, centraliza no meio
            pos_x_imgs  = [W/2]
            pos_x_texts = [W/2]

        # embaralha cada lista separadamente
        pos_imgs  = random.sample(pos_x_imgs, n)
        pos_texts = random.sample(pos_x_texts, n)

        # fixa Y para imagens e textos
        y_img  = 80         # linha de cima para as imagens
        y_text = H - 80     # linha de baixo para as labels

        # ——————— 4) Instancia cada Simbologia com o center alignment corrigido ———————
        self.items = []
        for i,(nome,caminho) in enumerate(lista):
            img_c   = (pos_imgs[i],  y_img)
            text_c  = (pos_texts[i], y_text)
            self.items.append(
                Simbologia(nome, caminho, img_c, text_c, fonte)
            )

        self.selecao = []   # lista temporária de seleções [(item, tipo)]
        self.fios     = []  # pares acertados para desenhar as linhas

    def atualizar(self, eventos):
        for ev in eventos:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for item in self.items:
                    # só permite clicar em itens que ainda não foram matched
                    if not item.matched:
                        if item.rect_img.collidepoint(ev.pos):
                            self._selecionar(item, "img")
                        elif item.rect_text.collidepoint(ev.pos):
                            self._selecionar(item, "text")

    def _selecionar(self, item, tipo):
        self.selecao.append((item, tipo))
        if len(self.selecao) == 2:
            (i1,t1), (i2,t2) = self.selecao
            # se for clique em img + clique em text (na ordem que vier) e for o mesmo objeto:
            if t1 != t2 and i1 is i2:
                i1.matched = True
                self.fios.append((i1, i2))
            # atualiza a tela para mostrar feedback e dá um pequeno delay
            pygame.display.flip()
            time.sleep(0.3)
            self.selecao.clear()

    def desenhar(self, tela):
        tela.fill((255,255,255))

        # desenha todas as imagens e labels, matched ou não
        for item in self.items:
            item.draw(tela)

        # desenha linhas verdes conectando pares acertados
        for a, b in self.fios:
            p1 = a.rect_img.center
            p2 = b.rect_text.center
            pygame.draw.line(tela, (0,150,0), p1, p2, 4)

        # destaca borda vermelha em torno do item selecionado no momento
        for it, tipo in self.selecao:
            r = it.rect_img if tipo == "img" else it.rect_text
            pygame.draw.rect(tela, (255,0,0), r, 3)
