from django.shortcuts import render ,HttpResponse ,redirect
from PyPDF2 import PdfMerger
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image, UnidentifiedImageError
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from django.utils.text import slugify
from PIL import Image, UnidentifiedImageError
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError
import os
import uuid
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import os
from django.conf import settings
from io import BytesIO
from pdf2docx import Converter


def base(request):
    return render(request , 'base.html')

def home(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Get the uploaded image and compression quality
        uploaded_image = request.FILES['image']
        quality = int(request.POST.get('quantity', 50))  # Default compression quality is 50
        
        # Read the image into memory
        image_array = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        
        # Compress the image
        _, compressed_image = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        
        # Create an HTTP response with the compressed image
        response = HttpResponse(compressed_image.tobytes(), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="compressed_image.jpg"'
        
        return response

    return render(request, 'home.html')

def about(request):
    return HttpResponse("saurav")


def mergepdf(request):
    if request.method == "POST":
        try:
            input_files = request.FILES.getlist('pdf_files')
            
            if not input_files:
                return HttpResponse("No files selected for upload.", status=400)
            
            merger = PdfMerger()

            for pdf in input_files:
                merger.append(pdf)  
            output_file_path = "merged_output.pdf"

            with open(output_file_path, 'wb') as output_file:
                merger.write(output_file)
            
            with open(output_file_path, 'rb') as merged_file:
                response = HttpResponse(
                    merged_file.read(),
                    content_type="application/pdf"
                )
                response['Content-Disposition'] = 'attachment; filename="merged_output.pdf"'
                return response

        except Exception as e:
            return HttpResponse(f"Error while merging PDFs: {e}")

    return render(request, 'Mergepdf.html')


def png(request):
    converted_image = None
    error_message = None

    if request.method == "POST" and request.FILES.get("uploadFile"):
        uploaded_file = request.FILES["uploadFile"]

        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1].lower()}"

        # Save the uploaded file in the media/uploads folder
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        fs = FileSystemStorage(location=upload_path)
        saved_file_path = fs.save(unique_filename, uploaded_file)

        try:
            # Open the uploaded file as an image
            img = Image.open(fs.path(saved_file_path))

            # Generate a new file name for the PNG version
            output_file_name = f"{uuid.uuid4()}.png"
            output_file_path = os.path.join(upload_path, output_file_name)

            # Save the image as PNG
            img.save(output_file_path, "PNG")

            # Provide the converted image path to the template
            converted_image = f"{settings.MEDIA_URL}uploads/{output_file_name}"

            # Optionally, delete the original uploaded file
            os.remove(fs.path(saved_file_path))
        except UnidentifiedImageError:
            error_message = "The uploaded file is not a valid image."
            os.remove(fs.path(saved_file_path))  # Clean up invalid file
        except Exception as e:
            error_message = f"An error occurred during conversion: {e}"

    return render(request, "png.html", {"converted_image": converted_image, "error_message": error_message})


def jpgs(request):
    converted_image = None
    error_message = None

    if request.method == "POST" and request.FILES.get("uploadFile"):
        uploaded_file = request.FILES["uploadFile"]

        # Generate a unique filename for the uploaded file
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1].lower()}"

        # Define the upload path
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        fs = FileSystemStorage(location=upload_path)
        saved_file_path = fs.save(unique_filename, uploaded_file)

        try:
            # Open the uploaded file as an image
            img = Image.open(fs.path(saved_file_path))

            # Convert the image to RGB if it has an alpha channel
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Generate a new file name for the JPG version
            output_file_name = f"{uuid.uuid4()}.jpg"
            output_file_path = os.path.join(upload_path, output_file_name)

            # Save the image as JPG
            img.save(output_file_path, "JPEG")

            # Provide the converted image path to the template
            converted_image = f"{settings.MEDIA_URL}uploads/{output_file_name}"

            # Optionally, delete the original uploaded file
            os.remove(fs.path(saved_file_path))
        except UnidentifiedImageError:
            error_message = "The uploaded file is not a valid image."
            os.remove(fs.path(saved_file_path))  # Clean up invalid file
        except Exception as e:
            error_message = f"An error occurred during conversion: {e}"

    return render(request, "jpg.html", {"converted_image": converted_image, "error_message": error_message})


import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError

