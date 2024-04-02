from numpy import sign

def nod(a, b):
    if type(a) != type(b) != type(1) or a < 1 or b < 1:
        print("Incorect value of numbers")
        return 0
    a, b = max(a, b), min(a, b)
    while b != 0:
        a, b = b, a % b
    return a


class Fract:
    # __slots__ = ('__num', '__den')
    __type = "Fract"
    __num = 1
    __den = 1

    def __init__(self, num, den):
        if type(num) != type(1) or int(num) != num:
            print(f"Incorrect numerator value: {num}")
            return
        if type(den) != type(1) or den < 1 or int(den) != den:
            print(f"Incorrect denomerator value: {den}")
            return
        if num == 0:
            self.__num = 0
            self.__den = 1
        else:
            nod_fract = nod(abs(num), den)
            self.__num = int(num / nod_fract)
            self.__den = int(den / nod_fract)

    def __del__(self):
        # print(f'Дробь {str(self)} удалена')
        pass

    def __str__(self):
        return f"{self.__num}/{self.__den}" if (self.__den != 1) else str(self.__num)

    def __add__(fract1, fract2):
        res_num = fract1.__num * fract2.__den + fract2.__num * fract1.__den
        res_den = fract1.__den * fract2.__den
        nod_fract = nod(abs(res_num), res_den)
        return Fract(int(res_num / nod_fract), int(res_den / nod_fract))
    
    def __iadd__(self, other):
        res = self + other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __mul__(fract1, fract2):
        res_num = fract1.__num * fract2.__num
        res_den = fract1.__den * fract2.__den
        nod_fract = nod(abs(res_num), res_den)
        return Fract(int(res_num / nod_fract), int(res_den / nod_fract))
    
    def __imul__(self, other):
        res = self * other
        self.__num = res.__num
        self.__den = res.__den
        return self
    
    def __sub__(fract1, fract2):
        res_num = fract1.__num * fract2.__den - fract2.__num * fract1.__den
        res_den = fract1.__den * fract2.__den
        nod_fract = nod(abs(res_num), res_den)
        return Fract(int(res_num / nod_fract), int(res_den / nod_fract))
    
    def __isub__(self, other):
        res = self - other
        self.__num = res.__num
        self.__den = res.__den
        return self
    
    def __truediv__(fract1, fract2):
        res_num = fract1.__num * fract2.__den * sign(fract2.__num)
        res_den = fract1.__den * abs(fract2.__num)
        nod_fract = nod(abs(res_num), res_den)
        return Fract(int(res_num / nod_fract), int(res_den / nod_fract))
    
    def __itruediv__(self, other):
        res = self / other
        self.__num = res.__num
        self.__den = res.__den
        return self


if __name__ == "__main__":
    # fr1 = Fract(1, 2)
    # fr2 = Fract(-1, 2)
    # fr3 = Fract(6, 12)
    # fr4 = Fract(0, 2)
    # print(fr1, fr2, fr3, fr4)
    # print(fr1 + fr4)
    # print(Fract(2, 3) * Fract(3, 4))
    # print(Fract(1, 3) + Fract(1, 6))
    # print(Fract(1, 3) - Fract(1, 6))
    # print(Fract(1, 3) / Fract(1, 6))
    fr = Fract(1, 2)
    print(fr)
    fr += Fract(-1, 6)
    print(fr)
    fr -= Fract(-1, 6)
    print(fr)
    fr *= Fract(-1, 6)
    print(fr)
    fr /= Fract(-1, 6)
    print(fr)
