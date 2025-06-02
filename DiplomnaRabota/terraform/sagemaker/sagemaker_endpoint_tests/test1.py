import boto3
import json
import matplotlib.pyplot as plt
import pandas as pd

region = "eu-central-1"
endpoint_name = "ppetrov-endpoint"
runtime_client = boto3.client("sagemaker-runtime", region_name=region)


input_data = {"placeholder": True} 

# call the endpoint
response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=json.dumps(input_data),
    ContentType="application/json"
)

# Decode response
result = json.loads(response["Body"].read().decode())

# Extract predictions
future_predictions = result.get("future_predictions", [])
node_predictions = result.get("node_predictions", {})
predictions = result.get("predictions", [])

# Print structured output
print("Future Predictions:", future_predictions)
print("Node Predictions:", node_predictions)
print("Predictions for the next 2 hours and 30 minutes:", predictions)

# Split predictions for each node
node_1 = predictions[0::3]  
node_2 = predictions[1::3]  
node_3 = predictions[2::3]  


min_length = min(len(node_1), len(node_2), len(node_3))
node_1 = node_1[:min_length]
node_2 = node_2[:min_length]
node_3 = node_3[:min_length]

# Create DataFrames for each node
df_all = pd.DataFrame({"Time Step": list(range(min_length)), "Node 1": node_1, "Node 2": node_2, "Node 3": node_3})
df_node_1 = pd.DataFrame({"Time Step": list(range(min_length)), "Node 1": node_1})
df_node_2 = pd.DataFrame({"Time Step": list(range(min_length)), "Node 2": node_2})
df_node_3 = pd.DataFrame({"Time Step": list(range(min_length)), "Node 3": node_3})

print("\nFull Prediction Table:")
print(df_all.to_string(index=False))
print("\nNode 1 Predictions:")
print(df_node_1.to_string(index=False))
print("\nNode 2 Predictions:")
print(df_node_2.to_string(index=False))
print("\nNode 3 Predictions:")
print(df_node_3.to_string(index=False))

# plot combined predictions
plt.figure(figsize=(10, 6))
plt.plot(node_1, marker='o', linestyle='-', label='Node 1')
plt.plot(node_2, marker='s', linestyle='-', label='Node 2')
plt.plot(node_3, marker='^', linestyle='-', label='Node 3')
plt.xlabel("Time Steps")
plt.ylabel("Memory Usage Prediction")
plt.title("Memory Usage Predictions for All Nodes")
plt.legend()
plt.grid(True)
plt.show(block=False)

plt.figure()
plt.plot(node_1, marker='o', linestyle='-', color='b', label='Node 1')
plt.title("Node 1 Predictions")
plt.xlabel("Time Steps")
plt.ylabel("Memory Usage")
plt.grid(True)
plt.legend()
plt.show(block=False) 

plt.figure()
plt.plot(node_2, marker='s', linestyle='-', color='g', label='Node 2')
plt.title("Node 2 Predictions")
plt.xlabel("Time Steps")
plt.ylabel("Memory Usage")
plt.grid(True)
plt.legend()
plt.show(block=False)

plt.figure()
plt.plot(node_3, marker='^', linestyle='-', color='r', label='Node 3')
plt.title("Node 3 Predictions")
plt.xlabel("Time Steps")
plt.ylabel("Memory Usage")
plt.grid(True)
plt.legend()
plt.show() 
