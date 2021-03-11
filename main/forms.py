from django import forms
from main.models import Info, Answer

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['name', 'ph', 'message', 'agree']
        labels = {
            'name': '이름',
            'ph': '전화번호',
            'message': '메세지',
            'agree': '개인정보취급동의'
        }
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['memo']
        labels = {
            'memo': '메모',
        }
