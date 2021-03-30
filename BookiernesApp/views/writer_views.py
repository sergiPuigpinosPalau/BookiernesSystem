from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView


# def PublishedBooks(request):
#     #article_list = Article.objects.order_by('-publish_date')
#     #scientist_list = Scientist.objects.order_by('-name')
#     template = loader.get_template('base.html')
#     context = {}
#     # context = {
#     #     'article_list': article_list,
#     #     'scientist_list': scientist_list,
#     # }
#     return HttpResponse(template.render(context, request))
# from django.views.generic import DetailView
from BookiernesApp.decorators import writer_required


@method_decorator([login_required, writer_required], name='dispatch')
class PublishedBooks(TemplateView):
    template_name = 'html_templates/Escriptor/Escriptor_LibrosPresentados.html'
