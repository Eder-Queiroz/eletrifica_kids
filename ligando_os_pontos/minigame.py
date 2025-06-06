from enum import Enum, auto
from typing import Optional, List, Dict, Tuple, Any

import pygame

pygame.init()
pygame.font.init()

# =============================================================================
# 1. CONFIGURAÇÃO E CONSTANTES
# =============================================================================
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_LIGHT_GREY = (200, 200, 200)
COLOR_BACKGROUND = (20, 20, 60)
COLOR_TERMINAL_HOVER = (0, 255, 255)
COLOR_GREEN_WIN = (0, 200, 0)
COLOR_ORANGE_CONNECT = (255, 165, 0)


class WireType(Enum):
    R = "R"
    S = "S"
    T = "T"
    N = "N"
    PE = "PE"


class TerminalRole(Enum):
    INPUT = auto()
    OUTPUT = auto()
    SOURCE = auto()


class ComponentType(Enum):
    DJ = "DJ"
    DR = "DR"
    CARGA = "CARGA"


WIRE_TYPE_TO_COLOR = {
    WireType.R: (200, 0, 0),
    WireType.S: (200, 200, 0),
    WireType.T: (50, 50, 50),
    WireType.N: (0, 0, 200),
    WireType.PE: (0, 150, 0),
}

TERMINAL_VISUAL_TO_COLOR = {
    "F1": (255, 0, 0),
    "F2": (255, 255, 0),
    "F3": (30, 30, 30),
    "N": (0, 0, 255),
    "PE": (0, 200, 0),
    "R": WIRE_TYPE_TO_COLOR[WireType.R],
    "S": WIRE_TYPE_TO_COLOR[WireType.S],
    "T": WIRE_TYPE_TO_COLOR[WireType.T],
}

# =============================================================================
# 2. ESTRUTURA DE DADOS DA CENA (Data-Driven Design)
# =============================================================================
SCENE_CONFIG = {
    "source_types": [WireType.R, WireType.S, WireType.T, WireType.N, WireType.PE],
    "circuits": [
        {
            "label": "Monofásico (F+N)",
            "components": [
                {
                    "id": "dj1_fn",
                    "name": "DJ F+N",
                    "type": ComponentType.DJ,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_n", 0.7, "N", "N"),
                    ],
                },
                {
                    "id": "dr1_fn",
                    "name": "DR F+N",
                    "type": ComponentType.DR,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_n", 0.7, "N", "N"),
                    ],
                },
                {
                    "id": "c1_fn",
                    "name": "Carga F+N",
                    "type": ComponentType.CARGA,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_n", 0.7, "N", "N"),
                        ("in_pe", 0.5, "PE", "PE", 0.75),
                    ],
                },
            ],
        },
        {
            "label": "Bifásico (F+F)",
            "components": [
                {
                    "id": "dj2_ff",
                    "name": "DJ F+F",
                    "type": ComponentType.DJ,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_f2", 0.7, "Fase", "F2"),
                    ],
                },
                {
                    "id": "dr2_ff",
                    "name": "DR F+F",
                    "type": ComponentType.DR,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_f2", 0.7, "Fase", "F2"),
                    ],
                },
                {
                    "id": "c2_ff",
                    "name": "Carga F+F",
                    "type": ComponentType.CARGA,
                    "terminals": [
                        ("in_f1", 0.3, "Fase", "F1"),
                        ("in_f2", 0.7, "Fase", "F2"),
                        ("in_pe", 0.5, "PE", "PE", 0.75),
                    ],
                },
            ],
        },
        {
            "label": "Bifásico (2F+N)",
            "components": [
                {
                    "id": "dj3_2fn",
                    "name": "DJ 2F+N",
                    "type": ComponentType.DJ,
                    "terminals": [
                        ("in_f1", 0.25, "Fase", "F1"),
                        ("in_f2", 0.5, "Fase", "F2"),
                        ("in_n", 0.75, "N", "N"),
                    ],
                },
                {
                    "id": "dr3_2fn",
                    "name": "DR 2F+N",
                    "type": ComponentType.DR,
                    "terminals": [
                        ("in_f1", 0.25, "Fase", "F1"),
                        ("in_f2", 0.5, "Fase", "F2"),
                        ("in_n", 0.75, "N", "N"),
                    ],
                },
                {
                    "id": "c3_2fn",
                    "name": "Carga 2F+N",
                    "type": ComponentType.CARGA,
                    "terminals": [
                        ("in_f1", 0.25, "Fase", "F1"),
                        ("in_f2", 0.5, "Fase", "F2"),
                        ("in_n", 0.75, "N", "N"),
                        ("in_pe", 0.5, "PE", "PE", 0.75),
                    ],
                },
            ],
        },
        {
            "label": "Trifásico (3F+N)",
            "components": [
                {
                    "id": "dj4_3fn",
                    "name": "DJ 3F+N",
                    "type": ComponentType.DJ,
                    "width_multiplier": 1.25,
                    "terminals": [
                        ("in_f1", 0.2, "Fase", "F1"),
                        ("in_f2", 0.4, "Fase", "F2"),
                        ("in_f3", 0.6, "Fase", "F3"),
                        ("in_n", 0.8, "N", "N"),
                    ],
                },
                {
                    "id": "dr4_3fn",
                    "name": "DR 3F+N",
                    "type": ComponentType.DR,
                    "width_multiplier": 1.25,
                    "terminals": [
                        ("in_f1", 0.2, "Fase", "F1"),
                        ("in_f2", 0.4, "Fase", "F2"),
                        ("in_f3", 0.6, "Fase", "F3"),
                        ("in_n", 0.8, "N", "N"),
                    ],
                },
                {
                    "id": "c4_3fn",
                    "name": "Carga 3F+N",
                    "type": ComponentType.CARGA,
                    "width_multiplier": 1.25,
                    "terminals": [
                        ("in_f1", 0.2, "Fase", "F1"),
                        ("in_f2", 0.4, "Fase", "F2"),
                        ("in_f3", 0.6, "Fase", "F3"),
                        ("in_n", 0.8, "N", "N"),
                        ("in_pe", 0.5, "PE", "PE", 0.75),
                    ],
                },
            ],
        },
    ],
}


