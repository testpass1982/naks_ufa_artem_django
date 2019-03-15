from django.shortcuts import render
from .models import Document, Post, PostPhoto
from .forms import SendMessageForm

# Create your views here.

def index(request):
    title = 'НАКС Уфа'
    """this is mainpage view with forms handler and adapter to messages"""
    # tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    # docs = Document.objects.filter(
    #     publish_on_main_page=True).order_by('-created_date')[:3]

    main_page_news = Post.objects.filter(
        publish_on_main_page=True).order_by('-published_date')[:7]

    #Посты с картинками
    posts = {}
    for post in main_page_news:
        posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()
    
    #Посты без картинок
    # posts = Post.objects.all()[:3]

    # main_page_articles = Article.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    content = {
        'title': title,
        'posts': posts,
        # 'docs': docs,
        # 'articles': main_page_articles,
        'send_message_form': SendMessageForm(),
        # 'subscribe_form': SubscribeForm(),
        # 'ask_question_form': AskQuestionForm()
    }

    return render(request, 'mainapp/index.html', content)

def reestr(request):
    title = 'Реестр'

    content = {
        'title': title
    }
    return render(request, 'mainapp/reestr.html', content)

def doc(request):
    return render(request, 'mainapp/doc.html')
def news(request):
    return render(request, 'mainapp/news.html')

def details(request, pk=None, content=None):

    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.GET:
        content = request.GET.get('content_type')
        pk = request.GET.get('pk')

    content_select = {
        'post': Post,
        'article': Article
    }
    obj = get_object_or_404(content_select[content], pk=pk)
    print(obj)
    common_content = {'title': obj.title}
    if content == 'post':
        attached_images = PostPhoto.objects.filter(post__pk=pk)
        attached_documents = Document.objects.filter(post__pk=pk)
        post_content = {
            'post': obj,
            'images': attached_images,
            'documents': attached_documents,
            'bottom_related': Article.objects.all().order_by(
                '-created_date')[:3]
        }
    if content == 'article':
        tags_pk_list = [tag.pk for tag in obj.tags.all()]
        related_articles = Article.objects.filter(
            tags__in=tags_pk_list).exclude(pk=pk).distinct()
        post_content = {
            'post': obj,
            'related': related_articles,
            'bottom_related': related_articles.order_by('-created_date')[:3]
        }

    context = common_content.copy()
    context.update(post_content)
    context['return_link'] = return_link

    print(request.resolver_match)
    print(request.resolver_match.url_name)

    return render(request, 'mainapp/page_details.html', context)