answers = {
    (0, 1): "DISJUNTOR",
    (1, 0): "FIO",
    (1, 4): "Neutro",  # Agora com espaço explícito
    (2, 0): "volts",
    (2, 6): "fase",
    (3, 1): "CIRCUITO",
    (4, 0): "PAINEL",
    (4, 7): "dps",
    (5, 0): "neon",
    (5, 5): "terra",
    (6, 0): "watts",
    (6, 6): "luz",
    (7, 1): "Fio-Duplo",
    (8, 0): "CC",
    (8, 3): "CA",
    (8, 6): "QDC",
    (9, 0): "POSTE",
    (9, 7): "FDP"
}

def normalize_input(answer):
    # Troca hífen por espaço
    return answer.replace('-', ' ').upper()

def check_answer(row, block, cell_letters):
    start_col, end_col = block
    user_answer = ''.join(cell_letters[row][c] for c in range(start_col, end_col + 1))

    correct_answer = answers.get((row, start_col))
    if correct_answer is None:
        return None

    return normalize_input(user_answer) == normalize_input(correct_answer)


# Falta a configuração da msg quando terminar sabomba ou passar para o prox exercicio sla
# oq aqueles bobo quer
def all_correct(cell_letters):
    from cruzadinha.grid import find_block

    for (row, start_col), correct_answer in answers.items():
        _, end_col = find_block(row, start_col)
        user_answer = ''.join(cell_letters[row][c] for c in range(start_col, end_col + 1))
        if normalize_input(user_answer) != normalize_input(correct_answer):
            return False
    return True
