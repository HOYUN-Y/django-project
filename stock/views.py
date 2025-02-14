from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from stock.models import Item
from django.views import View
from .forms import InvestigateItemForm, ItemForm, CSVUploadForm
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import io
from io import BytesIO
from django.http import HttpResponse
import qrcode

from . import models


def list_item(request):
    search_query = request.POST.get('search','')

    if search_query:
        all_item = Item.objects.filter(name__icontains=search_query)
    else:
        all_item = models.Item.objects.all()
    first_item = models.Item.objects.order_by('pk').first()
    #print(all_item)
    context = {'all_item':all_item,'first_item':first_item}
    
    return render(request, 'stock/list.html', context= context)

def share_list(request):
    inspection_time = datetime.now(ZoneInfo("Asia/Seoul"))
    print(inspection_time)
    items = models.Item.objects.order_by('place','itemCode')
    group_items = defaultdict(list)
    for item in items:
        group_items[item.place].append(item)
    print(dict(group_items))
    context = {'group_items':dict(group_items),'time':inspection_time}
    return render(request, 'stock/share_list.html', context=context)

class InvestigateItemView(UpdateView):
    model = Item
    #fields = ['name','typeOfItem','place','amountOfBulk','amountOfEach']
    template_name = 'stock/item_investigate.html'
    form_class = InvestigateItemForm

    def form_valid(self, form):
        """폼이 유효하면 저장하고 로그를 출력"""
        # response = super().form_valid(form)
        # print(f"Updated Item: {self.object.name}, Bulk: {self.object.amountOfBulk}, Each: {self.object.amountOfEach}")
        # return response
        item = form.save(commit=False)
        if not form.cleaned_data.get("name"):
            item.name = self.object.name  
        if not form.cleaned_data.get("typeOfItem"):
            item.typeOfItem = self.object.typeOfItem  
        if not form.cleaned_data.get("place"):
            item.place = self.object.place  
        
        item.save()  # ✅ 저장
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_item']=Item.objects.filter(pk__lt=self.object.pk).order_by('-pk').first()
        context['next_item']=Item.objects.filter(pk__gt=self.object.pk).order_by('pk').first()
        return context
    
    def get_success_url(self):
        next_item = Item.objects.filter(pk__gt = self.object.pk).order_by('pk').first()
        if next_item:
            return reverse_lazy('stock:investigate_item',kwargs={'pk':next_item.pk})
        return reverse_lazy('stock:list')
    

    
    def form_invalid(self, form):
        """폼이 유효하지 않은 경우 디버깅 출력"""
        print("❌ form_invalid() 실행됨")
        print("❌ form.errors:", form.errors)  # 어떤 오류가 발생했는지 확인
        return self.render_to_response(self.get_context_data(form=form))
# class ItemDetailView(DetailView):
#     model = Item

class ItemCreateView(CreateView):
    model = Item
    #fields = ['typeOfItem','name','units','place']
    form_class = ItemForm
    success_url = reverse_lazy('stock:list')
    

    def form_valid(self,form):
        last_item = Item.objects.order_by('-itemCode').first()
        if last_item:
            form.instance.itemCode = last_item.itemCode + 1
        else:
            form.instance.itemCode = 1

        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['itemCode','typeOfItem','name','units','place']
    template_name = 'stock/item_update_info.html'
    success_url = reverse_lazy('stock:list')


    def post(self,request, *args, **kwargs):
        item = self.get_object()

        if "delete" in request.POST:
            item.delete()
            return redirect('stock:list')
        return super().post(request, *args, **kwargs)

class ItemAmountUpdateView(UpdateView):
    model = Item
    fields = ['amountOfBulk','amountOfEach']
    template_name = 'stock/item_update_amount.html'
    success_url = reverse_lazy('stock:list')


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('stock:list')


class ItemDetailVeiw(DetailView):
    model = Item

    def post(self,request, *args, **kwargs):
        item = self.get_object()
        if "delete" in request.POST:
            item.delete()
            return redirect('stock:list')
        return super().get(request, *args, **kwargs)
            
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            #UTF-8 인코딩으로 파일 읽기
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)

            Item.objects.all().delete()

            next(reader, None)

            for row in reader:
                try:
                    Item.objects.create(
                        itemCode=int(row[0]),
                        typeOfItem=row[1],
                        name=row[2],
                        units = int(row[3]),
                        place= row[4],
                        amountOfBulk = float(row[5]),
                        amountOfEach = float(row[6]),
                    )
                except Exception as e:
                    messages.error(request, f"Error:{e}")
                    return redirect('stock:upload_csv')
            messages.success(request, "csv file uploaded successful")
            return redirect('stock:list')
    else:
        form = CSVUploadForm()

    return render(request, 'stock/upload_csv.html', {'form':form})


def readonly_list(request):
    items = Item.objects.order_by('place','itemCode')
    context = {'items':items}
    return render(request, 'stock/readonly_list.html', context=context)

def generate_qr(request):
    url = request.build_absolute_uri('/stock/readonly_list/')
    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['코드','타입','이름','단위','재고위치','벌크수량','개별수량'])

    for item in Item.objects.all():
        writer.writerow([item.itemCode, item.typeOfItem, item.name, item.units, item.place, item.amountOfBulk, item.amountOfEach])

    return response