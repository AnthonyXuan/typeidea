from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Post, Tag, Category
# Register your models here.

class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前的用户的分类 """
    
    title = '分类过滤器'
    parameter_name = 'owner_category'
    
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(id=category_id)
        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','status','created_time', 'operator')
    list_display_links = []
    
    list_filter = [CategoryOwnerFilter]
    # ? category__name里的双下划线: 一种特殊用法，指定搜索了关联Model的数据
    search_fields = ['title', 'category__name']
    
    actions_on_top = True
    actions_on_bottom = True
    
    save_on_top = True
    
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )
    
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    
    operator.short_description = '操作'
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = admin.ModelAdmin.get_queryset(request) 
        return qs.filter(owner=request.user)