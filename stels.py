from PIL import Image


def image_to_bit_array(image_path):
    img = Image.open(image_path)
    image_bytes = img.tobytes()
    bit_array = []

    for byte in image_bytes:
        bit_array.append(format(byte, '08b'))

    return bit_array


def bit_array_to_image(bit_array, width, height):
    image_bytes = bytearray()
    for bits in bit_array:
        image_bytes.append(int(bits, 2))

    img = Image.frombytes('RGB', (width, height), bytes(image_bytes))
    return img


def hide_image(path_container_img: str, path_secret_img: str):
    bit_array_of_container = image_to_bit_array(path_container_img)
    bit_array_of_secret = image_to_bit_array(path_secret_img)
    for index_byte in range(0, len(bit_array_of_secret)):
        for index_bit in range(0, len(bit_array_of_secret[index_byte])):
            bit_array_of_container[index_byte * 8 + index_bit] = bit_array_of_container[index_byte * 8 + index_bit][
                                                                 0:-1] + bit_array_of_secret[index_byte][index_bit]
    bit_array_to_image(bit_array_of_container, 400, 200).save("stegano_hidden/encoded_img.bmp")
    print(bit_array_of_container[0:200])


def reveal(path_to_encoded_image: str):
    bit_array_of_encoded_image = image_to_bit_array(path_to_encoded_image)
    bit_array_of_reveal_image = []
    buff_byte = ''
    print(len(bit_array_of_encoded_image))
    for index_of_byte in range(0, len(bit_array_of_encoded_image)):

        if index_of_byte % 8 == 0 and index_of_byte != 0:
            bit_array_of_reveal_image.append(buff_byte)
            buff_byte = ''
        buff_byte += bit_array_of_encoded_image[index_of_byte][-1]

    if buff_byte:
        buff_byte = buff_byte.ljust(8, '0')
        bit_array_of_reveal_image.append(buff_byte)

    print(len(bit_array_of_reveal_image))
    bit_array_to_image(bit_array_of_reveal_image, 100, 100).save('stegano_revealed/revealed_img.bmp')


def main():
    hide_image('images/white(1).bmp', 'images/krasivie-kartinki-peizazh-1.bmp')
    reveal("stegano_hidden/encoded_img.bmp")


main()
