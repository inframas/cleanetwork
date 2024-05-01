def simple_hash_function(data):
    """
    A simple one-way hash function.
    This function simulates the behavior of cryptographic hash functions.
    """
    # Initialize the hash value to a constant
    hash_value = 0xDEADBEEF
    
    # Process each character of the input data
    for char in data:
        # Convert the character to its ASCII code
        char_code = ord(char)
        # Update the hash value using bitwise operations
        hash_value = ((hash_value << 5) + hash_value) ^ char_code
    
    # Return the final hash value
    return hash_value

# Example usage
input_data = "Hello, World!"
hashed_value = simple_hash_function(input_data)
print("Hashed value of '{}' is: {}".format(input_data, hashed_value))
