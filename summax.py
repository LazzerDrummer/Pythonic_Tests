# import copy

pyramid = [[5],
           [2, 4],
           [7, 5, 6],
           [6, 6, 5, 5],
           [3, 4, 3, 4, 4]]
"""
pyramid_graph = copy.deepcopy(pyramid)
y=1
for i in range(len(pyramid)):
    for j in range(i+1):
        pyramid_graph[i][j]=y
        y += 1
"""


def number_position(x, y):
    return ((x * (x + 1)) // 2) + y + 1


def gauss(x):
    return (x * (x + 1)) // 2


def reversed_string(a_string):
    return a_string[::-1]


pyramid_graph = [[number_position(i, j) for j in range(i + 1)]
                 for i in range(len(pyramid))]


def make_road(start_i, start_j, finish_i, finish_j):
    roads.append([pyramid_graph[start_i][start_j],
                  pyramid_graph[finish_i][finish_j]])


def compare_add(row, r, temp_maxvalue, final_maxvalue):
    for j in range(1, r):
        if temp_maxvalue[j - 1] == temp_maxvalue[j]:
            final_maxvalue[j] = row[j] + temp_maxvalue[j - 1]
            make_road(i - 1, j - 1, i, j)
            make_road(i - 1, j, i, j)
        elif temp_maxvalue[j - 1] > temp_maxvalue[j]:
            final_maxvalue[j] = row[j] + temp_maxvalue[j - 1]
            make_road(i - 1, j - 1, i, j)
        else:
            final_maxvalue[j] = row[j] + temp_maxvalue[j]
            make_road(i - 1, j, i, j)


maxvalue = [pyramid[0][0]]
roads = []
i = 0
for i in range(1, len(pyramid)):
    temp = maxvalue.copy()
    n = len(pyramid[i])
    maxvalue[0] += pyramid[i][0]
    maxvalue.append(temp[n - 2] + pyramid[i][n - 1])
    make_road(i - 1, 0, i, 0)
    make_road(i - 1, n - 2, i, n - 1)
    compare_add(pyramid[i], n - 1, temp, maxvalue)

biggest_index = [0]
biggest = 0

for i in range(len(maxvalue)):
    if maxvalue[i] > biggest:
        biggest_index = [i]
        biggest = maxvalue[i]
    elif maxvalue[i] == biggest:
        biggest_index.append(i)

n = gauss(len(pyramid))

graph_matrix = [[0 for x in range(n + 1)] for y in range(n + 1)]

for i in range(len(roads)):
    graph_matrix[roads[i][0]][roads[i][1]] = 1
    graph_matrix[roads[i][1]][roads[i][0]] = 1

"""
def recursive_road_print(graph, i, j):
    print(j + 1, end='')
    if i > 1 :
        if (graph_matrix[graph[i][j]][graph[i - 1][j - 1]]
            and graph_matrix[graph[i][j]][graph[i - 1][j]]):
            recursive_road_print(graph, i - 1, j - 1)
            recursive_road_print(graph, i - 1, j)
        elif graph_matrix[graph[i][j]][graph[i - 1][j]]:
            recursive_road_print(graph, i - 1, j)
        else:
            recursive_road_print(graph, i - 1, j - 1)
    return ' '
"""


def road_print(graph, i, j):
    queue = []
    current_road = ''
    save = []
    while True:
        if i == - 1:
            # print(reversed_string(current_road), end=' ')
            print(reversed_string(current_road))
            if queue:
                print()
                i = queue[len(queue) - 1][0] - 1
                j = queue[len(queue) - 1][1]
                current_road = save.pop()
                queue.pop()
            else:
                break
        if j == 0:
            i -= 1
            current_road += str(j + 1)
            continue
        if i == j:
            while j >= 0:
                current_road += str(j + 1)
                j -= 1
            i = -1
            continue
        if (graph_matrix[graph[i][j]][graph[i - 1][j - 1]]
                and graph_matrix[graph[i][j]][graph[i - 1][j]]):
            queue.append((i, j))
            current_road += str(j + 1)
            save.append(current_road)
            i -= 1
            j -= 1
        elif graph_matrix[graph[i][j]][graph[i - 1][j]]:
            current_road += str(j + 1)
            i -= 1
        else:
            current_road += str(j + 1)
            i -= 1
            j -= 1
    return ''


for i in biggest_index:
    print(road_print(pyramid_graph, len(pyramid_graph) - 1, i))
