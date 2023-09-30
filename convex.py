from re import S
from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def partial_perimeter(self, triangle=None):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):

    def __init__(self, p, q):
        self.p, self.q = p, q
        self.partial_perimeter_ = 0

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def intersection(self, segment2):
        """
        Функция принимает два отрезка, представленных объектами класса Segment,
        и возвращает точку их пересечения, если она есть, иначе возвращает None
        """
        x1, y1 = self.p.x, self.p.y
        x2, y2 = self.q.x, self.q.y
        x3, y3 = segment2.p.x, segment2.p.y
        x4, y4 = segment2.q.x, segment2.q.y

        if (x2, y2) == (x3, y3) and (x1, y1) != (x2, y2):
            return R2Point(x2, y2)
        elif (x1, y1) == (x4, y4) and (x1, y1) != (x2, y2):
            return R2Point(x1, y1)

        # Вычисляем уравнения прямых, проходящих через отрезки
        a1 = y2 - y1
        b1 = x1 - x2
        c1 = x2 * y1 - x1 * y2

        a2 = y4 - y3
        b2 = x3 - x4
        c2 = x4 * y3 - x3 * y4

        # Вычисляем точку пересечения двух прямых
        det = a1 * b2 - a2 * b1
        if det == 0:
            return None
        #    if R2Point.is_triangle(R2Point(x1, y1), R2Point(x2, y2), R2Point(x3, y3)):
        #       return None;
        #    if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2):
        #        return None
        #    if max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
        #        return None
            # return Segment(R2Point(abs(x3 - x1), abs(y3 - y1)),
            #              R2Point(abs(x4 - x2), abs(y4 - y2)))

        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det

        # Проверяем, лежит ли точка пересечения на отрезках
        if min(x1, x2) <= x <= max(x1, x2) and\
                min(y1, y2) <= y <= max(y1, y2) and \
                min(x3, x4) <= x <= max(x3, x4) and \
                min(y3, y4) <= y <= max(y3, y4):
            return R2Point(x, y)

        return None  # Точка пересечения лежит вне отрезков

    def partial_perimeter(self, triangle):
      #  flag = False
        a, b, c = triangle[0], triangle[1], triangle[2]
        segs = [Segment(a, b), Segment(b, c), Segment(a, c)]
        inters = []
        count = 0
        for i in segs:
            inform = self.intersection(i)
            if inform is not None and inform not in inters:
                inters.append(inform)
             #   if type(inform).__name__ == 'Segment':
             #      base_seg = inform
                count += 1

       # if flag:
       #    return base_seg.perimeter()
        if count == 0:
            if self.q.is_inside_triangle(
                    triangle) and self.p.is_inside_triangle(triangle):
                return self.perimeter()
            return 0.0
        elif count == 1:
            if self.q.is_inside_triangle(triangle):
                return inters[0].dist(self.q)
            else:
                return inters[0].dist(self.p)
        elif count == 2:
            return 2 * inters[0].dist(inters[1])
        elif flag:
            return base_seg.perimeter()


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._partial_perimeter = 0
        self.flag_ = False

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):
        if not self.flag_:
            self.triangle = Polygon(
                R2Point(
                    0, 0), R2Point(
                    0, 0), R2Point(
                    0, 0))
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            self._partial_perimeter -= Segment(
                self.points.first(),
                self.points.last()).partial_perimeter(
                self.triangle) / 2

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self._partial_perimeter -= Segment(
                    p, self.points.first()).partial_perimeter(
                    self.triangle) / 2
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self._partial_perimeter -= Segment(
                    p, self.points.last()).partial_perimeter(
                    self.triangle) / 2
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())

            self._partial_perimeter += \
                (Segment(t, self.points.first()).partial_perimeter(self.triangle) +
                 Segment(t, self.points.last()).partial_perimeter(self.triangle)) / 2
            self.points.push_first(t)

        return self

    def __getitem__(self, key):
        return self.points.array[key]

    def partial_perimeter(self, triangle):
        self.flag_ = True
        self.triangle = triangle
        if len(self.points.array) > 3:
            return self._partial_perimeter
        self._partial_perimeter = 0
        self.segs = [Segment(self[1], self[0]),
                     Segment(self[1], self[2]),
                     Segment(self[0], self[2])]
        for seg in self.segs:
            self._partial_perimeter += seg.partial_perimeter(triangle) / 2
#        if math.isclose(self._partial_perimeter, 0.0, abs_tol=1e-16):
#           self._partial_perimeter = 0
        if abs(self._partial_perimeter) < 0.0000000001:
            self._partial_perimeter = 0.0
        return self._partial_perimeter


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
