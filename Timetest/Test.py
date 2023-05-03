from time import time


def time_test(func):
    print('- - - НАЧАЛО ТЕСТА - - -')
    time_start = time()
    print(f'РЕЗУЛЬТАТ --> {func} <-- РЕЗУЛЬТАТ')
    print(f'КОНТРОЛЬНОЕ ВРЕМЯ --> {time() - time_start} <-- КОНТРОЛЬНОЕ ВРЕМЯ')
    print('- - - КОНЕЦ ТЕСТА - - -')