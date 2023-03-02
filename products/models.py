from django.db import models
from core.models import User, BaseModel
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import datetime


class Category(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    type_choice = [('M', 'Main Category'), ('Sub', 'Sub-Category')]
    name = models.CharField('Name', max_length=100)
    type = models.CharField(max_length=3, choices=type_choice)
    main_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="sub_cats")

    def __str__(self):
        return f"{self.name}"



