import requests
import time

# Function to send a GET request to the create_transactions endpoint and measure time
def measure_create_transactions_time():
    start_time = time.time()  # Record the start time

    # Send a GET request to the create_transactions endpoint
    response = requests.get('http://localhost:5000/create_transactions')

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time  # Calculate the total time taken

    return total_time

for x in range(100):

    # Call the function to measure the time
    total_time = measure_create_transactions_time()

    print("Total time taken:", total_time, "seconds")
