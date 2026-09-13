
import numpy as np


# ==========================================================
# CALCULATE TOTAL COST

def calculate_cost(allocation, cost):

    return np.sum(allocation * cost)


# ==========================================================
# FIND CLOSED LOOP
def find_cycle(start, basic, rows, cols):

    cells = set(basic)
    cells.add(start)

    def dfs(path):

        current = path[-1]

        # Closed loop found
        if len(path) >= 4 and current == start:
            return path

        r, c = current

        # --------------------------------------------------
        # Find cells in the same row
       
        possible = []

        for j in range(cols):

            if j != c and (r, j) in cells:
                possible.append((r, j))

        # --------------------------------------------------
        # Find cells in the same column
       
        for i in range(rows):

            if i != r and (i, c) in cells:
                possible.append((i, c))

        for next_cell in possible:

            if next_cell == start:

                if len(path) >= 4:
                    return path + [start]

                continue

            if next_cell in path:
                continue

            # Movement must alternate:
            # row -> column -> row -> column
            if len(path) >= 2:

                previous = path[-2]

                same_row_previous = (
                    previous[0] == r
                )

                same_row_next = (
                    next_cell[0] == r
                )

                if same_row_previous == same_row_next:
                    continue

            result = dfs(
                path + [next_cell]
            )

            if result is not None:
                return result

        return None

    return dfs([start])


# ==========================================================
# MODI METHOD
# ==========================================================

def modi_method(cost, allocation):

    cost = np.array(cost, dtype=float)
    allocation = np.array(
        allocation,
        dtype=float
    )

    rows, cols = cost.shape

    # ------------------------------------------------------
    # Identify basic cells
    # ------------------------------------------------------

    basic = set()

    for i in range(rows):

        for j in range(cols):

            if allocation[i][j] > 0:
                basic.add((i, j))

    iteration = 1

    print("\n" + "=" * 70)
    print("MODI METHOD")
    print("=" * 70)

    while True:

        print("\n" + "-" * 70)
        print(f"MODI ITERATION {iteration}")
        print("-" * 70)

        print("\nCurrent Allocation:")
        print(allocation.astype(int))

        # --------------------------------------------------
        # Calculate u and v
        # --------------------------------------------------

        u = [None] * rows
        v = [None] * cols

        # Set one potential to zero
        u[0] = 0

        changed = True

        while changed:

            changed = False

            for i, j in basic:

                if u[i] is not None and v[j] is None:

                    v[j] = cost[i][j] - u[i]

                    changed = True

                elif v[j] is not None and u[i] is None:

                    u[i] = cost[i][j] - v[j]

                    changed = True

        u = np.array(u, dtype=float)
        v = np.array(v, dtype=float)

        print("\nU values:")
        print(u)

        print("\nV values:")
        print(v)

        # --------------------------------------------------
        # Calculate opportunity costs
        # Δij = cij - (ui + vj)
        # --------------------------------------------------

        delta = np.zeros(
            (rows, cols)
        )

        for i in range(rows):

            for j in range(cols):

                if (i, j) in basic:

                    delta[i][j] = 0

                else:

                    delta[i][j] = (
                        cost[i][j]
                        - u[i]
                        - v[j]
                    )

        print("\nOpportunity Cost Table:")
        print("Δij = cij - (ui + vj)")

        print(delta)

        # --------------------------------------------------
        # Find most negative opportunity cost
        # --------------------------------------------------

        entering = None
        minimum = 0

        for i in range(rows):

            for j in range(cols):

                if (i, j) not in basic:

                    if delta[i][j] < minimum:

                        minimum = delta[i][j]

                        entering = (i, j)

        # --------------------------------------------------
        # Optimality condition
        # --------------------------------------------------

        if entering is None:

            print("\nAll opportunity costs are >= 0.")

            print(
                "Therefore, the solution is OPTIMAL."
            )

            final_cost = calculate_cost(
                allocation,
                cost
            )

            print("\n" + "=" * 70)
            print("FINAL OPTIMAL SOLUTION")
            print("=" * 70)

            print("\nOptimal Allocation:")
            print(allocation.astype(int))

            print(
                f"\nMinimum Transportation Cost = "
                f"{final_cost:.2f}"
            )

            return allocation, final_cost

        # --------------------------------------------------
        # Entering cell
        # --------------------------------------------------

        ei, ej = entering

        print(
            f"\nMost negative opportunity cost:"
            f" Δ(S{ei + 1},D{ej + 1}) = "
            f"{minimum:.2f}"
        )

        print(
            f"Entering cell = "
            f"S{ei + 1} -> D{ej + 1}"
        )

        # --------------------------------------------------
        # Find closed loop
        # --------------------------------------------------

        cycle = find_cycle(
            entering,
            basic,
            rows,
            cols
        )

        if cycle is None:

            print(
                "Error: Could not find a closed loop."
            )

            return

        cycle = cycle[:-1]

        print("\nClosed Loop:")

        for k, (i, j) in enumerate(cycle):

            if k % 2 == 0:
                sign = "+"
            else:
                sign = "-"

            print(
                f"{sign} S{i + 1}-D{j + 1}"
                f"   Allocation = "
                f"{allocation[i][j]:g}"
            )

        # --------------------------------------------------
        # Calculate theta
        # --------------------------------------------------

        minus_cells = []

        for k in range(
            1,
            len(cycle),
            2
        ):

            minus_cells.append(
                cycle[k]
            )

        theta = min(
            allocation[i][j]
            for i, j in minus_cells
        )

        print(
            f"\nTheta = {theta:g}"
        )

        # --------------------------------------------------
        # Improve allocation
        # --------------------------------------------------

        for k, (i, j) in enumerate(cycle):

            if k % 2 == 0:

                allocation[i][j] += theta

            else:

                allocation[i][j] -= theta

        # Entering cell becomes basic
        basic.add(entering)

        # --------------------------------------------------
        # Remove leaving cell
        # --------------------------------------------------

        for cell in minus_cells:

            i, j = cell

            if abs(allocation[i][j]) < 1e-9:

                basic.remove(cell)

                print(
                    f"Leaving cell = "
                    f"S{i + 1} -> D{j + 1}"
                )

                break

        # --------------------------------------------------
        # Display new cost
        # --------------------------------------------------

        new_cost = calculate_cost(
            allocation,
            cost
        )

        print("\nNew Allocation:")

        print(allocation.astype(int))

        print(
            f"\nTransportation Cost = "
            f"{new_cost:.2f}"
        )

        iteration += 1


# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    # ------------------------------------------------------
    # Transportation cost matrix
    # ------------------------------------------------------

    cost = np.array([
        [19, 30, 50, 10],
        [70, 30, 40, 60],
        [40,  8, 70, 20]
    ])

    # ------------------------------------------------------
    # VAM initial basic feasible solution
    # ------------------------------------------------------

    initial_allocation = np.array([
        [5, 0, 0, 2],
        [0, 0, 7, 2],
        [0, 8, 0, 10]
    ])

    print("\nTRANSPORTATION PROBLEM")

    print("\nCost Matrix:")
    print(cost)

    print("\nInitial Allocation from VAM:")
    print(initial_allocation)

    initial_cost = calculate_cost(
        initial_allocation,
        cost
    )

    print(
        f"\nInitial Cost = "
        f"{initial_cost:.2f}"
    )

    # ------------------------------------------------------
    # Run MODI
    # ------------------------------------------------------

    modi_method(
        cost,
        initial_allocation
    )


if __name__ == "__main__":
    main()
