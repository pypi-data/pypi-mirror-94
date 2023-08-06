# Tests that sugarrush works as expected
# Also a showcase of how to use the functionality

from sugarrush.solver import SugarRush

FAIL = '\033[91m'
OKAY = '\033[94m'
ENDC = '\033[0m'

def plus_test():
    solver = SugarRush()

    N = 4
    a = [solver.var() for _ in range(N)]
    b = [solver.var() for _ in range(N)]
    z = [solver.var() for _ in range(N)]

    cnf = solver.plus(a, b, z)
    solver.add(cnf)

    for i in range(2**N):
        a_assumptions = to_binary(N, i, a)
        for j in range(2**N):
            b_assumptions = to_binary(N, j, b)
            solver.solve(assumptions = a_assumptions + b_assumptions)
            z_solve = [solver.solution_value(zp) for zp in z]
            z_int = sum([2**i * zp for i, zp in enumerate(z_solve[::-1])])
            if z_int != (i + j) % 2**N:
                s = "plus_test error: ({2:d} + {3:d}) % 2^{0:d} != {1:d}" \
                    .format(N, z_int, i, j)
                print(FAIL + s, ENDC)
                break
        else:
            continue
        break
    else:
        print(OKAY + "plus_test passed", ENDC)
        return True
    return False


def to_binary(N, n, a):
    n = n % 2**N
    b = "{1:0{0:d}b}".format(N, n)
    return [ap if bp == '1' else -ap for bp, ap in zip(b, a)]  


def less_test():
    solver = SugarRush()

    N = 4
    a = [solver.var() for _ in range(N)]
    b = [solver.var() for _ in range(N)]    

    t, cnf = solver.less(a, b)
    solver.add(cnf)
    solver.add([t])

    for i in range(2**N):
        a_assumptions = to_binary(N, i, a)
        for j in range(2**N):
            b_assumptions = to_binary(N, j, b)
            satisfiable = solver.solve(assumptions = a_assumptions + b_assumptions)
            if satisfiable and (i >= j):
                print(FAIL + "less_test false positive:", i, j, ENDC)
                break
            if (not satisfiable) and (i < j):
                print(FAIL + "less_test false negative:", i, j, ENDC)
                break                
        else:
            continue
        break
    else:
        print(OKAY + "less_test passed", ENDC)
        return True
    return False

def leq_test():
    solver = SugarRush()

    N = 4
    a = [solver.var() for _ in range(N)]
    b = [solver.var() for _ in range(N)]    

    t, cnf = solver.leq(a, b)
    solver.add(cnf)
    solver.add([t])

    for i in range(2**N):
        a_assumptions = to_binary(N, i, a)
        for j in range(2**N):
            b_assumptions = to_binary(N, j, b)
            satisfiable = solver.solve(assumptions = a_assumptions + b_assumptions)
            if satisfiable and (i > j):
                print(FAIL + "leq_test false positive:", i, j, ENDC)
                break
            if (not satisfiable) and (i <= j):
                print(FAIL + "leq_test false negative:", i, j, ENDC)
                break
        else:
            continue
        break
    else:
        print(OKAY + "leq_test passed", ENDC)
        return True
    return False

def run_all_tests():
    less_test()
    leq_test()
    plus_test()

if __name__ == '__main__':
    run_all_tests()
