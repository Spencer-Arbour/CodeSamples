from enum import Enum, unique
from abc import ABC, abstractmethod


@unique
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


@unique
class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4


@unique
class Price(Enum):
    CHEAP = 1
    AVERAGE = 2
    EXPENSIVE = 3
    VERY_EXPENSIVE = 4


class Product:

    def __init__(self, name, color, size, price):
        self.name = name
        self.color = color
        self.size = size
        self.price = price

    def __str__(self):
        return "The {0} {1} {2} {3}.".\
            format(self.size.name, self.color.name, self.name, self.price)


class Specification(ABC):

    @abstractmethod
    def specification(self, product: Product) -> bool:
        pass


class ColorSpecification(Specification):

    def __init__(self, color):
        self.color = color

    def specification(self, product):
        return product.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def specification(self, product):
        return product.size == self.size


class PriceSpecification(Specification):

    def __init__(self, price):
        self.price = price

    def specification(self, product: Product) -> bool:
        return product.price == self.price


class AndSpecification(Specification):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def specification(self, product):
        return self.first.specification(product) and self.second.specification(product)


class OrSpecification(Specification):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def specification(self, product):
        return self.first.specification(product) or self.second.specification(product)


class XorSpecification(Specification):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def specification(self, product):
        return self.first.specification(product) ^ self.second.specification(product)


class Filter:
    @staticmethod
    def filter(products, spec):
        return list(filter(lambda product: spec.specification(product), products))


if __name__ == "__main__":
    products = [
        Product("Apple", Color.RED, Size.SMALL, Price.CHEAP),
        Product("Car", Color.RED, Size.LARGE, Price.EXPENSIVE),
        Product("House", Color.BLUE, Size.HUGE, Price.VERY_EXPENSIVE),
        ]

    print("\nGOOD")
    print("Red Items:")
    items = Filter.filter(products, ColorSpecification(Color.RED))
    for item in items:
        print(item)

    print("\nGOOD")
    print("Large Items:")
    items = Filter.filter(products, SizeSpecification(Size.LARGE))
    for item in items:
        print(item)

    print("Large Red Items:")
    items = Filter.filter(products, AndSpecification(SizeSpecification(Size.LARGE), ColorSpecification(Color.RED)))
    for item in items:
        print(item)

    print("Not Small Red Items:")
    items = Filter.filter(products, XorSpecification(SizeSpecification(Size.SMALL), ColorSpecification(Color.RED)))
    for item in items:
        print(item)
