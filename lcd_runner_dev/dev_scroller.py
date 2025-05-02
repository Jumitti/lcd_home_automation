from lcd_runner_dev.emulator import LcdEmulator, CustomCharactersEmulator
from PIL import Image
from time import sleep

def block_to_binary_string(block):
    """Convertit un bloc 5x8 en une chaîne binaire de 40 bits."""
    bits = ""
    for y in range(8):  # 8 lignes
        for x in range(5):  # 5 colonnes
            pixel = block.getpixel((x, y))
            bits += "1" if pixel == 0 else "0"
    return bits

def extract_blocks_scroll(img, offset, num_blocks=16):
    """
    Extrait une série de blocs 5x8 avec un décalage horizontal global (offset).
    """
    width, height = img.size
    top_blocks = []
    bottom_blocks = []

    for i in range(num_blocks):
        x = offset + i * 5  # Avancer par blocs de 5 pixels
        if x + 5 > width:
            break  # Éviter de dépasser l'image

        top_block = img.crop((x, 0, x + 5, 8))
        bottom_block = img.crop((x, 8, x + 5, 16))

        top_blocks.append(block_to_binary_string(top_block))
        bottom_blocks.append(block_to_binary_string(bottom_block))

    string1 = "{" + "}{".join(top_blocks) + "}"
    string2 = "{" + "}{".join(bottom_blocks) + "}"
    return string1, string2


# Chargement de l'image une fois
img = Image.open("mountain_16x640.png").convert("1")
img_width, _ = img.size

# Lancement de l'affichage LCD
display = LcdEmulator(TITTLE_WINDOWS="Runner LCD")

offset = 0
while True:
    display.lcd_clear()
    if offset + 5 + 16 > img_width:
        offset = 0  # Reset à 0 pour boucle

    string1, string2 = extract_blocks_scroll(img, offset)
    display.lcd_display_extended_string(string1, line=1)
    display.lcd_display_extended_string(string2, line=2)

    offset += 1
    sleep(0.05)  # Ajuste la vitesse de défilement ici
