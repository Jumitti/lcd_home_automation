from PIL import Image

def block_to_binary_string(block):
    """Convertit un bloc 5x8 en une chaîne binaire de 40 bits."""
    bits = ""
    for y in range(8):  # 8 lignes
        for x in range(5):  # 5 colonnes
            pixel = block.getpixel((x, y))
            bits += "1" if pixel == 0 else "0"
    return bits  # Sans les crochets

def extract_blocks(image_path):
    img = Image.open(image_path).convert('1')  # Noir et blanc pur
    width, height = img.size

    if height != 16:
        raise ValueError("L'image doit faire exactement 16 pixels de haut.")

    top_blocks = []
    bottom_blocks = []

    for x in range(0, width, 5):
        # Haut : lignes 0 à 7
        top_block = img.crop((x, 0, x + 5, 8))
        top_blocks.append(block_to_binary_string(top_block))

        # Bas : lignes 8 à 15
        bottom_block = img.crop((x, 8, x + 5, 16))
        bottom_blocks.append(block_to_binary_string(bottom_block))

    string1 = "{" + "}{".join(top_blocks) + "}"
    string2 = "{" + "}{".join(bottom_blocks) + "}"
    return string1, string2

# Utilisation
string1, string2 = extract_blocks("mountain_16x640.png")

print("string1 =", string1)
print("string2 =", string2)
