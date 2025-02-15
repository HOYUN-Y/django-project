from django import forms
from .models import Item
from django.forms import ModelForm

# class MyModelForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['amountOfBulk','amountOfEach']
#         widgets = {
#             'amountOfBulk':forms.NumberInput(attrs={'step':'0.5','min':'0'}),
#             'amountOfEach':forms.NumberInput(attrs={'step':'0.5','min':'0'})
#         }

# class ItemForm(ModelForm):
#     class Meta:
#         model = Item
#         fields = "__all__"

#         labels = {
#             'amountOfBulk':'벌크',
#             'amountOfEach':'낱개',
#         }

class InvestigateItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name','typeOfItem','place','amountOfBulk','amountOfEach']

        widgets = {
            'name' : forms.TextInput(attrs={'readonly':'readonly'}),
            'typeOfItem' : forms.TextInput(attrs={'readonly':'readonly'}),
            'place': forms.TextInput(attrs={'readonly' : 'readonly'}),
            'amountOfBulk':forms.NumberInput(attrs={'step':'0.5','min':'0'}),
            'amountOfEach':forms.NumberInput(attrs={'step':'0.5','min':'0'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required=False
        self.fields['typeOfItem'].required=False
        self.fields['place'].required=False

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     print(f"Saving: {instance.name}, Bulk: {instance.amountOfBulk}, Each: {instance.amountOfEach}")
    #     if commit:
    #         instance.save()
    #     return instance

class ItemForm(forms.ModelForm):
    #dessert, md, seasonal, stock, syrup, etc
    TYPE_CHOICES = [
        ('dessert','dessert'),
        ('md','md'),
        ('seasonal','seasonal'),
        ('stock','stock'),
        ('syrup','syrup'),
        ('etc','etc')
    ]
    PLACE_CHOICES = [
        ('창고','창고'),
        ('냉장실','냉장실'),
        ('냉동실','냉동실'),
        ('뒷문','뒷문'),
        ('쇼케이스','쇼케이스'),
        ('캐비닛','캐비닛'),
        ('전시대','전시대'),
        ('앞문','앞문'),
        ('etc','etc'),
    ]

    typeOfItem = forms.ChoiceField(choices=TYPE_CHOICES, label="Type")
    place = forms.ChoiceField(choices=PLACE_CHOICES, label="Place")

    class Meta:
        model = Item
        fields = ['typeOfItem', 'name', 'units', 'place']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSV Upload')