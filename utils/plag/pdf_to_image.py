from pdf2image import convert_from_path
from PIL import Image
import os
import io


def compress_image_to_size(img, output_path, max_size_mb=19, min_quality=30):
    """Compress and save image to be under max_size_mb."""
    quality = 95
    while quality >= min_quality:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        size_mb = buffer.tell() / (1024 * 1024)
        if size_mb <= max_size_mb:
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            return output_path
        quality -= 10
    # If still too big, resize and try again
    width, height = img.size
    while size_mb > max_size_mb and width > 500:
        width = int(width * 0.9)
        height = int(height * 0.9)
        img = img.resize((width, height), Image.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=min_quality)
        size_mb = buffer.tell() / (1024 * 1024)
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    return output_path


def pdf_to_stitched_image(pdf_path, output_path, poppler_path=None):
    # Convert all PDF pages to images
    kwargs = {}
    if poppler_path:
        kwargs['poppler_path'] = poppler_path
    pages = convert_from_path(pdf_path, **kwargs)
    if not pages:
        raise ValueError("No pages found in PDF.")

    # Calculate total height and max width for the stitched image
    widths, heights = zip(*(p.size for p in pages))
    max_width = max(widths)
    total_height = sum(heights)

    # Create a new blank image to paste all pages
    stitched_img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    y_offset = 0
    for page in pages:
        # If page width is less than max_width, pad it
        if page.width < max_width:
            new_page = Image.new('RGB', (max_width, page.height), (255, 255, 255))
            new_page.paste(page, (0, 0))
            page = new_page
        stitched_img.paste(page, (0, y_offset))
        y_offset += page.height

    # Compress to under 20MB before saving
    return compress_image_to_size(stitched_img, output_path, max_size_mb=19)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python pdf_to_image.py <pdf_path> <output_image_path> [poppler_bin_path]")
        print("On Linux, you usually don't need to specify poppler_bin_path if poppler-utils is installed.")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    poppler_path = sys.argv[3] if len(sys.argv) > 3 else None
    out = pdf_to_stitched_image(pdf_path, output_path, poppler_path)
    print(f"Stitched image saved to: {out}")
