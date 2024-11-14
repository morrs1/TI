import base64

#
# with open('images/krasivie-kartinki-peizazh-1.jpg', 'rb') as image_file:
#
#     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#
# with open('output.txt', 'w', encoding='utf-8') as text_file:
#     text_file.write(encoded_string)

# #################################################################################
#

# with open('decoded_files/decoded.txt', 'r', encoding='utf-8') as text_file:
#     encoded_string = text_file.read()
#
#
# image_data = base64.b64decode(encoded_string)
#
#
# with open('output_image.png', 'wb') as image_file:
#     image_file.write(image_data)


def convert_bytearray(byte_arr):
    result = []
    for i in range(8):
        new_arr = bytearray(len(byte_arr))
        for j in range(len(byte_arr)):
            mask = 0x80 >> i  # создание маски для очистки бита
            new_arr[j] = byte_arr[j] & mask  # обнуление всех битов кроме i-го
        result.append(new_arr)
    return result


def combine_bytearrays(bytearrays_list):
    num_bytes = len(bytearrays_list[0])
    result = bytearray(num_bytes)
    for i in range(num_bytes):
        mask = 0x80  # начальная маска с наибольшим весом
        for j in range(8):
            if bytearrays_list[j][i] & mask:
                result[i] |= mask  # установка бита в новом bytearray
            mask >>= 1  # сдвиг маски на один бит вправо
    return result


def shift_bits_right(byte_array, shift_count):
    result = bytearray(len(byte_array))
    for i in range(len(byte_array)):
        shifted_byte = byte_array[i] >> shift_count
        result[i] = shifted_byte
    return result


# Открыть файл BMP для чтения
with open('images/some.bmp', 'rb') as f:
    bmp_header = bytearray(f.read(54))
    bmp_data = bytearray(f.read())
    result_ = convert_bytearray(bmp_data)

with open('images/white(1).bmp', 'rb') as f1:
    f1.read(138)
    bmp_data1 = bytearray(f1.read())
    result1 = convert_bytearray(bmp_data1)

# result[1] = shift_bits_right(result1[0], 1)

result_[5] = shift_bits_right(result1[0], 5)
result_[6] = shift_bits_right(result1[1], 6)
result_[7] = shift_bits_right(result1[2], 7)


# for i, bit_buffer in enumerate(result):
#     output_filename = f'output_bit{i}.bmp'
#
#     with open(output_filename, 'wb') as f:
#         f.write(bmp_header)
#         f.write(bit_buffer)

end_result = combine_bytearrays(result_)

with open('out.bmp', 'wb') as f:
    f.write(bmp_header)
    f.write(end_result)
