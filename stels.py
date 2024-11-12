from PIL import Image


# Функция для встраивания секретного изображения в контейнер
def encode_image(container_path, secret_path, output_path):
    # Открытие контейнера и секретного изображения
    container_img = Image.open(container_path)
    secret_img = Image.open(secret_path)

    # Преобразуем секретное изображение в RGB (если оно не RGB)
    secret_img = secret_img.convert("RGB")

    # Получаем размеры контейнера и секретного изображения
    container_width, container_height = container_img.size
    secret_width, secret_height = secret_img.size

    # Проверка, что контейнер достаточно велик для встраивания секретного изображения
    if container_width < secret_width or container_height < secret_height:
        raise ValueError("Размер контейнера меньше размера секретного изображения")

    # Скопируем контейнер, чтобы изменить его на месте
    container_pixels = container_img.load()

    # Встраиваем секретное изображение в контейнер
    secret_pixels = secret_img.load()

    for y in range(secret_height):
        for x in range(secret_width):
            # Получаем пиксель из секретного изображения
            r, g, b = secret_pixels[x, y]

            # Получаем текущий пиксель контейнера
            cr, cg, cb = container_pixels[x, y]

            # Заменяем LSB (наименее значащие биты) контейнера на биты пикселя секретного изображения
            container_pixels[x, y] = (
                (cr & 0xFE) | (r >> 7),  # Для красного канала
                (cg & 0xFE) | (g >> 7),  # Для зеленого канала
                (cb & 0xFE) | (b >> 7)  # Для синего канала
            )

    # Сохраняем измененное изображение
    container_img.save(output_path)


# Функция для извлечения скрытого изображения из контейнера
def decode_image(container_path, output_path):
    # Открываем изображение контейнер
    container_img = Image.open(container_path)
    container_img = container_img.convert("RGB")

    container_pixels = container_img.load()
    container_width, container_height = container_img.size

    # Создаем новое изображение для извлеченной информации
    secret_img = Image.new("RGB", (container_width, container_height))
    secret_pixels = secret_img.load()

    for y in range(container_height):
        for x in range(container_width):
            # Получаем пиксель контейнера
            cr, cg, cb = container_pixels[x, y]

            # Извлекаем LSB биты для каждого канала
            r = (cr & 1) << 7
            g = (cg & 1) << 7
            b = (cb & 1) << 7

            # Вставляем извлеченные пиксели в новое изображение
            secret_pixels[x, y] = (r, g, b)

    # Сохраняем извлеченное изображение
    secret_img.save(output_path)


# Пример использования:
encode_image("images/white.bmp", "images/some.bmp", "encoded_stels_image.png")
decode_image("encoded_stels_image.png", "decoded_secret.png")
