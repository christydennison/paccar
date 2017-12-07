import numpy as np
import pandas
import glob

s_veh_key = 'Veh Ref ID'
r_veh_key = 'Chassis Reference Number'
s_time_key = 'Event DateTime'
r_time_key = 'Rpr_Dt'

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

        ## Best indicator of repair type is the ATA9 code
        ## Iterate over each repair type and append slices
        for repair_type, repair_group in grouped_repairs:
            start = start_date

            ## null check
            if repair_type not in repair_slices:
                repair_slices[repair_type] = {}
            veh_slices_repair = repair_slices[repair_type]
            
            ## for each repair type, grab slices of snapshots
            for end in repair_group[r_time_key]:
                range_mask = (v_snapshots[s_time_key] >= start) & (v_snapshots[s_time_key] <= end)
                snapshot_range = v_snapshots[range_mask]
                
                for i,slices in get_slices(num_windows, window_size, snapshot_range, ignore_past):
                    if len(slices) > 0:
                        if i not in veh_slices_repair:
                            veh_slices_repair[i] = []
                        veh_slices_repair[i].append(slices)

                ## reset start to end for next iteration
                start = end

    return repair_slices


def save_map(repairs_map, filename):
    for code in repairs_map.keys():
        for window in repairs_map[code].keys():  
            for i in range(len(repairs_map[code][window])):
                n = "{}_{}_{}_{}_.pkl".format(filename, code, window, i)
                repairs_map[code][window][i].to_pickle(n)

def open_map(filename):
    repairs_map = {}
    for file in glob.glob("{}*".format(filename)):
        keys = file.split("_")
        if len(keys) == 5:
            code = int(keys[1])
            window = int(keys[2])
            i = int(keys[3])
            n = "{}_{}_{}_{}_.pkl".format(filename, code, window, i)            
            repairs_map_slice = pandas.read_pickle(n)
            if code not in repairs_map:
                repairs_map[code] = {}
            if window not in repairs_map[code]:
                repairs_map[code][window] = []
            repairs_map[code][window].append(repairs_map_slice)

    return repairs_map