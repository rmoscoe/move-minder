# MoveMinder

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Technology Used](#technology-used)
  - [Badges](#badges)
- [Description](#description)
- [Code Examples](#code-examples)
- [Installation and Usage](#installation-and-usage)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Getting Started](#getting-started)
- [Learning Points](#learning-points)
- [Author Info](#author-info)
  - [Ryan Moscoe](#ryan-moscoe)
- [Credits](#credits)
- [License](#license)
- [Badges](#badges-1)
- [Features](#features)
- [Contributing](#contributing)
- [Tests](#tests)

<br/>

## Technology Used 

| Technology Used         | Resource URL           | 
| ------------- |:-------------:| 
| Python | [https://www.python.org/](https://www.python.org/) |
| Django | [https://www.djangoproject.com/](https://www.djangoproject.com/) |
| Django-Phonenumber-Field | [https://django-phonenumber-field.readthedocs.io/en/latest/](https://django-phonenumber-field.readthedocs.io/en/latest/) |
| Django-PWA | [https://github.com/silviolleite/django-pwa](https://github.com/silviolleite/django-pwa) |
| Django-Tailwind | [https://django-tailwind.readthedocs.io/en/latest/](https://django-tailwind.readthedocs.io/en/latest/) |
| HTML    | [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | 
| FontAwesome | [https://fontawesome.com/](https://fontawesome.com/) |
| CSS     | [https://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)      |  
| TailwindCSS |  [https://tailwindcss.com/](https://tailwindcss.com/) |
| JavaScript | [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) |
| Node.js | [https://nodejs.org/en](https://nodejs.org/en) |
| ApexCharts | [https://apexcharts.com/](https://apexcharts.com/) |
| PostgreSQL | [https://www.postgresql.org/](https://www.postgresql.org/)
| Git | [https://git-scm.com/](https://git-scm.com/)     |  
| GitHub | [https://github.com/](https://github.com/) |
| Green Unicorn (gunicorn) | [https://gunicorn.org/](https://gunicorn.org/) |
| Whitenoise | [https://whitenoise.readthedocs.io/en/latest/](https://whitenoise.readthedocs.io/en/latest/) |
| Amazon Web Services (AWS) | [https://aws.amazon.com/](https://aws.amazon.com/) |
| AWS Simple Storage Service (S3) | [https://aws.amazon.com/](https://aws.amazon.com/) |
| AWS Relational Database Service (RDS) | [https://aws.amazon.com/](https://aws.amazon.com/) |
| Heroku | [https://www.heroku.com/](https://www.heroku.com/) |
| Gemini | [https://gemini.google.com/app](https://gemini.google.com/app) |

<br/>

### Badges

![Static Badge](https://img.shields.io/badge/JavaScript-86.9%25-%23eddc1c) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/CSS-9.2%25-%23395ded) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/HTML-2.0%25-%23db441f) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/Python-0.9%25-%234584b6) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/Other-1.0%25-lightgray)

<br/>

## Description 

[Visit the Deployed Site](https://moveminder-tracker-f210fd4c1414.herokuapp.com/)

MoveMinder lets you track the contents and status of every box, appliance, and piece of furniture throughout a move. Create a record for each move with the date(s), origin address, and destination address. Add a record for each parcel, including its type, contents, and weight, as well as the room in which it belongs at its destination. Print labels with a QR code for each parcel, and scan the QR code to update the parcel's status. MoveMinder is a Progressive Web App (PWA), so you can install it on your mobile device, making it easy to use your mobile device as a scanner.

<br/>

![Site Langing Page](./move_minder/static/images/home-light.png)

<br/>

I had been sitting on the idea for this project for some time, until I found myself at a point where I needed to create a project as a way to learn Django's generic views, forms, and the Django Template Language. I chose to create this application specifically because it lent itself well to the list, detail, create, update, and delete structure of Django's generic views.

For the data layer, I opted for a PostgreSQL database, hosted on AWS RDS. Because I needed to include images in the database, I am also using AWS S3. I used Python and Django for both the back end and front end of this application, augmented by TailwindCSS for styling. Finally, I used Gemini to generate images for the homepage.

<br/>

## Code Examples

This first example demonstrates the use of the generic DetailView to create a View for parcel details. This view is slightly more complex than a typical detail view, because it also includes a form for updating the status of the parcel.


```python
class ParcelDetailView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = Parcel
    template_name = "tracker/parcel_detail.html"
    form_class = ParcelStatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get("success", None)
        if success is not None:
            context["success"] = success
        return context
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == f"Parcel Detail: {self.get_object().id}":
                history.pop(i)
                break
        history.insert(0, { "name": f"Parcel Detail: {self.get_object().id}", "url": url})
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        url = reverse("tracker:parcel-detail", kwargs={'move_id': self.get_object().move_id.id, 'pk': self.get_object().id})
        url += "?success=true"
        return url
```

The following example shows a Form. I extended Django's built-in User model, so the signup and update forms needed to seamlessly merge the User model with my Userprofile model. I also needed to override the clean() method to account for dual password fields that both related to the single `password` field in the User model.

```python
class UpdateUserForm(ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

        def __init__(self, *args, **kwargs):
            self.user = kwargs.get("instance", None)
            super().__init__(*args, **kwargs)

            self.fields["username"].initial = self.user.username
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

```

Finally, this example shows a portion of my parcel_update.html template. For some forms in this application, I was able to simply use the {{ form.as_div }} tag to render all form fields, including applicable help text and error messages. This particular form was more complicated, however, because it included a photo input. By default, Django renders the photo input with an Upload button, but I wanted to enable users to snap a photo with the camera on their mobile device. I needed to add a camera button, so I had to render each form field individually.

```html
    <form id="update-parcel-form" method="post" class="form-grid my-2 sm:my-3 mx-0 md:mx-auto md:my-8 rounded-md lg:rounded-lg box p-4 md:p-8 lg:p-12 xl:p-16 w-full md:w-4/5 lg:w-2/3 xl:w-1/2 box-border space-y-4 lg:space-y-6" enctype="multipart/form-data">
        <h2 class="text-center">{{ move.nickname }}: Update Parcel</h2>
        {% csrf_token %}
        <div class="fieldWrapper">
            {{ form.type.as_field_group }}
        </div>
        <div class="fieldWrapper">
            {{ form.room.as_field_group }}
        </div>
        <div class="fieldWrapper">
            {{ form.contents.as_field_group }}
        </div>
        <div class="fieldWrapper">
            <label class="block" for="{{ form.photo.id_for_label }}">
                <span>Photo:</span>
            </label>
            <div class="flex flex-wrap justify-between space-x-2 lg:space-x-3 items-center">
                {{ form.photo }}
                <div class="flex mt-2 items-center space-x-2">
                    <span>&nbsp;or&nbsp;</span>
                    <button id="camera-button" class="btn-square primary">
                        <i id="camera-icon" class="fa fa-camera"></i>
                        <svg id="spinner" class="hidden animate-spin size-5 text-white dark:text-slate-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="fieldWrapper">
            {{ form.weight.as_field_group }}
        </div>
        <div class="fieldWrapper">
            {{ form.status.as_field_group }}
        </div>
        <div>
            {% if form.errors %}
                <div>
                    <p class="text-red-500 dark:text-red-600 text-sm md:text-base">Please correct the following errors:</p>
                    <ul class="errorlist">
                        {% for field, error_list in form.errors.items %}
                            {% for error in error_list %}
                                <li>{{ field }}: {{ error }}</li>
                            {% endfor %}
                        {% endfor %}
                    </ul>
                </div>
            {% endif %}
            <div class="flex flex-wrap justify-between pt-3">
                <a href="{% url 'tracker:parcel-detail' move.id object.id %}" class="btn primary subtle">Cancel</a>
                <input type="submit" value="Submit" class="btn primary" />
            </div>
        </div>
    </form>
```

<br/>

## Installation and Usage 

### Installation

Because MoveMinder is a web application, you do not need to install it. You do have the **option** to install it, though, because it is a PWA.
1. Visit [MoveMinder](https://moveminder-tracker-f210fd4c1414.herokuapp.com/) in any modern web browser. Alternatively, to install the app and have it open directly to the Receiving page, visit [Receiving Page](https://moveminder-tracker-f210fd4c1414.herokuapp.com/parcels/receiving/).
2. Click the *Install* icon in the address bar. In Chrome, it looks something like this:

<br/>

![Install icon](./move_minder/static/images/install.png)

<br/>

### Usage

#### Getting Started

Click the `Get Started` button on the homepage to sign up for a user account.


## Learning Points 


This is a good place to Explain what you Learned by creating this application.
This is a great way to remind about all of the Complex Skills you now have.
If the user is less experienced than you:
They will be impressed by what you can do!

If the user is more experienced than you:
They will be impressed by what you can do!

Remember, it is easy to forget exactly how Valuable and Impressive your skills are, as well as How Much You’ve Learned!
So quantify that here!


## Author Info

### Ryan Moscoe 

* [Portfolio](https://rmoscoe.github.io/my-portfolio/)
* [LinkedIn](https://www.linkedin.com/in/ryan-moscoe-8652973/)
* [Github](https://github.com/rmoscoe)

The user has looked through your whole README, and gotten familiar with your application. 
This is where you take credit, and make it easy for them to learn more about you!
Direct them to the following:
- Your GitHub Profile
- Your LinkedIn
- Your Portfolio Website
- And Anything Else You Want!

Give credit where credit is due! 

If you Pseudocode or Pair Program with someone else, give them kudos in your Contributors section!


## Credits

Starter code provided by Trilogy Education Services, LLC, a 2U, Inc. brand, in conjunction with the University of California, Berkeley.

List your collaborators, if any, with links to their GitHub profiles.

If you used any third-party assets that require attribution, list the creators with links to their primary web presence in this section.

If you followed tutorials, include links to those here as well.


## License

The last section of a good README is a license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, use [https://choosealicense.com/](https://choosealicense.com/)


---

🏆 The sections listed above are the minimum for a good README, but your project will ultimately determine the content of this document. You might also want to consider adding the following sections.

## Badges

![badmath](https://img.shields.io/github/languages/top/nielsenjared/badmath)

Badges aren't _necessary_, per se, but they demonstrate street cred. Badges let other developers know that you know what you're doing. Check out the badges hosted by [shields.io](https://shields.io/). You may not understand what they all represent now, but you will in time.

## Features

If your project has a lot of features, consider adding a heading called "Features" and listing them there.

## Contributing

If you created an application or package and would like other developers to contribute it, you will want to add guidelines for how to do so. The [Contributor Covenant](https://www.contributor-covenant.org/) is an industry standard, but you can always write your own.

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them.

---

© 2022 Trilogy Education Services, LLC, a 2U, Inc. brand. Confidential and Proprietary. All Rights Reserved.