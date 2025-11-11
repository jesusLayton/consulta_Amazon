def read_excel(file_path):
    # Function to read data from an Excel file
    import pandas as pd
    return pd.read_excel(file_path)

def write_to_excel(file_path, data):
    # Function to write data to an Excel file
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

def log_message(message):
    # Function to log messages to a file
    with open('log.txt', 'a') as log_file:
        log_file.write(message + '\n')

def validate_product_data(product_data):
    # Function to validate product data
    required_keys = ['name', 'price', 'url']
    return all(key in product_data for key in required_keys)