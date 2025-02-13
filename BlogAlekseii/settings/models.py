from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from settings.fields import SVGImageField
from django.utils import timezone




class socialSettings(models.Model):
    altSocial = models.CharField(max_length=500, verbose_name='Название соц. сети')
    lincSocial = models.URLField(max_length=1000)
    classSocial = models.CharField(max_length=500, verbose_name='Класс по каторому будет показана иконка', help_text='Ссылка на шрифтовой пак https://fontawesome.ru/')

    def __str__(self):
        return self.altSocial

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

class numberSettings(models.Model):
    numberTitle = models.CharField(max_length=500, verbose_name='Впишите число или текст')
    numberText = models.CharField(max_length=500, verbose_name='Напишите текст')
    numberDopSimvol = models.CharField(max_length=500, verbose_name='Доп символ после цифры')

    def __str__(self):
        return self.numberTitle

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

class experienceSettings(models.Model):
    yearExperience = models.CharField(max_length=500, verbose_name='Год начала карьеры')
    year_old_Experience = models.CharField(max_length=500, verbose_name='Год окончания карьеры', blank=True, null=True)
    postExperience = models.CharField(max_length=500, verbose_name='Название должности')
    companyExperience = models.CharField(max_length=500, verbose_name='Компания')
    textExperience = models.CharField(max_length=500, verbose_name='Краткое описание')

    def __str__(self):
        return self.companyExperience

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class skillsSettings(models.Model):
    titleSkills = models.CharField(max_length=500, verbose_name='Название')
    countSkills = models.PositiveIntegerField(verbose_name='Проценты')
    imgSkills = SVGImageField(upload_to='photos/home/skill/', verbose_name='Иконка')

    def __str__(self):
        return self.titleSkills

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

class contactSettings(models.Model):
    nameSontact = models.CharField(max_length=500, verbose_name='Название пункта с контактами')
    titleSontact = models.CharField(max_length=500, verbose_name='Номер телефона/почта/адрес')
    linkSontact = models.CharField(max_length=500, verbose_name='Ссылка', blank=True, null=True)
    imgSontact = models.CharField(max_length=500, verbose_name='Класс по каторому будет показана иконка', help_text='Ссылка на шрифтовой пак https://fontawesome.ru/')

    def __str__(self):
        return self.nameSontact

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

class MenuSite(models.Model):
    nameLink = models.TextField(verbose_name='Название ссылки в меню', default='#')
    link = models.TextField(verbose_name='Ссылка на блок на сайте', default='#')

    def __str__(self):
        return self.nameLink

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class Settings(models.Model):
    imgHome = models.ImageField(upload_to='media/photos/home/', verbose_name='Главное изображение')
    logoSite = models.ImageField(upload_to='media/photos/', verbose_name='Логотип сайта')
    favSite = models.ImageField(upload_to='media/photos/', verbose_name='Фавикон сайта')
    titleHome = models.CharField(max_length=500, verbose_name='Заголовок')
    buttonHeader = models.CharField(max_length=500, verbose_name='Название кнопки')
    sub_titleHome = models.CharField(max_length=500, verbose_name='Подзаголовок')
    textHome = models.TextField(verbose_name='Подзаголовок', default='Привет')
    socialHome = models.ManyToManyField(socialSettings, blank=True, verbose_name='Социальные сети')
    numberlHome = models.ManyToManyField(numberSettings, blank=True, verbose_name='Номер на главной страницы')
    experienceHome = models.ManyToManyField(experienceSettings, blank=True, verbose_name='Вакансия')
    skillsHome = models.ManyToManyField(skillsSettings, blank=True, verbose_name='Skill')
    contactHome = models.ManyToManyField(contactSettings, blank=True, verbose_name='Контакты')
    MenuSiteList = models.ManyToManyField(MenuSite, blank=True, verbose_name='Меню')
    copyText = models.CharField(max_length=500, verbose_name='Текст копирайта')
    admin_email = models.EmailField(default='bearcoderr@gmail.com')


    def __str__(self):
        return self.titleHome

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'


    def compress_img(self, image):
        im = Image.open(image)
        width, height = im.size

        # Желаемые размеры для обрезанного и сжатого изображения
        desired_width = 437
        desired_height = 475

        # Рассчитываем соотношение сторон текущего изображения
        aspect_ratio = width / height

        # Вычисляем новую высоту, сохраняя пропорции
        new_height = int(desired_width / aspect_ratio)

        # Масштабируем изображение до новых размеров
        im = im.resize((desired_width, new_height))

        # Обрезаем изображение, если необходимо
        if new_height > desired_height:
            x = 0
            y = (new_height - desired_height) // 2
            area = (x, y, x + desired_width, y + desired_height)
            im = im.crop(area)

        # Сохраняем изображение в формате WEBP
        im_bytes = BytesIO()
        im.save(im_bytes, format="WEBP", quality=100)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + '.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        try:
            this = Settings.objects.get(id=self.id)
            if this.imgHome != self.imgHome:
                this.imgHome.delete(save=False)
                try:
                    new_image = self.compress_img(self.imgHome)
                    self.imgHome = new_image
                    super(Settings, self).save(*args, **kwargs)
                except ValueError:
                    super(Settings, self).save(*args, **kwargs)
            else:
                super(Settings, self).save(*args, **kwargs)
        except Settings.DoesNotExist:
            try:
                new_image = self.compress_img(self.imgHome)
                self.imgHome = new_image
                super(Settings, self).save(*args, **kwargs)
            except ValueError:
                super(Settings, self).save(*args, **kwargs)




class FormsHome(models.Model):
    SERVICE_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
    ]


    nameFormsHome = models.CharField(max_length=200, verbose_name='Имя отправителя')
    emailFormsHome = models.EmailField(verbose_name='Email отправителя')
    callFormsHome = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    massageFormsHome = models.TextField(verbose_name='Сообщение')
    time_create = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.nameFormsHome

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'