import sys

def load_problem(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as file:
        n = int(file.readline())

        problem = [[] for _ in range(2*n)]

        for i in range(2*n):
            problem[i] = list(map(int, file.readline().split()))

    return problem

def encode(problem: list) -> list:
    cnf = []


    return cnf

def main():
    problem = load_problem(sys.argv[1])

    print(problem)

if __name__ == "__main__":
    main()