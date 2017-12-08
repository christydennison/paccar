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
    repairs = repairs.drop(['Unnamed: 0'],1)
    snapshots = snapshots.drop(['Unnamed: 0'],1)
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
                        veh_slices_repair[i].append(slices)

                ## reset start to end for next iteration
                start = end

    return repair_slices


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
            i = int(keys[4])
            n = "{}_{}_{}_{}_{}_.pkl".format(filename, veh_id, code, window, i)            
            repairs_map_slice = pandas.read_pickle(n)
            if veh_id not in repairs_map:
                repairs_map[veh_id] = {}
            if code not in repairs_map[veh_id]:
                repairs_map[veh_id][code] = {}
            if window not in repairs_map[veh_id][code]:
                repairs_map[veh_id][code][window] = []
            repairs_map[veh_id][code][window].append(repairs_map_slice)

    return repairs_map