from PIL import Image

def pixelize_image(input_path, output_path, target_width, target_height):
    """
    Converts an image to a pixelized version at the desired resolution.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the pixelized output image.
        target_width (int): Target width in pixels.
        target_height (int): Target height in pixels.
    """
    try:
        # Open the input image
        img = Image.open(input_path)
        
        # Resize the image to the target resolution
        img_pixelized = img.resize((target_width, target_height), resample=Image.NEAREST)
        
        # Save the pixelized image directly
        img_pixelized.save(output_path)
        print(f"Pixelized image saved to {output_path} at resolution {target_width}x{target_height}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Input and output paths
    input_image = "assets/original_images/wizard/drake.png"  # Replace with your input image path
    output_image = "assets/pixelized_images/drake.png"  # Replace with your desired output path

    # Desired resolution (e.g., 32x32 pixels)
    target_width = 60
    target_height = 60

    pixelize_image(input_image, output_image, target_width, target_height)
