from sugarrush.solver import SugarRush

# Exercise 2 in 7.2.2.2 TAOCP

def run_pincus():
    solver = SugarRush()

    dancing = solver.var()
    happy = solver.var()
    healthy = solver.var()
    lazy = solver.var()

    # healthy but not lazy like dancing
    # (healthy AND NOT lazy) => dancing
    # (NOT healthy OR lazy OR dancing)
    solver.add([-healthy, lazy, dancing])

    # lazy nondancers are happy
    solver.add([-lazy, dancing, happy])

    # healthy dancers are happy
    solver.add([-healthy, -dancing, happy])

    # happy nondancers are healthy
    solver.add([-happy, dancing, healthy])

    # lazy and healthy aren't happy
    solver.add([-lazy, -healthy, -happy])

    # unhappy unhealthy are always lazy
    solver.add([happy, healthy, lazy])

    # lazy dancers are healhy
    solver.add([-lazy, -dancing, healthy])

    status = solver.solve()
    print("Satisfiable: {}".format(status))

    if status:
        print("dancing: {}".format(solver.solution_value(dancing)))
        print("happy: {}".format(solver.solution_value(happy)))
        print("healthy: {}".format(solver.solution_value(healthy)))
        print("lazy: {}".format(solver.solution_value(lazy)))

    # solver.solve(assumptions=[-dancing]) is not satisfiable => all are dancing
    # solver.solve(assumptions=[-happy]) is not satisfiable => all are happy
    # solver.solve(assumptions=[lazy]) is not satisfiable => none are lazy

    # solver.solve(assumptions=[healthy]) is satisfiable
    # solver.solve(assumptions=[-healthy]) is satisfiable
    # so we can't conclude anything about their health
    

if __name__ == '__main__':
    run_pincus()