import numpy as np
import pandas
import glob

s_veh_key = 'Veh Ref ID'
r_veh_key = 'Chassis Reference Number'
s_time_key = 'Event DateTime'
r_time_key = 'Rpr_Dt'
code = 'ATA6'

def get_slices(num_windows, window_size, snapshots, ignore_past=False):
    slices = []
    num_snapshots = len(snapshots)
    for i in range(num_windows):
        start = num_snapshots - (i+1)*window_size
        end = num_snapshots - i*window_size
        
        if not ignore_past and i == num_windows-1 and num_snapshots - start > 0: # last iter
            start = 0
            
        if start >=0 and end >=0:
            slices.append((i, snapshots[start : end]))
        else:
            break
            
    return slices

def get_repair_slices_map(veh_ids, snapshots, repairs, num_windows=10, window_size=10, code='ATA9', ignore_past=False):
    repairs = repairs
    snapshots = snapshots
    repair_slices = {}
    for veh_id in veh_ids:
        v_snapshots = snapshots[snapshots[s_veh_key] == veh_id].sort_values(by=s_time_key)
        v_repairs = repairs[repairs[r_veh_key] == veh_id].sort_values(by=r_time_key)

        start_date = pandas.to_datetime('1/1/2000') ## in past so first snapshot is captured

        grouped_repairs = v_repairs.groupby([code])
        
        if len(grouped_repairs) == 0:
            continue
            
        repair_slices[veh_id] = {}
        veh_slices = repair_slices[veh_id]

        ## Best indicator of repair type is the ATA9 code
        ## Iterate over each repair type and append slices
        for repair_type, repair_group in grouped_repairs:
            start = start_date

            ## null check
            if repair_type not in veh_slices:
                veh_slices[repair_type] = {}
            veh_slices_repair = veh_slices[repair_type]
            
            ## for each repair type, grab slices of snapshots
            for end in repair_group[r_time_key]:
                range_mask = (v_snapshots[s_time_key] >= start) & (v_snapshots[s_time_key] <= end)
                snapshot_range = v_snapshots[range_mask]

                for i,slices in get_slices(num_windows, window_size, snapshot_range, ignore_past):
                    if len(slices) > 0:
                        if i not in veh_slices_repair:
                            veh_slices_repair[i] = []
                        veh_slices_repair[i].append(slices.drop(['Veh Ref ID','Event DateTime'],1))

                ## reset start to end for next iteration
                start = end

    return repair_slices

def get_ok_slices_map(veh_ids, snapshots, num_windows, window_size):
    ok_map = {}
    for veh_id in veh_ids:
        ok_map[veh_id] = {0:{0:[]}}
        v_snapshots = snapshots[snapshots[s_veh_key] == veh_id].sort_values(by=s_time_key)
        for i,slices in get_slices(num_windows, window_size, v_snapshots, True):
            ok_map[veh_id][0][0].append(slices.drop(['Veh Ref ID','Event DateTime'],1))
    return ok_map

def save_map(repairs_map, filename):
    for veh_id in repairs_map.keys():
        for code in repairs_map[veh_id].keys():
            for window in repairs_map[veh_id][code].keys():  
                for i in range(len(repairs_map[veh_id][code][window])):
                    n = "{}_{}_{}_{}_{}_.pkl".format(filename, veh_id, code, window, i)
                    repairs_map[veh_id][code][window][i].to_pickle(n)

def open_map(filename):
    repairs_map = {}
    for file in glob.glob("{}*".format(filename)):
        keys = file.split("_")
        if len(keys) == 6:
            veh_id = int(keys[1])
            code = int(keys[2])
            window = int(keys[3])
            repairs_map_slice = pandas.read_pickle(file)
            if veh_id not in repairs_map:
                repairs_map[veh_id] = {}
            if code not in repairs_map[veh_id]:
                repairs_map[veh_id][code] = {}
            if window not in repairs_map[veh_id][code]:
                repairs_map[veh_id][code][window] = []
            repairs_map[veh_id][code][window].append(repairs_map_slice)

    return repairs_map

def save_ok_map(ok_map, filename):
    for veh_id in ok_map.keys():
        slices = ok_map[veh_id][0][0]
        for i,s in enumerate(slices):
            n = "{}_OK_{}_{}_.pkl".format(filename, veh_id, i)
            s.to_pickle(n)

def open_ok_map(filename):
    ok_map = {}
    for file in glob.glob("{}*".format(filename)):
        keys = file.split("_")
        if len(keys) == 5 and keys[1] == "OK":
            veh_id = int(keys[2])
            if veh_id not in ok_map:
                ok_map[veh_id] = {0:{0:[]}}
            ok_map_slice = pandas.read_pickle(file)
            ok_map[veh_id][0][0].append(ok_map_slice)

    return ok_map

def create_maps(num_windows, window_size, snapshots, ok_snapshots, ids_tuple, ids_ok_tuple, repairs_tuple):
    train_ids, val_ids, test_ids = ids_tuple
    train_ok_ids, val_ok_ids, test_ok_ids = ids_ok_tuple
    train_repairs, val_repairs, test_repairs = repairs_tuple
    
    train_repairs_map = get_repair_slices_map(train_ids, snapshots, train_repairs, num_windows=num_windows, window_size=window_size, code=code, ignore_past=True)
    val_repairs_map = get_repair_slices_map(val_ids, snapshots, val_repairs, num_windows=num_windows, window_size=window_size, code=code, ignore_past=True)
    test_repairs_map = get_repair_slices_map(test_ids, snapshots, test_repairs, num_windows=num_windows, window_size=window_size, code=code, ignore_past=True)
    
    train_ok_map = get_ok_slices_map(train_ok_ids, ok_snapshots, num_windows, window_size)
    val_ok_map = get_ok_slices_map(val_ok_ids, ok_snapshots, num_windows, window_size)
    test_ok_map = get_ok_slices_map(test_ok_ids, ok_snapshots, num_windows, window_size)

    name = "{}-{}".format(num_windows, window_size)
    
    save_map(train_repairs_map, '/home/cs231n/data/train-'+name)
    save_map(val_repairs_map, '/home/cs231n/data/val-'+name)
    save_map(test_repairs_map, '/home/cs231n/data/test-'+name)
    
    save_ok_map(train_ok_map, '/home/cs231n/data/trainOK-'+name)
    save_ok_map(val_ok_map, '/home/cs231n/data/valOK-'+name)
    save_ok_map(test_ok_map, '/home/cs231n/data/testOK-'+name)

def load_maps(num_windows, window_size):
    name = "{}-{}".format(num_windows, window_size)
    
    train_map_deser = open_map('/home/cs231n/data/train-'+name)
    val_map_deser = open_map('/home/cs231n/data/val-'+name)
    test_map_deser = open_map('/home/cs231n/data/test-'+name)

    train_map_deser_ok = open_ok_map('/home/cs231n/data/trainOK-'+name)
    val_map_deser_ok = open_ok_map('/home/cs231n/data/valOK-'+name)
    test_map_deser_ok = open_ok_map('/home/cs231n/data/testOK-'+name)
    
    train_combined = {**train_map_deser, **train_map_deser_ok}
    val_combined = {**val_map_deser, **val_map_deser_ok}
    test_combined = {**test_map_deser, **test_map_deser_ok}
    
    return (train_combined, val_combined, test_combined)