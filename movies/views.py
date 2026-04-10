from rest_framework import viewsets, permissions
from .models import Genre, Movie
from .serializers import GenreSerializer, MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related('genres').all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        genre = self.request.query_params.get('genre')
        if genre:
            qs = qs.filter(genres__name__icontains=genre)
        language = self.request.query_params.get('language')
        if language:
            qs = qs.filter(language__icontains=language)
        return qs
