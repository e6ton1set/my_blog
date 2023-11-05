from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm


def post_share(request, post_id):
    # Извлекаем пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} рекомендует прочесть " \
                      f"{post.title}."
            message = f"Прочитать {post.title} можно здесь: {post_url}\n\n" \
                      f"{cd['name']}\'s комментарий: {cd['comments']}"
            send_mail(subject, message, 'testblogapp1@gmail.com',
                      [cd['to']])
            sent = True
    else:
        # Форма была впервые запрошена методом GET
        form = EmailPostForm()
    return render(request, 'blog_app/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})


# базовый класс ListView позволяет отображать перечисление любого типа объектов
class PostListView(ListView):
    """
     Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    # default = object_list
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog_app/post/list.html'


def post_list(request):
    post_list = Post.published.all()
    # постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog_app/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found.")

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog_app/post/detail.html',
                  {'post': post})
