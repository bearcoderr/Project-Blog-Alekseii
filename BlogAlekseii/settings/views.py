from django.shortcuts import render, redirect
from .models import Settings, socialSettings, numberSettings, experienceSettings, skillsSettings, contactSettings
from services.models import ServicesSite
from worck.models import WorckSite, GalleryWorck, categoryWorck
from News.models import News

#Форма обратной связи
from .forms import formsHome
from django.core.mail import send_mail
from django.conf import settings

#Рендер данных в резюме
# -*- coding: utf-8 -*-
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ImageFilter
import textwrap
import os

def generate_pdf(request):
    try:
        # Получаем объект Settings (предполагаем, что в базе данных есть только одна запись)
        settings = Settings.objects.first()

        # Создаем объект для сохранения PDF в памяти
        buffer = BytesIO()

        # Создаем PDF-документ
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Регистрация шрифта
        pdfmetrics.registerFont(TTFont('NotoSansCondensedMedium', 'static/path/to/NotoSans_Condensed-Medium.ttf'))

        # Устанавливаем шрифт и размер текста для основного контента
        pdf.setFont('NotoSansCondensedMedium', 12)

        # Определяем начальные координаты для размещения контента
        x = 50
        y = 750

        # Добавляем изображение, если оно задано в настройках
        if settings.imgHome:
            img_path = settings.imgHome.path  # Получаем полный путь к изображению
            if os.path.exists(img_path):  # Проверяем существование файла
                try:
                    # Открываем изображение и масштабируем его до 150x150 пикселей с использованием LANCZOS
                    img = Image.open(img_path)
                    img = img.convert("RGB")  # Преобразуем в RGB, если необходимо
                    img.thumbnail((150, 150), Image.LANCZOS)  # Используем LANCZOS для масштабирования
                    img_width, img_height = img.size

                    # Рисуем изображение на PDF
                    pdf.drawInlineImage(img, x, y - img_height, width=img_width, height=img_height)
                    y -= img_height + 20
                except Exception as e:
                    print(f"Error loading image: {str(e)}")
                    return HttpResponse(f"Error loading image: {str(e)}", status=500)
            else:
                print(f"Image file not found: {img_path}")
                return HttpResponse(f"Image file not found: {img_path}", status=404)
        else:
            print("No image found in settings.imgHome")
            return HttpResponse("No image found in settings.imgHome", status=404)

        # Добавляем заголовок
        pdf.setFont('NotoSansCondensedMedium', 18)
        pdf.drawString(x, y, settings.titleHome)
        y -= 20  # Уменьшаем y для следующего элемента

        # Добавляем подзаголовок
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, settings.sub_titleHome)
        y -= 30  # Уменьшаем y для следующего элемента

        # Добавляем текст о себе с автоматическим переносом строк
        pdf.setFont('NotoSansCondensedMedium', 12)
        wrapped_text = textwrap.wrap(settings.textHome, width=70)  # Разбиваем текст на строки по 70 символов
        for line in wrapped_text:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 12)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.drawString(x, y, line)
            y -= 15  # Уменьшаем y для следующей строки

        # Нарисовать линию после подзаголовка
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 15

        # Мои достижения
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Мои достижения")
        y -= 20  # Уменьшаем y для следующего элемента
        numbers = settings.numberlHome.all()

        for nums in numbers:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.setFont('NotoSansCondensedMedium', 12)
            pdf.drawString(x, y, f"{nums.numberTitle}{nums.numberDopSimvol} {nums.numberText}")
            y -= 15  # Уменьшаем y для следующей строки

        # Нарисовать линию после блока "Мои достижения"
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 15

        # Что я могу?
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Что я могу?")
        y -= 20  # Уменьшаем y для следующего элемента
        services = ServicesSite.objects.all()

        for service in services:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.setFont('NotoSansCondensedMedium', 12)
            pdf.drawString(x, y, f"{service.titleServices}")
            y -= 15  # Уменьшаем y для следующей строки
            service_text = textwrap.wrap(service.exeptServices, width=100)
            for service_ex in service_text:
                pdf.setFont('NotoSansCondensedMedium', 10)
                pdf.drawString(x + 10, y, service_ex)
                y -= 15  # Уменьшаем y для следующей строки
            y -= 5  # Дополнительный отступ между блоками услуг

        # Нарисовать линию после блока "Что я могу?"
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 15

        # Добавляем раздел "Опыт работы"
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Опыт работы")
        y -= 20  # Уменьшаем y для следующего элемента

        # Получаем и добавляем информацию об опыте работы
        experiences = settings.experienceHome.all()
        for experience in experiences:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.setFont('NotoSansCondensedMedium', 12)
            pdf.drawString(x, y, f"{experience.postExperience} в {experience.companyExperience}, {experience.yearExperience} - {experience.year_old_Experience if experience.year_old_Experience else 'настоящее время'}")
            y -= 15  # Уменьшаем y для следующей строки
            wrapped_text = textwrap.wrap(experience.textExperience, width=70)  # Разбиваем текст на строки по 70 символов
            for line in wrapped_text:
                pdf.setFont('NotoSansCondensedMedium', 10)
                pdf.drawString(x + 10, y, line)
                y -= 15  # Уменьшаем y для следующей строки
            y -= 0  # Дополнительный отступ между блоками опыта работы

        # Нарисовать линию после блока "Опыт работы"
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 20

        # Получаем и добавляем информацию о навыках
        skills = settings.skillsHome.all()
        # Добавляем раздел "Навыки"
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Мои навыки")
        y -= 15  # Уменьшаем y для следующего элемента
        # Создаем строку для перечисления навыков
        skills_str = ", ".join(skill.titleSkills for skill in skills)
        pdf.setFont('NotoSansCondensedMedium', 12)
        pdf.drawString(x, y, skills_str)
        y -= 20  # Уменьшаем y для следующей строки

        # Нарисовать линию после блока "Навыки"
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 15

        # Добавляем раздел "Контактная информация"
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Контактная информация")
        y -= 20  # Уменьшаем y для следующего элемента

        # Получаем и добавляем информацию о контактах
        contacts = settings.contactHome.all()
        for contact in contacts:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.setFont('NotoSansCondensedMedium', 12)
            pdf.drawString(x, y, f"{contact.nameSontact}: {contact.titleSontact}")
            y -= 15  # Уменьшаем y для следующей строки

        # Нарисовать линию после блока "Контактная информация"
        draw_line(x, y, 500, pdf)  # Примерная длина линии
        y -= 20

        # Добавляем раздел "Социальные сети"
        pdf.setFont('NotoSansCondensedMedium', 14)
        pdf.drawString(x, y, "Социальные сети")
        y -= 20  # Уменьшаем y для следующего элемента

        # Получаем и добавляем информацию о социальных сетях
        social_networks = settings.socialHome.all()
        for social in social_networks:
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы
            pdf.setFont('NotoSansCondensedMedium', 12)
            pdf.drawString(x, y, f"{social.altSocial}: {social.lincSocial}")
            y -= 15  # Уменьшаем y для следующей строки

            # Проверяем, осталось ли место на странице для следующего элемента
            if y < 50:
                pdf.showPage()  # Переход на новую страницу
                pdf.setFont('NotoSansCondensedMedium', 14)  # Возвращаем шрифт
                y = 750  # Сбрасываем y в начало новой страницы

        # Сохраняем PDF
        pdf.showPage()
        pdf.save()

        # Возвращаем PDF как HTTP-ответ
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        response['Content-Title'] = 'Резюме: Алексей Ачкасов - Программист'
        return response

    except Exception as e:
        # Логируем ошибку для отладки
        print(f"Error generating PDF: {str(e)}")
        # Возвращаем HTTP-ответ с информацией об ошибке
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

