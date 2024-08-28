import matplotlib.pyplot as plt
import numpy as np

def distance(p1, p2):
    """Обчислення відстані між двома точками."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force(points):
    """Брутфорс метод для знаходження найближчої пари точок.
    Перебирає всі можливі пари точок для знаходження мінімальної відстані."""
    min_dist = float('inf')
    p1, p2 = None, None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                p1, p2 = points[i], points[j]
    return p1, p2, min_dist

def strip_closest(strip, d):
    """Пошук у смузі для знаходження найближчої пари точок.
    Враховує лише точки, що знаходяться на відстані менше d від середньої лінії."""
    min_dist = d
    p1, p2 = None, None
    strip.sort(key=lambda point: point[1])
    n = len(strip)
    for i in range(n):
        for j in range(i + 1, n):
            if (strip[j][1] - strip[i][1]) < min_dist:
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    p1, p2 = strip[i], strip[j]
    return p1, p2, min_dist

def closest_pair_recursive(points_sorted_x, points_sorted_y):
    """Рекурсивна функція для знаходження найближчої пари точок.
    Використовує метод розділяй і володарюй."""
    n = len(points_sorted_x)
    if n <= 3:
        return brute_force(points_sorted_x)

    mid = n // 2
    mid_point = points_sorted_x[mid]

    Qx = points_sorted_x[:mid]
    Rx = points_sorted_x[mid:]
    
    midpoint = points_sorted_x[mid][0]
    Qy = list(filter(lambda x: x[0] <= midpoint, points_sorted_y))
    Ry = list(filter(lambda x: x[0] > midpoint, points_sorted_y))

    # Рекурсивний пошук у лівій і правій половинах
    (p1_left, p2_left, dist_left) = closest_pair_recursive(Qx, Qy)
    (p1_right, p2_right, dist_right) = closest_pair_recursive(Rx, Ry)

    if dist_left < dist_right:
        d = dist_left
        p1, p2 = p1_left, p2_left
    else:
        d = dist_right
        p1, p2 = p1_right, p2_right

    # Створюємо смугу навколо середньої лінії і знаходимо найближчу пару у цій смузі
    strip = [point for point in points_sorted_y if abs(point[0] - mid_point[0]) < d]
    (p1_strip, p2_strip, dist_strip) = strip_closest(strip, d)

    if dist_strip < d:
        return p1_strip, p2_strip, dist_strip
    else:
        return p1, p2, d

def closest_pair(points):
    """Основна функція для знаходження найближчої пари точок.
    Сортує точки і викликає рекурсивну функцію."""
    points_sorted_x = sorted(points, key=lambda x: x[0])
    points_sorted_y = sorted(points, key=lambda x: x[1])
    return closest_pair_recursive(points_sorted_x, points_sorted_y)

def visualize(points, closest_points):
    """Візуалізація множини точок та найближчої пари точок.
    Малює всі точки і з'єднує найближчу пару червоною лінією."""
    x_points, y_points = zip(*points)
    plt.scatter(x_points, y_points, color='blue')  # Всі точки синіми

    p1, p2 = closest_points
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', linewidth=2)
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='red')  

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Closest Pair of Points')
    plt.show()

# Приклад використання
points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
p1, p2, min_dist = closest_pair(points)
print(f'Найближча пара точок: {p1} і {p2} з відстанню {min_dist}')
visualize(points, (p1, p2))
