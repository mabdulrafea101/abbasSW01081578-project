from django import forms

from user.models import CustomUser
from .models import Event, EventCategory


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'description', 'images',
                  'start_date_time', 'end_date_time', 'status',
                  'max_organizers', 'max_participants',
                  'event_type', 'location',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_organizers': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'organizers_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_location'}),
            'event_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_event_type'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class AddOrganizerForm(forms.Form):
    organizer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type__in=['teacher', 'student']),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, event, *args, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)
        
        # Exclude users already assigned as organizers for this event
        existing_organizers = event.organizers.values_list('user_id', flat=True)
        self.fields['organizer'].queryset = CustomUser.objects.filter(
            user_type__in=['teacher', 'student'],
            is_account_confirmed=True
        ).exclude(id__in=existing_organizers)
    
    def clean(self):
        cleaned_data = super().clean()
        # Check if the event's organizer limit has been reached
        current_count = self.event.organizers.count()
        max_organizers = self.event.max_organizers
        
        if current_count >= max_organizers:
            raise forms.ValidationError(f"This event already has the maximum number of organizers ({max_organizers}).")
            
        return cleaned_data

