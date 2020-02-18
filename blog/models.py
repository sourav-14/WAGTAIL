from django.db import models
from django.shortcuts import render

from django import forms
from modelcluster.fields import ParentalKey,ParentalManyToManyField
from wagtail.core.models import Page,Orderable
from wagtail.admin.edit_handlers import FieldPanel,StreamFieldPanel,MultiFieldPanel,InlinePanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin,route
from wagtail.snippets.models import register_snippet


class BlogAuthorOrderables(Orderable):
    """ To select authors from Snippet """

    page = ParentalKey("blog.BlogDetailPage",related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete= models.CASCADE,
    )

    panels =[
        SnippetChooserPanel("author")

    ]



class BlogAuthor(models.Model):
    """ Blog Author For Snippets """
    
    name = models.CharField(max_length = 100)
    website = models.URLField(blank=True,null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = '+'
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],heading="Name And Image"
        ),
        MultiFieldPanel([
                FieldPanel("website"),
            ],heading="Links"
        ) 
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(
        verbose_name = "slug",
        allow_unicode = True,
        max_length = 200,
        help_text = 'Slug TO Identify Posts by Category'
    )

    def __str__(self):
        return self.name

    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]    

    class Meta:
        verbose_name = "BlogCategory"
        verbose_name_plural = "BlogCategories"
        ordering =["name"]


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin,Page):

    template = "blog/bloglisting.html"
    custom_title = models.CharField(
        max_length = 100,
        blank = False,
        null = True,
        help_text = 'Overwrites the default title'
    )

    def get_context(self,request,*args,**kwargs):

        context = super().get_context(request,*args,**kwargs)
        context["posts"] = BlogDetailPage.objects.live().public() 
        context["categories"] = BlogCategory.objects.all()

        #context["authors"] = BlogAuthor.all()
        return context

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    @route(r'^latest/$',name="latestposts")
    def latest_blog_posts(self, request,*args,**kwargs,):
        context = self.get_context(request,*args,**kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1] 

        return render(request,"blog/latest_posts.html",context)


class BlogDetailPage(Page):

    template = "blog/blog_detail.html"
    custom_title = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        help_text = 'Overwrites the default title'
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank = False,
        null = True,
        related_name ='+',
        on_delete = models.SET_NULL,
    )

    categories = ParentalManyToManyField("blog.BlogCategory")
    
    content = StreamField(
        [
            ("title_and_text",blocks.TitleAndTextBlock()),
            ("full_richtext",blocks.RichTextBlock()),
            ("cards",blocks.CardBLock()),
            ("cta",blocks.CTABlock()),
        ],
        null =True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author",min_num=1,max_num=4)
            ],heading="Author(s)"
        ), 
        MultiFieldPanel(
            [
                FieldPanel("categories",widget= forms.CheckboxSelectMultiple)
            ],heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]


class ArticlePage(BlogDetailPage):
    """ Subclassed Page inheriting from BlogDetail Page """

    template = "blog/article_blog_page.html"
    subtitle = models.CharField(max_length=100,blank=True,null=True)
    intro_image = models.ForeignKey("wagtailimages.Image",blank=True,null=True,on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("custom_title"),
                FieldPanel("subtitle"),
            ],heading="Sub Title"
        ),
        MultiFieldPanel( [
                ImageChooserPanel("blog_image"),
                ImageChooserPanel("intro_image"),
            ],heading="Images"
        ),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author",min_num=1,max_num=4)
            ],heading="Author(s)"
        ), 
        MultiFieldPanel(
            [
                FieldPanel("categories",widget= forms.CheckboxSelectMultiple)
            ],heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]



class VideoBlogPage(BlogDetailPage):

    youtube_video_id = models.CharField(max_length=100)


    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author",min_num=1,max_num=4)
            ],heading="Author(s)"
        ), 
        MultiFieldPanel(
            [
                FieldPanel("categories",widget= forms.CheckboxSelectMultiple)
            ],heading="Categories"
        ),
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("content"),
    ]