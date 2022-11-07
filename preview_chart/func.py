import math


class Linear_func:
    """
    线性函数（val=kt+b）。
    """

    def __init__(self, k: float, b: float) -> None:
        self.k = k
        self.b = b

    def __call__(self, t: float) -> float:
        return self.k*t+self.b


class Sine_func:
    """
    正弦函数（val=Asin(wt+φ)+b）。
    """

    def __init__(self, A: float, o: float, p: float, b: float) -> None:
        self.A = A
        self.o = o
        self.p = p
        self.b = b

    def __call__(self, t: float) -> float:
        return self.A*math.sin(self.o*t+self.p)+self.b


class Quadratic_func:
    """
    二次函数（val=at^2+bt+c）。
    """

    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, t: float) -> float:
        # 不会有人不知道秦九韶算法吧
        return (self.a*t+self.b)*t+self.c
