from django.shortcuts import render


def render_page(request, slug):
    with open(f"text/pages/{slug}.html") as f:
        context = {"page": f.read()}
    return render(request, "text/page.html", context)
