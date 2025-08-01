from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple tractor icon"""
    # Create a new image with a blue background
    img = Image.new('RGB', (size, size), '#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple tractor shape (rectangle with wheels)
    margin = size // 8
    tractor_width = size - 2 * margin
    tractor_height = tractor_width // 2
    
    # Tractor body
    draw.rectangle([margin, margin + tractor_height//2, margin + tractor_width, margin + tractor_height], 
                   fill='#ffffff', outline='#333333', width=2)
    
    # Wheels
    wheel_size = tractor_height // 3
    draw.ellipse([margin + tractor_width//4 - wheel_size//2, margin + tractor_height - wheel_size//2,
                  margin + tractor_width//4 + wheel_size//2, margin + tractor_height + wheel_size//2], 
                 fill='#333333')
    draw.ellipse([margin + 3*tractor_width//4 - wheel_size//2, margin + tractor_height - wheel_size//2,
                  margin + 3*tractor_width//4 + wheel_size//2, margin + tractor_height + wheel_size//2], 
                 fill='#333333')
    
    # Save the icon
    os.makedirs('static/icons', exist_ok=True)
    img.save(f'static/icons/{filename}')

# Create icons for different sizes
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    create_icon(size, f'icon-{size}x{size}.png')

print("App icons created successfully!") 