# =============================================================================
# 3. CLASSES PRINCIPAIS
# =============================================================================
class WireDragState:
    """Armazena o estado de um fio sendo arrastado."""

    def __init__(self, start_terminal: "Terminal", wire_type: WireType):
        self.start_terminal = start_terminal
        self.wire_type = wire_type
        self.mouse_pos = pygame.mouse.get_pos()


class Terminal:
    """Representa um ponto de conexão em um componente elétrico."""

    def __init__(
        self,
        id_: str,
        parent_id: str,
        pos: pygame.Vector2,
        radius: int,
        expected_wire_type: str,
        visual_type: str,
        role: TerminalRole,
        pair_id: Optional[str] = None,
    ):
        self.id = id_
        self.parent_component_id = parent_id
        self.pos = pos
        self.radius = radius
        self.rect = pygame.Rect(pos.x - radius, pos.y - radius, radius * 2, radius * 2)

        self.expected_wire_type = expected_wire_type
        self.terminal_type_visual = visual_type
        self.role = role
        self.pair_id = pair_id

        self.is_connected_to: Optional[str] = None
        self.connected_wire_type: Optional[WireType] = None
        self.actual_provided_type: Optional[WireType] = None

        if self.role == TerminalRole.SOURCE:
            self.actual_provided_type = WireType(self.terminal_type_visual)

    def set_actual_provided_type(self, wire_type: WireType):
        """Define o tipo de fio que este terminal de SAÍDA fornecerá."""
        if self.role == TerminalRole.OUTPUT:
            self.actual_provided_type = wire_type

    def reset_connection_state(self):
        """Reseta o estado de conexão do terminal."""
        self.is_connected_to = None
        self.connected_wire_type = None
        if self.role == TerminalRole.OUTPUT:
            self.actual_provided_type = None
        elif self.role == TerminalRole.SOURCE:
            self.actual_provided_type = WireType(self.terminal_type_visual)

    def draw(self, surface: pygame.Surface, is_hovered: bool = False):
        """Desenha o terminal na tela."""

        color = TERMINAL_VISUAL_TO_COLOR.get(self.terminal_type_visual, COLOR_GREY)
        pygame.draw.circle(surface, color, self.rect.center, self.radius)

        if self.role == TerminalRole.OUTPUT and self.actual_provided_type:
            provided_color = WIRE_TYPE_TO_COLOR.get(self.actual_provided_type, color)
            pygame.draw.circle(
                surface, provided_color, self.rect.center, int(self.radius * 0.6)
            )

        if is_hovered:
            pygame.draw.circle(
                surface, COLOR_TERMINAL_HOVER, self.rect.center, self.radius + 2, 2
            )

        if self.role == TerminalRole.INPUT and self.is_connected_to:
            pygame.draw.circle(
                surface, COLOR_ORANGE_CONNECT, self.rect.center, int(self.radius * 0.3)
            )


