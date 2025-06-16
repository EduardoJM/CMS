from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogHomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        
        latest_posts = BlogPage.objects.live().order_by('-first_published_at')[0:3]
        context['latest_posts'] = latest_posts
        
        return context

    class Meta(Page.Meta):
        verbose_name = _('Blog home page')
        verbose_name_plural = _('Blog home pages')

class BlogListPage(Page):
    posts_per_page = 2

    def get_context(self, request):
        context = super().get_context(request)
        all_posts = self.get_children().live().order_by('-first_published_at')
        
        paginator = Paginator(all_posts, self.posts_per_page)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context
    
    class Meta(Page.Meta):
        verbose_name = _('Blog posts list page')
        verbose_name_plural = _('Blog posts list pages')

class BlogListByTagPage(Page):
    posts_per_page = 2

    def get_context(self, request):
        context = super().get_context(request)

        tag = request.GET.get('tag')
        if not tag:
            queryset = list(
                BlogPageTag.objects
                .select_related('tag')
                .annotate(tag_name=models.F('tag__name'))
                .values('tag_name')
                .annotate(num_posts=models.Count('tag_name'))
                .order_by('-num_posts')
            )
            context['tags'] = queryset
        else:
            all_posts = BlogPage.objects.live().order_by('-first_published_at').filter(tags__name=tag)
            paginator = Paginator(all_posts, self.posts_per_page)
            page = request.GET.get("page")
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context['posts'] = posts

        return context

    class Meta(Page.Meta):
        verbose_name = _('Blog posts list by tag tag page')
        verbose_name_plural = _('Blog posts list by tag pages')

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField(_('post date'))
    intro = models.CharField(
        verbose_name=_('introduction'),
        max_length=250,
    )
    body = RichTextField(
        verbose_name=_('article'),
        blank=True
    )
    authors = ParentalManyToManyField(
        'blog.Author',
        verbose_name=_('authors'),
        blank=True
    )
    tags = ClusterTaggableManager(
        verbose_name=_('tags'),
        through=BlogPageTag,
        blank=True,
    )

    scroll_display_title = True
    scroll_share_buttons = True

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                "date",
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                "tags",
            ],
            heading=_("post informations"),
        ),
        "intro",
        "body",
        InlinePanel("gallery_images", label=_('Image'), heading=_('Images')),
    ]

    class Meta(Page.Meta):
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog posts')

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('image'),
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(
        verbose_name=_('image caption'),
        blank=True,
        max_length=250
    )

    def __str__(self):
        return self.caption

    panels = ["image", "caption"]

    class Meta:
        verbose_name = _('post image')
        verbose_name_plural = _('post images')

@register_snippet
class Author(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
    )
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('author image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    abstract = models.CharField(
        verbose_name=_('small abstract'),
        max_length=255,
        blank=True,
    )

    panels = ["name", "author_image", "abstract"]

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name

@register_snippet
class NavBarLink(models.Model):
    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
    )
    link = models.URLField(_('link'), blank=True)
    page = ParentalKey(
        Page,
        on_delete=models.CASCADE,
        verbose_name=_('page'),
        blank=True,
        null=True,
        default=None
    )

    panels = ['text', 'link', 'page']

    class Meta:
        verbose_name = _('Navbar link')
        verbose_name_plural = _('Navbar links')

    def __str__(self):
        return self.text
