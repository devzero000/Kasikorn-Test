def can_solve(a, b):
    n = len(a)
    result = []
    map_value = set()
    for i in range(n):
        for j in range(n):
            map_value.add(a[i] + a[j])

    for i in b:
        for j in a:
            if (i - j) in map_value:
                result.append(1)
                break
        else:
            result.append(0)

    return result


a = [5, 2, 3, 4, 10]
b = [10]

print(can_solve(a, b))
