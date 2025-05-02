from lcd_runner_dev.emulator import LcdEmulator
from PIL import Image
from time import sleep

def sprite_to_raw_bits(sprite):
    return "".join(sprite)

def merge_sprite_on_block(sprite_bits, block_bits):
    # Fait un "OU" logique entre sprite et bloc
    return "".join("1" if s == "1" or b == "1" else "0" for s, b in zip(sprite_bits, block_bits))

def block_to_binary_string(block):
    bits = ""
    for y in range(8):
        for x in range(5):
            pixel = block.getpixel((x, y))
            bits += "1" if pixel == 0 else "0"
    return bits

def extract_blocks_scroll(img, offset, num_blocks=16):
    width, _ = img.size
    top_blocks = []
    bottom_blocks = []

    for i in range(num_blocks):
        x = offset + i * 5
        if x + 5 > width:
            break
        top_block = img.crop((x, 0, x + 5, 8))
        bottom_block = img.crop((x, 8, x + 5, 16))
        top_blocks.append(block_to_binary_string(top_block))
        bottom_blocks.append(block_to_binary_string(bottom_block))

    return top_blocks, bottom_blocks

# Définition des sprites
sprite1 = ["00000", "00000", "11000", "01100", "00110", "11111", "01110", "00000"]
sprite2 = ["00000", "00000", "00000", "11000", "01101", "11111", "00110", "00000"]
sprite3 = ["00000", "00000", "00000", "00110", "11111", "01100", "00000", "00000"]
sprite4 = ["00000", "00000", "01100", "11111", "00110", "11000", "00000", "00000"]
sprites = [sprite1, sprite2, sprite3, sprite4]

# Initialisation écran
display = LcdEmulator(TITTLE_WINDOWS="Runner LCD")
img = Image.open("mountain_16x640.png").convert("1")
img_width, _ = img.size

offset = 0
frame = 0

while True:
    if offset + 5 + 16 > img_width:
        offset = 0

    top_blocks, bottom_blocks = extract_blocks_scroll(img, offset)

    # Ligne 1 : montagne normale
    line1 = "{" + "}{".join(top_blocks) + "}"

    # Ligne 2 : sprite fusionné dans le premier bloc
    sprite_bits = sprite_to_raw_bits(sprites[frame % len(sprites)])
    original_block = bottom_blocks[0]
    merged_block = merge_sprite_on_block(sprite_bits, original_block)
    bottom_blocks[0] = merged_block
    line2 = "{" + "}{".join(bottom_blocks) + "}"

    display.lcd_clear()
    display.lcd_display_extended_string(line1, line=1)
    display.lcd_display_extended_string(line2, line=2)

    offset += 1
    frame += 1
    sleep(1/12)
