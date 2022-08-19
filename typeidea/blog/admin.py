from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post, Tag, Category
from .adminforms import PostAdminForm

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
            a = queryset.filter(category_id=category_id)
            print(a)
            return a
        return queryset

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline,]
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'
    
@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    
    form = PostAdminForm
    
    list_display = ('title','category','status','created_time', 'operator')
    list_display_links = []
    
    list_filter = [CategoryOwnerFilter]
    # category__name里的双下划线: 一种特殊用法，指定搜索了关联Model的数据
    search_fields = ['title', 'category__name']
    
    actions_on_top = True
    actions_on_bottom = True
    
    save_on_top = True
    
    # exclude = ('owner',)
    
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    
    fieldsets = (
        ('基础配置', {
            'description':'基础配置描述',
            'fields':(
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields':(
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields':('tag',),
        })
    )
    
    # filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)
    
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    
    operator.short_description = '操作'
    
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']