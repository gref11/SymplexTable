from fraction import Fract
import numpy as np


class Task:
    def __init__(self, n, m, c, a, c_l=[]):
        self.__n = n
        self.__m = m
        self.__has_parameter = False
        if len(c_l):
            self.__has_parameter = True
        self.symplextable = self.SymplexTable(n, m, c, a, c_l)
        self.to_canonical()

    class SymplexTable:
        def __init__(self, n, m, c, a, c_l=[]):
            self.__n = n
            self.__n_art = 0
            self.__m = m
            self.__A = np.array([Fract(0, 1)] * ((n + 1) * m), Fract)
            self.__A = self.__A.reshape((m, n + 1))
            self.choosen_row = -1
            self.choosen_col = -1

            for i in range(m):
                for j in range(n + 1):
                    self.__A[i][j] = Fract(a[i][j], 1)

            self.__C = np.array([Fract(0, 1)] * n, Fract)
            for i in range(n):
                self.__C[i] = Fract(c[i])

            self.__C_l = np.array([Fract(0, 1)] * n, Fract)
            if len(c_l):
                for i in range(n):
                    self.__C_l[i] = Fract(c_l[i])

            self.__basis = np.array([-1] * m, int)

            self.__scores = np.array([Fract(0, 1)] * (n + 1), Fract)

            self.par = Fract(0)
            self.parameter = False

        def __str__(self):
            col_len = 7
            res_str = ""
            amp1 = "'"
            amp2 = '"'
            res_str += (
                "-"
                * col_len
                * (
                    3
                    + self.n
                    + self.n_art
                    + (1 if (self.n_art or self.parameter) else 0)
                )
                + "\n"
            )

            res_str += f"Базис  C{amp1 if (self.parameter) else ' '}     {'Cm     ' if (self.n_art) else ''}{f'C{amp2}     ' if (self.parameter) else ''}"
            for i in range(self.n + self.n_art + 1):
                res_str += f"A{i}     "
            res_str += "\n"
            res_str += (
                " " * col_len * (3 + (1 if (self.n_art or self.parameter) else 0))
            )
            for i in range(self.n + self.n_art):
                res_str += str(self.C[i] + self.C_l[i] * self.par) + " " * (
                    col_len - len(str(self.C[i] + self.C_l[i] * self.par))
                )
            res_str += "\n"
            if self.n_art > 0:
                res_str += " " * col_len * 4
                for i in range(self.n + self.n_art):
                    res_str += str(self.C_art[i]) + " " * (
                        col_len - len(str(self.C_art[i]))
                    )
                res_str += "\n"
            if self.parameter:
                res_str += " " * col_len * 4
                for i in range(self.n + self.n_art):
                    res_str += str(self.C_l[i]) + " " * (
                        col_len - len(str(self.C_l[i]))
                    )
                res_str += "\n"

            res_str += (
                "-"
                * col_len
                * (
                    3
                    + self.n
                    + self.n_art
                    + (1 if (self.n_art or self.parameter) else 0)
                )
                + "\n"
            )

            for i in range(self.m):
                res_str += str(self.basis[i] + 1) + " " * (
                    col_len - len(str(self.basis[i] + 1))
                )
                res_str += str(
                    self.__C[self.basis[i]] + self.__C_l[self.basis[i]] * self.par
                ) + " " * (
                    col_len
                    - len(
                        str(
                            self.__C[self.basis[i]]
                            + self.__C_l[self.basis[i]] * self.par
                        )
                    )
                )
                if self.__n_art:
                    res_str += str(self.C_art[self.basis[i]]) + " " * (
                        col_len - len(str(self.C_art[self.basis[i]]))
                    )
                if self.parameter:
                    res_str += str(self.C_l[self.basis[i]]) + " " * (
                        col_len - len(str(self.C_l[self.basis[i]]))
                    )
                for j in range(self.n + self.n_art + 1):
                    if i == self.choosen_row and j == self.choosen_col:
                        res_str += (
                            "\x1b[41m"
                            + str(self.A[i][j])
                            + " " * (col_len - len(str(self.A[i][j])))
                            + "\x1b[0m"
                        )
                    else:
                        res_str += str(self.A[i][j]) + " " * (
                            col_len - len(str(self.A[i][j]))
                        )
                res_str += "\n"

            res_str += (
                "-"
                * col_len
                * (
                    3
                    + self.n
                    + self.n_art
                    + (1 if (self.n_art or self.parameter) else 0)
                )
                + "\n"
            )

            res_str += (
                " " * col_len * (1 + (1 if (self.n_art or self.parameter) else 0))
                + f"Δ{(amp1 + ' ' * (col_len - 2)) if (self.parameter) else ' ' * (col_len - 1)}"
            )
            for i in range(self.n + self.n_art + 1):
                res_str += str(self.scores[i]) + " " * (
                    col_len - len(str(self.scores[i]))
                )
            res_str += "\n"
            if self.n_art:
                res_str += " " * col_len * 2 + "Δm     "
                for i in range(self.n + self.n_art + 1):
                    res_str += str(self.scores_art[i]) + " " * (
                        col_len - len(str(self.scores_art[i]))
                    )
                res_str += "\n"
            if self.parameter:
                print(self.n, self.n_art)
                res_str += " " * col_len * 2 + 'Δ"     '
                for i in range(self.n + 1):
                    res_str += str(self.scores_l[i]) + " " * (
                        col_len - len(str(self.scores_l[i]))
                    )
                res_str += "\n"

            return res_str

        @property
        def A(self):
            return self.__A

        @property
        def C(self):
            return self.__C

        @property
        def C(self):
            return self.__C

        @property
        def C_l(self):
            return self.__C_l

        @property
        def C_art(self):
            return self.__C_art

        @property
        def n(self):
            return self.__n

        @property
        def n_art(self):
            return self.__n_art

        @property
        def m(self):
            return self.__m

        @property
        def scores(self):
            return self.__scores

        @property
        def scores_art(self):
            return self.__scores_art

        @property
        def scores_l(self):
            return self.__scores_l

        @property
        def basis(self):
            return self.__basis

        def get_table_line(self, *s):
            res_str = "<tr>"
            for i in s:
                if i == "skip":
                    continue
                res_str += f"<th><div>{i}</div></th>"
            res_str += "</tr>\n"
            return res_str

        def get_table(self):
            res_str = "<br><table><thead>"
            amp1 = "'"
            amp2 = '"'
            res_str += self.get_table_line(
                *[
                    "Базис",
                    f"C{amp1 if (self.parameter) else ''}",
                    f"C{amp2}" if (self.parameter) else "skip",
                    *[f"A{i}" for i in range(self.n + self.n_art + 1)],
                ]
            )
            res_str += self.get_table_line(
                *([" "] * (3 + (1 if (self.parameter) else 0))),
                *(map(lambda x: str(x), self.C[: self.n])),
                *(["-M"] * self.n_art),
            )

            if self.parameter:
                res_str += self.get_table_line(
                    *([" "] * 4),
                    *(map(lambda x: str(x), self.C_l[: self.n])),
                )
            res_str += "</thead>"

            for i in range(self.m):
                res_str += self.get_table_line(
                    str(self.basis[i] + 1),
                    (
                        str(self.C[self.basis[i]])
                        if (not (self.n_art) or not (self.C_art[self.basis[i]] != 0))
                        else "-M"
                    ),
                    str(self.C_l[self.basis[i]]) if (self.parameter) else "skip",
                    *[
                        (
                            f'"{str(self.A[i, j])}"'
                            if (i == self.choosen_row and j == self.choosen_col)
                            else str(self.A[i][j])
                        )
                        for j in range(self.n + self.n_art + 1)
                    ],
                )

            res_str += "<tfoot>"
            res_str += self.get_table_line(
                *([" "] * (1 + (1 if (self.parameter) else 0))),
                f"Δ{amp1 if (self.parameter) else ''}",
                *(map(lambda x: str(x), self.scores[: self.n + self.n_art + 1])),
            )
            if self.n_art:
                res_str += self.get_table_line(
                    *([" "] * 1),
                    "Δm",
                    *(
                        map(
                            lambda x: str(x), self.scores_art[: self.n + self.n_art + 1]
                        )
                    ),
                )
            if self.parameter:
                res_str += self.get_table_line(
                    *([" "] * (1 + (1 if (self.parameter) else 0))),
                    f"Δ{amp2}",
                    *(map(lambda x: str(x), self.scores_l[: self.n + 1])),
                )

            res_str += "</tfoot></table><br>"
            return res_str

        def row_mul(self, row, x):
            self.__A[row] *= x

        def calc_scores(self):
            for column in range(self.n + self.n_art + 1):
                self.__scores[column] = (
                    (self.C[column - 1] + self.C_l[column - 1] * self.par) * (-1)
                    if column
                    else Fract(0)
                )
                for row in range(self.m):
                    self.__scores[column] += (
                        self.C[self.basis[row]] + self.C_l[self.basis[row]] * self.par
                    ) * self.A[row][column]

            if self.n_art:
                self.__scores_art = np.array(
                    [Fract(0, 1)] * (self.n + self.n_art + 1), Fract
                )
                for column in range(self.n + self.n_art + 1):
                    self.__scores_art[column] = (
                        self.C_art[column - 1] * (-1) if column else Fract(0)
                    )
                    for row in range(self.m):
                        self.__scores_art[column] += (
                            self.C_art[self.basis[row]] * self.A[row][column]
                        )

            if self.parameter:
                self.__scores_l = np.array([Fract(0, 1)] * (self.n + 1), Fract)
                for column in range(self.n + 1):
                    self.__scores_l[column] = (
                        self.C_l[column - 1] * (-1) if column else Fract(0)
                    )
                    for row in range(self.m):
                        self.__scores_l[column] += (
                            self.C_l[self.basis[row]] * self.A[row][column]
                        )

        def calc_basis(self):
            cond_col = (
                np.count_nonzero(self.A[:, 1 : self.n + 1] == 1, axis=0) == 1
            ) & (np.count_nonzero(self.A[:, 1 : self.n + 1] == 0, axis=0) == self.m - 1)
            self.__basis = np.array([-1] * self.m, int)
            for column in range(self.n):
                if cond_col[column]:
                    for row in range(self.m):
                        if self.A[row][column + 1] == 1:
                            self.__basis[row] = column
            if np.count_nonzero(self.basis == -1):
                self.add_basis()

        def add_basis(self):
            for row in range(self.__m):
                if self.__basis[row] == -1:
                    self.__n_art += 1
                    self.__basis[row] = self.n + self.n_art - 1
                    self.__A = np.append(self.A, [[Fract(0)]] * (self.m), axis=1)
                    self.__A[row][self.basis[row] + 1] = Fract(1)
                    self.__scores = np.append(self.scores, [Fract(0)])

                    self.__C = np.append(self.C, [Fract(0)] * self.n_art)
                    self.__C_l = np.append(self.C_l, [Fract(0)] * self.n_art)
                    self.__C_art = np.array(
                        [Fract(0, 1)] * (self.n + self.n_art), Fract
                    )
                    for i in range(self.__n):
                        self.__C_art[i] = Fract(0)
                    for i in range(self.n, self.n + self.n_art):
                        self.__C_art[i] = Fract(-1)

        def make_basis(self, row, column):
            if self.n_art:
                self.__A = np.delete(
                    self.__A,
                    list(range(self.n + 1, self.n + self.n_art + 1)),
                    axis=1,
                )
                self.__C = np.delete(self.__C, list(range(self.n, self.n + self.n_art)))
                self.__C_l = np.delete(
                    self.__C_l, list(range(self.n, self.n + self.n_art))
                )
                self.__n_art = 0
            self.row_mul(row, Fract(1) / self.A[row][column])
            self.__basis[row] = column - 1
            for i in range(self.m):
                if i != row:
                    self.__A[i] -= self.A[row] * self.A[i][column]

        def choose_basis_row(self, column):
            min_ratio_row = -1
            for row in range(0, self.__m):
                if self.A[row][column] <= 0:
                    continue
                if min_ratio_row == -1:
                    min_ratio_row = row
                    continue
                ratio = self.A[row][0] / self.A[row][column]
                if self.A[min_ratio_row][0] / self.A[min_ratio_row][column] > ratio:
                    min_ratio_row = row
            return min_ratio_row

        def choose_basis(self):
            if self.n_art:
                min_score_column = 1
                for column in range(2, self.n + self.n_art + 1):
                    if self.scores_art[min_score_column] > self.scores_art[column]:
                        min_score_column = column
            else:
                min_score_column = 1
                for column in range(2, self.__n + 1):
                    if self.scores[min_score_column] > self.scores[column]:
                        min_score_column = column

            min_ratio_row = self.choose_basis_row(min_score_column)
            if min_ratio_row == -1:
                print("Your task is really shit")
                return -1, -1
            return min_ratio_row, min_score_column

        def check_for_optimality(self):
            if self.n_art:
                return False
            for i in range(1, self.n + 1):
                if self.scores[i] < 0:
                    return False
            return True

        def get_x(self):
            x = [Fract(0)] * self.n
            for i in range(self.m):
                x[self.basis[i]] = self.A[i][0]
            return x

    def to_canonical(self):
        for row in range(self.__m):
            if self.symplextable.A[row][0] < 0:
                self.symplextable.row_mul(row, -1)

    def solve(self, par=0):
        res_str = ""
        self.symplextable.calc_basis()
        self.symplextable.calc_scores()
        while not (self.symplextable.check_for_optimality()):
            self.symplextable.choosen_row, self.symplextable.choosen_col = (
                self.symplextable.choose_basis()
            )
            res_str += self.symplextable.get_table()
            print(self.symplextable)
            if (
                self.symplextable.choosen_row == -1
                and self.symplextable.choosen_col == -1
            ):
                res_str += "Решения не существует"
                return res_str
            self.symplextable.make_basis(
                self.symplextable.choosen_row, self.symplextable.choosen_col
            )
            self.symplextable.calc_basis()
            self.symplextable.calc_scores()
        self.symplextable.choosen_row, self.symplextable.choosen_col = -1, -1
        print(self.symplextable)
        print(f"L* = {str(self.symplextable.scores[0])}")
        print(f'X* = ({", ".join(list(map(str, self.symplextable.get_x())))})')
        res_str += self.symplextable.get_table()
        res_str += f"L* = {str(self.symplextable.scores[0])}<br>"
        res_str += (
            f'X* = ({", ".join(list(map(str, self.symplextable.get_x())))})<br>'
            + "<br>"
        )
        if self.__has_parameter:
            self.symplextable.par = 0
            self.symplextable.parameter = True
            self.__answer = self.parameter_analys()
            res_str += self.__answer[0]
            print("Ответ:")
            print(self.__answer[1])
            res_str += "Ответ:"
            res_str += self.__answer[1]
        # print(res_str)
        return res_str

    def parameter_analys_caller(self, row, column, direction):
        current_basis = self.symplextable.basis[row]
        self.symplextable.make_basis(row, column)
        self.symplextable.calc_basis()
        res = self.parameter_analys(direction)
        self.symplextable.make_basis(row, current_basis + 1)
        self.symplextable.calc_basis()
        return res

    def parameter_analys(self, direction="either"):
        res_str = ""
        res_ans = ""

        self.symplextable.calc_scores()
        print(self.symplextable)
        res_str += str(self.symplextable.get_table())
        left_l = -9999
        left_l_col = -1
        right_l = 9999
        right_l_col = -1

        for column in range(1, self.__n + 1):
            if self.symplextable.scores_l[column] != 0:
                l = (
                    self.symplextable.scores[column]
                    * (-1)
                    / self.symplextable.scores_l[column]
                )
                if left_l < l and self.symplextable.scores_l[column] > 0:
                    left_l = l
                    left_l_col = column
                elif right_l > l and self.symplextable.scores_l[column] < 0:
                    right_l = l
                    right_l_col = column

        str_ = (
            (f"[{left_l}" if (left_l != -9999) else "(-∞")
            + "; "
            + (f"{right_l}]" if (right_l != 9999) else "+∞)")
            + ": "
            + str(self.symplextable.scores[0])
            + " + "
            + str(self.symplextable.scores_l[0])
            + "λ; "
            + f'X* = ({", ".join(list(map(str, self.symplextable.get_x())))})'
        ) + "\n"

        print(str_)
        res_str += str_ + "<br><br>"

        if direction == "either" or direction == "right":
            if right_l != 9999:
                min_ratio_row = self.symplextable.choose_basis_row(right_l_col)
                if min_ratio_row == -1:
                    res_ans += (f"[{right_l}" + "; +∞): решений нет") + "\n" + "<br>"
                    res_str += str_ + "<br><br>"
                    print(res_ans)

                else:
                    callback = self.parameter_analys_caller(
                        min_ratio_row, right_l_col, "right"
                    )
                    res_str += callback[0]
                    res_ans += callback[1]

        res_ans += str_ + "<br>"

        if direction == "either" or direction == "left":
            if left_l != -9999:
                min_ratio_row = self.symplextable.choose_basis_row(left_l_col)
                if min_ratio_row == -1:
                    str_ = "(-∞; " + f"{left_l}]: решений нет"
                    res_str += str_ + "<br><br>"
                    res_ans += str_ + "<br>"
                    print(str_)
                else:
                    callback = self.parameter_analys_caller(
                        min_ratio_row, left_l_col, "left"
                    )
                    res_str += callback[0]
                    res_ans += callback[1] + "\n"

        return [res_str, res_ans]
