from typing import Dict
import random
from datetime import datetime
from multiprocessing import Pool


ACCURACY = 10 ** 8  # our ACCURACY to count PI
PROC_NUMBER = 5


def dots_in_circle(n: int) -> Dict[str, int]:

    inside, outside, one = 0, 0, 0
    for step in range(int(ACCURACY*n/PROC_NUMBER), int(ACCURACY*(n+1)/PROC_NUMBER)):
        x = random.randint(0, ACCURACY)/ACCURACY  # 0 < x < 1
        y = random.randint(0, ACCURACY)/ACCURACY  # 0 < y < 1

        # dot inside circle or outside it
        if x**2 + y**2 < 1:
            inside += 1
        elif x**2 + y**2 == 1:
            one += 1
        else:
            outside += 1
    print(f'dots inside: {inside}, all dots: {outside}', f'On line: {one}')
    return {'inside': inside, 'outside': outside, 'ONE': one}


now = datetime.now()

nums = range(0, PROC_NUMBER)

processes = Pool(processes=PROC_NUMBER)
all_dots = processes.map(dots_in_circle, nums)
processes.close()

dots_inside_circle, dots_outside_circle, dots_on_circle_line = 0, 0, 0

for item in all_dots:
    dots_inside_circle += item["inside"]
    dots_on_circle_line += item["ONE"]
    dots_outside_circle += item["outside"]

end = datetime.now()
print('execution time (seconds):', (end-now).seconds)
print(f'dots inside: {dots_inside_circle}, dots outside: {dots_outside_circle}, On line: {dots_on_circle_line}')
print(dots_inside_circle/ACCURACY*4)
