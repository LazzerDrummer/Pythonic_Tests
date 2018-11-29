def merge(left, right):
    result = []
    left_idx = 0
    right_idx = 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left:
        result.extend(left[left_idx:])
    if right:
        result.extend(right[right_idx:])

    return result


def merge_sort(list):
    if len(list) == 1:
        return list

    middle = len(list) // 2
    left = list[:middle]
    right = list[middle:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


A = [2000, 8, 1, 4, 14, 7, 16, 10, 9, 3]
B = merge_sort(A)
print(B)
