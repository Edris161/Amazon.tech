from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=150)  # Primary, Middle, High School
    description = models.TextField()
    curriculum = models.TextField()
    syllabus_file = models.FileField(upload_to='syllabus/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name