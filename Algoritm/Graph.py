class Graph:
    def __init__(self, main_dir, sub_dir, character):
        self.main_dir = main_dir
        self.sub_dir = sub_dir
        self.character = character
        self.graph = self.__all_graph_init(self.main_dir, self.sub_dir, self.character)

    def __all_graph_init(self, main_dir, sub_der, character):
        final_dikt = {}
        for i in main_dir:
            final_dikt.update(self.__graph_init(sub_der, {i: main_dir[i]}, character))
        return final_dikt

    def __graph_init(self, sub_dir, old_cd, character):
        """Графа где водиться суб директория и один элемент из директории стоящей над ней + character(символ остановки)"""
        # примечание: old_connection_directory == old_cd, subdirectory == sub_dir, new_connection_directory == new_cd
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

                for sub_item in sub_dir:
                    # переберем все значения подкаталога

                    if past_path[-1] == sub_item[0] and sub_item not in past_path:
                        # если найдём в подкаталоге путь начинающийся, на то, на что заканчивается
                        # наш последний элемент, но при этом он не одинаковый с нашим то

                        new_cd[past_path + sub_item[1]] = old_cd[past_path] + sub_dir[sub_item]
                        # занесём его в новую директорию

            else:
                # внесли готовые элементы в директорию
                new_cd[past_path] = old_cd[past_path]

        # вносим все новые пути и элементы оканчивающиеся на последний символ в новую директорию
        if new_cd != old_cd:
            # если старый список равен новому мы максимально углубились и нашли все пути
            return self.__graph_init(sub_dir, new_cd, character)
        return new_cd

    def maximal(self, obj: object = None):
        if isinstance(obj, Graph):
            return max(obj.graph, key=lambda k: obj.graph[k])
        return max(self.graph, key=lambda k: self.graph[k])

    def minimal(self, obj: object = None):
        if isinstance(obj, Graph):
            return min(obj.graph, key=lambda k: obj.graph[k])
        return min(self.graph, key=lambda k: self.graph[k])

    def _append(self, dir: str, obj: object, val: dict):
        """Сделана для реализации других функций"""
        if dir == 'sub_dir':
            obj.sub_dir.update(val)
            self.__class__.__init__(self, obj.main_dir, obj.sub_dir, obj.character)
        else:
            obj.main_dir.update(val)
            self.__class__.__init__(self, obj.main_dir, obj.sub_dir, obj.character)

    def all_paths(self):
        return self.graph

    def __len__(self):
        return len(self.graph)

    def __repr__(self):
        return self.graph

    def __str__(self):
        line = ''
        for key, val in self.graph.items():
            line += f'{key} = {val}, '
        return line[:-2]


def all_paths(obj: Graph):
    if isinstance(obj, Graph):
        return obj.all_paths()
    raise ValueError("Вводите объект Graph")


def append_sub_dir(obj: Graph, val: dict):
    obj._append('sub_dir', obj, val)
    return True


def append_main_dir(obj: Graph, val: dict):
    obj._append('main_dir', obj, val)
    return True


def minimal(obj: Graph):
    if isinstance(obj, Graph):
        return Graph.minimal(obj)
    raise ValueError("Вводите объект Graph")


def maximal(obj: Graph):
    if isinstance(obj, Graph):
        return Graph.maximal(obj)
    raise ValueError("Вводите объект Graph")