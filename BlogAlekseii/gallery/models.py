from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image
from io import BytesIO
from ckeditor.fields import RichTextField
import datetime

TRANSLIT_DICT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
    'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
    'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
    'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
    'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
    'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
    'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
}


def custom_slugify(text):
    transliterated_text = ''.join(TRANSLIT_DICT.get(c, c) for c in text)
    sanitized_text = transliterated_text.replace("'", "").replace('"', "").replace(',', '').replace(';', '').replace(
        ':', '')
    return sanitized_text.replace(' ', '-').lower()


class GallerySite(models.Model):
    titleGallery = models.CharField(max_length=500, verbose_name='Название страницы с фотографиями')
    slugGallery = models.SlugField(max_length=200, unique=True, verbose_name='Заполняется автоматически', blank=True,
                                   null=True)
    dataGallery = models.DateField(default=datetime.date.today, verbose_name='Дата поездки')
    exeptGallery = models.TextField(max_length=500, verbose_name='Краткое описание')
    contentGallery = RichTextField(verbose_name='Контент для галереи', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slugGallery:
            self.slugGallery = custom_slugify(self.titleGallery)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titleGallery

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class Photo(models.Model):
    gallery = models.ForeignKey(GallerySite, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_photos')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or f"Фото в {self.gallery.titleGallery}"

    def compress_img(self, image):
        try:
            # Открываем изображение и получаем его размеры
            im = Image.open(image)
            width, height = im.size

            # Проверяем, если одно измерение превышает 1000 пикселей
            if width > 1000 or height > 1000:
                # Вычисляем новые размеры с сохранением пропорций
                aspect_ratio = width / height
                if aspect_ratio > 1:
                    new_width = min(width, 1000)
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = min(height, 1000)
                    new_width = int(new_height * aspect_ratio)

                # Масштабируем изображение до новых размеров
                im = im.resize((new_width, new_height))

            # Сохраняем изображение в формате WEBP
            im_bytes = BytesIO()
            im.save(im_bytes, format="WEBP", quality=100)

            # Создаем ContentFile и File для сохранения в модели Django
            image_content_file = ContentFile(im_bytes.getvalue())
            name = image.name.split('.')[0] + f'_{new_width}x{new_height}.webp'
            new_image = File(image_content_file, name=name)
            return new_image

        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return None

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект чтобы получить его ID
        super().save(*args, **kwargs)

        # Обработайте изображение только если оно было изменено или создано новое
        if self.image:
            try:
                # Создайте сжатое изображение
                compressed_image = self.compress_img(self.image)

                # Если успешно создано сжатое изображение, сохраните его
                if compressed_image:
                    self.image.save(compressed_image.name, compressed_image, save=True)

            except Exception as e:
                print(f"Ошибка при обработке изображения: {e}")
