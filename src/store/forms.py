from django import forms

from store.models import ReviewRating


class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'message', 'rating']
        
    def __init__(self, *args, **kwargs):
        super(ReviewRatingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    