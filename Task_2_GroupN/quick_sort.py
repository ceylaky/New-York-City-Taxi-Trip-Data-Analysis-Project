import csv
import time
import random
from typing import List, Tuple, Dict

def readfile(file_path: str) -> List[dict]:
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

filepath = "/Users/ceylakaya/Desktop/small/nyc_dataset_small.txt"
data = readfile(filepath)

def aligndata(data: List[dict], aligndata: str) -> List[float]:
    keymappings = {
        "num_passengers": "passenger_count",
        "fare_amounts": "fare_amount",          #these are the keys that we will be assigning with the data
        "total_amounts": "total_amount",
        "tips_amounts": "tip_amount"
    }
    key = keymappings.get(aligndata)
    if key is not None:
        return [float(entry.get(key, 0.0)) for entry in data if entry.get(key)]
    else:              #this part aligns the data corresponding to the keys so that we have everything in place, ready to iterate. 
        return []

def quick_sort(data):
    def partdata(data):
        pivot = data[0]
        left = []
        right = []
        equal = [pivot]
        for num in data[1:]:
            if num < pivot:
                right.append(num) #appending the numbers smaller than the pivot to the right so it becomes a descending list.
            elif num > pivot:
                left.append(num) #appending the numbers greater than the pivot to the left so it becomes a descending list.
            else:
                equal.append(num)
        return left, equal, right #returning in an aligned way with the descending order.

    if len(data) <= 1:
        return data, 0
    left, equal, right = partdata(data)
    left_sorted, left_time = quick_sort(left)     #making recursive calls so it runs through all the data
    right_sorted, right_time = quick_sort(right)
    execution_time = left_time + right_time
    return left_sorted + equal + right_sorted, execution_time

def timed_quick_sort(arr: List[float]) -> Tuple[List[float], float]: #timing the running time of the algorithm
    start_time = time.time()
    sorted_arr, execution_time = quick_sort(arr)
    end_time = time.time()
    total_execution_time = end_time - start_time + execution_time
    return sorted_arr, total_execution_time

num_passengers = aligndata(data, "num_passengers")
fare_amounts = aligndata(data, "fare_amounts")      #defnining the aligned and ordered data  
total_amounts = aligndata(data, "total_amounts")
tips_amounts = aligndata(data, "tips_amounts")

print(timed_quick_sort(num_passengers))
print(timed_quick_sort(fare_amounts))         #calling quicksort on these datasets
print(timed_quick_sort(total_amounts))
print(timed_quick_sort(tips_amounts))
