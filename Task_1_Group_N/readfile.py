# Luiss - Management and Computer Science - Algorithm 2022/2023
from typing import List, Dict
from datetime import datetime

def read_file(file_path: str) -> List[Dict]:
    datas = []
    with open(file_path, 'r') as f:
        columns = f.readline().strip().split(',')  # Extract column names

        for line in f:
            data = {}
            values = line.strip().split(',')
            for i in range(len(values)):
                value = values[i]
                # Convert appropriate fields to float or datetime
                if i not in [0, 1, 2, 6]:
                    value = float(value) if value else 0
                if i in [1, 2]:
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                
                data[columns[i]] = value  # Map values to columns
            datas.append(data)  # Add the row dictionary to the list

    return datas


