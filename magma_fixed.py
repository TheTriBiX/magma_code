s_table = [
    ['1100', '0100', '0110', '0010', '1010', '0101', '1011', '1001', '1110', '1000', '1101', '0111', '0000', '0011',
     '1111', '0001'],
    ['0110', '1000', '0010', '0011', '1001', '1010', '0101', '1100', '0001', '1110', '0100', '0111', '1011', '1101',
     '0000', '1111'],
    ['1011', '0011', '0101', '1000', '0010', '1111', '1010', '1101', '1110', '0001', '0111', '0100', '1100', '1001',
     '0110', '0000'],
    ['1100', '1000', '0010', '0001', '1101', '0100', '1111', '0110', '0111', '0000', '1010', '0101', '0011', '1110',
     '1001', '1011'],
    ['0111', '1111', '0101', '1010', '1000', '0001', '0110', '1101', '0000', '1001', '0011', '1110', '1011', '0100',
     '0010', '1100'],
    ['0101', '1101', '1111', '0110', '1001', '0010', '1100', '1010', '1011', '0111', '1000', '0001', '0100', '0011',
     '1110', '0000'],
    ['1000', '1110', '0010', '0101', '0110', '1001', '0001', '1100', '1111', '0100', '1011', '0000', '1101', '1010',
     '0011', '0111'],
    ['0001', '0111', '1110', '1101', '0000', '0101', '1000', '0011', '0100', '1111', '1010', '0110', '1001', '1100',
     '1011', '0010']]
s_main_table = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011',
                '1100', '1101', '1110', '1111']


