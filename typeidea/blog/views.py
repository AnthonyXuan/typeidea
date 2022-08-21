
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from config.models import SideBar
from .models import Category, Tag, Post

# Create your views here.

# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
    
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars': SideBar.get_all(),
#     }
    
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)

# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None

#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
    
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)

# ! PostListView 是一个demo类，没有实际作用
class PostListView(ListView):
    queryset = Post.latest_posts()
    # 列表一页只有1个数据
    paginate_by = 1
    # 默认情况下使用ListView类，在template里面渲染出的变量名为：object_list，但这个名字体现不出是哪个model的列表。所以django提供了两个便利，第一是(如果提供了model域)允许使用小写的Model类名代替'object'，eg. comment_list;二是允许使用context_object_name变量用户自定义这个list的名字。
    context_object_name = 'post_list'
    template_name = 'blog/list.html'
    
# mixin指django中view功能的小组件，是比class-based view更小的单位，拥有更高的复用性。
# 下面这个mixin类的主要功能是提供了Sidbar和Category导航栏与底栏
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context
    
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'  
    context_object_name = 'post'
    # 设置p(rimary)k(ey)为'post_id'(如果不设置的话，默认查找关键字为'pk').此外，DetailView还有一种查找数据的方式是通过slug查找，对应的设置slug的变量为 slug_url_kwags(如果不设置的话，默认查找关键字为'slug')
    pk_url_kwarg = 'post_id'
    
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    # IndexView是我们定义的所有列表视图的基础视图，使用了list.html模板，并继承了CommonViewMixin，从而拥有侧边栏和导航及尾栏。CategoryView和TagView继承了IdexView，因而也使用list.html模板
    template_name  = 'blog/list.html'
    
class CategoryView(IndexView):
    # 执行顺序：先get_queryset()，后get_context_data()
    def get_queryset(self):
        """ 重写queryset, 根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context    
class TagView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        # 双下划线可以实现related fields across model的访问（eg. 下面从Post.tag 跨到了 Tag.id）
        return queryset.filter(tag__id=tag_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context