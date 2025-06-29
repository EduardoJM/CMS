from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page


class BioLinkAccount(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('image'),
        on_delete=models.CASCADE,
    )
    ajax_template = 'biolink/bio_link_account_partial.html'

    content_panels = Page.content_panels + [
        "image",
    ]

    posts_per_page = 12

    class Meta(Page.Meta):
        verbose_name = _('Account to bio links')
        verbose_name_plural = _('Accounts to bio links')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

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

class BioLinkPost(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('image'),
        on_delete=models.CASCADE,
    )
    multiple = models.BooleanField(
        _('show multiple icon?'),
        default=False,
    )
    link = models.URLField(
        _('post link')
    )

    content_panels = Page.content_panels + [
        "image",
        "multiple",
        "link",
    ]

    class Meta(Page.Meta):
        verbose_name = _('Post to bio link')
        verbose_name_plural = _('Posts to bio links')
