#!/usr/bin/env python3

import sys

def load_problem(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as file:
        n = int(file.readline())

        problem = [[] for _ in range(2*n)]

        for i in range(2*n):
            problem[i] = list(map(int, file.readline().split()))
            problem[i].reverse()

    return problem

def model_into_number(model: list) -> int:
    val = 0

    for i in range(len(model)):
        val <<= 1

        if model[i]:
            val += 1

    return val

def number_into_model(val: int, n: int) -> list:
    model = [0]*n

    i = 0
    while val > 0:
        if val & 1:
            model[i] = 1
        else:
            model[i] = -1

        val >>= 1
        i += 1

    return model

def dimacs_cnf(model: list, n: int, i: int, row: bool) -> str:
    dimacs = []

    for j in range(n):
        if row:
            k = i + j + 1
        else:
            k = i + n*j + 1

        if model[j] == 1:
            dimacs.append(-k)
        elif model[j] == -1:
            dimacs.append(k)

    return " ".join(map(str, dimacs))

def generate_cnf(dnf: list, n: int, start: int, row: bool) -> list:
    cnf = []
    m = len(dnf)

    model_number = [0] * m

    for i in range(m - 1, -1, -1):
        model_number[i] = model_into_number(dnf[i])

    #print(model_number)

    idx = 0

    with open("./output/cnf.txt", "a", encoding="utf-8") as file:
        for i in range(1<<n):
            if i in model_number:
                print(i)
                continue

            #cnf.append(number_into_model(i, n))
            file.write(dimacs_cnf(number_into_model(i, n), n, start, row) + " 0 \n")

    return cnf

def encode_to_dnf_recur(params: list, idx: int, start: int, n: int, all_models: list, active: list) -> None:
    if idx == len(params):
        all_models.append(list(active))
        return

    if idx == len(params) - 1:
        offset = -1
    else:
        offset = 0

    for i in range(start, n - params[idx] - offset):
        for j in range(i, i + params[idx]):
            active[j] = 1

        encode_to_dnf_recur(params, idx + 1, i + params[idx] + 1, n, all_models, active)

        for j in range(i, i + params[idx]):
            active[j] = -1

def concatenate(a: list, b: list, n: int) -> list:
    model = a.copy()
    print(a, b)

    for i in range(n):
        if model[i] != 0:
            if model[i] + b[i] == 0:
                #print("Tautologie")
                return []
        else:
            model[i] = b[i]

    return model

def distribute(a: list, b: list, n: int) -> list:
    # 1 - true, -1 - false, 0 - can be both
    new = []
    a_n = len(a)
    b_n = len(b)

    for i in range(a_n):
        for j in range(b_n):
            m = concatenate(a[i], b[j], n)
            if m != []:
                new.append(m)
    """
    useful = False

    for i in range(x):
        for j in range(y):
            useful = True
            model = [0] * n
            model[i] = a[i]

            if model[j] == 0:
                model[j] = b[j]
            else:
                #detekce tautologie
                if model[j] + b[j] == 0:
                    print("find tautology")
                    continue

            new.append(model)
    """

    return new

def dnf_to_cnf_distribution(models: list, n: int) -> list:
    #1 - true, -1 - false, 0 - can be both

    for i in range(len(models)):
        mods = []
        for j in range(n):
            mod = [0] * n
            mod[j] = models[i][j]

            mods.append(mod)

        models[i] = mods

    new_models = []

    while len(models) > 1:
        print(len(models))
        new_models = []
        for i in range(0, len(models) - 1, 2):
            new_models.append(distribute(models[i], models[i + 1], n))

        models = list(new_models)

    #print(models)

    return models

def encode(problem: list) -> list:
    cnf = []
    n = len(problem) // 2

    all_models = []
    complement = []

    with open("./output/cnf.txt", "w", encoding="utf-8") as file:
        #file.write(f"p cnf {n**2} \n")
        pass

    for i in range(n * 2):
        all_models.clear()
        encode_to_dnf_recur(problem[i], 0, 0, n, all_models, [-1] * n)
        #print(all_models)

        cnf = dnf_to_cnf_distribution(all_models, n)

        with open("./output/cnf.txt", "a", encoding="utf-8") as file:
            for c in cnf[0]:
                #print(c)
                if i < n:
                    file.write(dimacs_cnf(c, n, i, False) + " 0 \n")
                else:
                    file.write(dimacs_cnf(c, n, (i - n) * n, True) + " 0 \n")

    return cnf

def main():
    problem = load_problem(sys.argv[1])

    #print(problem)
    cnf = encode(problem)

if __name__ == "__main__":
    main()