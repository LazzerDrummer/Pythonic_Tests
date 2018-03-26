
def quick_sort(arr):
    less = []
    pivot_list = []
    more = []
    if len(arr) <= 1:
        return arr
    for num in arr:
        pivot = arr[0]
        if num < pivot:
            less.append(num)
        elif num > pivot:
            more.append(num)
        else:
            pivot_list.append(num)
    less = quick_sort(less)
    more = quick_sort(more)
    return less + pivot_list + more


a = [1, 3, 7, 2, 4, 9]
print(quick_sort(a))
