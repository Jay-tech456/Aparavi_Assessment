from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
img = Image.new('RGB', (600, 100), color='white')
d = ImageDraw.Draw(img)

# Use a common font and size (may need to specify the path to the font on your machine)
font = ImageFont.load_default()
# If you have TTF fonts:
# font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 32)

d.text((10,40), "This is a sample OCR test image.", font=font, fill=(0, 0, 0))

img.save('sample_ocr_test.png')
