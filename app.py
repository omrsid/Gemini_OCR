import PIL.Image
import os
import google.generativeai as genai
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv


# Config the Google AI API
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not add to env variable")
genai.configure(api_key = API_KEY)


def upload(extracted_text_area):
    # Open file dialog to select an image
    image_path = filedialog.askopenfilename(
        title = "Select an Image file",
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.WEBP *.HEIC *.HEIF")]
    )

    if not image_path:
        messagebox.showwarning("No File Selected", "Please select an image file.")
        return

    try:
        # Load the selected image
        sample_file = PIL.Image.open(image_path)
    except Exception as e:
        print(f"Error opening image file: {e}")
        return

    # Choose a Gemini Model
    model = genai.GenerativeModel(model_name = 'gemini-1.5-flash')

    # Prompt
    prompt = "Extract text for the handwriting (only provide text of the image in the response nothing else"

    # Get the Text
    try:
        response = model.generate_content([prompt, sample_file])

        # Prepare the output data
        new_entry = {
            "ID": f"Image_ID_{image_path}",
            "Text": response.text
        }

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
        messagebox.showinfo("Succes", f"Response saved to {output_file_path}")

        # Display the extracted text in the text area
        extracted_text_area.config(state=tk.NORMAL)  # Enable editing temporarily
        extracted_text_area.delete(1.0, tk.END)  # Clear existing text
        extracted_text_area.insert(tk.END, response.text.strip())  # Insert new text
        extracted_text_area.config(state=tk.DISABLED)  # Disable editing

    except Exception as e:
        print(f"Error is extracting text: {e}")


# Create the main Tkinter window
def main():
    root = tk.Tk()
    root.title("Image Text Extractor")
    root.geometry("600x400")

    # Create a label and a button
    tk.Label(root, text="Upload an Image to Extract Text", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Upload Image", command=lambda: upload(extracted_text_area), font=("Arial", 12)).pack(pady=10)

    # Create a label for the extracted text area
    tk.Label(root, text="Extracted Text", font=("Arial", 12)).pack(pady=5)

    # Create a text widget to display the extracted text
    extracted_text_area = tk.Text(root, wrap=tk.WORD, height=10, width=70, font=("Arial", 12))
    extracted_text_area.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
