from flask import Flask, request, jsonify
import os
import csv

# add trigger test

app = Flask(__name__)
pv_dir = "/tmp/persistent_volume"

@app.route('/sum', methods = ['POST'])
def calculate():
    data  = request.json
    file_name = data.get('file')
    product = data.get('product')

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."})

    file_path = os.path.join(pv_dir, file_name)
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."})
    
    sum = 0
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        # Check that the file contains the expected column names
        if reader.fieldnames is None or 'product' not in reader.fieldnames or 'amount' not in reader.fieldnames:
            return jsonify({"file": file_name, "error": "Input file not in CSV format."})

        for row in reader:
            if row['product'] == product:
                if not row['amount'].isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."})
                sum += int(row['amount'])

    return jsonify({"file": file_name, "sum": sum})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
