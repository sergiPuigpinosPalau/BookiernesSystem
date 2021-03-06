from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView, ListView

from django.conf import settings
from django.conf.urls.static import static

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    path('', login_required(mainView), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),

    #Escritor
    # http://127.0.0.1:8000/writer_published/
    url(r'^writer_published/$', login_required(PublishedBooks.as_view()), name='writer_published_books'),
    # http://127.0.0.1:8000/writer_published/get_book/33
    url(r'^writer_published/get_book/(?P<pk>\d+)/$', login_required(Get_Books.as_view()), name='books'),
    # http://127.0.0.1:8000/writer_published/add_book/
    url(r'^writer_published/add_book/$', login_required(PublishBook.as_view()), name='writer_publish_book'),
    # http://127.0.0.1:8000/writer_published/edit_book/33
    url(r'^writer_published/edit_book/(?P<pk>\d+)/$', login_required(Edit_Book.as_view()), name='writer_modify_a_book'),
    # http://127.0.0.1:8000/writer_published/edit_book/33
    url(r'^writer_message/get_book/(?P<pk>\d+)/$', login_required(Chat_Book.as_view()), name='chat_book'),
    url(r'^writer_message/post_book/(?P<pk>\d+)/send/$', login_required(post_chat), name='send_message'),

    url(r'^writer_published/book_delete/(?P<pk>\d+)$', login_required(deleteBook), name='book_delete'),

    url(r'^writer_notification/(?P<pk>\d+)/$', login_required(writer_notification), name='notification'),

    url(r'^writer_published/serch/$', login_required(SerchBooks.as_view()), name='serch_book'),

    # Editor
    url(r'^editor_book_revision/$', login_required(EditorBookRevision.as_view()), name='editor_book_revision'),


    url(r'^editor_message/get_book/(?P<pk>\d+)/$', login_required(Editor_Chat_Book.as_view()), name='chat_book_editor'),
    url(r'^editor_message/post_book/(?P<pk>\d+)/send/$', login_required(editor_post_chat), name='send_message_editor'),
    url(r'^editor_notification/(?P<pk>\d+)/$', login_required(editor_notification), name='notification_editor'),


    # Main Editor
    #url(r'^maineditor_book_revision/$', login_required(MainEditorBookRevision.as_view()), name='maineditor_book_revision'),


    #url(r'^maineditor_message/get_book/(?P<pk>\d+)/$', login_required(Maineditor_Chat_Book.as_view()), name='chat_book_maineditor'),
    #url(r'^maineditor_message/post_book/(?P<pk>\d+)/send/$', login_required(maineditor_post_chat), name='send_message_maineditor'),
    #url(r'^maineditor_notification/(?P<pk>\d+)/$', login_required(maineditor_notification), name='notification_maineditor'),




    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # writer

    # editor urls
    url(r'^editor_book_revision/$', EditorBookRevision.as_view(), name='editor_book_revision'),
    url(r'^editor_book_revision/book_revision_detail/(?P<pk>\d+)/$',
        EditorBookDetail.as_view(), name='editor_book_detail'),
    url(r'^editor_book_revision/book_revision_detail/(?P<pk>\d+)/accept_or_reject$',
        accept_or_reject, name='editor_accept_or_reject'),

    url(r'^editor_books_to_design/book_design_detail/(?P<pk>\d+)/$',
        EditorBookDesignDetail.as_view(), name='editor_design_detail'),

    path('editor_books_to_design', EditorBooksToDesign.as_view(), name='editor_books_to_design'),
    path('editor_image_petitions', EditorImagePetitions.as_view(), name='editor_image_petitions'),
    path('editor_image_petitions/image_petition_detail/<int:pk>/', EditorImagePetitionDetail.as_view(), name='image_petition_detail'),
    path('editor_image_petitions/new_petiton', EditorImagePetitionsCreate.as_view(), name='editor_image_petition_create'),

    # main editor urls
    # TODO create date_presented attribute to sort books
    url(r'^maineditor__books_presented_in_editorial/$',
        MainEditorBooksPresentedInEditorial.as_view(), name='maineditor_books_presented_editorial'),
    url(r'^maineditor__books_presented_in_editorial/book_presented_detail/(?P<pk>\d+)/$',
        MainEditorBookPresentedDetail.as_view(), name='maineditor_book_presented_detail'),
    url(r'^maineditor__books_presented_in_editorial/book_presented_detail/(?P<pk>\d+)/assign_or_reject$',
        assign_or_reject, name='maineditor_assign_or_reject'),


    # it urls
    url(r'^it_view/$', ItView.as_view(), name='user_list'),
    url(r'^it_view/get_user/(?P<pk>\d+)/$', ItDetailUser.as_view(), name='user_view'),
    url(r'^it_view/active_user/(?P<pk>\d+)/$', active_user, name='active_user'),
    url(r'^it_view/add_user/$', ITCrateUser.as_view(), name='create_user'),
    url(r'^it_view/edit_pass/(?P<pk>\d+)/$', ItPassword.as_view(), name='user_edit_pass'),
    url(r'^it_view/edit_pass_post/$', postEditPass, name='user_edit_pass_post'),
    url(r'^reset/password/$', ViewResetPass.as_view(), name='reset_password_view'),
    url(r'^post/reset/password/$', resetPass, name='reset_password'),


    # Graphic Designer main
    url(r'^main_graphic_designer/petitionview/$', AssignmentListImg.as_view(), name='main_petitionview_list'),
    url(r'^main_graphic_designer/get_petitionview/(?P<pk>\d+)/$', AssignmentDetaliImg.as_view(), name='main_petitionview_view'),

    url(r'^main_graphic_designer/bockmaquetat/$', AssignmentListBockMaquetat.as_view(), name='main_bockmaquetat_list'),
    url(r'^main_graphic_designer/get_bockmaquetat/(?P<pk>\d+)/$', AssignmentDetaliBockMaquetat.as_view(), name='main_bockmaquetat_view'),

    url(r'^main_graphic_designer/post_to_assign_GraphicDesigner/$', asignarGraphicDesigner,name='main_to_assign_graphicdesigner'),

    # Graphic Designer
    url(r'^graphic_designer/petitionview/$', ListImg.as_view(), name='petitionview_list'),
    url(r'^graphic_designer/get_petitionview/(?P<pk>\d+)/$', DetaliImg.as_view(), name='petitionview_view'),
    url(r'^graphic_designer/bockmaquetat/$', ListBockMaquetat.as_view(), name='bockmaquetat_list'),
    url(r'^graphic_designer/get_bockmaquetat/(?P<pk>\d+)/$', DetaliBockMaquetat.as_view(), name='bockmaquetat_view'),

    url(r'^graphic_designer/post_bockmaquetat/uploadbook/(?P<pk>\d+)/$', uploadbook, name='uploadbook_post'),
    url(r'^graphic_designer/post_bockmaquetat/uploadimg/$', uploadimg, name='uploadimg_post'),

    url(r'^graphic_designer/uploadimg/viewimg/(?P<pk>\d+)/$', GalleryImg.as_view(), name='get_uploadimg_view'),
    url(r'^graphic_designer/post_bockmaquetat/deleteimg/(?P<pk>\d+)/$', delete_img, name='get_deleteimg'),

    url(r'^graphic_designer_notification/(?P<pk>\d+)/$', designer_notification, name='notification_graphic_designer'),

    url(r'^graphic_designer_message/get_book/(?P<pk>\d+)/$', Graphic_designer_Chat_Book.as_view(), name='chat_book_graphic_designer'),
    url(r'^graphic_designer_message/post_book/(?P<pk>\d+)/send/$', graphic_designer_post_chat, name='send_message_graphic_designer'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

