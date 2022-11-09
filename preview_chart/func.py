import math


class Linear_func:
    """
    线性函数（val=kt+b）
    """

    def __init__(self, k: float, b: float) -> None:
        self.k = k
        self.b = b

    def __call__(self, t: float) -> float:
        return self.k*t+self.b


class Sine_func:
    """
    正弦函数（val=Asin(wt+φ)+b）
    """

    def __init__(self, A: float, o: float, p: float, b: float) -> None:
        self.A = A
        self.o = o
        self.p = p
        self.b = b

    def __call__(self, t: float) -> float:
        return self.A*math.sin(self.o*t+self.p)+self.b
