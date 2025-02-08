from flask import Flask, request, send_file, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        
        file = request.files["file"]
        
        if file.filename == "":
            return "No selected file"
        
        # ✅ Save File in 'uploads/' Directory
        file_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
        file.save(file_path)

        # ✅ Check if File is Saved Correctly
        if not os.path.exists(file_path):
            return "File upload failed"

        return "File uploaded successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
