from django.db import models

class Technology(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    @property
    def num_projects(self):
        return self.project_set.count()

class Industry(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    @property
    def num_projects(self):
        return self.project_set.count()

class Project(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    technologies = models.ManyToManyField(Technology)
    description = models.TextField()
    industries = models.ManyToManyField(Industry)

    def __str__(self):
        return self.title
