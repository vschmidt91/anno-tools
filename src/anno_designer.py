from itertools import product
import numpy as np
from skimage.segmentation import flood_fill

BLOCKING = {
    # 'A7_residence_SkyScraper_4lvl3',
    # 'A7_residence_SkyScraper_5lvl3',
    # 'A7_residence_SkyScraper_5lvl5',
    # 'Airship landing platform',
    'BlockTile_1x1',
    # 'Culture_1x1_plaza',
    # 'DepartmentStore_Toaster',
    # 'Dockland - Main',
    # 'Dockland_Module_Export',
    # 'Dockland_Module_SpeedUp',
    # 'Dockland_Module_Storage',
    # 'Electricity_03 (Gas Power Plant)',
    # 'Factory_11 (Clay Pit)',
    # 'FurnitureStore_BankersLamp',
    # 'Guild_house',
    # 'Harbor_01 (Depot)',
    # 'Harbor_08 (Pier)',
    # 'HarbourSystem',
    # 'Kontor_imperial_01',
    # 'Logistic_02 (Warehouse I)',
    # 'Mining_03_slot (Clay Pit Slot)',
    # 'Palace Ministry',
    # 'Pharmacy_ToothPaste',
    # 'Platform module post',
    # 'Post box',
    'Random slot mining',
    # 'Random slot oil pump',
    # 'Road',
    # 'Service_07 (University)',
    # 'Town hall',
 }

EXCLUDE_COLORS = [
    {"A": 255, "R": 192, "G": 192, "B": 192},
]
EXCLUDE_COLORS_STR = {str(c) for c in EXCLUDE_COLORS}

ID_TOWNHALL = "Town hall"
ID_GUILDHOUSE = "Guild_house"

def string_to_tuple(s):
    return tuple(map(int, s.split(",")))

def object_positions(data, obj_id=ID_TOWNHALL):
    sources = []
    for obj in data["Objects"]:
        if obj["Identifier"] != obj_id:
            continue
        i, j = string_to_tuple(obj["Position"])
        w, h = string_to_tuple(obj["Size"])
        sources.append((i + w//2, j + h//2))
    return sources

def ad_to_grid(data) -> np.ndarray:

    assert data["FileVersion"] == 4
    assert data["LayoutVersion"] == "1.0.0.0"

    # colors = {obj["Color"] for obj in data["Objects"]}
    
    ii = []
    jj = []
    for obj in data["Objects"]:
        if obj["Identifier"] not in BLOCKING:
            continue
        if str(obj["Color"]) in EXCLUDE_COLORS_STR:
            continue
        i, j = string_to_tuple(obj["Position"])
        w, h = string_to_tuple(obj["Size"])
        for di, dj in product(range(w), range(h)):
            ii.append(i + di)
            jj.append(j + dj)

    i1 = max(ii)
    j1 = max(jj)

    grid = np.full((i1 + 1, j1 + 1), True)
    grid[ii, jj] = False
    # return grid.T

    grid = np.pad(grid, 1, constant_values=True)
    grid_filled = flood_fill(grid, (0, 0), False, connectivity=1)
    grid_filled = grid_filled[1:-1,1:-1]

    return grid_filled.T