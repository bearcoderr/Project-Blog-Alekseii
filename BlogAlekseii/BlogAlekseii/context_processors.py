from settings.models import Settings, MenuSite


def global_context(request):
    settings = Settings.objects.first()
    menu_links_queryset = MenuSite.objects.all()

    menu_links = []
    for link in menu_links_queryset:
        menu_links.append({
            'nameLink': link.nameLink,
            'link': link.link
        })

    context = {
        'titleHome': settings.titleHome,
        'favSite': settings.favSite,
        'copy': settings.copyText,
        'button_header': settings.buttonHeader,
        'menu_links': menu_links,
    }

    return context
