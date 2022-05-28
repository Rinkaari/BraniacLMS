import json

from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get models
    News = apps.get_model("mainapp", "News")
    Courses = apps.get_model("mainapp", "Courses")
    Lesson = apps.get_model("mainapp", "Lesson")
    CourseTeachers = apps.get_model("mainapp", "CourseTeachers")
    # Create models objects
    with open("mainapp/fixtures/001_news.json") as news:
        news_data = json.loads(news.read())
    for item in news_data:
        News.objects.create(
            title=item["fields"]["title"], preambule=item["fields"]["preambule"], body=item["fields"]["body"]
        )
    with open("mainapp/fixtures/002_courses.json") as courses:
        courses_data = json.loads(courses.read())
    for item in courses_data:
        Courses.objects.create(
            name=item["fields"]["name"],
            description=item["fields"]["description"],
            description_as_markdown=item["fields"]["description_as_markdown"],
            cost=item["fields"]["cost"],
            cover=item["fields"]["cover"],
        )


def reverse_func(apps, schema_editor):
    # Get model
    News = apps.get_model("mainapp", "News")
    Courses = apps.get_model("mainapp", "Courses")
    # Delete objects
    News.objects.all().delete()
    Courses.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0004_course_teachers_table"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
