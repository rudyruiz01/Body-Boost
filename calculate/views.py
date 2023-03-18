from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

# Form for calories Total Metabolic Rate
class NewCaloriesForm(forms.Form):
    gender_choices = (("male", "Male"),("female", "Female"))
    gender = forms.ChoiceField(choices=gender_choices)
    feet = forms.IntegerField(min_value=3, max_value=7)
    inches = forms.IntegerField(min_value=0, max_value=11, required=False)
    weight = forms.IntegerField()
    age = forms.IntegerField(max_value=99)
    activity_level_choices = (
        ("0", ""),
        ("1", "No exercise "),
        ("2", "Light Exercise"),
        ("3", "Regular Exercise"),
        ("4", "Daily Exercise or Physical Job"),
        ("5", "Daily Exercise and Physical Job")
    )
    activity_level = forms.ChoiceField(choices=activity_level_choices)
    goal_choices = (("", "Maintain"), ("gain", "Gain"), ("lose", "Lose"))
    weight_goal = forms.ChoiceField(choices=goal_choices, required=False)
    pound = forms.FloatField(min_value=0, max_value=2, label="Pounds a week", required=False)


# Create your views here.
def index(request):
    if request.method == "POST":
        form = NewCaloriesForm(request.POST)
        if form.is_valid():
        # Get info from form
            gender = form.cleaned_data["gender"]
            feet = form.cleaned_data["feet"]
            inches = form.cleaned_data["inches"]
            if inches == '':
                inches = 0
            weight = float(form.cleaned_data["weight"])
            age = int(form.cleaned_data["age"])
            activity_level = int(form.cleaned_data["activity_level"])
            weight_goal = form.cleaned_data["weight_goal"]
            pound = form.cleaned_data["pound"]
            if pound is None:
                pound = 0
            # Convert feet and inches into inches
            height = feet * 12 + inches
            # Convert pounds into calories
            cal_per_pound = 3500
            pound = pound * cal_per_pound / 7
            # Calculates basil metabolic rate
            if gender == 'male':
                bmr = 66.47 + (6.24 * weight) + (12.7 * height) - (6.75 * age)
            else:
                bmr = 655.1 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
            # Calculates Total metabolic rate based on activity level
            if activity_level == 1: 
                tmr = bmr * 1.2
            elif activity_level == 2:
                tmr = bmr * 1.375
            elif activity_level == 3:
                tmr = bmr * 1.55
            elif activity_level == 4:
                tmr = bmr * 1.725
            else:
                tmr = bmr * 1.9
            # Calculate caloric intake goal based on weight goals
            if weight_goal == 'gain': 
                tmr += pound
            elif weight_goal == 'lose':
                tmr -= pound

            return render(request, "calculate/index.html", {
                "calories" : format(tmr, ',.0f'),
                "form" : NewCaloriesForm(request.POST)
            })
        else:
            return render(request, "calculate/index.html", {
                "form" : NewCaloriesForm(request.POST)
            })
    
    return render(request, "calculate/index.html", {
        "form" : NewCaloriesForm()
    })

def meals(request):
    return 