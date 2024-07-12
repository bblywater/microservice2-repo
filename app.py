from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)
pv_dir = "/tmp/persistent_volume"

@app.route('/sum', methods=['POST'])
def sum_product():
    data = request.json
    file_name = data.get('file')
    product = data.get('product')

    if not file_name or not product:
        return jsonify({"file": None, "error": "Invalid JSON input."})

    file_path = os.path.join(pv_dir, file_name)
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."})

    total_sum = 0
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # Ensure the CSV has the correct headers
            if reader.fieldnames is None or 'product' not in reader.fieldnames or 'amount' not in reader.fieldnames:
                return jsonify({"file": file_name, "error": "Input file not in CSV format."})

            for row in reader:
                # Ensure each row has the correct format
                if 'product' not in row or 'amount' not in row:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."})
                if row['product'] == product:
                    try:
                        amount = int(row['amount'])
                    except ValueError:
                        return jsonify({"file": file_name, "error": "Input file not in CSV format."})
                    total_sum += amount

        return jsonify({"file": file_name, "sum": total_sum})
    except Exception as e:
        return jsonify({"file": file_name, "error": f"Error processing file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
