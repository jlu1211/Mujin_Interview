# Mujin Pallet Feasibility Checker

## 📌 Problem Statement
Given a pallet of fixed size and a set of boxes with fixed dimensions (L × W × H) and fixed quantities, determine whether all boxes can fit on a **single layer** of a pallet in a **stable** arrangement.

Stability in this simplified model is defined as:
1. Selecting **four boxes of the same height** to serve as the four pallet corners.
2. Ensuring that the **remaining boxes** can fit inside the **remaining usable pallet area** after the corners are placed.
3. Boxes are not rotatable — each dimension is fixed.

This is not a full geometric packing model; the goal is to build a clean, explainable algorithmic approach using heuristics and dynamic programming.

---

## ✅ What Has Been Implemented
### 1. **Corner Placement Heuristic**
- Automatically finds **four boxes with identical height**.
- These are treated as the four pallet corners to form a stable outer frame.

### 2. **Area-Based Capacity Check**
- Calculates the footprint area of the four corner boxes.
- Subtracts their area from the pallet area to get the **remaining capacity**.

### 3. **Dynamic Programming (1D DP) Feasibility Check**
- Models the remaining boxes as fixed items with fixed areas.
- Uses a **subset-sum / knapsack-style DP** to check if the exact total footprint of the remaining boxes fits inside the remaining pallet capacity.
- Ensures all remaining boxes are used.

### 4. **Adjustable Pallet Dimensions**
- Pallet length and width can be changed directly in the code.
- The DP logic automatically adapts.

### 5. **Pure Python**
- No OR-Tools, no PuLP, no external solvers.
- Simple, clear logic, easy to read and explain.

---

## 🚧 What Will Be Done in the Future
The next major step is a **3D DP model** for more realistic packing.

Planned features include:

### 🔜 1. **2D Geometry-Aware Placement (in progress)**
- Discretized pallet into grid cells.
- Check actual box placement, not only total area.
- Prevent overlap and out-of-bound placement.

### 🔜 2. **Full 3D DP Prototype**
- State representation like:


## 📝 TODO

- [ ] Implement 2D grid-based pallet discretization  
  - Convert pallet surface into coarse (x, y) grid  
  - Map each box footprint onto grid cells  
  - Prevent box overlap and out-of-bound placement  

- [ ] Add more accurate geometric feasibility checks  
  - Consider real L × W packing, not just total area  
  - Respect exact box placement instead of area-only DP  

- [ ] Prototype full 3D DP solver  
  - Represent pallet volume in discrete (x, y, z) space  
  - Allow vertical stacking and layer transitions  
  - Track box occupancy and stability in all 3 dimensions  

- [ ] Support optional box rotation  
  - Allow L/W swap  
  - Later: allow full 6-orientation support in 3D  

- [ ] Add stability metrics  
  - Center of mass calculations  
  - Bottom support ratio for each box  
  - Prevent unstable overhangs  

- [ ] Visualization  
  - Generate simple ASCII or grid-based visual output  
  - (Future) Consider matplotlib or a lightweight viewer  

- [ ] Add CLI interface  
  - Specify pallet size and SKUs from command line  
  - Output feasibility summary  

- [ ] Add tests  
  - Unit tests for DP  
  - Tests for corner selection  
  - Edge cases (no matching heights, pallet too small, etc.)


