from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Document, QAHistory
from .serializers import DocumentSerializer, QAHistorySerializer
from rest_framework.response import Response
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.views import APIView
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.fake import FakeListLLM


# Create your views here.

class DocumentCreateView(generics.CreateAPIView):
    permission_class = permissions.IsAdminUser
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "tags"]
    ordering_fields = ["created_at", "title"]


class DocumentListView(generics.ListAPIView):
    permission_class = permissions.IsAdminUser
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "tags"]
    ordering_fields = ["created_at", "title"]


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAdminUser]




class QADetailView(generics.RetrieveAPIView):

    permission_classes = permissions.AllowAny
    queryset = QAHistory.objects.all()
    serializer_class = QAHistorySerializer


class IntegratedQAView(APIView):

    """
    Using a fake LLM to generate answers to user questions
    """

    def post(self, request):

        question = request.data.get('question', '')

        if not question:
            return Response({"error": "لطفاً پرسش خود را وارد کنید."}, status=400)

        vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
        query = SearchQuery(question)

        results = list(Document.objects.annotate(
            rank=SearchRank(vector, query)
        ).filter(rank__gte=0.05).order_by('-rank')[:3])

        serializer = DocumentSerializer(results, many=True)
        serialized_docs = serializer.data
        for i, obj in enumerate(results):
            serialized_docs[i]['relevance_score'] = round(obj.rank, 3)

        context_texts = [f"عنوان: {doc.title}\nمتن: {doc.content}" for doc in results]
        context = "\n\n---\n\n".join(context_texts)

        if not context:
            answer = "پاسخی در اسناد یافت نشد."
            QAHistory.objects.create(question=question, answer=answer)
            return Response({
                "question": question,
                "answer": answer,
                "related_documents": []
            })

        template = """شما یک دستیار هوشمند پاسخگو هستید.

        اطلاعات مستندات: {context}
        پرسش کاربر: {question}

        پاسخ:"""

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        fake_responses = [
            f"این یک پاسخ تستی و خودکار است.  با موفقیت اسناد مرتبط بررسی شد و این جواب را برای سوال «{question}» تولید کردم."
        ]

        try:
            llm = FakeListLLM(responses=fake_responses)

            chain = prompt | llm
            answer = chain.invoke({"context": context, "question": question}).strip()

        except Exception as e:
            answer = f"خطایی رخ داد {str(e)}"

        # saving in QA history
        QAHistory.objects.create(
            question=question,
            answer=answer,
            related_docs=serialized_docs)

        return Response({
            "question": question,
            "answer": answer,
            "related_documents": serialized_docs
        })


class QAHistoryListView(generics.ListAPIView):
    queryset = QAHistory.objects.all().order_by('-created_at')
    serializer_class = QAHistorySerializer
