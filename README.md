# Image Text Extractor

This project is a **Python-based GUI application** that uses the **Google Generative AI API** to extract text from images, including handwritten text. The application supports multilingual text (e.g., Hindi) and saves the extracted results to a JSON file.

---

## Features

- **Image Upload via GUI**: Select image files directly using a user-friendly Tkinter interface.
- **Text Extraction**: Extracts text from images using the Google Generative AI `gemini-1.5-flash` model.
- **Multilingual Support**: Handles Unicode text, including Hindi.
- **JSON Output**: Saves extracted text to a `JSON` file and appends new results if the file already exists.
- **Real-Time Display**: Shows the extracted text in a dedicated text area in the GUI.(Might not work for languages other than English)

---

## Requirements

- Python 3.8+
- **Python Libraries:**
  - `tkinter`
  - `PIL` (from `Pillow`)
  - `google-generativeai`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/omrsid/Gemini_OCR.git
   cd Gemini_OCR
   ```

2. Install the required dependencies:
   ```bash
   pthon -m venv venv
   <activate the venv accrording to your OS>
   pip install -r requirements.txt
   ```

3. Set up the **Google Generative AI API key**:
   - Obtain an API key from the Google Cloud Console.
   - Add the key to your environment variables:
     ```bash
     export GOOGLE_API_KEY="your-api-key"
     ```

---

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. **Upload an Image**:
   - Click the **"Upload Image"** button in the application.
   - Select an image file (e.g., `.png`, `.jpg`, `.jpeg`).

3. **View Extracted Text**:
   - The extracted text will be displayed in the **"Extracted Text"** area.

4. **JSON Output**:
   - Results are saved in the `output/output_file.json` file.
   - If the file already exists, new entries are appended.

---

## File Structure

```plaintext
.
├── app.py                # Main application script
|—— main.py               # Contains the simple python for better understanding on how Gemini API hows
├── requirements.txt      # Python dependencies
|—— Images/               # Contains some sample images for testing 
├── output/               # Directory for output JSON files
├── README.md             # Project documentation
```

---

## Example JSON Output

After extracting text, the JSON file (`output/output_file.json`) will look like this:

```json
[
    {
        "ID": "Image_ID_sample_image.png",
        "Text": "मेरा नाम अमित है।"
    },
    {
        "ID": "Image_ID_example_image.jpg",
        "Text": "Hello, this is an example text."
    }
]
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

---

## Acknowledgments

- **Google Generative AI**: For powering the text extraction process.
- **Pillow (PIL)**: For image handling.
- **Tkinter**: For creating the GUI.
