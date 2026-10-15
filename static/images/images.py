from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(filename, text, size=(1200, 800), bg_color=(255,77,109), text_color=(255,255,255)):
    """Create a placeholder image with text"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Add decorative elements
    draw.ellipse([(50, 50), (150, 150)], fill=(255,255,255,100))
    draw.ellipse([(size[0]-150, size[1]-150), (size[0]-50, size[1]-50)], fill=(255,255,255,100))
    
    img.save(filename)
    print(f"Created: {filename}")

# Create images directory if it doesn't exist
os.makedirs("static/images", exist_ok=True)

# Create placeholder images
create_placeholder_image("static/images/hero-bg.jpg", "SafeHer - Women Safety", size=(1920, 1080))
create_placeholder_image("static/images/login-bg.jpg", "SafeHer Login", size=(800, 600), bg_color=(230,62,92))
create_placeholder_image("static/images/feedback-bg.jpg", "We Value Your Feedback", size=(800, 600))
create_placeholder_image("static/images/5.png", "SafeHer Hero", size=(1920, 1080))
create_placeholder_image("static/images/3.png", "Safety Check", size=(1920, 1080))
create_placeholder_image("static/images/login.png", "Login to SafeHer", size=(800, 600))
create_placeholder_image("static/images/feedback.png", "Share Your Feedback", size=(800, 600))

print("\n✅ All placeholder images created successfully!")
print("Note: For production, replace these with actual images from Unsplash or your own photos.")