# Вспомогательная функция для рисования линии
def draw_line(x, y, length, pdf):
    pdf.line(x, y, x + length, y)









def viewHome(request):
    settings = Settings.objects.first()
    social_networks = socialSettings.objects.all()
    number_settings = numberSettings.objects.all()
    experience_settings = experienceSettings.objects.all()
    skills_settings = skillsSettings.objects.all()
    contact_settings = contactSettings.objects.all()
    services_site = ServicesSite.objects.all()
    worck_site = WorckSite.objects.all()
    gallery_worck = GalleryWorck.objects.all()
    category_worck = categoryWorck.objects.all()
    news_home = News.objects.order_by('-dataNews')[:3]
    context = {
        'settings': settings,
        'social_networks': social_networks,
        'number_settings': number_settings,
        'experience_settings': experience_settings,
        'skills_settings': skills_settings,
        'contact_settings': contact_settings,
        'services_site': services_site,
        'worck_site': worck_site,
        'gallery_worck': gallery_worck,
        'category_worck': category_worck,
        'news_home': news_home,
    }
    return render(request, "settings/index.html", context)



def FormsVievs(request):
    if request.method == 'POST':
        form = formsHome(request.POST)
        if form.is_valid():
            # Сохраняем форму и получаем объект FormsHome
            forms_home_instance = form.save()

            # Отправка электронной почты
            #send_mail(
                #'Новое сообщение с главной страницы',
                #forms_home_instance.massageFormsHome,  # Текст сообщения
                #settings.EMAIL_HOST_USER,  # Отправитель (лучше использовать адрес электронной почты из настроек Django)
                #[Settings.admin_email],  # Получатель (может быть список адресов)
                #fail_silently=False,
            #)
        return redirect('forms_home_thanks')
    else:
        form = formsHome()
    return render(request, 'settings/index.html', {
        'form': form,
    })

def contact_thanks_view(request):
    return render(request, 'settings/contact_thanks.html')