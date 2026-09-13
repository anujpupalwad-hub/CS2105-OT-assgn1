import numpy as np


def big_m_simplex(c, A, b, signs, M=1e6):
    """
    Big-M Simplex Method for maximization.

    c      : objective coefficients
    A      : constraint coefficient matrix
    b      : RHS values
    signs  : constraint signs: <=, >=, =
    M      : Big-M penalty
    """

    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    m, n = A.shape

    #Step1 convert constrains into standard form

    columns = [A[:, j].copy() for j in range(n)]
    variable_names = [f"x{j + 1}" for j in range(n)]

    artificial_indices = []

    for i, sign in enumerate(signs):

        if sign == "<=":
            # Add slack variable
            col = np.zeros(m)
            col[i] = 1

            columns.append(col)
            variable_names.append(f"s{i + 1}")

        elif sign == ">=":
            # Add surplus variable (-1)
            col = np.zeros(m)
            col[i] = -1

            columns.append(col)
            variable_names.append(f"s{i + 1}")

            # Add artificial variable (+1)
            col = np.zeros(m)
            col[i] = 1

            artificial_indices.append(len(columns)+1)
            columns.append(col)
            variable_names.append(f"a{i + 1}")

        elif sign == "=":
            # Add artificial variable
            col = np.zeros(m)
            col[i] = 1

            artificial_indices.append(len(columns)+1)
            columns.append(col)
            variable_names.append(f"a{i + 1}")

        else:
            raise ValueError("Constraint must be <=, >= or =")

    A_std = np.column_stack(columns)
    total_vars = len(variable_names)

    # -------------------------------------------------
    # STEP 2: Objective function

    obj = np.zeros(total_vars)
    obj[:n] = c

    # Big-M penalty
    for idx in artificial_indices:
        obj[idx - 1] = -M

    # -------------------------------------------------
    # STEP 3: Find initial basic variables

    basis = []

    for i in range(m):

        found = False

        for j in range(n, total_vars):

            column = A_std[:, j]

            if abs(column[i] - 1) < 1e-9 and \
               all(abs(column[k]) < 1e-9 for k in range(m) if k != i):

                # Do not use artificial variables unless necessary
                if signs[i] in (">=", "="):
                    if j + 1 in artificial_indices:
                        basis.append(j)
                        found = True
                        break
                else:
                    basis.append(j)
                    found = True
                    break

        if not found:
            raise ValueError("Could not find an initial basis.")

    # -------------------------------------------------
    # STEP 4: Simplex iterations

    iteration = 0

    while True:

        iteration += 1

        # Calculate Cj - Zj
        cB = obj[basis]

        zj = cB @ A_std
        cj_minus_zj = obj - zj

        print("\n" + "=" * 60)
        print("Iteration:", iteration)
        print("=" * 60)

        print("Basis:", [variable_names[i] for i in basis])
        print("Cj - Zj:", np.round(cj_minus_zj, 4))

        # For maximization:
        # positive Cj-Zj means improvement possible
        entering = np.argmax(cj_minus_zj)

        if cj_minus_zj[entering] <= 1e-9:
            break

        # Ratio test
        ratios = []

        for i in range(m):

            if A_std[i, entering] > 1e-9:
                ratios.append(b[i] / A_std[i, entering])
            else:
                ratios.append(np.inf)

        leaving_row = np.argmin(ratios)

        if ratios[leaving_row] == np.inf:
            print("Problem is unbounded.")
            return None

        leaving = basis[leaving_row]

        print("Entering variable:", variable_names[entering])
        print("Leaving variable:", variable_names[leaving])

        # -------------------------------------------------
        # Pivot operation
        

        pivot = A_std[leaving_row, entering]

        A_std[leaving_row] /= pivot
        b[leaving_row] /= pivot

        for i in range(m):

            if i != leaving_row:

                factor = A_std[i, entering]

                A_std[i] -= factor * A_std[leaving_row]
                b[i] -= factor * b[leaving_row]

        basis[leaving_row] = entering

    # -------------------------------------------------
    # STEP 5: Extract solution
    

    solution = np.zeros(total_vars)

    for i, basic_variable in enumerate(basis):
        solution[basic_variable] = b[i]

    Z = obj @ solution

    # Check artificial variables
    for idx in artificial_indices:
        if solution[idx - 1] > 1e-6:
            print("\nNo feasible solution.")
            return None

    print("\n" + "=" * 60)
    print("OPTIMAL SOLUTION")
    print("=" * 60)

    for i in range(total_vars):
        print(f"{variable_names[i]} = {solution[i]:.4f}")

    print(f"\nMaximum Profit = {Z:.4f}")

    return solution, Z


#Problem Data
#Maximize Z = 40*x1 + 30*x2

# Constraints:
# 2x1 + 3x2 <= 12
# 2x1 +  x2 <= 8
# x1 >= 1
# x2 >= 1

c = [40, 30]

A = [
    [2, 3],
    [2, 1],
    [1, 0],
    [0, 1]
]

b = [12, 8, 1, 1]

signs = ["<=", "<=", ">=", ">="]


# Solve
big_m_simplex(c, A, b, signs)