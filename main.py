#!/usr/bin/env python3

import sys
import subprocess

def load_problem(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as file:
        n = int(file.readline())

        problem = [[] for _ in range(2*n)]

        for i in range(2*n):
            problem[i] = list(map(int, file.readline().split()))

    return problem

def model_into_number(model: list) -> int:
    val = 0

    for i in range(len(model)):
        val <<= 1

        if model[i]:
            val += 1

    return val

def number_into_model(val: int, n: int) -> list:
    model = [False]*n

    i = 0
    while val > 0:
        if val & 1:
            model[i] = True

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

        if model[j]:
            dimacs.append(-k)
        else:
            dimacs.append(k)

    return " ".join(map(str, dimacs))

def generate_cnf(dnf: list, n: int, start: int, row: bool) -> list:
    cnf = []
    m = len(dnf)

    model_number = [0] * m

    for i in range(m - 1, -1, -1):
        model_number[i] = model_into_number(dnf[i])

    with open("./output/cnf.txt", "a", encoding="utf-8") as file:
        for i in range(1<<n):
            if not i in model_number:
                file.write(dimacs_cnf(number_into_model(i, n), n, start, row) + " 0 \n")

    return cnf

def encode_to_dnf_recur(params: list, idx: int, start: int, n: int, all_models: list, active: list) -> None:
    if idx == len(params):
        all_models.append(list(active))
        return

    offset = -1 if idx == len(params) - 1 else 0

    for i in range(start, n - params[idx] - offset):
        for j in range(i, i + params[idx]):
            active[j] = True

        encode_to_dnf_recur(params, idx + 1, i + params[idx] + 1, n, all_models, active)

        for j in range(i, i + params[idx]):
            active[j] = False

def encode(problem: list) -> None:
    cnf = []
    n = len(problem) // 2

    all_models = []

    with open("./output/cnf.txt", "w", encoding="utf-8") as _:
        pass

    for i in range(n * 2):
        all_models.clear()
        
        encode_to_dnf_recur(problem[i], 0, 0, n, all_models, [False] * n)

        if i < n:
            cnf.append(generate_cnf(all_models, n, i, False))
        else:
            cnf.append(generate_cnf(all_models, n, (i-n)*n, True))

##############
# DISCLAIMER #
##############

#Functions call_glucose and print_result were strongly inspired by sample solution, as was said that it is allowed.

def call_glucose():
    return subprocess.run(["./glucose-simp", "-model", "./output/cnf.txt"], stdout=subprocess.PIPE)

def print_result(result, problem):
    n = len(problem) // 2

    for line in result.stdout.decode('utf-8').split("\n"):
        print(line)

    if (result.returncode == 20):
        print("NEMÁ ŘEŠENÍ")
        return

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):   
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)      
    model.remove(0) 

    for i in range(n):
        for j in range(n):
            if model[i*n + j] > 0:
                print("#", end="")
            else:
                print(".", end="")
        print("")

def main():
    problem = load_problem(sys.argv[1])

    encode(problem)

    result = call_glucose()
    print_result(result, problem)

if __name__ == "__main__":
    main()