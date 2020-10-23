from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["core/index.html"]
        else:
            return ["core/landing.html"]
