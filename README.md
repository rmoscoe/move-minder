# MoveMinder

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Technology Used](#technology-used)
  - [Badges](#badges)
- [Description](#description)
- [Code Example](#code-example)
- [Installation and Usage](#installation-and-usage)
  - [Installation](#installation)
  - [Usage](#usage)
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

![Static Badge](https://img.shields.io/badge/JavaScript-75.3%25-%23eddc1c) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/CSS-8.0%25-%23395ded) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/HTML-1.7%25-%23db441f) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/Python-0.9%25-%234584b6) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/Other-0.7%25-lightgray)

<br/>

## Description 

[Visit the Deployed Site](https://moveminder-tracker-f210fd4c1414.herokuapp.com/)

MoveMinder lets you track the contents and status of every box, appliance, and piece of furniture throughout a move. Create a record for each move with the date(s), origin address, and destination address. Add a record for each parcel, including its type, contents, and weight, as well as the room in which it belongs at its destination. Print labels with a QR code for each parcel, and scan the QR code to update the parcel's status. MoveMinder is a Progressive Web App (PWA), so you can install it on your mobile device, making it easy to use your mobile device as a scanner.

<br/>

![Site Langing Page](./move_minder/static/images/home-light.png)

<br/>

I had been sitting on the idea for this project for some time, until I found myself at a point where I needed to create a project as a way to learn Django's generic views and the Django Template Language. I chose to create this application specifically because it lent itself well to the list, detail, create, update, and delete structure of Django's generic views.

<br/>

## Code Example

What are the steps required to install your project? Provide a step-by-step description of how to get the development environment running.


```html
<div class="header">
        <h1>Hori<span class="seo">seo</span>n</h1>
        <div>
            <ul>
                <li>
                    <a href="#search-engine-optimization">Search Engine Optimization</a>
                </li>
                <li>
                    <a href="#online-reputation-management">Online Reputation Management</a>
                </li>
                <li>
                    <a href="#social-media-marketing">Social Media Marketing</a>
                </li>
            </ul>
        </div>
    </div>
```

Converting the above non-semantic div with the class of 'header' to an appropriate [<header> semantic element](https://www.w3schools.com/html/html5_semantic_elements.asp). 

```html
<header>
        <h1>Hori<span class="seo">seo</span>n</h1>
        <nav>
            <ul>
                <li>
                    <a href="#search-engine-optimization">Search Engine Optimization</a>
                </li>
                <li>
                    <a href="#online-reputation-management">Online Reputation Management</a>
                </li>
                <li>
                    <a href="#social-media-marketing">Social Media Marketing</a>
                </li>
            </ul>
        </nav>
    </header>

```

This change require some additional modification to the CSS selector: 

```css
.header {
    padding: 20px;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    background-color: #2a607c;
    color: #ffffff;
}
```

No longer targeting the element on the page with the class of 'header' but instead the css selector targeting the 'header' element 

```css
header {
    padding: 20px;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    background-color: #2a607c;
    color: #ffffff;
}

```

## Installation and Usage 

### Installation

Provide instructions and examples for use. Include screenshots as needed. 

### Usage

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

```md
![alt text](assets/images/screenshot.png)
```


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