from wtforms import TextField, Form


class SearchForm(Form):
    search_autocomplete = TextField("Enter movie", id="autocomplete")
