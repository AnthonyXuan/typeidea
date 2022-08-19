from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """_summary_
    1. 用来自动补充文章、分类、标签、侧边栏和友链这些Model的owner字段为当前用户(注意：评论Model不含owner字段，所以不需要继承BaseOwnerAdmin)
    2. 用来针对queryset过滤当前用户的数据
    Args:
        admin (_type_): _description_
    """
    
    # 不在admin的表格中展示owner字段
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = admin.ModelAdmin.get_queryset(self, request) 
        return qs.filter(owner=request.user)