from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Tuple

filepath = "/Users/ceylakaya/Desktop/Small dataset/nyc_dataset_small.txt"

zonetimedistance = defaultdict(list)   #we will store zone data here

#We read the file and populate zone data
with open(filepath, "r") as f:
    for line in f:
        columns = line.strip().split(',')
        zoneid = columns[7]  
        pickuptime = columns[1][11:].rstrip('.0')
        dropofftime = columns[2][11:].rstrip('.0')
        distance_str = columns[4]
        zonetext = {'1': 'Newark', '132': 'JFK Airport', '74': 'East Harlem Manhattan', '43': 'Central Park'}        
        zonename = zonetext.get(zoneid, "none") 
        
        try:
            distancekm = float(distance_str)
        except ValueError:
            continue  
        
        if zonename != "none":
            zonetimedistance[zonename].append((pickuptime, dropofftime, distancekm))

def calculate_duration(pickup_time, dropoff_time):
    if len(pickup_time) == 6:   #for values without seconds we add 00's at the end for simplicity in calculation
        pickup_time += "00"
    if len(dropoff_time) == 6:
        dropoff_time += "00"
    
    #we handle different cases individually so we don't encounter an error
    try:
        pickup_datetime = datetime.strptime(pickup_time, '%H:%M:%S')
        dropoff_datetime = datetime.strptime(dropoff_time, '%H:%M:%S') #if both times have seconds
    except ValueError:
        try:
            pickup_datetime = datetime.strptime(pickup_time, '%H:%M:%S') #if dropoff doesn't have seconds
            dropoff_datetime = datetime.strptime(dropoff_time, '%H:%M')
        except ValueError:
            try:
                pickup_datetime = datetime.strptime(pickup_time, '%H:%M')
                dropoff_datetime = datetime.strptime(dropoff_time, '%H:%M:%S') #if pickup doesn't have seconds
            except ValueError:
                return None
#if both don't have seconds it will simply return hh:mm values.
    if dropoff_datetime < pickup_datetime:
        dropoff_datetime += timedelta(days=1)  #for values like 00:08:25, on the next day. Because the calculation would be negative and throw an error otherwise. 
        
    return (dropoff_datetime - pickup_datetime).total_seconds()

def calculate_speed(data: List[Tuple[str, str, float]]) -> Tuple[float, float, float]:
    min_speed = float('inf')
    max_speed = float('-inf')
    total_speed = 0
    count = 0
    
    for pickup_time, dropoff_time, distancekm in data:
        duration_seconds = calculate_duration(pickup_time, dropoff_time)
        if duration_seconds is not None and duration_seconds > 0: #checking if duration is not negative 
            speedkmh = distancekm / (duration_seconds / 3600)
            min_speed = min(min_speed, speedkmh)
            max_speed = max(max_speed, speedkmh)
            total_speed += speedkmh
            count += 1
    
    if count == 0:
        return 0, 0, 0
    
    avg_speed = total_speed / count   #We calculate average speed for each zone
    return min_speed, avg_speed, max_speed

zone_speed_stats = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'total': 0, 'count': 0})

for zonename, datalist in zonetimedistance.items():
    min_speed, avg_speed, max_speed = calculate_speed(datalist)
    zone_speed_stats[zonename]['min'] = min_speed
    zone_speed_stats[zonename]['avg'] = avg_speed
    zone_speed_stats[zonename]['max'] = max_speed
    
#Finally we are printing the min avg and max speeds in kmh for each zone.
for zonename, stats in zone_speed_stats.items():
    print(f"Zone: {zonename}")
    print(f"Minimum Speed: {stats['min']} km/h")
    print(f"Average Speed: {stats['avg']} km/h")
    print(f"Maximum Speed: {stats['max']} km/h")
    print()
