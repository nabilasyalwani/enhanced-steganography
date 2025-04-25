from PIL import Image
import math

key = []


def modPix(pix, data):
    data_bin = ''.join(format(ord(c), '08b') for c in data)
    lendata = len(data_bin)
    lenpix = len(pix)
    print(f"Bit Secret Data: {data_bin}")
    (idx_pix, idx_bin) = (0, 0)

    if lendata > lenpix:
        raise ValueError("There is no enough space to hide data.")

    while idx_bin < lendata and idx_pix < lenpix:
        p1, p2 = [pix[idx_pix], pix[idx_pix + 1]]
        d = p1 - p2
        s = int(data_bin[idx_bin])

        if d >= 0 and d <= 3:
            stego_pixel = p1 + d + s

            if stego_pixel < 255:
                new_pixel = stego_pixel
            else:
                new_pixel = p1
            key.append(1)
            idx_bin += 1

        elif d >= 4 and d <= 5:
            d_ = math.ceil(d / 2)

            stego_pixel = p1 + d_ + s

            if stego_pixel < 255:
                new_pixel = stego_pixel
            else:
                new_pixel = p1
            key.append(2)
            idx_bin += 1

        else:
            new_pixel = p1
            key.append(0)

        idx_pix += 2
        yield new_pixel
        yield p2

    print(f"Total bits embedded: {idx_bin}")
    print(f"Key length: {len(key)}")


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for new_pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), new_pixel)

        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    image = image.convert("L")

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("\nEnter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    key_filename = new_img_name.split(".")[0] + "_key.txt"
    key_str = ' '.join(str(k) for k in key)
    with open(key_filename, 'w') as f:
        f.write(key_str)

    print(f"Key saved to {key_filename}")


def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    image = image.convert("L")

    key_filename = img.split(".")[0] + "_key.txt"
    try:
        with open(key_filename, 'r') as f:
            key_str = f.read()
        key = list(map(int, key_str.strip().split()))

    except FileNotFoundError:
        print("Key file not found.")
        return ''

    data_bits = ''
    imgdata = image.getdata()
    lenkey = len(key)
    idx_pix = 0

    for i in range(lenkey):
        p1, p2 = [imgdata[idx_pix], imgdata[idx_pix + 1]]
        idx_pix += 2

        k = key[i]
        d = p1 - p2

        if k == 1 or k == 2:
            s = d % 2
            data_bits += str(s)

            diff = math.ceil(abs(d) / 2)
            cover_pixel = p1 - diff

            if k == 2:
                cover_pixel += 1

    data = ''
    for i in range(0, len(data_bits), 8):
        byte = data_bits[i:i + 8]
        if len(byte) == 8:
            data += chr(int(byte, 2))

    print("Decoded binary:", data_bits)
    return data


def main():
    a = int(input(":: Welcome to Steganography ::\n"
                  "1. Encode\n2. Decode\n"))

    if (a == 1):
        encode()

    elif (a == 2):
        print("\nDecoded Word :  " + decode())
    else:
        raise Exception("Enter correct input")


if __name__ == '__main__':
    main()
