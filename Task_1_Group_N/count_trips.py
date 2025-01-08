

file_path = "/Users/mac/Desktop/ALGORITHMS/algorithm project/nyc_dataset_small.txt" #insert your pathfile in here 
result = read_file(file_path)
#print(result)

#FOURTH TASK
from typing import List, Dict
import csv 
def count_trips(data: List[int], zones: Dict[int, str]) -> Dict[str, int]:
    trips_count={}
    for zone_id in data:
        zone_name=zones.get(zone_id)
        if zone_name not in trips_count:
            trips_count[zone_name]=1
        else:
            trips_count[zone_name]+=1
    return trips_count


def zone_idss(dictn):
    dataa=[]
    for row_dict in dictn:
        id=row_dict.get("RatecodeID", None)
        dataa.append(id)
    return dataa

def zone_names(filepathh):
    zones={}
    with open(filepathh, 'r', newline='') as csvfile:
        header_line = csvfile.readline()
        columns = header_line.strip().split(',')
        for line in csvfile:
            values = line.strip().split(',')
            zone_id=int(values[0])
            zone_name=values[2]
            zones[zone_id] = zone_name
        return zones


zones=zone_names("/Users/mac/Desktop/ALGORITHMS/algorithm project/taxi+_zone_lookup.csv")
datalst=zone_idss(result)

final_result=count_trips(datalst, zones)
print(final_result)

