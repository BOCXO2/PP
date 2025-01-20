from flask import Flask, render_template, request, jsonify
import os
import json
import yaml
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def process_text(content):
    lines = content.splitlines() 
    processed_lines = []
    for line in lines:
        try:
            processed_line = str(eval(line.strip()))
        except Exception as e:
            processed_line = f"Error: {str(e)}"
        processed_lines.append(processed_line)
    return '\n'.join(processed_lines) 


def process_json(content):
    data = json.loads(content)
    return json.dumps(process_nested_data(data), indent=4)

def process_yaml(content):
    data = yaml.safe_load(content)
    return yaml.dump(process_nested_data(data), sort_keys=False)

def process_xml(content):
    root = ET.fromstring(content)
    process_xml_recursive(root)
    return ET.tostring(root, encoding='unicode')

def process_nested_data(data):
    if isinstance(data, dict):
        return {key: process_nested_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [process_nested_data(item) for item in data]
    elif isinstance(data, str):
        return process_text(data)
    return data

def process_xml_recursive(element):
    if element.text and element.text.strip():
        element.text = process_text(element.text)
    for child in element:
        process_xml_recursive(child)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        if file.filename.endswith('.json'):
            processed_content = process_json(content)
        elif file.filename.endswith('.yaml') or file.filename.endswith('.yml'):
            processed_content = process_yaml(content)
        elif file.filename.endswith('.xml'):
            processed_content = process_xml(content)
        elif file.filename.endswith('.txt'):
            processed_content = process_text(content)
        else:
            return jsonify({"error": "Unsupported file format"})
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"})

    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file.filename)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)

    return jsonify({"message": "File processed", "output_file": output_file_path})

if __name__ == '__main__':
    app.run(debug=True)
