import math
import os
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from config.settings import BASE_DIR
from mainapp import models as mainapp_models
from mainapp.views import CoursesListView, NewsListView


class TestPagesAvailabilityUnauthUser(TestCase):
    def setUp(self):
        super().setUp()

    def test_pages_open_OK(self):
        """
        Function to test main web pages availability for unauthenticated users.
        """
        # urls got by show_url command from django_extensions
        with open(os.path.join(BASE_DIR, "urls_all.txt"), "r") as urls:
            urls_list = []
            for line in urls:
                urls_list.append(line.split("\t")[-1].split("\n")[0].split(":"))

        namespaces_to_check = ["mainapp", "authapp"]

        url_names_check_ignore = [
            "logout",
            "profile_edit",
            "course_feedback",
            "log_download",
            "log_view",
            "news_delete",
            "news_update",
            "news_create",
            "courses_detail",
            "news_detail",
        ]

        courses_count = mainapp_models.Courses.objects.count()
        news_count = mainapp_models.News.objects.count()

        url_names_check_with_lists = {"courses_detail": courses_count, "news_detail": news_count}

        courses_pages = math.ceil(courses_count / CoursesListView.paginate_by)
        news_pages = math.ceil(news_count / NewsListView.paginate_by)

        url_names_check_pagination = {"courses": courses_pages, "news": news_pages}

        for url in urls_list:
            if url[0] in namespaces_to_check:
                if url[1] not in url_names_check_ignore:
                    path = reverse(f"{url[0]}:{url[1]}")
                    result = self.client.get(path)
                    self.assertEqual(result.status_code, HTTPStatus.OK)
                if url[1] in url_names_check_with_lists:
                    for pk in range(url_names_check_with_lists[url[1]]):
                        path = reverse(f"{url[0]}:{url[1]}", args=[pk + 1])
                        result = self.client.get(path)
                        self.assertEqual(result.status_code, HTTPStatus.OK)
                if url[1] in url_names_check_pagination:
                    for page in range(url_names_check_pagination[url[1]]):
                        path = f"/{url[0]}/{url[1]}/?page={page+1}"
                        result = self.client.get(path)
                        self.assertEqual(result.status_code, HTTPStatus.OK)
