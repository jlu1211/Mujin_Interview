import numpy as np
import time

# --- 2D Grid Logic ---
class PalletGrid:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.grid = np.zeros((length, width), dtype=np.int8)
        self.placements = []

    def is_region_empty(self, x, y, l, w):
        if x + l > self.length or y + w > self.width:
            return False
        return not np.any(self.grid[x : x + l, y : y + w])

    def place_item(self, x, y, l, w, name="X"):
        self.grid[x : x + l, y : y + w] = 1
        self.placements.append((name, x, y, l, w))

    def remove_item(self, x, y, l, w, name):
        """Used by backtracking to UNDO a placement."""
        self.grid[x : x + l, y : y + w] = 0
        self.placements.remove((name, x, y, l, w))

    def visualize_to_file(self, filename="layout_backtracking.txt", scale=20):
        rows = self.length // scale
        cols = self.width // scale
        canvas = [['.' for _ in range(cols)] for _ in range(rows)]
        
        for (name, x, y, l, w) in self.placements:
            r_start, c_start = x // scale, y // scale
            r_end, c_end = (x + l) // scale, (y + w) // scale
            char = name[0]
            for r in range(r_start, min(r_end, rows)):
                for c in range(c_start, min(c_end, cols)):
                    canvas[r][c] = char

        with open(filename, "w") as f:
            f.write(f"BACKTRACKING Visualization (Scale: 1 char = {scale}mm)\n")
            f.write(f"Grid Size: {self.length}x{self.width}\n")
            f.write("-" * (cols + 2) + "\n")
            for row in canvas:
                f.write("|" + "".join(row) + "|\n")
            f.write("-" * (cols + 2) + "\n")
        print(f"📄 Visualization saved to: {filename}")

# --- Recursive Solver with Print Logging ---
def solve_recursive(pallet, boxes_to_pack, depth=0):
    # Indentation string for visualization
    indent = "  " * depth

    # BASE CASE: No boxes left -> Success
    if not boxes_to_pack:
        print(f"{indent}🎉 All boxes placed successfully!")
        return True

    # Get the next box
    current_box = boxes_to_pack[0]
    remaining_boxes = boxes_to_pack[1:]
    name, l, w, h = current_box

    print(f"{indent}Trying to place box {name} ({l}x{w})...")

    # Optimization: Step size > 1 speeds up search but might miss tight fits.
    # Set step=1 for perfect precision (very slow), step=10 for speed.
    step = 50 
    
    # Iterate through potential positions
    for r in range(0, pallet.length - l + 1, step):
        for c in range(0, pallet.width - w + 1, step):
            
            # Check if empty
            if pallet.grid[r, c] == 0 and pallet.is_region_empty(r, c, l, w):
                
                # DO: Place the box
                pallet.place_item(r, c, l, w, name)
                # print(f"{indent}  -> Placed {name} at ({r}, {c})") # Optional verbose
                
                # RECURSE: Try to pack the rest
                if solve_recursive(pallet, remaining_boxes, depth + 1):
                    return True
                
                # UNDO: Backtrack
                # print(f"{indent}  ❌ Backtracking {name} from ({r}, {c})...") # Optional verbose
                pallet.remove_item(r, c, l, w, name)

    print(f"{indent}⚠️ Failed to fit box {name} anywhere. Going back up...")
    return False

# --- Core Logic ---
def find_four_same_height(boxes):
    height_groups = {}
    for b in boxes:
        h = b[3]
        height_groups.setdefault(h, []).append(b)
    for h, group in height_groups.items():
        if len(group) >= 4:
            return group[:4]
    return None

def compute_possibility(skus, boxes, pallet_l, pallet_w, layout_filename=None):
    # 1. Identify Corners
    corner_boxes = find_four_same_height(boxes)
    if corner_boxes is None:
        print("No set of 4 same height boxes available for corners")
        return False
    
    for b in corner_boxes:
        boxes.remove(b)

    # 2. Setup Grid
    pallet = PalletGrid(pallet_l, pallet_w)

    # 3. Place Corners
    c1, c2, c3, c4 = corner_boxes
    pallet.place_item(0, 0, c1[1], c1[2], c1[0])
    pallet.place_item(0, pallet_w - c2[2], c2[1], c2[2], c2[0])
    pallet.place_item(pallet_l - c3[1], 0, c3[1], c3[2], c3[0])
    pallet.place_item(pallet_l - c4[1], pallet_w - c4[2], c4[1], c4[2], c4[0])
    
    print("Corners placed. Starting Recursive Solver...\n")

    # 4. Start Recursive Solver
    # Sort largest to smallest (Heuristic to speed up recursion)
    boxes.sort(key=lambda x: x[1]*x[2], reverse=True)

    start_time = time.perf_counter()
    
    # We pass depth=0 to start indentation
    success = solve_recursive(pallet, boxes, depth=0)

    elapsed = (time.perf_counter() - start_time) * 1000

    if success:
        print(f"\n✅ BACKTRACKING Success! Time: {elapsed:.4f} ms")
        filename = layout_filename if layout_filename else "layout_backtracking.txt"
        pallet.visualize_to_file(filename)
        return True
    else:
        print(f"\n❌ Failed to find a solution after {elapsed:.4f} ms")
        return False

if __name__ == "__main__":
    pallet_l, pallet_w = 1200, 800
    
    skus = {
        'A': [206, 198, 278, 6],
        'B': [360, 300, 165, 2],
        'C': [388, 280, 192, 1],
        'D': [370, 298, 220, 1]
    }
    
    boxes = []
    # Add unique IDs to names so we can track specific boxes in logs
    count_id = 1
    for name, (L, W, H, count) in skus.items():
        for _ in range(count):
            boxes.append((f"{name}_{count_id}", L, W, H))
            count_id += 1
    
    compute_possibility(skus, boxes, pallet_l, pallet_w)