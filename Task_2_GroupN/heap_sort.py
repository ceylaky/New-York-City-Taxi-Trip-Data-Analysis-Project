import csv
import time
from typing import List, Tuple

def read_file(file_path: str) -> List[dict]:
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def align_data(data: List[dict], aligndata: str) -> List[float]:
    key_mappings = {
        "num_passengers": "passenger_count",
        "fare_amounts": "fare_amount",
        "total_amounts": "total_amount",
        "tips_amounts": "tip_amount"
        #there, we are just intructing the dictionary key_mappings to connect each type of data (aligndata) to the corresponding key in the dataset.
    }
    key = key_mappings.get(aligndata)
    if key is not None:
        return [float(entry.get(key, 0.0)) for entry in data if entry.get(key)]
    #there, it checks if the key exists inside of the dataset. if yes, it should return the list of the data that was extracted, as floats.
    else:
        return []
    #if the key doesn't exist in the dataset, we ask to return an empty list back to us.

def heapsort(arr: List[float]) -> Tuple[List[float], float]:
    def heapify(arr, n, i):
        #we are defining the heapify to maintain the heap property
        largest = i
        #index of the root node in the array
        l = 2 * i + 1
        #left child
        r = 2 * i + 2
        #right child

        if l < n and arr[i] < arr[l]:
            largest = l
            #to find the largest value among this values
        if r < n and arr[largest] < arr[r]:
            largest = r
            #then it check this data for the largest value

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
#if a new largest value was found, we instruct it to swap the values of the arr[i] with arr[largest] to satisfy heap property. 
    def max_heap(arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

    start_time = time.time()
    #to record a time before we start to execute the data
    max_heap(arr)
    for i in range(len(arr) - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    #moving maximum to the end of the array
    end_time = time.time()
    #records the time after execution
    execution_time = end_time - start_time
    #calculates execution time
    return arr, execution_time

def timed_heapsort(arr: List[float]) -> Tuple[List[float], float]:
    start_time = time.time()
    sorted_arr, execution_time = heapsort(arr)
    end_time = time.time()
    total_execution_time = end_time - start_time + execution_time
    return sorted_arr, total_execution_time

file_path = "/Users/sabinanurseitova/Desktop/ALGORITHMS/nyc_dataset_small.txt"
data = read_file(file_path)

num_passengers = align_data(data, "num_passengers")
fare_amounts = align_data(data, "fare_amounts")
total_amounts = align_data(data, "total_amounts")
tips_amounts = align_data(data, "tips_amounts")

print(timed_heapsort(num_passengers))
print(timed_heapsort(fare_amounts))
print(timed_heapsort(total_amounts))
print(timed_heapsort(tips_amounts))
