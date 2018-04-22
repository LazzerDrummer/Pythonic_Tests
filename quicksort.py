
def quick_sort(list):
    less = []
    pivot_list = []
    more = []
    if len(list) <= 1:
        return list
    for num in list:
        pivot = list[0]
        if num < pivot:
            less.append(num)
        elif num > pivot:
            more.append(num)
        else:
            pivot_list.append(num)
    less = quick_sort(less)
    more = quick_sort(more)
    return less + pivot_list + more


A = [2000, 8, 1, 4, 14, 7, 16, 10, 9, 3]
B = quick_sort(A)
print(B)
