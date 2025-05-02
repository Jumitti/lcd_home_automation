import random
from PIL import Image, ImageDraw, ImageOps

def generate_mountain_contour(width, height):
    img = Image.new('1', (width, height), color=1)  # Fond blanc
    draw = ImageDraw.Draw(img)

    contour_points = [(0, height)]

    for x in range(1, width):
        variation = random.randint(-2, 2)
        new_y = contour_points[-1][1] + variation
        new_y = max(0, min(new_y, height))
        contour_points.append((x, new_y))

    contour_points.append((width - 1, height))
    draw.line(contour_points, fill=0, width=1)

    return img

def add_horizontal_mirror_loop(img):
    """
    Duplique l'image horizontalement avec un effet miroir pour faire une boucle visuelle,
    en supprimant le dernier pixel pour éviter une ligne noire au centre.
    """
    # Supprimer la dernière colonne (bord droit)
    cropped = img.crop((0, 0, img.width - 1, img.height))

    # Créer le miroir
    mirrored = ImageOps.mirror(cropped)

    # Assembler l'image + miroir
    new_img = Image.new('1', (cropped.width * 2, img.height), color=1)
    new_img.paste(cropped, (0, 0))
    new_img.paste(mirrored, (cropped.width, 0))
    return new_img


def upscale_image(img, scale_factor):
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    return img.resize((new_width, new_height), Image.NEAREST)

def main():
    small_width = 5 * 64
    small_height = 16
    base_img = generate_mountain_contour(small_width, small_height)

    loop_img = add_horizontal_mirror_loop(base_img)
    loop_img.show()

    upscale_factor = 720 / small_height
    large_img = upscale_image(loop_img, upscale_factor)
    large_img.show()

    loop_img.save("mountain_16x640.png")
    large_img.save("mountain_720p.png")

if __name__ == '__main__':
    main()
