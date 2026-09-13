# Transportation Problem using VAM and MODI

## 📌 Problem Description
In this project, the Transportation Problem is solved using:

1. **Vogel's Approximation Method (VAM)** – to obtain an Initial Basic Feasible Solution (IBFS).
2. **MODI (Modified Distribution) Method** – to test the initial solution for optimality and improve it iteratively until the optimal solution is obtained.

---

## 🎯 Objective

The objective is to determine:

- The optimal shipment quantity from each source to each destination.
- The minimum total transportation cost.
- The initial feasible solution obtained using VAM.
- The improvements made using the MODI method.

---

## 📊 Transportation Problem

There are **3 sources** and **4 destinations**.

### Transportation Cost Matrix

| Source / Destination | D1 | D2 | D3 | D4 | Supply |
|----------------------|----|----|----|----|--------|
| S1 | 19 | 30 | 50 | 10 | 7 |
| S2 | 70 | 30 | 40 | 60 | 9 |
| S3 | 40 | 8 | 70 | 20 | 18 |
| **Demand** | **5** | **8** | **7** | **14** | |

### Total Supply

$$
7 + 9 + 18 = 34
$$

### Total Demand

$$
5 + 8 + 7 + 14 = 34
$$

Therefore,

$$
\text{Total Supply} = \text{Total Demand}
$$

Hence, the transportation problem is **balanced**.

---

## 🔹 Step 1: Vogel's Approximation Method (VAM)

VAM is used to obtain an Initial Basic Feasible Solution.

At each iteration:

1. Calculate the penalty for every available row.
2. Calculate the penalty for every available column.
3. Select the row or column having the maximum penalty.
4. Select the least-cost cell in that row/column.
5. Allocate as much as possible to that cell.
6. Update the supply and demand.
7. Repeat until all supply and demand requirements are satisfied.

### Initial Solution obtained using VAM

| Source / Destination | D1 | D2 | D3 | D4 | Supply |
|----------------------|----|----|----|----|--------|
| S1 | 5 | 0 | 0 | 2 | 7 |
| S2 | 0 | 0 | 7 | 2 | 9 |
| S3 | 0 | 8 | 0 | 10 | 18 |
| **Demand** | **5** | **8** | **7** | **14** | |

### VAM Transportation Cost

$$
5(19) + 2(10) + 7(40) + 2(60) + 8(8) + 10(20)
$$

$$
= 95 + 20 + 280 + 120 + 64 + 200
$$

$$
\boxed{779}
$$

Therefore, the **initial transportation cost obtained using VAM is 779**.

> Note: VAM provides a good Initial Basic Feasible Solution, but it does not necessarily guarantee the optimal solution.

---

## 🔹 Step 2: MODI Method

The MODI method is used to check whether the VAM solution is optimal.

For each basic cell, the following relationship is used:

$$
u_i + v_j = c_{ij}
$$

where:

- $u_i$ = row potential
- $v_j$ = column potential
- $c_{ij}$ = transportation cost

For every non-basic cell, calculate the opportunity cost:

$$
\Delta_{ij} = c_{ij} - (u_i + v_j)
$$

### Optimality Condition

For a minimization transportation problem:

$$
\Delta_{ij} \geq 0
$$

for all non-basic cells.

If any:

$$
\Delta_{ij} < 0
$$

then the current solution is not optimal and the allocation must be improved.

---

## 🔄 MODI Iteration 1

The most negative opportunity cost is:

$$
\Delta_{S2,D2} = -18
$$

Therefore, cell **S2-D2** enters the basis.

A closed loop is formed and the allocations are adjusted.

The improved transportation plan becomes:

| Source / Destination | D1 | D2 | D3 | D4 | Supply |
|----------------------|----|----|----|----|--------|
| S1 | 5 | 0 | 0 | 2 | 7 |
| S2 | 0 | 2 | 7 | 0 | 9 |
| S3 | 0 | 6 | 0 | 12 | 18 |
| **Demand** | **5** | **8** | **7** | **14** | |

### Improved Cost

$$
5(19) + 2(10) + 2(30) + 7(40) + 6(8) + 12(20)
$$

$$
= 95 + 20 + 60 + 280 + 48 + 240
$$

$$
\boxed{743}
$$

---

## ✅ Optimality Test

After the MODI improvement, all opportunity costs satisfy:

$$
\Delta_{ij} \geq 0
$$

Therefore, the current transportation plan is **optimal**.

---

## 🏆 Final Optimal Shipment Plan

| Source / Destination | D1 | D2 | D3 | D4 |
|----------------------|----|----|----|----|
| **S1** | 5 | 0 | 0 | 2 |
| **S2** | 0 | 2 | 7 | 0 |
| **S3** | 0 | 6 | 0 | 12 |

The optimal shipments are:

- S1 → D1 = **5 units**
- S1 → D4 = **2 units**
- S2 → D2 = **2 units**
- S2 → D3 = **7 units**
- S3 → D2 = **6 units**
- S3 → D4 = **12 units**

---

## 💰 Final Minimum Transportation Cost

$$
\boxed{743}
$$

Therefore:

| Method | Cost |
|--------|------|
| VAM Initial Solution | 779 |
| After MODI Improvement | 743 |
| **Optimal Cost** | **743** |

The MODI method reduces the transportation cost from:

$$
779 \rightarrow 743
$$

Thus, the **minimum transportation cost is 743**.

---

## 🛠️ Technologies Used

- **Python 3**
- **NumPy**
- Vogel's Approximation Method (VAM)
- MODI (Modified Distribution) Method

---

