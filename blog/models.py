from django import forms
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase

class BlogIndexPage(Page):
    # TODO: remove this intro and do a better index.
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

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

class BlogTagIndexPage(Page):
    posts_per_page = 2

    def get_context(self, request):
        tag = request.GET.get('tag')
        all_posts = BlogPage.objects.live().order_by('-first_published_at').filter(tags__name=tag)
        paginator = Paginator(all_posts, self.posts_per_page)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = super().get_context(request)
        context['posts'] = posts
        return context

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

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

@register_snippet
class NavBarLink(models.Model):
    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
    )
    link = models.URLField(_('link'))

    panels = ['text', 'link']

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = _('Navbar link')
        verbose_name_plural = _('Navbar links')
