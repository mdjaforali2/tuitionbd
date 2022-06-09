from django.urls import path, include
from .views import contact, apply, applicants, commentdelete, commentedit, replyedit, replydelete, confirmcommentdelete, postupdate, addphoto, postcreate, likepost, addcomment, postview, filter, postview,  search, PostDeleteView, PostEditView, PostDetailView, subview, ContactView, PostCreateView, PostListView
from .forms import ContactFormtwo
from .pdf import contact_pdf

app_name = 'tuition'

urlpatterns = [
    # path('contact/', contact, name='contact'),
    # path('post/', post, name="post"),
    path('search/', search, name='search'),
    path('addphoto/<int:id>/', addphoto, name='addphoto'),
    path('filter/', filter, name='filter'),
    path('pdf/', contact_pdf, name='pdf'),
    path('postview/', postview, name='postview'),
    path('likepost/<int:id>/', likepost, name='likepost'),
    path('addcomment/', addcomment, name='addcomment'),
    path('commentedit/<int:id>/<int:pk>/', commentedit, name='commentedit'),
    path('commentdelete/<int:id>/<int:pk>/', commentdelete, name='commentdelete'),
    path('confirmcommentdelete/<int:id>/<int:pk>/', confirmcommentdelete, name='confirmcommentdelete'),
    path('replyedit/<int:id>/<int:pk>/', replyedit, name='replyedit'),
    path('replydelete/<int:id>/<int:pk>/', replydelete, name='replydelete'),
    # path('commentedit/', commentedit, name='commentedit'),
    # path('commentdelete/<int:pk>/', CommentDeleteView.as_view(), name='commentdelete'),
    path('contact/', ContactView.as_view(), name="contact"),
    # path('contact2/', ContactView.as_view(form_class=ContactFormtwo, template_name="contact2.html"), name="contact"),
    path('posts/', postview, name="posts"),
    path('postlist/', PostListView.as_view(), name="postlist"),
    path('subjects/', subview, name="subjects"),
    path('create/', postcreate, name="create"),
    path('update/<str:id>/', postupdate, name="postupdate"),
    # path('create/', PostCreateView.as_view(), name="create"),
    path('postdetail/<int:pk>/', PostDetailView.as_view(), name="postdetail"),
    path('edit/<int:pk>/', PostEditView.as_view(), name="edit"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name="delete"),
    path('apply/<int:id>/', apply, name="apply"),
    path('applicants/<int:id>/', applicants, name="applicants"),
]