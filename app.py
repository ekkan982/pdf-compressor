from flask import Flask, request, send_file, render_template
import os
from pdf2image import convert_from_path
from PIL import Image
import img2pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

TARGET_SIZE = 200 * 1024  # 200KB

def compress_pdf(input_path, output_path):
    images = convert_from_path(input_path, dpi=150)  # Convert PDF pages to images
    temp_images = []

    quality = 85  # Initial quality
    step = 5  # Reduce quality in each loop
    min_quality = 10  # Minimum quality limit

    while quality >= min_quality:
        temp_images.clear()

        for img in images:
            temp_img_path = f"{UPLOAD_FOLDER}/temp_{quality}.jpg"
            img.save(temp_img_path, "JPEG", quality=quality)
            temp_images.append(temp_img_path)

        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(temp_images))

        if os.path.getsize(output_path) <= TARGET_SIZE:
            break

        quality -= step

    for temp_img in temp_images:
        os.remove(temp_img)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file uploaded", 400

        pdf_file = request.files["pdf"]
        if pdf_file.filename == "":
            return "No selected file", 400

        input_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        output_path = os.path.join(COMPRESSED_FOLDER, "compressed_" + pdf_file.filename)
        pdf_file.save(input_path)

        compress_pdf(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
