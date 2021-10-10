from django import forms


class CKEditorWidget(forms.Textarea):
    class Media:
        js = (
            'dadmin/build/ckeditor.js',
            'dadmin/build/translations/zh.js',
            'dadmin/build/config.js',
        )
