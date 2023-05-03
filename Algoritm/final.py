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


class Graph:
    def __init__(self, father_der, sub_der, character):
        self.graph = self.__all_graph_init(father_der, sub_der, character)

    def __all_graph_init(self, father_der, sub_der, character):
        final_dikt = {}
        for i in father_der:
            final_dikt.update(self.__graph_init(sub_der, {i: father_der[i]}, character))
        return final_dikt

    def __graph_init(self, sub_der, old_cd, character):
        """Графа где водиться суб директория и один элемент из директории стоящей над ней + character(символ остановки)"""
        # примечание: old_connection_directory == old_cd, subdirectory == sub_der, new_connection_directory == new_cd
        # важно, чтобы в поддиректории сначала шли завершающие дорожки
        new_cd = {}
        # в будущем понадобиться
        for past_path in old_cd:
            # переберем все возможные "пути"

            if past_path[-1] != character:
                # если символ не равен завершающему, то продолжим иначе сразу вносим в готовую директорию
                # создали базовый случай

                # last_item = None
                # вводим переменную последний item

                for sub_item in sub_der:
                    # переберем все значения подкаталога

                    if past_path[-1] == sub_item[0] and sub_item not in past_path:
                        # если найдём в подкаталоге путь начинающийся, на то, на что заканчивается наш последний элемент,
                        # но при этом он не одинаковый с нашим то

                        new_cd[past_path + sub_item[1]] = old_cd[past_path] + sub_der[sub_item]
                        # занесём его в новую директорию

            else:
                # внесли готовые элементы в директорию
                new_cd[past_path] = old_cd[past_path]

        # вносим все новые пути и элементы оканчивающиеся на последний символ в новую директорию
        if new_cd != old_cd:
            # если старый список равен новому мы максимально углубились и нашли все пути
            return self.__graph_init(sub_der, new_cd, character)
        return new_cd

    def all_paths(self):
        return self.graph

    def minimal(self, obj=None):
        if obj:
            return min(obj.graph, key=lambda k: obj.graph[k])
        return min(self.graph, key=lambda k: self.graph[k])

    def maximal(self, obj=None):
        if obj:
            return max(obj.graph, key=lambda k: obj.graph[k])
        return max(self.graph, key=lambda k: self.graph[k])

    def __len__(self):
        return len(self.graph)

    def __repr__(self):
        return self.graph

    def __str__(self):
        srting = ''
        for key, val in self.graph.items():
            srting += f'{key} = {val}, '
        return srting[:-2]
