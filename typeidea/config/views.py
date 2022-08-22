from blog.views import CommonViewMixin

from django.views.generic import ListView
from .models import Link
# Create your views here.

class LinkListView(CommonViewMixin, ListView):
    querySet = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'