import pandas as pd
import json

# Read the raw data file line by line
data = []
with open('model_data.jsonl', 'r') as file:
    for line in file:
        # Parse each line as JSON
        json_data = json.loads(line.strip())
        
        # Extract relevant fields
        start = json_data.get('start')
        target = json_data.get('target')[0] if json_data.get('target') else None  # Extract the first value in the 'target' list
        instance = json_data.get('instance')
        
        # Append the extracted data to the list
        data.append({'start': start, 'target': target, 'instance': instance})

# Create a DataFrame from the parsed data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
