"""
Есть абстрактная задача:

У нас есть лес из json массива

Гораздо дешевле в качестве транспорта их передавать в виде списка кортежей

(вида ключ: значение),

(ключ.ключ: значение)

Пример:
"""
import json
from typing import Any, List, Tuple

forest = {'b': 1,
          'c': {'d': 2,
                'f': 3,
                },
          'e': {'i': 4,
                'j': {'k': 5,
                      'l': 6,
                      },
                },
          'm': {'n': 7,
                'o': {'p': 8,
                      'r': {'s': 9,
                            't': 10,
                            },
                      },
                },
          }

# Переводим в такой вид:
result = [('b', 1), ('c.d', 2), ('c.f', 3), ('e.i', 4), ('e.j.k', 5), ('e.j.l', 6), ('m.n', 7),
          ('m.o.p', 8), ('m.o.r.s', 9), ('m.o.r.t', 10), ]


def dict_to_list(sub_tree: dict, current_name: str, items_list: List[tuple]) -> List[tuple]:

    for key in sub_tree:
        if isinstance(sub_tree[key], dict):
            dict_to_list(sub_tree=sub_tree[key], current_name=current_name + key, items_list=items_list)
        else:
            items_list.append(('.'.join(current_name + key), sub_tree[key]))
    return items_list


res = dict_to_list(forest, '', [])
print(res)


# Reverse task:


def list_to_dict(data: List[Tuple['str', int]]) -> dict:
    tree = {}
    for item in data:
        curr_tree = tree
        keys = item[0].split('.')
        for i in range(0, len(keys)):
            if i == len(keys) - 1:
                curr_tree[keys[i]] = item[1]
            elif keys[i] not in curr_tree:
                curr_tree[keys[i]] = {}
            curr_tree = curr_tree[keys[i]]
    return tree


parsed = json.dumps(list_to_dict(result), indent=4)
print(parsed)
