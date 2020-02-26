from django.db import models
from django.shortcuts import render

from django import forms
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from modelcluster.fields import ParentalKey,ParentalManyToManyField
from wagtail.api import APIField

from wagtail.core.models import Page,Orderable
from wagtail.admin.edit_handlers import FieldPanel,StreamFieldPanel,MultiFieldPanel,InlinePanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin,route
from wagtail.snippets.models import register_snippet
from rest_framework.fields import Field





class BlogListingPage(RoutablePageMixin,Page):

    template = "blog/bloglisting.html"
    max_count = 1

    subpage_types =[
        'blog.VideoBlogPage',
        'blog.ArticlePage',
    ]

    custom_title = models.CharField(
        max_length = 100,
        blank = False,
        null = True,
        help_text = 'Overwrites the default title'
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]


    def get_context(self,request,*args,**kwargs):

        context = super().get_context(request,*args,**kwargs)
        all_posts = BlogDetailPage.objects.live().public().order_by("-first_published_at") 
        
    
        paginator = Paginator(all_posts,3)

        page = request.GET.get("page")
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()
   
        #context["authors"] = BlogAuthor.all()
        return context


    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None

        if category is None:
            pass

        context["latest_posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])
        return render(request, "blog/latest_posts.html", context)

    @route(r'^latest/$',name="latestposts")
    def latest_blog_posts(self, request,*args,**kwargs,):
        context = self.get_context(request,*args,**kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:3] 

        return render(request,"blog/latest_posts.html",context)





class BlogDetailPage(Page):

    template = "blog/blog_detail.html"
    subpage_types =[]
    parent_page_types = ['blog.BlogListingPage']

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


    api_fields =[
        APIField("blog_authors"),
        APIField("content"),

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




class ImageSerializedField(Field):
    def to_representation(self,value):
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


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

    @property
    def author_name(self):
        return self.author.name
    
    @property
    def author_website(self):
        return self.author.website

    @property
    def author_image(self):
        return self.author.image

    api_fields = [
        APIField("author_name"),
        APIField("author_website"),
        APIField("author_image",serializer=ImageSerializedField()),
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


