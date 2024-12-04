import os
from PIL import Image


def resize_and_center_image(image_path, template_path, output_path, max_size=980):
    """
    Resizes an image to fit within max_size while maintaining aspect ratio,
    centers it on a template image, and saves the output.
    """
    # Open the source image
    with Image.open(image_path) as img:
        # Determine the scale factor to fit the image within max_size
        original_width, original_height = img.size
        scale = min(max_size / original_width, max_size / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Open the template image
    with Image.open(template_path) as template:
        template_width, template_height = template.size
        output_img = template.copy()

        # Calculate position to center the image on the template
        x_offset = (template_width - new_width) // 2
        y_offset = (template_height - new_height) // 2

        # Paste the resized image onto the template
        output_img.paste(resized_img, (x_offset, y_offset), mask=resized_img if resized_img.mode == "RGBA" else None)

    # Save the output image
    output_img.save(output_path)
    print(f"Saved: {output_path}")


def process_images(directory, template_image_path, output_directory, max_size=980):
    """
    Processes all images in the directory that end with '_unboxed',
    resizing and centering them on a template.
    """
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.lower().rsplit('.', 1)[0].endswith("_unboxed"):
            print(f"Processing {file_name}.")
            image_path = os.path.join(directory, file_name)
            output_path = os.path.join(output_directory, f"{file_name.lower().rsplit('.', 1)[0]}.png")
            resize_and_center_image(image_path, template_image_path, output_path, max_size)
            os.remove(image_path)
            print(f"Removed original file: {image_path}")


if __name__ == "__main__":
    image_directory = "images/paper"
    template_image_path = ".github/scripts/paper_thumbnail/template_box.png"
    output_directory = "images/paper"
    max_dimension = 980

    process_images(image_directory, template_image_path, output_directory, max_dimension)