def jpeg(request):
    converted_image_url = None
    error_message = None

    if request.method == "POST" and request.FILES.get("uploadFile"):
        uploaded_file = request.FILES["uploadFile"]

        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1].lower()}"
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        fs = FileSystemStorage(location=upload_path)
        saved_file_path = fs.save(unique_filename, uploaded_file)

        try:
            img = Image.open(fs.path(saved_file_path))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_file_name = f"{uuid.uuid4()}.jpeg"
            output_file_path = os.path.join(upload_path, output_file_name)
            img.save(output_file_path, "JPEG")

            converted_image_url = f"{settings.MEDIA_URL}uploads/{output_file_name}"
            os.remove(fs.path(saved_file_path))
        except UnidentifiedImageError:
            error_message = "The uploaded file is not a valid image."
            os.remove(fs.path(saved_file_path))
        except Exception as e:
            error_message = f"An error occurred during the conversion: {e}"

    return render(request, "jpeg.html", {
        "converted_image_url": converted_image_url,
        "error_message": error_message
    })


import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError

def webp(request):
    converted_image_url = None
    error_message = None

    if request.method == "POST" and request.FILES.get("uploadFile"):
        uploaded_file = request.FILES["uploadFile"]

        # Generate a unique filename for the uploaded file
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1].lower()}"

        # Define the upload path
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        fs = FileSystemStorage(location=upload_path)
        saved_file_path = fs.save(unique_filename, uploaded_file)

        try:
            # Open the uploaded file as an image
            img = Image.open(fs.path(saved_file_path))

            # Convert the image to RGB if it has an alpha channel (WebP does not support all alpha modes)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Generate a unique name for the WebP output
            output_file_name = f"{uuid.uuid4()}.webp"
            output_file_path = os.path.join(upload_path, output_file_name)

            # Save the image in WebP format
            img.save(output_file_path, "WEBP")

            # Provide the converted image's URL
            converted_image_url = f"{settings.MEDIA_URL}uploads/{output_file_name}"

            # Optionally, delete the original uploaded file
            os.remove(fs.path(saved_file_path))
        except UnidentifiedImageError:
            error_message = "The uploaded file is not a valid image."
            os.remove(fs.path(saved_file_path))  # Clean up invalid file
        except Exception as e:
            error_message = f"An error occurred during the conversion: {e}"

    return render(request, "webp.html", {
        "converted_image_url": converted_image_url,
        "error_message": error_message
    })




def image_to_pdf(request):
    converted_pdf_url = None
    error_message = None

    if request.method == "POST" and request.FILES.get("uploadFile"):
        uploaded_file = request.FILES["uploadFile"]

        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1].lower()}"

        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        fs = FileSystemStorage(location=upload_path)
        saved_file_path = fs.save(unique_filename, uploaded_file)

        try:
            img = Image.open(fs.path(saved_file_path))

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_file_name = f"{uuid.uuid4()}.pdf"
            output_file_path = os.path.join(upload_path, output_file_name)

            img.save(output_file_path, "PDF", resolution=100.0)

            converted_pdf_url = f"{settings.MEDIA_URL}uploads/{output_file_name}"

            os.remove(fs.path(saved_file_path))
        except UnidentifiedImageError:
            error_message = "The uploaded file is not a valid image."
            os.remove(fs.path(saved_file_path))  
        except Exception as e:
            error_message = f"An error occurred during the conversion: {e}"

    return render(request, "imagetopdf.html", {
        "converted_pdf_url": converted_pdf_url,
        "error_message": error_message
    })

