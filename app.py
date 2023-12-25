from flask import Flask, render_template, request, url_for, send_from_directory
from PIL import Image
import pytesseract as tess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define the upload folder for images

# Setting Tesseract path
tess.pytesseract.tesseract_cmd = r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Function to process image and extract text
def predict_text_from_image(image):
    text = tess.image_to_string(image)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        # Save the uploaded file temporarily
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        img = Image.open(file_path)
        predicted_text = predict_text_from_image(img)
        image_url = url_for('uploaded_file', filename=file.filename)  # Get the URL for the uploaded image

        # Pass both predicted text and image URL to the template
        return render_template('index.html', prediction=predicted_text, prediction_image=image_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
