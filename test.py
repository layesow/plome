import requests
import pandas as pd

# Replace 'your_api_key_here' with your actual JotForm API key
api_key = '210c836a9974c7a935312b1ea8943c90'

# Replace 'your_table_id_here' with the actual table ID you want to retrieve
formId = '222203090268952'

# Define the API endpoint URL
url = f'https://reselform.jotform.com/API/form/{formId}/submissions?apiKey={api_key}'

# Make a GET request to the API
response = requests.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    try:
        table_data = response.json()
        # Process the table data here
        df = pd.DataFrame(table_data['content'])  # Create a DataFrame from the content
        # Save the DataFrame to an Excel file
        df.to_excel('jotform_data.xlsx', index=False)
        print("Data imported and saved to jotform_data.xlsx")
    except ValueError as e:
        print("Error decoding JSON response:", e)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Print the response content for debugging
