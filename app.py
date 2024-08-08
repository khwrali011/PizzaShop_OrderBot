from flask import Flask, request, render_template
from ResponseGenerator import ResponseGenerator
import os
import json

app_file_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
RG = ResponseGenerator()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    if request.method == 'POST':
        user_message = request.data.decode('utf-8')
    else:
        return "Invalid Method"
    
    system_message = """You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collect the order, \
and then ask if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally, you collect the payment. \
Make sure to clarify all options, extras, and sizes to uniquely \
identify the item from the menu. \
The menu includes: \
pepperoni pizza 12.95, 10.00, 7.00 \
cheese pizza 10.95, 9.25, 6.50 \
eggplant pizza 11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00"""

    # Define the full path for the records.json file
    record_path = os.path.join(app_file_path, 'records.json')

    messages = [{'role': 'system', 'content': system_message}]
    current_user_message = {'role': 'user', 'content': user_message}

    # Check if the file exists and load existing records
    if os.path.exists(record_path):
        with open(record_path, 'r') as json_file:
            records = json.load(json_file)
        user_responses = records.get('user', [])
        assistant_responses = records.get('assistant', [])
        for i in range(min(len(user_responses), len(assistant_responses))):
            messages.append({'role': 'user', 'content': user_responses[i]})
            messages.append({'role': 'assistant', 'content': assistant_responses[i]})
        messages.append(current_user_message)

    else:
        records = {"user": [], "assistant": []}
        messages.append(current_user_message)
    
    # Append the user message to the records
    records['user'].append(user_message)

    # Generate the response using the ResponseGenerator
    response = RG.generate_response(messages)

    # Append the assistant's response to the records
    records['assistant'].append(response)

    # Write the updated records back to the JSON file
    with open(record_path, 'w') as json_file:
        json.dump(records, json_file, indent=4)

    return response

if __name__ == '__main__':
    app.run(debug=False)
