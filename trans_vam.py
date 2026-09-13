
import numpy as np


def calculate_cost(allocation, cost):
    return np.sum(allocation * cost)


def vogel_approximation(cost, supply, demand):

    cost = np.array(cost, dtype=float)
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)

    rows, cols = cost.shape

    allocation = np.zeros((rows, cols))

    print("\n" + "=" * 70)
    print("VOGEL'S APPROXIMATION METHOD (VAM)")
    print("=" * 70)

    step = 1

    while np.sum(supply) > 0 and np.sum(demand) > 0:

        # Calculate row penalties
        row_penalty = []

        for i in range(rows):

            if supply[i] == 0:
                row_penalty.append(-1)
                continue

            available = []

            for j in range(cols):
                if demand[j] > 0:
                    available.append(cost[i][j])

            if len(available) >= 2:
                available.sort()
                penalty = available[1] - available[0]

            elif len(available) == 1:
                penalty = available[0]

            else:
                penalty = -1

            row_penalty.append(penalty)

        # Calculate column penalties
        col_penalty = []

        for j in range(cols):

            if demand[j] == 0:
                col_penalty.append(-1)
                continue

            available = []

            for i in range(rows):
                if supply[i] > 0:
                    available.append(cost[i][j])

            if len(available) >= 2:
                available.sort()
                penalty = available[1] - available[0]

            elif len(available) == 1:
                penalty = available[0]

            else:
                penalty = -1

            col_penalty.append(penalty)

        # Display penalties
       
        print(f"\n--- Step {step} ---")

        print("Row penalties:")

        for i in range(rows):
            if row_penalty[i] != -1:
                print(f"S{i + 1} = {row_penalty[i]:g}")

        print("\nColumn penalties:")

        for j in range(cols):
            if col_penalty[j] != -1:
                print(f"D{j + 1} = {col_penalty[j]:g}")

        # Find maximum penalty
      
        max_row = max(row_penalty)
        max_col = max(col_penalty)

        # Select row or column having maximum penalty
    
        if max_row >= max_col:

            i = row_penalty.index(max_row)

            # Find cheapest cell in selected row
            available_columns = [
                j for j in range(cols)
                if demand[j] > 0
            ]

            j = min(
                available_columns,
                key=lambda x: cost[i][x]
            )

            print(
                f"\nMaximum penalty = {max_row:g}"
            )
            print(
                f"Selected row = S{i + 1}"
            )

        else:

            j = col_penalty.index(max_col)

            # Find cheapest cell in selected column
            available_rows = [
                i for i in range(rows)
                if supply[i] > 0
            ]

            i = min(
                available_rows,
                key=lambda x: cost[x][j]
            )

            print(
                f"\nMaximum penalty = {max_col:g}"
            )
            print(
                f"Selected column = D{j + 1}"
            )

        # Allocate as much as possible
       
        quantity = min(supply[i], demand[j])

        print(
            f"Selected cell = S{i + 1} -> D{j + 1}"
        )

        print(
            f"Transportation cost = {cost[i][j]:g}"
        )

        print(
            f"Allocation = min("
            f"{supply[i]:g}, {demand[j]:g}) "
            f"= {quantity:g}"
        )

        allocation[i][j] += quantity

        supply[i] -= quantity
        demand[j] -= quantity

        print(
            f"Allocate {quantity:g} unit(s)"
        )

        print(
            "Remaining supply:",
            supply.astype(int)
        )

        print(
            "Remaining demand:",
            demand.astype(int)
        )

        step += 1

    # Display final VAM allocation
    
    print("\n" + "=" * 70)
    print("INITIAL BASIC FEASIBLE SOLUTION")
    print("=" * 70)

    print("\nAllocation Matrix:")

    print(allocation.astype(int))

    initial_cost = calculate_cost(
        allocation,
        cost
    )

    print(
        f"\nInitial Transportation Cost = "
        f"{initial_cost:.2f}"
    )

    return allocation

# MAIN PROGRAM

def main():

    # Transportation cost matrix
    cost = np.array([
        [19, 30, 50, 10],
        [70, 30, 40, 60],
        [40,  8, 70, 20]
    ])

    # Supply of each source
    supply = np.array([
        7,
        9,
        18
    ])

    # Demand of each destination
    demand = np.array([
        5,
        8,
        7,
        14
    ])

    print("\nTRANSPORTATION PROBLEM")

    print("\nCost Matrix:")
    print(cost)

    print("\nSupply:")
    print(supply)

    print("\nDemand:")
    print(demand)

    if np.sum(supply) != np.sum(demand):
        print("\nProblem is unbalanced.")
        return

    print("\nProblem is balanced.")

    allocation = vogel_approximation(
        cost,
        supply,
        demand
    )

if __name__ == "__main__":
    main()
