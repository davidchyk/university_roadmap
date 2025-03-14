def calculate_variant(group_number, student_index):
    """
    Обчислення варіанту за формулою:
    Z = (student_index + group_number % 60) % 30 + 1
    """

    return (student_index + group_number % 60) % 30 + 1

def build_relation_S(set_A, set_B, gender):
    """
    Формує відношення S: aSb, якщо a мати b.
    Умови:
      - a повинна бути жіночої статі (gender[a] == 'female')
      - a не може дорівнювати b
    """
    relation_S = set()
    for a in set_A:
        if gender.get(a, '') == 'female':
            for b in set_B:
                if a != b:
                    relation_S.add((a, b))
    return relation_S

def build_relation_R(set_A, set_B, gender):
    """
    Формує відношення R: aRb, якщо a свекруха b.
    Умови:
      - a повинна бути жіночої статі
      - b повинна бути чоловічої статі
      - a не може дорівнювати b
    """
    relation_R = set()
    for a in set_A:
        if gender.get(a, '') == 'female':
            for b in set_B:
                if a != b and gender.get(b, '') == 'male':
                    relation_R.add((a, b))
    return relation_R

def build_matrix(relation, set_A, set_B):
    """
    Створює матричне представлення відношення.
    Рядки відповідають елементам з set_A, а стовпці – з set_B.
    Якщо пара (a, b) належить відношенню, ставимо 1, інакше 0.
    """
    matrix = []
    for a in set_A:
        row = []
        for b in set_B:
            row.append(1 if (a, b) in relation else 0)
        matrix.append(row)
    return matrix

def inverse_relation(relation):
    """
    Обчислює обернений зв’язок (інверсію) відношення.
    """
    return {(b, a) for (a, b) in relation}