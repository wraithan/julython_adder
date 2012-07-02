from django import forms


class RepoEnableForm(forms.Form):
    repos = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, repos):
        super(RepoEnableForm, self).__init__()
        self.fields['repos'].choices = repos
