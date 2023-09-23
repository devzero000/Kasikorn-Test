import random


def unstable_sort(data, func):
    return sorted(data, key=lambda x: (func(x), random.random()))


def stable_sort(data, key):
    index_data = [(i, item) for i, item in enumerate(data)]
    unstable_sorted_arr = unstable_sort(index_data, func=lambda x: (key(x[1]), x[0]))
    return [item[1] for item in unstable_sorted_arr]

arr = [
    {'name': 'cat', 'city': 'BKK'},
    {'name': 'fish', 'city': 'BKK'},
    {'name': 'ant', 'city': 'BKK'},
    {'name': 'dog', 'city': 'LONDON'}
]


def get_city(o):
    return o['city']


unsorted_arr = unstable_sort(arr, get_city)
print(unsorted_arr)

sorted_arr = stable_sort(arr, get_city)
print(sorted_arr)

