from django.db import models
from django.contrib.postgres.indexes import GinIndex
# Create your models here.


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان", unique=True)
    content = models.TextField(verbose_name="متن کامل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "سند"
        verbose_name_plural = "اسناد"

    def __str__(self):
        return self.title


class QAHistory(models.Model):
    question = models.TextField(verbose_name="پرسش کاربر")
    answer = models.TextField(null=True, blank=True, verbose_name="پاسخ سیستم")
    related_docs = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تاریخچه پرسش و پاسخ"
