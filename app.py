from flask import Flask, request, send_from_directory, render_template
import pandas as pd
import os

# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route('/')
def index():
    # Render the HTML template with the file upload form
    return render_template('index.html')

# Define the upload route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Get the uploaded group CSV file
        group_file = request.files['group_csv']
        # Get the uploaded hostel CSV file
        hostel_file = request.files['hostel_csv']
        
        # Check if both files are provided
        if not group_file or not hostel_file:
            return 'Missing files', 400
        
        # Read the CSV files into pandas DataFrames
        group_df = pd.read_csv(group_file)
        hostel_df = pd.read_csv(hostel_file)
        
        # Allocate rooms based on the uploaded data
        allocation_df = allocate_rooms(group_df, hostel_df)
        
        # Define the path for the output CSV file
        output_path = 'room_allocation.csv'
        # Save the allocation DataFrame to a CSV file
        allocation_df.to_csv(output_path, index=False)
        
        # Send the generated CSV file as a download
        return send_from_directory(directory=os.getcwd(), path=output_path, as_attachment=True)
    except Exception as e:
        # Return any exception as an error message
        return str(e), 500

# Function to allocate rooms based on group and hostel data
def allocate_rooms(group_df, hostel_df):
    allocation = []
    
    # Separate hostel data by gender
    boys_hostels = hostel_df[hostel_df['Gender'] == 'Boys']
    girls_hostels = hostel_df[hostel_df['Gender'] == 'Girls']
    
    # Iterate over each group in the group DataFrame
    for _, group in group_df.iterrows():
        group_id, members, gender = group['Group ID'], group['Members'], group['Gender']
        
        # Select the appropriate hostel based on the group's gender
        if gender == 'Boys':
            hostel = boys_hostels
        else:
            hostel = girls_hostels
        
        allocated = False
        # Iterate over each room in the selected hostel
        for i, room in hostel.iterrows():
            # Check if the room can accommodate the group
            if room['Capacity'] >= members:
                # Allocate the group to the room
                allocation.append({
                    'Group ID': group_id,
                    'Hostel Name': room['Hostel Name'],
                    'Room Number': room['Room Number'],
                    'Members Allocated': members
                })
                # Update the room's remaining capacity
                hostel.at[i, 'Capacity'] -= members
                allocated = True
                break
                
        if not allocated:
            # If no room could accommodate the group, mark them as not allocated
            allocation.append({
                'Group ID': group_id,
                'Hostel Name': 'Not Allocated',
                'Room Number': 'N/A',
                'Members Allocated': members
            })
    
    # Return the allocation as a DataFrame
    return pd.DataFrame(allocation)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
