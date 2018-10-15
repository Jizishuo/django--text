from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import ShahuType, Location ,Shahu


shahutype = ShahuType.objects.all()
location = Location.objects.all()


class ShahuForm(forms.Form):
    title = forms.CharField(label='标题',
                               max_length=50,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-50位标题'}))

    shahutype = forms.ModelChoiceField(queryset=shahutype, empty_label='请选择分类',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=location,
                                      empty_label='请选择地点',
                                      widget=forms.Select(attrs={'class':'form-control'}))


    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '内容不能为空'})

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ShahuForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')


    def clean_title(self):
        title = self.cleaned_data['title']
        if Shahu.objects.filter(title=title).exists():
            raise forms.ValidationError('标题已存在')
        return title



