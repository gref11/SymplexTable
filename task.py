from fraction import Fract
import numpy as np


class Task:
    def __init__(self, n, m, c, a):
        self.__n = n
        self.__m = m
        self.symplextable = self.SymplexTable(n, m, c, a)
        self.to_canonical()

    class SymplexTable:
        def __init__(self, n, m, c, a):
            self.__n = n
            self.__n_art = 0
            self.__m = m
            self.__A = np.array([Fract(0, 1)] * ((n + 1) * m), Fract)
            self.__A = self.__A.reshape((m, n + 1))

            for i in range(m):
                for j in range(n + 1):
                    self.__A[i][j] = Fract(a[i][j], 1)

            self.__C = np.array([Fract(0, 1)] * n, Fract)
            for i in range(n):
                self.__C[i] = Fract(c[i])
            # self.__C = np.append(self.__C, [Fract(-1)] * m)

            self.__basis = np.array([-1] * m, int)

            self.__scores = np.array([Fract(0, 1)] * (n + 1), Fract)

        def __str__(self):
            res_str = ""
            res_str += (
                "-" * 6 * (3 + self.__n + self.__n_art + (1 if (self.__n_art) else 0))
                + "\n"
            )

            res_str += f"Базис C     {'Cm    ' if (self.__n_art) else ''}"
            for i in range(self.__n + self.__n_art + 1):
                res_str += f"A{i}    "
            res_str += "\n"
            res_str += " " * 6 * (3 + (1 if self.__n_art else 0))
            for i in range(self.__n + self.__n_art):
                res_str += str(self.__C[i]) + " " * (6 - len(str(self.__C[i])))
            res_str += "\n"
            if self.__n_art > 0:
                res_str += " " * 6 * 4
                for i in range(self.__n + self.__n_art):
                    res_str += str(self.__C_art[i]) + " " * (
                        6 - len(str(self.__C_art[i]))
                    )
                res_str += "\n"

            res_str += (
                "-" * 6 * (3 + self.__n + self.__n_art + (1 if (self.__n_art) else 0))
                + "\n"
            )

            for i in range(self.__m):
                res_str += str(self.__basis[i] + 1) + " " * (
                    6 - len(str(self.__basis[i] + 1))
                )
                res_str += str(self.__C[self.__basis[i]]) + " " * (
                    6 - len(str(self.__C[self.__basis[i]]))
                )
                if self.__n_art:
                    res_str += str(self.__C_art[self.__basis[i]]) + " " * (
                        6 - len(str(self.__C_art[self.__basis[i]]))
                    )
                for j in range(self.__n + self.__n_art + 1):
                    res_str += str(self.__A[i][j]) + " " * (
                        6 - len(str(self.__A[i][j]))
                    )
                res_str += "\n"

            res_str += (
                "-" * 6 * (3 + self.__n + self.__n_art + (1 if (self.__n_art) else 0))
                + "\n"
            )

            res_str += " " * 6 * (1 + (1 if self.__n_art else 0)) + "Δ     "
            for i in range(self.__n + self.__n_art + 1):
                res_str += str(self.__scores[i]) + " " * (
                    6 - len(str(self.__scores[i]))
                )
            res_str += "\n"
            if self.__n_art:
                res_str += " " * 6 * (1 + (1 if self.__n_art else 0)) + "Δm    "
                for i in range(self.__n + self.__n_art + 1):
                    res_str += str(self.__scores_art[i]) + " " * (
                        6 - len(str(self.__scores_art[i]))
                    )
                res_str += "\n"

            return res_str

        def row_mul(self, row, x):
            self.__A[row] *= x

        def calc_scores(self):
            for column in range(self.__n + self.__n_art + 1):
                self.__scores[column] = (
                    self.__C[column - 1] * (-1) if column else Fract(0)
                )
                for row in range(self.__m):
                    self.__scores[column] += (
                        self.__C[self.__basis[row]] * self.__A[row][column]
                    )

            if self.__n_art:
                self.__scores_art = np.array(
                    [Fract(0, 1)] * (self.__n + self.__n_art + 1), Fract
                )
                for column in range(self.__n + self.__n_art + 1):
                    self.__scores_art[column] = (
                        self.__C_art[column - 1] * (-1) if column else Fract(0)
                    )
                    for row in range(self.__m):
                        self.__scores_art[column] += (
                            self.__C_art[self.__basis[row]] * self.__A[row][column]
                        )

        def calc_basis(self):
            cond_col = (
                np.count_nonzero(self.__A[:, 1 : self.__n + 1] == 1, axis=0) == 1
            ) & (np.count_nonzero(self.__A[:, 1 : self.__n + 1] == 0, axis=0) == 2)
            self.__basis = np.array([-1] * self.__m, int)
            for column in range(self.__n):
                if cond_col[column]:
                    for row in range(self.__m):
                        if self.__A[row][column + 1] == 1:
                            self.__basis[row] = column
            if np.count_nonzero(self.__basis == -1):
                self.add_basis()

        def add_basis(self):
            for row in range(self.__m):
                if self.__basis[row] == -1:
                    self.__n_art += 1
                    self.__basis[row] = self.__n + self.__n_art - 1
                    self.__A = np.append(self.__A, [[Fract(0)]] * (self.__m), axis=1)
                    self.__A[row][self.__basis[row] + 1] = Fract(1)
                    self.__scores = np.append(self.__scores, [Fract(0)])

                    self.__C = self.__C = np.append(self.__C, [Fract(0)] * self.__n_art)
                    self.__C_art = np.array(
                        [Fract(0, 1)] * (self.__n + self.__n_art), Fract
                    )
                    for i in range(self.__n):
                        self.__C_art[i] = Fract(0)
                    for i in range(self.__n, self.__n + self.__n_art):
                        self.__C_art[i] = Fract(-1)

        def make_basis(self, row, column):
            if self.__n_art:
                self.__A = np.delete(self.__A, list(range(self.__n + 1, self.__n + self.__n_art + 1)), axis=1)
                self.__C = np.delete(self.__C, list(range(self.__n, self.__n + self.__n_art)))
                self.__n_art = 0
            self.row_mul(row, Fract(1) / self.__A[row][column])
            self.__basis[row] = column - 1
            for i in range(self.__m):
                if i != row:
                    self.__A[i] -= self.__A[row] * self.__A[i][column]

        def choose_basis(self):
            if self.__n_art:
                min_score_column = 1
                for column in range(2, self.__n + self.__n_art + 1):
                    if self.__scores_art[min_score_column] > self.__scores_art[column]:
                        min_score_column = column
            else:
                min_score_column = 1
                for column in range(2, self.__n + 1):
                    if self.__scores[min_score_column] > self.__scores[column]:
                        min_score_column = column

            min_ratio_row = -1
            for row in range(0, self.__m):
                if self.__A[row][min_score_column] < 0:
                    continue
                if min_ratio_row == -1:
                    min_ratio_row = row
                    continue
                ratio = self.__A[row][0] / self.__A[row][min_score_column]
                if (
                    self.__A[min_ratio_row][0]
                    / self.__A[min_ratio_row][min_score_column]
                    > ratio
                ):
                    min_ratio_row = row
            if min_ratio_row == -1:
                print("Your task is really shit") 
            return min_ratio_row, min_score_column
        
        def check_for_optimality(self):
            if self.__n_art:
                return False
            for i in range(1, self.__n + 1):
                if self.__scores[i] < 0:
                    return False
            return True

    def to_canonical(self):
        for row in range(self.__m):
            if self.symplextable._SymplexTable__A[row][0] < 0:
                self.symplextable.row_mul(row, -1)

    def solve(self):
        self.symplextable.calc_basis()
        self.symplextable.calc_scores()
        while not(self.symplextable.check_for_optimality()):
            print(self.symplextable)
            row, column = self.symplextable.choose_basis()
            self.symplextable.make_basis(row, column)
            self.symplextable.calc_basis()
            self.symplextable.calc_scores()
        print(self.symplextable)
