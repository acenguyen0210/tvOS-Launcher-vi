from PIL import Image

img = Image.open('C:/Users/Admin/.gemini/antigravity/brain/fe3f826e-8e4f-4c63-b3d6-efb654926064/.user_uploaded/media_1793510152016_279f12da.jpg')
w, h = img.size
print('Original:', w, h)

# In the image, the TV screen is bounded inside the black bezel:
# Left ~ 17px, Top ~ 20px, Right ~ 1007px, Bottom ~ 568px
# Let's crop the screen area
crop_box = (17, 20, 1007, 568)
screen = img.crop(crop_box)
screen = screen.resize((1920, 1080), Image.Resampling.LANCZOS)
screen.save('vietnam_wallpaper.jpg', quality=95)
print('Saved vietnam_wallpaper.jpg (1920x1080)')

