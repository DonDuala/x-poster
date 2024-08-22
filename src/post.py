import tweepy
import random
from PIL import Image, ImageDraw, ImageFont
import time
import sys

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Initialize Tweepy API with OAuth 1.0a
auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
api = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=None,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

quotes = [
   "Test Quote"
]

# Function to generate a random tropical color
def random_tropical_color():
    tropical_colors = [
        "#FF6F61",  # Coral
        "#FFB347",  # Peach
        "#FFDA77",  # Lemon
        "#6B5B95",  # Blueberry
        "#88D8B0",  # Mint
        "#F7D06A",  # Sunshine
        "#40E0D0"   # Turquoise
    ]
    return random.choice(tropical_colors)

# Convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

width, height = 800, 400

# Function to generate an image with a random gradient
def generate_image(text: str, file_path: str):
    color1 = random_tropical_color()
    color2 = random_tropical_color()

    # Convert colors to RGB
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    # Create a new image with a gradient
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

# Draw radial gradient
    for y in range(height):
        for x in range(width):
            dx = x - width / 2
            dy = y - height / 2
            distance = (dx**2 + dy**2)**0.5
            max_distance = ((width / 2)**2 + (height / 2)**2)**0.5
            ratio = distance / max_distance
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
            draw.point((x, y), fill=(r, g, b))

    # Load font
    font = ImageFont.truetype("VollkornSC-Regular.ttf", size=32)

    # Function to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ''
        while words:
            # Check size of the line with the next word added
            test_line = line + (words[0] + ' ')
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                line = test_line
                words.pop(0)
            else:
                lines.append(line.strip())
                line = ''
        if line:
            lines.append(line.strip())
        return lines

    # Wrap text and calculate dimensions
    max_width = width - 40
    wrapped_text = wrap_text(text, font, max_width)
    text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
    
    # Add extra spacing between lines
    line_spacing = 10  # Adjust this value as needed

    # Draw text
    y = (height - text_height - (len(wrapped_text) - 1) * line_spacing) // 2
    for line in wrapped_text:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), line, font=font, fill="#000000")
        y += bbox[3] - bbox[1] + line_spacing

    # Save the image
    image.save(file_path)

# Function to upload media and post a tweet with the media ID
def post_image_with_text(text: str, image_path: str):
    # Generate and save the image
    generate_image(text, image_path)
    
    # Upload media
    media = api.media_upload(filename=image_path)
    media_id = media.media_id


    # Post tweet with media ID
    tweet_response = client.create_tweet(
        media_ids=[media_id]
    )
    print(f"https://twitter.com/user/status/{tweet_response.data['id']}")

# Function to post a random quote
def post_random_quote():
    quote = random.choice(quotes)
    image_path = 'quote_image.png'
    post_image_with_text(quote, image_path)

# Function to post a bespoke quote from CLI
def post_bespoke_quote(quote):
    image_path = 'quote_image.png'
    post_image_with_text(quote, image_path)

# Main execution
# Example: python post.py "Making money on a CLOB is easy for you."
if __name__ == "__main__":
    # Check if a bespoke quote is provided via CLI
    if len(sys.argv) > 1:
        bespoke_quote = " ".join(sys.argv[1:])
        post_bespoke_quote(bespoke_quote)
        print('Waiting 8 hours')
        time.sleep(28800)
    
    while True:
        post_random_quote()
        # Wait for 8 hours (28800 seconds)
        print('Waiting 8 hours')
        time.sleep(28800)