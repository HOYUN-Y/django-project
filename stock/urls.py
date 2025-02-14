from django.urls import path
from . import views
from .views import (ItemCreateView,ItemUpdateView,ItemDeleteView,
                    ItemDetailVeiw,ItemAmountUpdateView,InvestigateItemView,
                    upload_csv,readonly_list,generate_qr,export_csv)

app_name = 'stock'

urlpatterns = [
    path('list/',views.list_item, name='list'),
    path('create_item', ItemCreateView.as_view(), name="create_item"),
    path('update_item/<int:pk>', ItemUpdateView.as_view(), name='update_item'),
    path('delete_item/<int:pk>', ItemDeleteView.as_view(), name='delete_item'),
    path('detail_item/<int:pk>', ItemDetailVeiw.as_view(), name='detail_item'),
    path('update_item_each/<int:pk>',ItemAmountUpdateView.as_view(), name='update_amount_item'),
    path('investigate_item/<int:pk>',InvestigateItemView.as_view(), name='investigate_item'),
    path('share_list/',views.share_list, name='share_list'),
    path('upload_csv/',upload_csv, name='upload_csv'),
    path('readonly_list/',readonly_list, name='readonly_list'),
    path('generate_qr/',generate_qr, name='generate_qr'),
    path('export_csv/', export_csv, name='export_csv'),
]