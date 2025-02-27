from random import sample

def parity(x): return x if x % 2 == 0 else False
def oddity(x): return x if x % 2 != 0 else False

first_list = sample(range(-100, 101), 10)
print(f'Список: {first_list}')

max_parity = max(first_list, key=parity)
max_oddity = max(first_list, key=oddity)
difference = max_oddity - max_parity
closest = min(first_list, key = lambda x: abs(x - difference))

print(f'Індекс максимального парного значення: {first_list.index(max_parity)}')
print(f'Індекс максимального непарного значення: {first_list.index(max_oddity)}')
print(f'Індекс найближчого значення до різниці максимумів: {first_list.index(closest)}')

first_list.remove(closest)
new_list = [x for x in first_list if x + closest > 10]

print(f'Новий список: {new_list}')