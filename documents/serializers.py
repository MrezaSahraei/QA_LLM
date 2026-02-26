from rest_framework import serializers
from .models import Document, QAHistory


class DocumentSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'tags', 'summary']
        read_only_fields = ('created_at', 'updated_at',)

    def get_summary(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 100 else obj.content


class QAHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QAHistory
        fields = '__all__'



