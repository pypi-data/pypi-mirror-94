# Sugar Rush

Additions to python-sat (https://github.com/pysathq/pysat)
to automate some things. Extra features:
- Convert disjunction of CNFs to an equivalent CNF
- Automatic optimization using ITotalizer (binary search)

Design rules
- Only one method adds constraints to the model (solver.add).
  Other methods only return the clauses that define the constraint.
  The reason is that the user may want to negate or reify the constraint,
  i.e. the user may not wish to use the specific constraint.
  Another benefit is that the user can easily grep in the model definition
  code for all places where constraints are added to the model. This
  simplifies debugging.
- The solver's state should only consist of 3 parts:
    1) The active CNF.
    2) The used literals.
    3) The solution values to a satisfied model.
  2) can of course be computed directly from 1), but is kept for performance. 
- The used literals can only be added to, and that should only be done via a
  single method (solver.var). The reason is to prevent strange bugs that
  result from re-using literals that are not meant to be equal. 
- The solution values to a satisfied model should only be accessible from a single 
  method (solver.solution_value). The reason is to prevent bugs resulting from
  different sets of solution values being different from each other. 
- All methods names should be lowercase. Underscore is used to separate words.