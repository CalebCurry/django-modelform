from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from djangouploads.forms import UploadForm
from djangouploads.models import Movie
from django.core.cache import cache


def home(request):
    return HttpResponse("ok")

def movie(request, movie_id):
    movie = cache.get(movie_id)
    if movie:
        print('cache')
        return render(request, 'movies/movie.html', {'movie': movie})
    
    else:
        print('db')
        movie = get_object_or_404(Movie, pk=movie_id)
        if movie is not None:
            cache.set(movie_id, movie)
            return render(request, 'movies/movie.html', {'movie': movie})
        #else:
        #    raise Http404('Movie does not exist')

def upload(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
        return redirect(home)
    return render(request, 'movies/upload.html', {'form' : UploadForm})