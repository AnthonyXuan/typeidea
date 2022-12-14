
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    
    def __str__(self):
        return self.name
    
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    
    name = models.CharField(max_length=150, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = verbose_name_plural = "分类"
        
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
           
        # * 下面注释掉的代码会产生两次数据库的I/O， 已经优化为当前的代码     
        # nav_categories = categories.filter(is_nav = True)
        # normal_categories = categories.filter(is_nav = False)
        
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }
    
class Tag(models.Model):
    
    def __str__(self):
        return self.name
    
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = verbose_name_plural = "标签"
        
class Post(models.Model):
    
    def __str__(self):
        return self.title
    
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFE = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFE, '草稿'),
    )
    
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    
    title = models.CharField(max_length=225, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="内容", help_text="正文必须为markdown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']
        
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status = Post.STATUS_NORMAL).select_related('owner', 'category')
            
        return post_list, tag
    
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id = category_id)
        except:
            category = None
            post_list = None
        else:
            # select_realated 用来解决外键查询的N+1问题，使得template只需要一次查询数据库即可
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
            
        return post_list, category
    
    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset
        
    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')