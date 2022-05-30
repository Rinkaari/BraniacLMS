import json

from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get models
    Lesson = apps.get_model("mainapp", "Lesson")
    CourseTeachers = apps.get_model("mainapp", "CourseTeachers")
    Courses = apps.get_model("mainapp", "Courses")
    # Create models objects
    with open("mainapp/fixtures/003_lessons.json") as lessons:
        lessons_data = json.loads(lessons.read())
    for item in lessons_data:
        Lesson.objects.create(
            num=item["fields"]["num"],
            course=Courses.objects.get(id=item["fields"]["course"]),
            title=item["fields"]["title"],
            description=item["fields"]["description"],
            description_as_markdown=item["fields"]["description_as_markdown"],
        )
    with open("mainapp/fixtures/004_teachers.json") as teachers:
        teachers_data = json.loads(teachers.read())
    for item in teachers_data:
        obj = None
        obj = CourseTeachers.objects.create(
            day_birth=item["fields"]["day_birth"],
            name_first=item["fields"]["name_first"],
            name_second=item["fields"]["name_second"],
        )
        obj.course.set(
            [Courses.objects.get(id=item["fields"]["course"][0]), Courses.objects.get(id=item["fields"]["course"][1])]
        )
        obj.save()


def reverse_func(apps, schema_editor):
    # Get model
    Lesson = apps.get_model("mainapp", "Lesson")
    CourseTeachers = apps.get_model("mainapp", "CourseTeachers")
    # Delete objects
    Lesson.objects.all().delete()
    CourseTeachers.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0005_data_migration"),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
