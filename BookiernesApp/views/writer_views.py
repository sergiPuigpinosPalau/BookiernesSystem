from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def PublishedBooks(request):
    #article_list = Article.objects.order_by('-publish_date')
    #scientist_list = Scientist.objects.order_by('-name')
    template = loader.get_template('Pllatila_Editor_escripto/Escriptor/Escriptor_LibrosPresentados.html')
    context = {}
    # context = {
    #     'article_list': article_list,
    #     'scientist_list': scientist_list,
    # }
    return HttpResponse(template.render(context, request))
