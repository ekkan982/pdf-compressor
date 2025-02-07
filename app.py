import os
import multiprocessing
from pdf2image import convert_from_path
from PIL import Image
import img2pdf

# Function to compress image
def compress_image(args):
    img, quality, temp_path = args
    img = img.convert("RGB")
    img.save(temp_path, "JPEG", quality=quality)

# Function to compress PDF
def compress_pdf(input_pdf, output_pdf, target_size=200 * 1024, dpi=100):
    # Convert PDF pages to images (Lower DPI for faster processing)
    images = convert_from_path(input_pdf, dpi=dpi)

    # Initial compression quality
    min_quality, max_quality = 5, 95
    best_quality = min_quality
    best_pdf_path = None

    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        temp_images = []
        temp_paths = [f"temp_{i}.jpg" for i in range(len(images))]

        # Parallel Processing for Faster Image Compression
        with multiprocessing.Pool() as pool:
            pool.map(compress_image, [(img, mid_quality, temp_paths[i]) for i, img in enumerate(images)])

        # Convert images back to PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(temp_paths))

        # Check file size
        compressed_size = os.path.getsize(output_pdf)

        # If size is within 195KB-205KB, accept it
        if 195 * 1024 <= compressed_size <= 205 * 1024:
            best_quality = mid_quality
            best_pdf_path = output_pdf
            break

        # Adjust compression quality
        if compressed_size > target_size:
            max_quality = mid_quality - 1  # Reduce quality for more compression
        else:
            min_quality = mid_quality + 1  # Increase quality for less compression

        # Cleanup temp images
        for temp_file in temp_paths:
            os.remove(temp_file)

    return best_pdf_path if best_pdf_path else output_pdf

# Example Usage
input_pdf = "input.pdf"
output_pdf = "compressed.pdf"
compress_pdf(input_pdf, output_pdf)