def block(string, block_len):
    # примнимает на вход строку и возвращает массив из этой строки где каждый блок равен длине block_len
    words = []
    for i in range(len(string) // block_len):
        word = string[i * block_len:(i + 1) * block_len]
        words.append(word)
    return words


def to_bits(s):
    # принимает на вход строку и преобразует ее в двоичную строку
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([str(b) for b in bits])
    return ''.join(result)


def from_bits(bits):
    # принимает двоичную строку и возвращает текстовую строку
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def xor(a, b):
    # принимает два числа и возваращет их xor
    res = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            res += '0'
        else:
            res += '1'
    return res


def sum_bits(a, b):
    # принимает два числа в двоичной системе и возвращает их сумму
    res = (int(a, 2) + int(b, 2))
    res = bin(res)[2::]
    if len(res) > 32:
        res = res[0:32]
    return res


def len_x(res, x):
    # принимает строку и добавет ведущие ноли так что длина строки становится x
    if len(str(res)) < x:
        res = '0' * (x - len(str(res))) + str(res)
    return str(res)


def cycle_sdvig(res):
    # принимает на вход строку и циклически сдвигает ее на 11 символов
    res = res[11::] + res[0:11:]
    return res


def encrypt(bit_text, keys):
    REVERSED = False  # флаг обозначающий разворот массива для последних раундов
    left_part, right_part = block(bit_text, 32)  # разбиваю текст на левую и правую часть длиной 32 бита
    for i in range(32):  # начинаем 32 раунда
        if i < 24:  # первые 24 раунда
            first_step = sum_bits(right_part, keys[i % 8])  # складываем
            first_step = len_x(first_step, 32)  # удлиняем если нужно
            # print(first_step)
            second_step = block(first_step, 4)  # делим блоки на 4-битовые
            # print(second_step)
            for n in range(len(second_step)):  # заменяю через таблицу замен
                second_step[n] = s_table[n][s_main_table.index(second_step[n])]
            second_step = ''.join(second_step)  # присоеденяем блоки
            third_step = cycle_sdvig(second_step)  # циклически сдвигаем на 11
            fourth_step = xor(left_part, third_step)  # xor левого блока с тем что получилось в 3 шаге
            left_part, right_part = right_part, fourth_step
            # Получившееся 32-битное число записывается в правую половину блока,
            # а старое содержимое правой половины переносится в левую половину блока.
        else:  # оставшиеся 8 проходят на ключах в обратном порядке
            if not REVERSED:
                keys = keys[::-1]
                REVERSED = True
            first_step = sum_bits(right_part, keys[i % 8])  # складываем
            first_step = len_x(first_step, 32)  # удлиняем если нужно
            # print(first_step)
            second_step = block(first_step, 4)  # делим блоки на 4-битовые
            # print(second_step)
            for n in range(len(second_step)):  # заменяю через таблицу замен
                second_step[n] = s_table[n][s_main_table.index(second_step[n])]
            second_step = ''.join(second_step)  # присоеденяем блоки
            third_step = cycle_sdvig(second_step)  # циклически сдвигаем на 11
            fourth_step = xor(left_part, third_step)  # xor левого блока с тем что получилось в 3 шаге
            left_part, right_part = right_part, fourth_step
            # Получившееся 32-битное число записывается в правую половину блока,
            # а старое содержимое правой половины переносится в левую половину блока.
    return right_part + left_part


def decrypt(bit_text, keys):
    REVERSED = False  # флаг обозначающий разворот массива для последних раундов
    left_part, right_part = block(bit_text, 32)  # разбиваю текст на левую и правую часть длиной 32 бита
    for i in range(32):  # начинаем 32 раунда
        if i < 8:
            first_step = sum_bits(right_part, keys[i % 8])  # складываем
            first_step = len_x(first_step, 32)  # удлиняем если нужно
            # print(first_step)
            second_step = block(first_step, 4)  # делим блоки на 4-битовые
            # print(second_step)
            for n in range(len(second_step)):  # заменяю через таблицу замен
                second_step[n] = s_table[n][s_main_table.index(second_step[n])]
            second_step = ''.join(second_step)  # присоеденяем блоки
            third_step = cycle_sdvig(second_step)  # циклически сдвигаем на 11
            fourth_step = xor(left_part, third_step)  # xor левого блока с тем что получилось в 3 шаге
            left_part, right_part = right_part, fourth_step
            # Получившееся 32-битное число записывается в правую половину блока,
            # а старое содержимое правой половины переносится в левую половину блока.
        else:
            if not REVERSED:
                keys = keys[::-1]
                REVERSED = True
            first_step = sum_bits(right_part, keys[i % 8])  # складываем
            first_step = len_x(first_step, 32)  # удлиняем если нужно
            # print(first_step)
            second_step = block(first_step, 4)  # делим блоки на 4-битовые
            # print(second_step)
            for n in range(len(second_step)):  # заменяю через таблицу замен
                second_step[n] = s_table[n][s_main_table.index(second_step[n])]
            second_step = ''.join(second_step)  # присоеденяем блоки
            third_step = cycle_sdvig(second_step)  # циклически сдвигаем на 11
            fourth_step = xor(left_part, third_step)  # xor левого блока с тем что получилось в 3 шаге
            left_part, right_part = right_part, fourth_step
            # Получившееся 32-битное число записывается в правую половину блока,
            # а старое содержимое правой половины переносится в левую половину блока.
    return right_part + left_part


if __name__ == '__main__':
    with open('input.txt', mode='r', encoding='utf-8') as f:
        text = f.read()
    answer = []
    bit_text = to_bits(text)
    if len(bit_text) % 64 != 0:
        bit_text = len_x(bit_text, (len(bit_text) // 64 + 1) * 64)
    bit_blocs = block(bit_text, 64)
    mode = input('Введите "1" для шифровки, "2" для расшифровки: ')
    key = 'asdfkljkcmfjhygbnaijhgbnhkiolmnb'
    bit_key = to_bits(key)
    KEYS = block(bit_key, 32)  # разбиваю ключи на блоки длиной 32
    if mode == '1':
        for i in bit_blocs:
            answer.append(encrypt(i, KEYS))
    if mode == '2':
        for i in bit_blocs:
            answer.append(decrypt(i, KEYS))
    with open('output.txt', mode='w', encoding='utf-8') as write_answer:
        write_answer.write(from_bits(''.join(answer)))
