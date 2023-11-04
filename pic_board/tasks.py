from celery import shared_task
from PIL import Image
from io import BytesIO
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile


@shared_task
def resize_image(image_path, max_size=8000):
    # print(image_path)
    try:
        # Open the uploaded image using Pillow
        img = Image.open(image_path)
        # Check the size of the image
        if img:
            # Resize the image to be less than 8000x8000 pixels
            new_width =  8000
            new_height = 8000
            img.thumbnail((new_width, new_height), Image.BILINEAR)

            # Save the resized image to a BytesIO object
            output = BytesIO()
            img.save(output, format='JPEG', quality=25)
            output.seek(0)
            resized_image = InMemoryUploadedFile(
                output, 'ImageField', f"{image_path.split('/')[-1]}",
                'image/jpeg', sys.getsizeof(output), None
            )


            with open(image_path, "wb") as f:
                f.write(output.read())

            return image_path
    except Exception as e:
        print(f"Exception during image resizing: {str(e)}")
        return None
