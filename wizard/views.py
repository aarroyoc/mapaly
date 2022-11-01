from django.shortcuts import render

from mapaly.settings import AZURE_CONTAINER_URL_WIZARD_MAP


def wizard(request):
    context = {"wizard_data_url": AZURE_CONTAINER_URL_WIZARD_MAP}
    return render(request, "wizard/game.html", context)
