from PIL import Image
import random


key_24 = ''
pos = 0
new_color = []
pixel = []


def show_banner():
    print("\r\n      *************************************************")
    print(
        "      *            \033[1;31mAuthor:WojciechSkumajTo\033[1;m            *")
    print("      *               Encrypt your photos             *")
    print("      *       I don't have a decryption tool yet!!!   *")
    print("      *************************************************\r\n")


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = chr(9608) * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")


def open_image(path):
    while True:
        try:
            with Image.open(path) as im:
                return im, im.load()
        except Exception as e:
            print(f"[ERROR] -> {str(e)[10:]}")
            path = input("Please re-enter file path: ")


def save_file_key(key):
    try:
        with open("key.txt", "w") as f:
            f.write(key)
    except Exception as e:
        print(f"[ERROR] -> {str(e)}")


def generator_key(length):
    key = []
    progress_bar(0, length)
    for i, _ in enumerate(range(length)):
        key.append(str(random.randint(0, 1)))
        progress_bar(i+1, length)
    return "".join(key)


def encryption_image(im, encryption_level, map_pixel, key):
    pos = 0
    for i in range(im.width):
        for j in range(im.height):
            pixel = im.getpixel((i, j))
            rgb = bin(pixel[0])[2:].zfill(8) + bin(pixel[1]
                                                   )[2:].zfill(8) + bin(pixel[2])[2:].zfill(8)

            key_24 = key[pos:pos+24]
            pos += 24

            for k in range(24):
                new_color.append(operation_logic(
                    rgb[k], key_24[k], encryption_level))

            map_pixel[i, j] = (int("".join(new_color[:8]), 2), int(
                "".join(new_color[8:16]), 2), int("".join(new_color[16:24]), 2))
            new_color.clear()


def operation_logic(bit_color, bit_key, level):
    if level == '1':
        if bit_color == '1' and bit_key == '1':
            return '1'
        return '0'
    elif level == '2':
        if bit_color == '0' and bit_key == '1':
            return '0'
        return '1'
    elif level == '3':
        if bit_color == bit_key:
            return '0'
        return '1'


def main():

    show_banner()
    inspect = input("Do you want to load image? (Y/N): ").lower()
    if inspect == "y":
        path = input("You have to enter absolute file path or relative path for exmaple: \n\
[absolute]: C:\\Users\\WojciechSkumajTo\\Downloads\\test\\image.png \n\
[relative]: image.png \n\
[your path]: ")
        print("[Key generation process]: ")
        im, map_pixel = open_image(path)
        key = generator_key(im.width * im.height * 24)
        print("\n")
        save_key = input("Do you want to save key? (Y/N): ").lower()
        if save_key == 'y':
            with open("key.txt", "w") as f:
                f.write(key)

        encryption_level = input("Select the encryption level: \n\
        1) LOW \n\
        2) MEDIUM \n\
        3) HIGH \n\
        Your choice: ")

        encryption_image(im, encryption_level, map_pixel, key)
        save_photo = input(
            "Do you want to save encryption image (Y/N): ").lower()
        if save_photo == 'y':
            im.save("encryption_image_or.png")
            print("Your photo has been saved!\n")
    else:
        print("Bye!")


if __name__ == "__main__":
    main()
