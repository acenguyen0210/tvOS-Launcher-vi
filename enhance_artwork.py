from PIL import Image, ImageEnhance, ImageFilter

# Load the clean artwork
img = Image.open('C:/Users/Admin/.gemini/antigravity/brain/fe3f826e-8e4f-4c63-b3d6-efb654926064/.user_uploaded/media_1793510846728_3c885493.png').convert('RGB')

# Upscale to 1920x1080 using Lanczos
upscaled = img.resize((1920, 1080), Image.Resampling.LANCZOS)

# Apply gentle unsharp mask to bring out details
sharp = upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

# Enhance color vibrancy slightly for projector display
enhancer = ImageEnhance.Color(sharp)
enhanced = enhancer.enhance(1.1)

enhanced.save('vietnam_clean_artwork_1080p.jpg', quality=95)
print('Saved vietnam_clean_artwork_1080p.jpg successfully')

