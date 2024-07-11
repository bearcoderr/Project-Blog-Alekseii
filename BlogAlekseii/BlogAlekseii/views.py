from django.shortcuts import render

def example_view(request):
    # Данные, которые вы хотите передать в шаблон
    context = {
        'my_data': 'Hello, World!',
        'another_data': 42,
    }
    return render(request, 'base.html', context)