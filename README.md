Flask-MsTranslate

=================

Flask extension to use with microsoft translate service.

Works as follows:
1. Register extension with the app
2. Use it either in template or in the view


in your config file you should add 2 variables:
MS_TRANSLATE_ID = 'yourApplicationId'
MS_TRANSLATE_SECRET = 'yourSecretKey'

The values for this 2 variables taken from azur marketplace as described here:
http://msdn.microsoft.com/en-us/library/hh454950.aspx

app.py:
```python
from flask import Flask, render_template
from flask.ext.mstrans import MsTranslate

app = Flask(__name__)
trans = MsTranslate(app)

@app.route('/translate_filter')
def index():
    return render_template('filter.html')

@app.route('/translate_in_view')
def translate():
    return render_template('translate.html', text=trans.translate('Hello World', 'ru')
```

filter.html:
```html
{{ 'Hello World'|translate('ru') }}
```

translate.html:
```html
{{ text }}
```

MsTranslate().translate(text, destLang='en', sourceLang='')

destLang defaults to 'en' 

sourceLang is empty by default and will try to guess language from the text

MsTranslate have translate_array method which recieving and array instead of text. All texts in array must be same language

