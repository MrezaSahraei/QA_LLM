from django.contrib import admin
from .models import Document, QAHistory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "short_content", "created_at")
    search_fields = ("title", "content", "tags")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

    def short_content(self, obj):
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content


@admin.register(QAHistory)
class QAHistoryAdmin(admin.ModelAdmin):
    list_display = ("short_question", "created_at", )
    search_fields = ("question", "answer")
    readonly_fields = ("created_at",)

    def short_question(self, obj):
        return obj.question[:60] + "..."

