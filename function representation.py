grid = []


for nr in range(12):
    grid.append(40 * " " + "|" + 40 * " ")

grid.append(81 * "-")

for nr in range(12):
    grid.append(40 * " " + "|" + 40 * " ")


def prent():
    for line in grid:
        print(line)


# ax^b + cx^d + ex + f
list_of_points = []


def function(a, b, c, d, e, f):
    a = a / 4
    c = c / 4
    e = e / 4
    global list_of_points, grid
    for x in range(-40, 41):
        if x == 0:
            x = 0.0001
        y = a * x ** b + c * x ** d + e * x + f
        pt = []
        if abs(x) < 40.5 and abs(y) < 12.5 and type(y) != complex:
            x = round(x)
            y = round(y)
            pt.append(x)
            pt.append(y)
            list_of_points.append(pt)
    print(list_of_points)

    # here beginth the implementation in the grid
    for point in list_of_points:
        x = point[0]
        y = point[1]
        liney = -y + 12
        indx = x + 40
        new_line = grid[liney][:indx] + "*" + grid[liney][indx + 1:]
        grid[liney] = new_line
    prent()


function(0.02, 3, 0.5, 2, -10, -1)
