def binary_search(original_list, val, copy_list=False, counter=0, maximum_item=0, minimum_item=0, index=0):
    """Бинарный поиск элемента в отсортированном массиве"""
    if not copy_list:
        # работает только при 1 запуске, тк copy_list=False

        copy_list = list(original_list)
        # создадим копию нашего списка, дабы не утерять его в итоге

        maximum_item = (len(copy_list) - 1) // 2
        # при первом запуске надо инициализировать max

    if len(copy_list) == 1:
        # базовый случай, когда остался 1 элемент

        if copy_list[0] == val:
            # если элемент не равен нашему, то его нет

            return f'индекс в списке {index}, попыток {counter}'
            # вернём результат

        return f'числа {val} нету в списке'
        # вернём результат

    else:
        # случай не базовый ==> рекурсивный, чистим список от лишних элементов

        counter += 1
        # не забываем добавить в счётчик попытку

        if copy_list[maximum_item] < val:
            # работает если максимум меньше нашего число ==> возьмём вторую часть списка

            index += len(copy_list[:maximum_item + 1])
            # +1 для включения максимума в список
            # добавим к индексу длину удалённых элементов

            del copy_list[:maximum_item + 1]
            # +1 для включения максимума в список
            # удалим лишнюю часть ==> первую часть

            maximum_item = (len(copy_list) - 1) // 2
            # определим новый максимум

        elif copy_list[maximum_item] > val:
            # работает если максимум больше нашего число ==> возьмём первую часть списка

            del copy_list[maximum_item:]
            # удалим 2 часть нашего списка

            maximum_item //= 2
            # и определим новый максимум

        else:
            # сработает если максимум окажется нужным числом

            index += len(copy_list[:maximum_item])
            # к индексу добавим длину списка до максимума

            return f'индекс в списке {index}, попыток {counter}'
            # вернём результат

        return binary_search(original_list, val, copy_list, counter, maximum_item, minimum_item, index)
        # сократили список и отправляем все данные, в эту же функцию ==> делаем рекурсию


class LinkedList:
    """Класс для связанного списка, где каждое значение связано со следующим, и предыдущим элементом
    + последний элемент связан с 1"""

    k = 0
    # при создании экземпляра счётчик элементов равен 0

    def __init__(self, data=None):
        """"Инициализируем"""
        if type(data) in (list, tuple, range):
            for i in data:
                self.append(i)
        else:
            self.data = data
            self.previous = None
            self.next = None
            self.k += 1
            # добавим в счётчик 1, тк добавляем новый экземпляр

    def append(self, val):
        """Функция добавления элемента"""
        if type(val) in (list, tuple, range):
            # расширим список выше перечисленными типами данных, если они передаются
            for i in val:
                self.append(i)
        else:
            # при инициализации может предаться список и тд, тогда нам нужно добавить каждый элемент поочерёдно, но чтоб
            # определить первый элемент используем длину
            if len(self) == 0:
                self.__init__(val)
            else:
                self.k += 1
                # добавим в счётчик 1, тк добавляем новый экземпляр
                end = self.__class__(val)
                n = self
                # end = новый экземпляр с переданным знач, n = изменяемая ссылка на тек. экземпляр
                z = self
                # z = ссылка на последний элемент
                while n.next != z and n.next:
                    # Если следующий элемент равен None или первому экземпляру, цикл завершиться.
                    n = n.next
                    # берём следующий элемент и проверяем условие

                n.next = end
                # тогда в ссылку след элемента ставим наш новый экземпляр

                end.next = z
                end.previous = n
                # В параметр down(нашего нового экземпляра) добавим ссылку на прошлый экземпляр ==>
                # на текущий, который итерировали

    def __len__(self):
        """Функция для высчитывания длинны"""
        return self.k

    def __repr__(self):
        # дальше представлен метод для чтения ОЧЕНЬ ЗАТРАТНЫЙ
        # n = self
        # string = str(n.data) + ', '
        # n = n.next
        # while n.previous:
        #     string += str(n.data) + ', '
        #     n = n.next
        # return string[:-2]
        return 'чтение связанного списка списка слишком затратная операция'


def speed_sort(ns_list):
    """Функция быстрой сортировки"""

    if len(ns_list) < 2:
        # базовый случай, если в списке 1 элемент ==> в списке 1 элемент, или больший, или меньший

        # вернём отсортированный список из 1 элемента
        return ns_list
    else:
        # рекурсивный случай

        val = len(ns_list) // 2
        # за начало сортировки берём середину списка

        less_list = [i for i in ns_list if i < ns_list[val]]
        # создаём список с элементами меньше нашего значения

        more_list = [i for i in ns_list if i > ns_list[val]]
        # создаём список с элементами больше нашего значения

        same = [ns_list[val]] * len([i for i in ns_list if i == ns_list[val]])
        # создаём список с элементами равными нашему значению

        # создаём рекурсию, где в середину вставляем все одинаковые элементы, а по сторонам отсортированные
        return speed_sort(less_list) + same + speed_sort(more_list)


def dynamic_store_list(title: list, price: list, max_weight: int):
    cell = [[0 for i in range(max_weight)] for _ in title]
    for mom_t in range(len(title)):
        # mom_t - moment title
        for mom_w in range(max_weight):
            # mom_w - moment weight
            if title[mom_t] - 1 <= mom_w:
                if mom_w + 1 - title[mom_t] > 0:
                    cell[mom_t][mom_w] = (max(price[mom_t] + cell[mom_t - 1][mom_w - title[mom_t]], cell[mom_t - 1][mom_w]))
                else:
                    cell[mom_t][mom_w] = (max(price[mom_t], cell[mom_t - 1][mom_w]))
            else:
                cell[mom_t][mom_w] = (cell[mom_t - 1][mom_w])
    return cell


def dynamic_store_dict(product_list: dict, max_weight: int):
    cell = [[(0, list()) for _ in range(max_weight)] for _ in product_list]
    mom_t = -1
    # mom_t - moment title
    for key, values in product_list.items():
        mom_t += 1
        for mom_w in range(max_weight):
            # mom_w - moment weight
            if values[0] - 1 <= mom_w:
                if mom_w + 1 - values[0] > 0:
                    cell[mom_t][mom_w] = (max(values[1] + cell[mom_t - 1][mom_w - values[0]][0], cell[mom_t - 1][mom_w][0]), cell[mom_t - 1][mom_w][1] + [key])
                else:
                    cell[mom_t][mom_w] = (max(values[1], cell[mom_t - 1][mom_w][0]), cell[mom_t - 1][mom_w][1] + [key])
            else:
                cell[mom_t][mom_w] = (cell[mom_t - 1][mom_w])
    return cell