class Component:
    """Representa um componente elétrico como um Disjuntor (DJ), DR ou Carga."""

    def __init__(
        self, id_: str, name: str, rect: pygame.Rect, comp_type: ComponentType
    ):
        self.id = id_
        self.name = name
        self.rect = rect
        self.component_type = comp_type
        self.terminals: List[Terminal] = []
        self.font = pygame.font.Font(None, 18)

    def add_terminal(
        self,
        id_suffix: str,
        rel_x: float,
        rel_y: float,
        radius: int,
        expected_type: str,
        visual_type: str,
        role: TerminalRole,
        pair_id_suffix: Optional[str] = None,
    ):
        """Adiciona um terminal ao componente com base em posições relativas."""
        abs_pos = pygame.Vector2(
            self.rect.x + int(self.rect.width * rel_x),
            self.rect.y + int(self.rect.height * rel_y),
        )

        terminal_id = f"{self.id}_{id_suffix}"
        paired_full_id = f"{self.id}_{pair_id_suffix}" if pair_id_suffix else None

        term = Terminal(
            terminal_id,
            self.id,
            abs_pos,
            radius,
            expected_type,
            visual_type,
            role,
            pair_id=paired_full_id,
        )
        self.terminals.append(term)
        return term

    def draw(self, surface: pygame.Surface):
        """Desenha o componente e seu nome."""
        pygame.draw.rect(surface, COLOR_LIGHT_GREY, self.rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_GREY, self.rect, 2, border_radius=5)

        text_surf = self.font.render(self.name, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class FaseLigandoOsPontos:
    """Classe principal que gerencia a lógica, estado e desenho da fase."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.screen_width, self.screen_height = self.surface.get_size()

        self.fonte_titulo = pygame.font.Font(None, 42)
        self.fonte_instr = pygame.font.Font(None, 26)
        self.fonte_legenda = pygame.font.Font(None, 22)
        self.fonte_vitoria = pygame.font.Font(None, 74)

        self.texto_titulo = self.fonte_titulo.render(
            "Ligando os Circuitos com Dispositivos de Proteção", True, COLOR_WHITE
        )
        self.texto_instrucoes = self.fonte_instr.render(
            "Conecte os fios. [R] para Resetar. [ESC] para Sair.", True, COLOR_WHITE
        )
        self.texto_vitoria_surf: Optional[pygame.Surface] = None

        self.components: Dict[str, Component] = {}
        self.source_terminals: List[Terminal] = []
        self.connections: List[Tuple[str, str, WireType]] = []

        self.dragging_wire: Optional[WireDragState] = None
        self.hovered_terminal: Optional[Terminal] = None
        self.terminal_radius = max(8, int(self.screen_height * 0.012))
        self.vitoria_alcancada = False

        self._setup_scene_from_config(SCENE_CONFIG)

    def _get_terminal_by_id(self, terminal_id: Optional[str]) -> Optional[Terminal]:
        """Encontra um terminal em qualquer lugar da cena pelo seu ID."""
        if not terminal_id:
            return None

        for term in self.source_terminals:
            if term.id == terminal_id:
                return term

        for comp in self.components.values():
            for term in comp.terminals:
                if term.id == terminal_id:
                    return term
        return None

    def _setup_scene_from_config(self, config: Dict[str, Any]):
        """Cria a cena dinamicamente a partir de um dicionário de configuração."""
        self.components.clear()
        self.source_terminals.clear()
        self.connections.clear()
        self.vitoria_alcancada = False
        self.texto_vitoria_surf = None

        num_sources = len(config["source_types"])
        source_y_pos = self.screen_height * 0.15
        source_total_width = self.screen_width * 0.7
        source_spacing = source_total_width / (num_sources - 1)
        source_x_start = (self.screen_width - source_total_width) / 2

        for i, wire_type in enumerate(config["source_types"]):
            pos = pygame.Vector2(source_x_start + i * source_spacing, source_y_pos)
            term = Terminal(
                f"source_{wire_type.value}",
                "source_bar",
                pos,
                self.terminal_radius,
                wire_type.value,
                wire_type.value,
                TerminalRole.SOURCE,
            )
            self.source_terminals.append(term)

        num_circuits = len(config["circuits"])
        circuit_col_width = self.screen_width / num_circuits
        y_positions = [
            self.screen_height * 0.35,
            self.screen_height * 0.55,
            self.screen_height * 0.75,
        ]

        for i, circuit_data in enumerate(config["circuits"]):
            col_center_x = (i + 0.5) * circuit_col_width

            for j, comp_data in enumerate(circuit_data["components"]):
                comp_w = int(
                    self.screen_width * 0.08 * comp_data.get("width_multiplier", 1.0)
                )
                comp_h = int(
                    self.screen_height
                    * (0.08 if comp_data["type"] == ComponentType.CARGA else 0.12)
                )
                comp_rect = pygame.Rect(
                    col_center_x - comp_w / 2, y_positions[j], comp_w, comp_h
                )

                comp = Component(
                    comp_data["id"], comp_data["name"], comp_rect, comp_data["type"]
                )

                for term_data in comp_data["terminals"]:
                    id_suffix, rel_x, expected, visual = (
                        term_data[0],
                        term_data[1],
                        term_data[2],
                        term_data[3],
                    )
                    is_load = comp.component_type == ComponentType.CARGA

                    if is_load:
                        rel_y_in, role_in = (
                            (term_data[4] if len(term_data) > 4 else 0.3),
                            TerminalRole.INPUT,
                        )
                        comp.add_terminal(
                            id_suffix,
                            rel_x,
                            rel_y_in,
                            self.terminal_radius,
                            expected,
                            visual,
                            role_in,
                        )
                    else:
                        pair_id = f"out_{id_suffix.split('_')[1]}"
                        comp.add_terminal(
                            id_suffix,
                            rel_x,
                            0.2,
                            self.terminal_radius,
                            expected,
                            visual,
                            TerminalRole.INPUT,
                            pair_id,
                        )
                        comp.add_terminal(
                            pair_id,
                            rel_x,
                            0.8,
                            self.terminal_radius,
                            expected,
                            visual,
                            TerminalRole.OUTPUT,
                            id_suffix,
                        )

                self.components[comp.id] = comp

    def _can_connect(self, start: Terminal, end: Terminal) -> bool:
        """Verifica se uma conexão entre dois terminais é válida usando cláusulas de guarda."""

        if not start or not end or start == end:
            return False
        if end.is_connected_to:
            return False
        if not (
            start.role in [TerminalRole.SOURCE, TerminalRole.OUTPUT]
            and end.role == TerminalRole.INPUT
        ):
            return False

        provided_type = start.actual_provided_type
        if start.role == TerminalRole.OUTPUT and not provided_type:
            return False

        start_comp = self.components.get(start.parent_component_id)
        end_comp = self.components.get(end.parent_component_id)
        if not end_comp:
            return False

        if (
            end_comp.component_type == ComponentType.DJ
            and start.role != TerminalRole.SOURCE
        ):
            return False
        if end_comp.component_type == ComponentType.DR and (
            not start_comp or start_comp.component_type != ComponentType.DJ
        ):
            return False
        if end_comp.component_type == ComponentType.CARGA:
            if provided_type != WireType.PE and (
                not start_comp or start_comp.component_type != ComponentType.DR
            ):
                return False

        if end.expected_wire_type == "Fase" and provided_type not in [
            WireType.R,
            WireType.S,
            WireType.T,
        ]:
            return False
        if end.expected_wire_type == "N" and provided_type != WireType.N:
            return False
        if end.expected_wire_type == "PE" and provided_type != WireType.PE:
            return False

        if provided_type in [WireType.R, WireType.S, WireType.T]:
            for term in end_comp.terminals:
                if (
                    term.role == TerminalRole.INPUT
                    and term.is_connected_to
                    and term.connected_wire_type == provided_type
                ):
                    return False

        return True

    def _check_win_condition(self):
        """Verifica se todas as cargas estão completamente conectadas."""
        for comp in self.components.values():
            if comp.component_type == ComponentType.CARGA:
                for terminal in comp.terminals:
                    if (
                        terminal.role == TerminalRole.INPUT
                        and not terminal.is_connected_to
                    ):
                        return False

        self.vitoria_alcancada = True
        self.texto_vitoria_surf = self.fonte_vitoria.render(
            "FASE CONCLUÍDA!", True, COLOR_GREEN_WIN
        )
        print("FASE CONCLUÍDA! Todas as cargas conectadas.")
        return None

    def run(self):
        """Loop principal do jogo."""
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.atualizar(events)
            self.desenhar()
            pygame.display.flip()

    def atualizar(self, events: List[pygame.event.Event]):
        """Atualiza o estado do jogo a cada frame."""
        if self.vitoria_alcancada:
            self._handle_events_victory(events)
            return

        mouse_pos = pygame.mouse.get_pos()
        self._update_hover_status(mouse_pos)
        self._handle_events_playing(events)
        self._update_drag_state(mouse_pos)

    def _handle_events_playing(self, events: List[pygame.event.Event]):
        """Processa a entrada do usuário durante o jogo."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._setup_scene_from_config(SCENE_CONFIG)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered_terminal:
                    can_start_drag = (
                        self.hovered_terminal.role == TerminalRole.SOURCE
                        or (
                            self.hovered_terminal.role == TerminalRole.OUTPUT
                            and self.hovered_terminal.actual_provided_type
                        )
                    )

                    if can_start_drag:
                        self.dragging_wire = WireDragState(
                            self.hovered_terminal,
                            self.hovered_terminal.actual_provided_type,
                        )

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging_wire and self.hovered_terminal:
                    start_term = self.dragging_wire.start_terminal
                    end_term = self.hovered_terminal

                    if self._can_connect(start_term, end_term):
                        self.connections.append((
                            start_term.id,
                            end_term.id,
                            self.dragging_wire.wire_type,
                        ))
                        end_term.is_connected_to = start_term.id
                        end_term.connected_wire_type = self.dragging_wire.wire_type

                        if end_term.pair_id:
                            paired_output = self._get_terminal_by_id(end_term.pair_id)
                            if (
                                paired_output
                                and paired_output.role == TerminalRole.OUTPUT
                            ):
                                paired_output.set_actual_provided_type(
                                    self.dragging_wire.wire_type
                                )

                        self._check_win_condition()

                self.dragging_wire = None

    def _handle_events_victory(self, events: List[pygame.event.Event]):
        """Processa a entrada do usuário na tela de vitória."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._setup_scene_from_config(SCENE_CONFIG)

    def _update_hover_status(self, mouse_pos: Tuple[int, int]):
        """Verifica se o mouse está sobre um terminal válido."""
        self.hovered_terminal = None
        all_terminals = self.source_terminals + [
            t for c in self.components.values() for t in c.terminals
        ]

        for term in all_terminals:
            if term.rect.collidepoint(mouse_pos):
                if self.dragging_wire:
                    if self._can_connect(self.dragging_wire.start_terminal, term):
                        self.hovered_terminal = term
                else:
                    if term.role == TerminalRole.SOURCE or (
                        term.role == TerminalRole.OUTPUT and term.actual_provided_type
                    ):
                        self.hovered_terminal = term
                break

    def _update_drag_state(self, mouse_pos: Tuple[int, int]):
        """Atualiza a posição do fio que está sendo arrastado."""
        if self.dragging_wire:
            self.dragging_wire.mouse_pos = mouse_pos

    def desenhar(self):
        """Desenha todos os elementos da cena na tela."""
        self.surface.fill(COLOR_BACKGROUND)
        self._draw_sources()
        self._draw_circuit_labels()
        self._draw_components_and_terminals()
        self._draw_connections()

        if self.dragging_wire:
            self._draw_dragging_wire()

        self._draw_ui_overlay()

        if self.vitoria_alcancada:
            self._draw_victory_message()

    def _draw_sources(self):
        """Desenha as fontes de energia na parte superior."""
        for term in self.source_terminals:
            color = WIRE_TYPE_TO_COLOR[term.actual_provided_type]
            pygame.draw.line(self.surface, color, (term.pos.x, 0), term.pos, 5)
            term.draw(self.surface, is_hovered=(self.hovered_terminal == term))

    def _draw_circuit_labels(self):
        """Desenha os nomes das colunas de circuitos."""
        num_circuits = len(SCENE_CONFIG["circuits"])
        circuit_col_width = self.screen_width / num_circuits
        y_label = self.screen_height * 0.28

        for i, circuit_data in enumerate(SCENE_CONFIG["circuits"]):
            col_center_x = (i + 0.5) * circuit_col_width
            label_surf = self.fonte_legenda.render(
                circuit_data["label"], True, COLOR_WHITE
            )
            label_rect = label_surf.get_rect(centerx=col_center_x, y=y_label)
            self.surface.blit(label_surf, label_rect)

    def _draw_components_and_terminals(self):
        """Desenha cada componente e seus respectivos terminais."""
        for comp in self.components.values():
            comp.draw(self.surface)
            for t in comp.terminals:
                is_hovered = (self.hovered_terminal == t) and not self.vitoria_alcancada
                t.draw(self.surface, is_hovered=is_hovered)

    def _draw_connections(self):
        """Desenha as linhas das conexões feitas."""
        for start_id, end_id, wire_type in self.connections:
            start_term = self._get_terminal_by_id(start_id)
            end_term = self._get_terminal_by_id(end_id)
            if start_term and end_term:
                color = WIRE_TYPE_TO_COLOR.get(wire_type, COLOR_GREY)
                pygame.draw.line(self.surface, color, start_term.pos, end_term.pos, 4)

    def _draw_dragging_wire(self):
        """Desenha a linha do fio sendo arrastado pelo mouse."""
        if not self.dragging_wire:
            return

        start_pos = self.dragging_wire.start_terminal.pos
        end_pos = self.dragging_wire.mouse_pos
        wire_color = WIRE_TYPE_TO_COLOR.get(self.dragging_wire.wire_type, COLOR_GREY)

        pygame.draw.line(self.surface, wire_color, start_pos, end_pos, 4)
        pygame.draw.circle(self.surface, wire_color, end_pos, 6)
        pygame.draw.circle(self.surface, COLOR_WHITE, end_pos, 6, 1)

    def _draw_ui_overlay(self):
        """Desenha os textos fixos da interface, como título e instruções."""
        title_rect = self.texto_titulo.get_rect(
            centerx=self.screen_width / 2, y=self.screen_height * 0.02
        )
        self.surface.blit(self.texto_titulo, title_rect)

        instr_rect = self.texto_instrucoes.get_rect(
            centerx=self.screen_width / 2, y=self.screen_height * 0.94
        )
        self.surface.blit(self.texto_instrucoes, instr_rect)

    def _draw_victory_message(self):
        """Desenha a mensagem de vitória centralizada."""
        if not self.texto_vitoria_surf:
            return

        rect_vitoria = self.texto_vitoria_surf.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2)
        )
        padding = 20
        bg_rect = rect_vitoria.inflate(padding * 2, padding * 2)

        bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))

        self.surface.blit(bg_surf, bg_rect.topleft)
        pygame.draw.rect(
            self.surface, COLOR_GREEN_WIN, bg_rect, width=3, border_radius=10
        )
        self.surface.blit(self.texto_vitoria_surf, rect_vitoria)
