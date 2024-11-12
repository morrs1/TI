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

with open('decoded_files/decoded.txt', 'r', encoding='utf-8') as text_file:
    encoded_string = text_file.read()


image_data = base64.b64decode(encoded_string)


with open('output_image.png', 'wb') as image_file:
    image_file.write(image_data)