def uploadimg(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        
        # Save the image
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_image_url = fs.url(filename)

        # Redirect to resize page with the image URL
        return redirect(f'/resize/?image_url={uploaded_image_url}')

    # Render the upload page for GET requests
    return render(request, 'resizeimage.html')


def resize(request):
    if request.method == "POST":
        width = request.POST.get("width")
        height = request.POST.get("height")

        # Check if width and height are valid positive integers
        if not width or not height or not width.isdigit() or not height.isdigit():
            return render(request, 'resize.html', {"error": "Width and Height must be positive integers."})

        width = int(width)
        height = int(height)

        # Handle file upload
        uploaded_file = request.FILES.get("image")
        if not uploaded_file:
            return render(request, 'resize.html', {"error": "Please upload an image file."})

        try:
            # Open the uploaded image using Pillow
            image = Image.open(uploaded_file)

            # Resize the image
            resized_image = image.resize((width, height))

            # Save the resized image in memory
            buffer = BytesIO()
            resized_image.save(buffer, format="PNG")
            buffer.seek(0)

            # Prepare the resized image for download
            response = HttpResponse(buffer, content_type="image/png")
            response["Content-Disposition"] = "attachment; filename=resized_image.png"

            return response

        except Exception as e:
            return render(request, 'resize.html', {"error": "Invalid image file."})

    return render(request, 'resize.html')

import cv2
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os

def crop(request):
    if request.method == "POST":
        try:
            # Check if the file is in the request
            if 'image' not in request.FILES:
                return JsonResponse({"error": "No image file provided."})
            
            # Save the uploaded image temporarily
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            file_path = fs.save(image_file.name, image_file)
            full_path = fs.path(file_path)
            
            # Load the image with OpenCV
            image = cv2.imread(full_path)
            if image is None:
                return JsonResponse({"error": "Failed to load image. Ensure the file is valid."})

            # Get crop coordinates from the request
            crop_coords = request.POST.get('crop_coords', '')
            if not crop_coords:
                return JsonResponse({"error": "Crop coordinates not provided."})
            
            try:
                x1, y1, x2, y2 = map(int, crop_coords.split(','))
            except ValueError:
                return JsonResponse({"error": "Invalid crop coordinates format. Use x1,y1,x2,y2."})

            # Validate coordinates
            h, w, _ = image.shape
            if x1 < 0 or y1 < 0 or x2 > w or y2 > h or x1 >= x2 or y1 >= y2:
                return JsonResponse({"error": "Crop coordinates are out of bounds."})

            # Perform the crop
            cropped_image = image[y1:y2, x1:x2]

            # Save the cropped image
            cropped_file_name = f"cropped_{os.path.basename(full_path)}"
            cropped_file_path = os.path.join(fs.location, cropped_file_name)
            cv2.imwrite(cropped_file_path, cropped_image)

            # Return the path to the cropped image
            cropped_image_url = fs.url(cropped_file_name)
            return JsonResponse({"saved_path": cropped_image_url})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return render(request, 'crop.html')

import cv2
import numpy as np
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO

def grascale(request):
    if request.method == "POST" and 'image' in request.FILES:
        image_file = request.FILES['image']
        action = request.POST.get('action')

        # Read the uploaded image using OpenCV
        image_array = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if action == "grayscale":
            # Convert the image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Save the grayscale image
            _, buffer = cv2.imencode('.png', grayscale_image)
            grayscale_io = BytesIO(buffer)
            processed_image_path = default_storage.save('processed_images/grayscale_image.png', ContentFile(grayscale_io.getvalue()))
            processed_image_url = default_storage.url(processed_image_path)

            # Render the page with the processed image and download link
            return render(request, "grascale.html", {
                "processed_image_url": processed_image_url,
                "download_link": processed_image_url,
            })

    return render(request, "grascale.html")


import cv2
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render

import cv2
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render

import cv2
import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse

def Remove(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Get the uploaded image
        uploaded_image = request.FILES['image']

        # Save the image temporarily to process
        temp_image_path = default_storage.save(uploaded_image.name, ContentFile(uploaded_image.read()))
        temp_image_full_path = default_storage.path(temp_image_path)

        # Read the image using OpenCV
        image = cv2.imread(temp_image_full_path)

        # Check if image loaded successfully
        if image is None:
            default_storage.delete(temp_image_path)
            return HttpResponse("Error: Could not process the image. Please upload a valid image.", status=400)

        # Define a rectangle for grabCut
        height, width = image.shape[:2]
        rect = (10, 10, width - 20, height - 20)

        # Initialize mask, background model, and foreground model
        mask = np.zeros(image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        # Apply grabCut to remove the background
        try:
            cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        except Exception as e:
            default_storage.delete(temp_image_path)
            return HttpResponse(f"Error: Could not remove background. Details: {str(e)}", status=500)

        # Create mask to extract foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        result = image * mask2[:, :, np.newaxis]

        # Save the processed image
        output_path = default_storage.save("processed_image.png", ContentFile(b""))
        cv2.imwrite(default_storage.path(output_path), result)

        # Serve the processed image back to the user
        with open(default_storage.path(output_path), 'rb') as processed_file:
            response = HttpResponse(processed_file.read(), content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="processed_image.png"'

        # Clean up temporary files
        default_storage.delete(temp_image_path)

        return response

    return render(request, 'RemoveBackground.html')





def mergepdf(request):
    if request.method == "POST":
        try:
            input_files = request.FILES.getlist('pdf_files')
            
            if not input_files:
                return HttpResponse("No files selected for upload.", status=400)
            
            merger = PdfMerger()

            for pdf in input_files:
                merger.append(pdf)  
            output_file_path = "merged_output.pdf"

            with open(output_file_path, 'wb') as output_file:
                merger.write(output_file)
            
            with open(output_file_path, 'rb') as merged_file:
                response = HttpResponse(
                    merged_file.read(),
                    content_type="application/pdf"
                )
                response['Content-Disposition'] = 'attachment; filename="merged_output.pdf"'
                return response

        except Exception as e:
            return HttpResponse(f"Error while merging PDFs: {e}")

    return render(request, 'Mergepdf.html')

from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO


def pdf_compressor(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES.get('pdf_file')
            if not uploaded_file:
                return render(request, 'pdf_compressor.html', {
                    'error_message': "No file selected for upload."
                })

            original_size = uploaded_file.size  # Original file size in bytes

            # Read and compress the PDF
            reader = PdfReader(uploaded_file)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            if reader.metadata:
                writer.add_metadata(reader.metadata)

            # Save the compressed PDF to a BytesIO buffer
            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)

            compressed_size = buffer.getbuffer().nbytes
            compression_percentage = ((original_size - compressed_size) / original_size) * 100

            # Return the compressed PDF as a downloadable file
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="compressed_output.pdf"'

            return response

        except Exception as e:
            return render(request, 'pdf_compressor.html', {
                'error_message': f"Error compressing PDF: {e}"
            })

    return render(request, 'pdf_compressor.html')


def pdf_to_word(request):

    if request.method == 'POST' and request.FILES.get('pdf_file'):

        pdf_file = request.FILES['pdf_file']
        
        fs = FileSystemStorage()
        pdf_path = fs.save(pdf_file.name, pdf_file)
        pdf_full_path = fs.path(pdf_path)

        word_filename = os.path.splitext(pdf_file.name)[0] + '.docx'
        word_full_path = os.path.join(fs.location, word_filename)

        try:
            converter = Converter(pdf_full_path)
            converter.convert(word_full_path)  
            converter.close()

            with open(word_full_path, 'rb') as word_file:
                response = HttpResponse(word_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename="{word_filename}"'
                return response

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render(request, 'pdf_to_word.html', {'error_message': error_message})

        finally:

            if os.path.exists(pdf_full_path):
                os.remove(pdf_full_path)
            if os.path.exists(word_full_path):
                os.remove(word_full_path)

    return render(request, 'pdf_to_word.html')

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
import os
import pythoncom
from comtypes.client import CreateObject

def word_to_pdf(request):
    if request.method == 'POST' and request.FILES.get('word_file'):
        # Get the uploaded Word file
        word_file = request.FILES['word_file']
        
        # Save the Word file to the media folder
        fs = FileSystemStorage()
        word_path = fs.save(word_file.name, word_file)
        word_full_path = fs.path(word_path)

        # Define the output PDF file path
        pdf_filename = os.path.splitext(word_file.name)[0] + '.pdf'
        pdf_full_path = os.path.join(fs.location, pdf_filename)

        try:
            # Initialize COM library
            pythoncom.CoInitialize()

            # Open Word application
            word = CreateObject("Word.Application")
            word.Visible = False

            # Open the Word document
            doc = word.Documents.Open(word_full_path)

            # Save the document as PDF
            doc.SaveAs(pdf_full_path, FileFormat=17)  # 17 corresponds to PDF format
            doc.Close()
            word.Quit()

            # Serve the PDF file as a response
            with open(pdf_full_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
                return response

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render(request, 'word_to_pdf.html', {'error_message': error_message})

        finally:
            # Cleanup: Delete temporary files
            if os.path.exists(word_full_path):
                os.remove(word_full_path)
            if os.path.exists(pdf_full_path):
                os.remove(pdf_full_path)

    return render(request, 'word_to_pdf.html')
