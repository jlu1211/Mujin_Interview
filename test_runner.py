import json
import time
import sys
import contextlib
import io
import os

# Import your solvers
# Ensure greedy.py and dp_backtrack.py are in the same folder
try:
    import greedy
    import dp_backtrack
except ImportError:
    print("Error: Could not find 'greedy.py' or 'dp_backtrack.py'.")
    sys.exit(1)

TEST_FILE = "test_cases.json"

def load_tests(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def expand_skus_to_boxes(skus):
    """Converts the compact SKU dictionary into a list of boxes."""
    boxes = []
    uid = 1
    for name, (l, w, h, count) in skus.items():
        for _ in range(count):
            boxes.append((f"{name}_{uid}", l, w, h))
            uid += 1
    return boxes

def run_algo_silently(algo_func, skus, boxes, L, W, layout_filename=None):
    """
    Runs the algorithm but suppresses its print statements 
    so the test runner output stays clean.
    """
    # Capture start time
    start = time.perf_counter()
    
    # Suppress stdout
    with contextlib.redirect_stdout(io.StringIO()):
        # Pass a COPY of boxes because algos modify the list (remove corners)
        boxes_copy = list(boxes) 
        try:
            if layout_filename:
                result = algo_func(skus, boxes_copy, L, W, layout_filename)
            else:
                result = algo_func(skus, boxes_copy, L, W)
        except Exception:
            result = False
            
    duration = (time.perf_counter() - start) * 1000
    return result, duration

def main():
    print(f"Loading tests from {TEST_FILE}...\n")
    test_cases = load_tests(TEST_FILE)

    # Create layout_result directory if it doesn't exist
    layout_dir = "layout_result"
    os.makedirs(layout_dir, exist_ok=True)

    # Table Header
    print(f"{'ID':<4} | {'Name':<25} | {'Exp':<5} | {'Greedy':<8} {'(ms)':<8} | {'Backtrack':<9} {'(ms)':<8} | {'Status'}")
    print("-" * 100)

    for case in test_cases:
        cid = case['id']
        name = case['name']
        L, W = case['pallet']
        skus = case['skus']
        expected = case['expected']

        # Prepare Box Lists
        boxes = expand_skus_to_boxes(skus)

        # Create layout filenames
        greedy_filename = os.path.join(layout_dir, f"test_{cid}_greedy.txt")
        dp_filename = os.path.join(layout_dir, f"test_{cid}_dp.txt")

        # 1. Run Greedy
        res_greedy, time_greedy = run_algo_silently(greedy.compute_possibility, skus, boxes, L, W, greedy_filename)
        
        # 2. Run Backtracking
        res_bt, time_bt = run_algo_silently(dp_backtrack.compute_possibility, skus, boxes, L, W, dp_filename)

        # Formatting Output
        greedy_mark = "PASS" if res_greedy else "FAIL"
        bt_mark = "PASS" if res_bt else "FAIL"
        
        # Determine overall test status
        # Note: Greedy might fail where Backtrack succeeds (e.g., Fragmentation). 
        # Only Backtrack must match Expected for the test to be technically "Correct" geometrically.
        if res_bt == expected:
            status = "✅ OK" 
        else:
            status = "❌ FAIL"

        print(f"{cid:<4} | {name[:25]:<25} | {str(expected):<5} | "
              f"{greedy_mark:<8} {time_greedy:<8.2f} | "
              f"{bt_mark:<9} {time_bt:<8.2f} | {status}")

    print("-" * 100)
    print("Note: 'Greedy' is allowed to fail on complex packing. 'Backtrack' should match 'Exp'.")

if __name__ == "__main__":
    main()