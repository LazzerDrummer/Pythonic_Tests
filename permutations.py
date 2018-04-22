def permutation(list, start, end):
    if (start == end):
        print(list)
    else:
        for i in range(start, end + 1):
            list[start], list[i] = list[i], list[start]  # The swapping
            permutation(list, start + 1, end)
            list[start], list[i] = list[i], list[start]


permutation([1, 2, 3, 4, 5, 6], 0, 5)
