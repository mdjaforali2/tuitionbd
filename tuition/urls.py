from django.urls import path, include
from .views import contact, candidate_delete, candidate_delete_confirm, candidate_accept, cancel, hire, candidate_cancel, candidate_decision_make, confirm_hiring, apply, applicants, commentdelete, commentedit, replyedit, replydelete, confirmcommentdelete, postupdate, addphoto, postcreate, likepost, addcomment, postview, filter, postview,  search, PostDeleteView, PostEditView, PostDetailView, ContactView, PostCreateView, PostListView
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
    path('create/', postcreate, name="create"),
    path('update/<str:id>/', postupdate, name="postupdate"),
    # path('create/', PostCreateView.as_view(), name="create"),
    path('postdetail/<int:pk>/', PostDetailView.as_view(), name="postdetail"),
    # path('edit/<int:pk>/', PostEditView.as_view(), name="edit"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name="delete"),
    path('apply/<int:id>/', apply, name="apply"),
    path('cancel/<int:id>/', cancel, name="apply"),
    path('applicants/<int:id>/', applicants, name="applicants"),
    path('hire/<int:id>/<int:pk>/', hire, name="hire"),
    path('confirm_hiring/<int:id>/<int:pk>/', confirm_hiring, name="confirm_hiring"),
    path('candidate_decission_make/<int:id>/<int:pk>/', candidate_decision_make, name="candidate_decision_make"),
    path('candidate_cancel/<int:id>/<int:pk>/', candidate_cancel, name="candidate_cancel"),
    path('candidate_delete/<int:id>/<int:pk>/', candidate_delete, name="candidate_delete"),
    path('candidate_accept/<int:id>/<int:pk>/', candidate_accept, name="candidate_accept"),
    path('candidate_delete_confirm/<int:id>/<int:pk>/', candidate_delete_confirm, name="candidate_delete_confirm"),
]