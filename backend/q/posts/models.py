from django.db import models
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as gis_models

from users.models import User

from .choices import (
    BOARD_TYPE_CHOICES, FIN_BOX_CHOICES, FIN_LAYOUT_CHOICES,
    CONDITION_CHOICES, CONSTRUCTION_CHOICES, US_STATES_CHOICES
) 

class Board(models.Model):
    shaper = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    board_type = models.CharField(
        max_length=1, choices=BOARD_TYPE_CHOICES, default='L'
    )
    fin_box_construction = models.CharField(
        max_length=1, choices=FIN_BOX_CHOICES, default='G'
    )
    fin_layout = models.CharField(
        max_length=1, choices=FIN_LAYOUT_CHOICES, default='S'
    )
    condition = models.CharField(
        max_length=1, choices=CONDITION_CHOICES, default='O'
    )
    construction = models.CharField(
        max_length=1, choices=CONSTRUCTION_CHOICES, default='P'
    )
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    volume = models.FloatField(blank=True, null=True)
    thickness = models.FloatField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} ({})".format(self.shaper, self.board_type)

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=50)
    pub_date = models.DateTimeField('Date published')
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                help_text="Price of the item")
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(
        max_length=30, choices=US_STATES_CHOICES, default='California'
    )
    zipcode = models.CharField(null=True, max_length=10)
    point_loc = gis_models.PointField(null=True, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to='pictures', blank=False, null=True,
                                default="pictures/default_post.png",)
                                # validators=[validate_file_size])
    picture_2 = models.ImageField(upload_to='pictures', default=None,
                                blank=True, null=True)
    picture_3 = models.ImageField(upload_to='pictures', default=None,
                                blank=True, null=True)
    picture_4 = models.ImageField(upload_to='pictures', default=None,
                                blank=True, null=True)
    display_picture = models.ImageField(upload_to='thumbnails',
                            default="thumbnails/default.png", blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField('Date Sold', blank=True, null=True)

    # views = GenericRelation(ObjectViewed)
    # flags = GenericRelation('Flag')
    # likes = GenericRelation('Like')



# class Author(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_of_death = models.DateField(null=True, blank=True)
#     headshot = models.ImageField(upload_to='author_headshot', blank=True,
#                                  null=True)

#     class Meta:
#         ordering = ['last_name', 'first_name']

#     def __str__(self):
#         return "{} {}".format(self.first_name, self.last_name)


# class Genre(models.Model):
#     """
#     Model representing a book genre
#     """
#     name = models.CharField(max_length=100, unique=True)
#     category = models.CharField(choices=CATEGORY_CHOICES,
#                                 default='fiction',
#                                 max_length=100, unique=False)

#     def __str__(self):
#         return self.name


# class Language(models.Model):
#     """
#     Model representing the written language
#     """
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Book(models.Model):
#     """
#     Model representing a book
#     """
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     genre = models.ForeignKey(Genre, related_name='books',
#                               on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, related_name='books',
#                                on_delete=models.CASCADE)
#     isbn = models.CharField('ISBN', max_length=13, null=True, blank=True)
#     cover_image = models.ImageField(upload_to='book_covers',
#                                     blank=False, null=True,
#                                     default='book_covers/bookDefault.png')
#     language = models.ForeignKey(
#         Language, on_delete=models.SET_NULL, null=True)
#     publication_date = models.DateField(null=True, blank=True)
#     # reads field used to keep track if a user read this book
#     reads = GenericRelation('ReadBook')
    
#     class Meta:
#         ordering = ['-publication_date']

#     def __str__(self):
#         return "{} ({}) by {}".format(
#             self.title, self.isbn, self.author.last_name)


# class Review(models.Model):
#     """
#     Model representing a book review by a user
#     """
#     user = models.ForeignKey(User, related_name='reviews',
#                              on_delete=models.CASCADE)
#     content = models.TextField()
#     date_published = models.DateTimeField('Date Published', auto_now_add=True)
#     star_rating = models.CharField(choices=STAR_CHOICES, default='⭐️⭐️⭐️',
#                                    max_length=10)
#     book = models.ForeignKey(Book, related_name='books',
#                              on_delete=models.CASCADE)

#     class Meta:
#         ordering = ['-date_published']

#     def __str__(self):
#         return "{} : {}".format(self.star_rating, self.book.title)


# class ReadBook(models.Model):
#     """
#     Model representing a book read by a user
#     This model is used to track a users read status of a Book
#     """
#     object_id = models.PositiveIntegerField()
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
#                                      null=True)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE,
#                              null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE,
#                              null=True, blank=True)
#     timestamp = models.DateField('Date marked read', auto_now_add=True)
#     content_object = GenericForeignKey()

#     def __str__(self):
#         return "{} read {}".format(self.user, self.book)