#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict

def calculate_stats_from_txt_file(file_path: str) -> Dict[str, Dict[str, float]]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
#creating a file path and assigning the code to read all data into a list called lines
    if not lines:
        raise ValueError("No data found in the text file")

    header_line = lines[0]
    #i added this, so the code will extract the header from the results
    columns = header_line.strip().split(',')
    #to split column names and keep them in the "column" list
    target_columns = ['passenger_count', 'fare_amount', 'total_amount', 'tip_amount']
    #to assign at which columns we are interested in and going to analyze further
    stats_dict = {column: {'min': float('inf'), 'max': float('-inf'), 'avg': 0.0} for column in target_columns}
    #assigning the format, according to which our data should appear
    lines = lines[1:]
    #to skip a header 
    total_values = {column: 0.0 for column in target_columns}

    for line in lines:
        values = line.strip().split(',')

        for i, value in enumerate(values):
            try:
                value = float(value)
                #converts each value into the float number
            except ValueError:
                
                continue

            column = columns[i]

            if column in target_columns:
                stats_dict[column]['min'] = min(stats_dict[column]['min'], value)
                stats_dict[column]['max'] = max(stats_dict[column]['max'], value)
                total_values[column] += value

    for column in target_columns:
        stats_dict[column]['avg'] = total_values[column] / len(lines)
        #formula for calculating average

    return stats_dict

txt_file_path = "/Users/sabinanurseitova/Desktop/ALGORITHMS/nyc_dataset_small.txt"
results = calculate_stats_from_txt_file(txt_file_path)

for column, values in results.items():
    print(f"{column}: {{'min': {values['min']}, 'max': {values['max']}, 'avg': {values['avg']}}}")