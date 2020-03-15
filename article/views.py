from django.shortcuts import render
from .models import ArticlePost
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入User模型
from django.contrib.auth.models import User
from taggit.models import Tag
from comment.models import Comment

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()
    taglist = Tag.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'tag': tag,
        'taglist': taglist,
    }

    return render(request, 'article/index.html', context)

def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
     # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 新增了md.toc对象
    context = { 'article': article, 'toc': md.toc, 'comments': comments }

    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

def aboutme(request):
    context = {}
    return render(request, 'aboutme.html', context)
