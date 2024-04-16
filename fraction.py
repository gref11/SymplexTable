from numpy import sign


def nod(a, b):
    if type(a) != int or type(b) != int or a < 1 or b < 1:
        # print("Incorect value of numbers:", a, b, type(a), type(b))
        return 0
    a, b = max(a, b), min(a, b)
    while b != 0:
        a, b = b, a % b
    return a


class Fract:
    __type = "Fract"
    __num = 1
    __den = 1

    def __init__(self, num, den=1):
        if type(num) != int or int(num) != num:
            # print(f"Incorrect numerator value: {num}")
            return
        if type(den) != int or den < 1 or int(den) != den:
            # print(f"Incorrect denomerator value: {den}")
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

    def reduce(self):
        nod_fract = nod(abs(self.__num), self.__den)
        if nod_fract == 0:
            self.__num = 0
            self.__den = 1
        else:
            self.__num = int(self.__num / nod_fract)
            self.__den = int(self.__den / nod_fract)
        return self

    def __add__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        res_num = fract1.__num * fract2.__den + fract2.__num * fract1.__den
        res_den = fract1.__den * fract2.__den
        res = Fract(res_num, res_den).reduce()
        return res

    def __iadd__(self, other):
        res = self + other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __mul__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        res_num = fract1.__num * fract2.__num
        res_den = fract1.__den * fract2.__den
        res = Fract(res_num, res_den).reduce()
        return res

    def __imul__(self, other):
        res = self * other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __sub__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        res_num = fract1.__num * fract2.__den - fract2.__num * fract1.__den
        res_den = fract1.__den * fract2.__den
        res = Fract(res_num, res_den).reduce()
        return res

    def __isub__(self, other):
        res = self - other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __truediv__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        res_num = fract1.__num * fract2.__den * int(sign(fract2.__num))
        res_den = fract1.__den * abs(fract2.__num)
        res = Fract(res_num, res_den).reduce()
        return res

    def __itruediv__(self, other):
        res = self / other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __lt__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        if fract1.__num * fract2.__den < fract2.__num * fract1.__den:
            return True
        else:
            return False

    def __le__(fract1, fract2):
        if fract1 == fract2 or fract1 < fract2:
            return True
        else:
            return False

    def __gt__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        if fract1.__num * fract2.__den > fract2.__num * fract1.__den:
            return True
        else:
            return False

    def __ge__(fract1, fract2):
        if fract1 == fract2 or fract1 < fract2:
            return True
        else:
            return False

    def __eq__(fract1, fract2):
        if type(fract2) == int:
            fract2 = Fract(fract2, 1)
        if fract1.__num == fract2.__num and fract1.__den == fract2.__den:
            return True
        else:
            return False
