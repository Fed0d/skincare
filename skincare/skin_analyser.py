import cv2
import mediapipe as mp
from rembg import remove


def skin_analyser(photo_id: str):
    """
    Функция для анализа кожи на изображении. Она выполняет следующие шаги:

    1. Считывание изображения и повышение контрастности с помощью CLAHE.
    2. Применение фильтра для уменьшения шумов.
    3. Обнаружение лица на изображении с помощью MediaPipe.
    4. Удаление фона с изображения.
    5. Преобразование изображения в HSV цветовое пространство для выделения красных оттенков на коже.
    6. Применение фильтра Canny для обнаружения контуров красных областей.
    7. Отрисовка контуров на изображении для выделения областей с красными оттенками, если их площадь больше заданного порога.
    8. Сохранение обработанных изображений (контуры, Canny-изображение, маска красных оттенков) в указанную директорию.

    :param photo_id: Строка, представляющая идентификатор изображения (используется для формирования пути к файлу).

    Обработанные изображения сохраняются с именами:
    - `photos/{photo_id}_contours.jpg` — изображение с наложенными контурами красных участков.
    - `photos/{photo_id}_canny.jpg` — результат фильтра Canny для выделения краев.
    - `photos/{photo_id}_mask_red.jpg` — маска красных оттенков на коже.

    Исключения:
    - Если лицо не обнаружено на изображении, вызывается исключение `ValueError` с текстом "Лицо не найдено".
    """
    input_image = f'photos/{photo_id}.jpg'
    mp_face_detection = mp.solutions.face_detection

    image = cv2.imread(input_image)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    lab = cv2.merge((cl, a_channel, b_channel))

    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    image = cv2.bilateralFilter(image, 9, 75, 75)

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        if results.detections:
            image_no_bg = remove(image)
        else:
            raise ValueError("Лицо не найдено.")

    image_no_bg_hsv = cv2.cvtColor(image_no_bg, cv2.COLOR_BGR2HSV)

    lower_red = (0, 100, 100)
    upper_red = (10, 255, 255)
    mask_red = cv2.inRange(image_no_bg_hsv, lower_red, upper_red)

    canny = cv2.Canny(mask_red, 0, 100)
    contours, h = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    image_with_contours = image_no_bg.copy()

    for contour in contours:
        p = cv2.arcLength(contour, True)
        num = cv2.approxPolyDP(contour, 0.03 * p, True)
        x, y, w, h = cv2.boundingRect(num)
        rect_area = w * h
        if rect_area < 1000:
            cv2.rectangle(image_with_contours, (x, y), (x + w, y + h), (0, 0, 255), 4)

    cv2.imwrite(f'photos/{photo_id}_contours.jpg', image_with_contours)
    cv2.imwrite(f'photos/{photo_id}_canny.jpg', canny)
    cv2.imwrite(f'photos/{photo_id}_mask_red.jpg', mask_red)
