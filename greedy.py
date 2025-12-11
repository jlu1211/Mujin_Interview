import numpy as np
import time

# --- 2D Grid Logic ---
class PalletGrid:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        # 0 = empty, 1 = occupied
        self.grid = np.zeros((length, width), dtype=np.int8)
        self.placements = []

    def is_region_empty(self, x, y, l, w):
        if x + l > self.length or y + w > self.width:
            return False
        return not np.any(self.grid[x : x + l, y : y + w])

    def place_item(self, x, y, l, w, name="X"):
        self.grid[x : x + l, y : y + w] = 1
        self.placements.append((name, x, y, l, w))

    def find_fit(self, l, w):
        # Greedy search: Scan for the first valid empty spot
        # Use step size to speed up search (same as backtracking for fair comparison)
        step = 50  # Match backtracking's step size for performance
        for r in range(0, self.length - l + 1, step):
            for c in range(0, self.width - w + 1, step):
                if self.grid[r, c] == 0: 
                    if self.is_region_empty(r, c, l, w):
                        return r, c
        return None, None

    def visualize_to_file(self, filename="layout_greedy.txt", scale=20):
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
            f.write(f"GREEDY Visualization (Scale: 1 char = {scale}mm)\n")
            f.write(f"Grid Size: {self.length}x{self.width}\n")
            f.write("-" * (cols + 2) + "\n")
            for row in canvas:
                f.write("|" + "".join(row) + "|\n")
            f.write("-" * (cols + 2) + "\n")
        print(f"📄 Visualization saved to: {filename}")

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
    
    # 4. Greedy Packing Loop
    # Sort largest to smallest to improve chances
    boxes.sort(key=lambda x: x[1]*x[2], reverse=True)

    start_time = time.perf_counter()
    
    for box in boxes:
        name, l, w, h = box
        x, y = pallet.find_fit(l, w)
        
        if x is not None:
            pallet.place_item(x, y, l, w, name)
        else:
            print(f"❌ Failed to fit box {name}")
            return False

    elapsed = (time.perf_counter() - start_time) * 1000
    print(f"✅ GREEDY Success! Time: {elapsed:.4f} ms")
    
    filename = layout_filename if layout_filename else "layout_greedy.txt"
    pallet.visualize_to_file(filename)
    return True

if __name__ == "__main__":
    pallet_l, pallet_w = 1200, 800
    
    # Data Setup
    skus = {
        'A': [206, 198, 278, 6],
        'B': [360, 300, 165, 2],
        'C': [388, 280, 192, 1],
        'D': [370, 298, 220, 1]
    }
    
    boxes = []
    for name, (L, W, H, count) in skus.items():
        for _ in range(count):
            boxes.append((name, L, W, H))
    
    compute_possibility(skus, boxes, pallet_l, pallet_w)