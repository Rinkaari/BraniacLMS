import json
from datetime import datetime

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        # Get all previous data
        context = super().get_context_data(**kwargs)
        # Create your own data
        with open("/home/amdin-gb/Desktop/djangoBasics/BraniacLMS/test_news.json") as news:
            test_news = json.loads(news.read())
        context["test_news"] = test_news
        context["datetime_obj"] = datetime.now()
        return context


class NewsWithPaginatorView(NewsPageView):
    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


def xiaomi_redirect(request):
    url = "https://www.google.com/search?q=" + request.GET["param"]
    return HttpResponseRedirect(url)
