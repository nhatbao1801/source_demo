from django.urls import path
from rest_framework.routers import DefaultRouter

from event.views.get_data_views import AllEventViewAPI, GetEventTypes
from event.views.set_data_views import AddEventAPI, EditEventAPI, DeleteEvent, JoinEventAPI, upload_a_post, \
    delete_a_post, MediasEvent
from event.views.set_get_data_views import TicketViewSet, EventViewSet, EventParticipantModelViewSet, \
    EventSponsorModelViewSet, EventCategoryModelViewSet

urlpatterns = [
    # Lấy danh sách các loại sự kiện
    path('get-event-type/', GetEventTypes.as_view(), name='get-event-type'),
    # Danh sách tất cả các sự kiện hiện có
    # path('all-event/', AllEventViewAPI.as_view(), name='all-event'),
    # Thêm sự kiện
    path('add-event/', AddEventAPI.as_view(), name='add-event'),
    # Lấy list sự kiện
    # path('get-list-event/', EventViewSet.as_view({'get':'list'}), name='get-list-event'),
    # Lấy thông tin chi tiết của 1 sự kiện theo id
    # path('get-detail-of-event/', EventViewSet.as_view({'get':'retrieve'}), name='get-detail-of-event'),
    # Cập nhật sự kiện
    # path('edit-event/', EditEventAPI.as_view(), name='edit-event'),
    path('<int:id>/', DeleteEvent.as_view(), name='delete-event'),
    # Đăng ký tham gia sự kiện
    path('join-event/', JoinEventAPI.as_view(), name='join-event'),
    # Đăng bài biết lên trang của sự kiện
    # path('upload-a-post/', upload_a_post, name='upload-a-post'),
    # Chủ bài viết | chủ sự kiện xóa một bài viết
    # path('delete-a-post/<int:post_id>/', delete_a_post, name='delete-a-post-of-event'),
    # path('medias/', MediasEvent.as_view({'get': 'list_images', 'post': 'update_medias'}), name='medias-event'),
    
]

# # EventCategory CRUD
event_category_router = DefaultRouter()
event_category_router.register('event-category', EventCategoryModelViewSet, basename='event-category')
urlpatterns += event_category_router.urls

# Event CRUD
event_router = DefaultRouter()
event_router.register('events', EventViewSet, basename='events')
urlpatterns += event_router.urls

# # EventTicket CRUD
# ticket_router = DefaultRouter()
# ticket_router.register('ticket', TicketViewSet, basename='ticket')
# urlpatterns += ticket_router.urls

# # Event participant CRUD
event_participant_router = DefaultRouter()
event_participant_router.register('event-participant', EventParticipantModelViewSet, basename='event-participant')
urlpatterns += event_participant_router.urls

# # Event Sponsor CRUD
# event_sponsor_router = DefaultRouter()
# event_sponsor_router.register('event-sponsor', EventSponsorModelViewSet, basename='event-sponsor')
# urlpatterns += event_sponsor_router.urls
