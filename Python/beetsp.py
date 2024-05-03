import matplotlib.pyplot as plt

def plot_tsp(coords_file, route_file):
    # read coords
    with open(coords_file, 'r') as f:
        coords = f.readlines()
        coords_list = []
        for cord in coords:
            c = cord.strip()
            c = c.split(' ')
            coords_list.append((float(c[0]), float(c[1])))

    with open(route_file, 'r') as f:
        route = f.read()
        route_list = route.split(' ')

    # calculate distance of route
    dist = 0
    for i in range(len(route_list)-1):
        dist += ((coords_list[int(route_list[i])][0] - coords_list[int(route_list[i+1])][0])**2 + (coords_list[int(route_list[i])][1] - coords_list[int(route_list[i+1])][1])**2)**0.5

    # plot
    x = []
    y = []
    for i in route_list:
        x.append(coords_list[int(i)][0])
        y.append(coords_list[int(i)][1])
    plt.plot(x, y, 'o-')
    plt.title('Distance: ' + str(dist))
    plt.show()

if __name__ == '__main__':
    plot_tsp('coords.txt', 'route.txt')