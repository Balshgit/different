"""
Есть абстрактная задача:

У нас есть лес из json массива

Гораздо дешевле в качестве транспорта их передавать в виде списка кортежей

(вида ключ: значение),

(ключ.ключ: значение)

Пример:
"""
import json
from typing import Any, List, Tuple, Union, Dict

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
          'a': 11,
          'u': {'w': {'z': {'y': 42,
                            'x': 100,
                            },
                      'f': 12,
                      'b': 15,
                      },
                'q': 90,
                }
          }


# Переводим в такой вид:
result = [('a', 11), ('b', 1), ('c.d', 2), ('c.f', 3), ('e.i', 4), ('e.j.k', 5), ('e.j.l', 6), ('m.n', 7), ('m.o.p', 8),
          ('m.o.r.s', 9), ('m.o.r.t', 10), ('u.q', 90), ('u.w.b', 15), ('u.w.f', 12), ('u.w.z.x', 100), ('u.w.z.y', 42),
          ]


def dict_to_list(sub_tree: dict, current_name: str, items_list: List[tuple]) -> List[tuple]:

    for key in sub_tree:
        if isinstance(sub_tree[key], dict):
            dict_to_list(sub_tree=sub_tree[key], current_name=current_name + key, items_list=items_list)
        else:
            items_list.append(('.'.join(current_name + key), sub_tree[key]))
    return items_list


res = dict_to_list(forest, '', [])
print(sorted(res))


# Reverse task:


def list_to_dict(data: List[Tuple[str, int]]) -> dict:
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


# without recursion

def dict_to_list_without_recursion(data: Dict[str, Union[int, dict]]) -> List[Tuple[str, Union[int, dict]]]:
    result_list = []
    temp_lst = []
    count = 0

    for key, value in data.items():
        if isinstance(value, dict):
            count += 1
        temp_lst.append((key, value))

    for _ in range(count):
        for item in temp_lst:
            if isinstance(item[1], dict):
                temp_lst.remove(item)
                for sub_key, sub_value in item[1].items():
                    temp_lst.append((f'{item[0]}.{sub_key}', sub_value))
            else:
                if item not in result_list:
                    result_list.append(item)

    del temp_lst
    return result_list


res_lst = dict_to_list_without_recursion(forest)
print(sorted(res_lst))
