from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    def test_part(self):
        assert self.f.partial_perimeter() == 0.0



class TestIntersection1:
    def setup_method(self):
        self.seg1 = Segment(R2Point(0, 0), R2Point(1, 1))
        self.seg2 = Segment(R2Point(1, 1), R2Point(0, 2))

    def test_intersec(self):
        assert self.seg1.intersection(self.seg2) == R2Point(1, 1)


class TestIntersection2:
    def setup_method(self):
        self.seg1 = Segment(R2Point(0, 0), R2Point(1, 1))
        self.seg2 = Segment(R2Point(-1, 0), R2Point(0, 0))

    def test_intersec(self):
        assert self.seg1.intersection(self.seg2) == R2Point(0, 0)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    def test_part(self):
        assert self.f.partial_perimeter() == 0.0


class TestSegment1:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    def test_part1(self):

        assert self.f.partial_perimeter(self.triangle) == self.f.perimeter()


class TestSegment2:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 1.0))

    def test_part(self):
        assert self.f.partial_perimeter(self.triangle) == approx(2 * sqrt(2))


class TestSegment3:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, -1.0))

    def test_part(self):
        assert self.f.partial_perimeter(self.triangle) == 0.0


class TestSegment4:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(1.0, 1.0), R2Point(1.0, 1.0))

    def test_part(self):
        assert self.f.partial_perimeter(self.triangle) == self.f.perimeter()


class TestSegment5:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(2.0, 0.0), R2Point(-1.0, -1.0))

        self.f = Segment(R2Point(-1.0, -1.0), R2Point(2.0, 0.0))

    def test_part(self):
        assert self.f.partial_perimeter(self.triangle) == 0.0


class TestSegment6:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Segment(R2Point(0.0, 2.0), R2Point(3.0, 3.0))

    def test_part(self):
        assert self.f.partial_perimeter(self.triangle) == 0.0


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                1.0, 0.0), R2Point(
                0.0, 1.0))

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon(self):
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    #   добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    #   добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    #   изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))
    #   добавление точки может его изменить

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)
    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)


class TestPolygon1:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                -1.0, -1.0), R2Point(
                1.0, -1.0))

    def test_part1(self):
        assert self.f.partial_perimeter(self.triangle) == 0.0


class TestPolygon2:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Polygon(
            R2Point(
                1.0, 1.0), R2Point(
                -1.0, 1.0), R2Point(
                0.0, 0.0))

    def test_part1(self):
        assert self.f.partial_perimeter(
            self.triangle) == approx(
            self.f.perimeter(), 0.001)


class TestPolygon3:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Polygon(
            R2Point(
                -1.0, -1.0), R2Point(
                1.0, -1.0), R2Point(
                1.0, 1.0))

    def test_part1(self):
        assert self.f.partial_perimeter(
            self.triangle) == approx(
            sqrt(2) + 1, 0.001)


class TestPolygon4:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Polygon(
            R2Point(
                5.0, 5.0), R2Point(
                5.0, -5.0), R2Point(
                -10.0, 0.0))

    def test_part1(self):
        assert self.f.partial_perimeter(self.triangle) == 0.0


class TestPolygon5:
    def setup_method(self):
        self.triangle = Polygon(R2Point(2, 0), R2Point(0, 2), R2Point(-2, 0))
        self.f = Polygon(
            R2Point(
                1.0, -1.0), R2Point(
                3.0, 0.0), R2Point(
                -1.0, 1.0))

    def test_part1(self):
        assert self.f.add(
            R2Point(
                1.0, 4.0)).partial_perimeter(
            self.triangle) != 0

    def test_part2(self):
        assert self.f.add(R2Point(1.0, 4.0)).add(
            R2Point(-10.0, -10.0)).partial_perimeter(self.triangle) == 0
