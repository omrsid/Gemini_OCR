import json
from types import new_class
import requests
from flask import Flask, request, render_template, jsonify
import os
import PIL.Image
import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure the Google Generative AI API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Set the 'GOOGLE_API_KEY' environment variable.")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check if the file is present in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Validate the image
        try:
            image = PIL.Image.open(file_path)
            image.verify()  # Ensure it's a valid image file
        except Exception:
            return jsonify({'error': 'Uploaded file is not a valid image'}), 400

        # Process the image and generate text
        prompt = "Convert the handwriting to text (only give extracted text in respone nothing else"

        # Call the Generative AI model
        try:
            response = model.generate_content([prompt, image])
            text_output = response.text
        except Exception as e:
            return jsonify({'error': f"AI processing failed: {str(e)}"}), 500

        new_entry = {
            "answers":[
                {"ID":"S1_Q1", "Text": text_output}
            ]
        }
        # Send rewuest
        url = 'http://192.168.1.11:9000/evaluate'
        evaluation_response = requests.post(
            url,
            json=new_entry,  # Use 'json' for automatic JSON serialization
            headers={'Content-Type': 'application/json'}  # Correct header format
        )

        # Outpur dir exist
        output_dir = './output'
        os.makedirs(output_dir, exist_ok = True)

        # Save the respone in  JSON format
        output_file_path = os.path.join(output_dir, "output_file.json")

        # Load existing data if the file exists
        if os.path.exists(output_file_path):
            try:
                with open(output_file_path, 'r') as json_file:
                    existing_data = json.load(json_file)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
            except json.JSONDecodeError:
                print("Error reading existing JSON file. Creating a new one")
                existing_data  =[]

        else:
            existing_data = []

        # Append the new entry
        existing_data.append(new_entry)

        # Save and Update the JSON file
        with open(output_file_path, 'w', encoding = 'utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent = 4)

        # Show sucess messagebox
        print("Succes", f"Response saved to {output_file_path}")
        print(new_entry)

        if evaluation_response.status_code != 200:
            return jsonify({'error':'Failed to send request to external API',
                            'details':evaluation_response.text}), 500

        # Include the external API response in the final output
        evaluation_result = evaluation_response.json()
        return jsonify({'text': text_output, 'evaluation_result': evaluation_result})

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 9000, debug=True)
