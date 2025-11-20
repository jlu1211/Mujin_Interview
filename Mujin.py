import numpy

# Returns 4 boxes that share same height
def find_four_same_height(boxes):
    height_groups = {}
    for b in boxes:
        h = b[3]
        height_groups.setdefault(h, []).append(b)
    for h, group in height_groups.items():
        if len(group) >= 4:
            return group[:4]
    return None

def area_calc(L, W):
    return L*W

def foot_print_area(skus):
    total_area = 0
    for name, (L, W, H, count) in skus.items():
        box_area = L*W
        if box_area > PALLET_AREA:
            print("Box size exceed pallet size, cannot fit.")
            return False
        total_area += box_area * count

def compute_possibility(skus, boxes):
    corner_boxes = find_four_same_height(boxes)
    remaining_boxes = boxes.copy()
    if corner_boxes is None:
        print("No set of 4 same height boxes available for corners")
        return False
    else:
        print("Selected corner boxes:")
        for b in corner_boxes:
            print(f" {b[0]} L = {b[1]}, W = {b[2]}, H= {b[3]}")
            corner_area = area_calc(b[1], b[2])
            remaining_boxes.remove(b)

    print(f"Total corner area =  {corner_area * 4}")
    remaining_pallet_area = PALLET_AREA - corner_area * 4
    print(f"Remaining pallet area = {remaining_pallet_area}")
    remaining_box_area = 0
    for (name, L, W, H) in remaining_boxes:
        remaining_box_area += area_calc(L, W)
    print(f"Remaining boxes area = {remaining_box_area}")
    if remaining_box_area <= remaining_pallet_area:
        print("All remaining boxes can fit in the pallet.")
        return True
    else:
        print("Remaining boxes cannot fit in the pallet.")
        return False

    
if __name__ == "__main__":
    case_a = [206, 198, 278, 6]
    case_b = [360, 300, 165, 2]
    case_c = [388, 280, 192, 1]
    case_d = [370, 298, 220, 1]

    PALLET_LENGTH = 1200
    PALLET_WIDTH = 800
    PALLET_HEIGHT = 145
    PALLET_AREA = PALLET_WIDTH * PALLET_LENGTH

    skus = {
        'A': case_a,
        'B': case_b,
        'C': case_c,
        'D': case_d
    }
    boxes = []

    for name, (L, W, H, count) in skus.items():
        for _ in range(count):
            boxes.append((name, L, W, H))
    
    compute_possibility(skus, boxes)
    print("Area won't be a problem, next is arrangement. Optimal layout can be established using DP approach.")
    print("3D Bin Packing Problem")
