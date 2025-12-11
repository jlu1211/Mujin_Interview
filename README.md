# Mujin Pallet Feasibility Checker

## 📌 Problem Statement

Given a pallet of fixed size and a set of boxes with fixed dimensions (L × W × H) and fixed quantities, determine whether all boxes can fit on a **single layer** of a pallet in a **stable** arrangement.

Stability in this simplified model is defined as:

1. Selecting **four boxes of the same height** to serve as the four pallet corners.
2. Ensuring that the **remaining boxes** can fit inside the **remaining usable pallet area** without overlapping.
3. Boxes are not rotatable — each dimension is fixed.

---

## ✅ What Has Been Implemented

### 1. **Corner Placement Heuristic**

- Automatically finds **four boxes with identical height**.
- Places them at the four extremes of the pallet (Top-Left, Top-Right, Bottom-Left, Bottom-Right) to form a stable outer frame.

### 2. **2D Grid Engine (Geometry-Aware)**

- **Discretized Grid**: Models the pallet as a binary Matrix (`numpy` array) where `0` is empty and `1` is occupied.
- **Collision Detection**: Strictly enforces geometric boundaries. Boxes cannot overlap or extend beyond the pallet edges.
- **Position Search Optimization**: Both algorithms use a 50mm step size when searching for placement positions, significantly improving performance while maintaining solution quality. This reduces the search space from millions of positions to hundreds per box.
- **Visualization**: Generates ASCII text files to visualize the exact physical layout of the boxes. When running the test suite, layouts are saved in the `layout_result/` folder with names like `test_1_greedy.txt`, `test_1_dp.txt`, etc.

### 3. **Dual Solver Strategies**

The project now includes two distinct algorithms to solve the packing problem:

#### A. Greedy Solver (`greedy.py`)

- **Algorithm**: First-Fit Decreasing.
- **Logic**: Sorts all remaining boxes by area (Largest to Smallest) and places them in the first available spot on the grid using a 50mm step size for efficient searching.
- **Pros**: Fast and efficient. Typically completes in milliseconds for most cases.
- **Cons**: Can fail to find a solution even if one exists (due to fragmentation). May miss optimal placements due to greedy nature.

#### B. Recursive Backtracking Solver (`dp_backtrack.py`)

- **Algorithm**: Depth-First Search (DFS) with Backtracking.
- **Logic**: Tries to place a box at positions spaced 50mm apart; if successful, recurses to the next box. If it reaches a dead end, it **backtracks** (removes the box) and tries the next coordinate. This systematic exploration ensures completeness.
- **Pros**: Exact and complete. If a solution exists within the search space, it will find it. Handles complex fragmentation cases that greedy may miss.
- **Cons**: Can be slower than greedy in worst-case scenarios (exponential time complexity), but optimized step size keeps it practical. Includes verbose logging to trace the decision tree.

---

## 🚀 How to Run

### 1. Run Individual Solvers

#### Greedy Solver

Fast check for feasibility. Saves layout to `layout_greedy.txt`.

```bash
python greedy.py
```

#### Backtracking Solver

Exact solution finder. Saves layout to `layout_backtracking.txt`.

```bash
python dp_backtrack.py
```

### 2. Run Test Suite

Run all test cases from `test_cases.json` and compare both algorithms:

```bash
python test_runner.py
```

This will:

- Execute both greedy and backtracking algorithms on all test cases
- Display a comparison table with timing and pass/fail status
- Save all layout visualizations to the `layout_result/` folder:
  - `test_1_greedy.txt`, `test_1_dp.txt`
  - `test_2_greedy.txt`, `test_2_dp.txt`
  - ... and so on for each test case

The test runner creates the `layout_result/` directory automatically if it doesn't exist.

## 📝 TODO Status

* [X] **Implement 2D grid-based pallet discretization** - [x] Convert pallet surface into (x, y) grid
  * [X] Map each box footprint onto grid cells
  * [X] Prevent box overlap and out-of-bound placement
* [X] **Add more accurate geometric feasibility checks** - [x] Consider real L × W packing, not just total area
  * [X] Respect exact box placement
* [X] **Visualization** - [x] Generate simple ASCII or grid-based visual output to text files
* [ ] **Prototype full 3D DP solver** - Represent pallet volume in discrete (x, y, z) space
  * Allow vertical stacking and layer transitions
* [ ] **Support optional box rotation** - Allow L/W swap during `find_fit` checks
* [ ] **Add stability metrics** - Center of mass calculations
  * Bottom support ratio for each box
* [ ] **Add CLI interface** - Allow user to specify pallet size and SKUs via command line arguments
* [ ] **Add Unit Tests** - Create `test_mujin.py` to verify edge cases (empty lists, oversized boxes, etc.) automatically.
