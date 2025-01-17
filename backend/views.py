from django.shortcuts import render
from django.views.generic import TemplateView

class ReactAppView(TemplateView):
    template_name = "build/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
