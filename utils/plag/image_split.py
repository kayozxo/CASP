from PIL import Image
import io
import os

def split_image_by_size(image_path, max_size_mb=19, min_height=200):
    """Splits a tall image into vertical chunks under max_size_mb."""
    img = Image.open(image_path)
    width, height = img.size
    chunks = []
    y = 0
    while y < height:
        # Start with a reasonable chunk height
        chunk_height = min(2000, height - y)
        while chunk_height >= min_height:
            box = (0, y, width, y + chunk_height)
            chunk = img.crop(box)
            buffer = io.BytesIO()
            chunk.save(buffer, format="JPEG", quality=85)
            size_mb = buffer.tell() / (1024 * 1024)
            if size_mb <= max_size_mb:
                # Save chunk to disk
                chunk_path = f"{image_path}_chunk_{len(chunks)}.jpg"
                chunk.save(chunk_path, format="JPEG", quality=85)
                chunks.append(chunk_path)
                y += chunk_height
                break
            chunk_height = int(chunk_height * 0.8)
        else:
            # If even the smallest chunk is too big, resize it
            chunk = img.crop((0, y, width, y + min_height))
            chunk = chunk.resize((width, int(min_height * 0.8)), Image.LANCZOS)
            chunk_path = f"{image_path}_chunk_{len(chunks)}.jpg"
            chunk.save(chunk_path, format="JPEG", quality=70)
            chunks.append(chunk_path)
            y += min_height
    return chunks
