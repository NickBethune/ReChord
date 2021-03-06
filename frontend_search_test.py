from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from search import prepare_tree, search, find_artic,get_measure
from lxml import etree

"""Turn user submitted MEI code snippet into xml file."""
def transform_xml(xml_code):
    xml = xml_code.encode()
    f = open('upload.xml', 'wb')
    f.write(xml)
    f.close()

"""Create the Flask app"""
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'r62h49vhjaqfr1280ejgqajfkdtf271sdaqwefasdgfda'

"""Construct the submission box and taxonomies"""
class SnipUpload(Form):
    name = TextField('Submit your MEI Code Snippets:', validators=[validators.required()])


"""Snippet submission"""
@app.route("/", methods=['GET', 'POST'])
def code_submit():
    form = SnipUpload(request.form)

    if request.method == 'POST':
        name = request.form['name']

        if form.validate():
            # Save the comment here.
            flash('Your snippet is submitted successfully')
            transform_xml(name)
            flash('Your input snippet:')
            flash(name)

            tree, root = prepare_tree('database/Chopin.xml')
            inputXML = etree.parse('upload.xml')
            input_root = inputXML.getroot()

            # print a list of matches to testinput.XML from Chopin.XML
            flash(search(input_root, tree))

            # get a list of artic element that has a staccato articulation
            element_artic_list = find_artic(tree, 'stacc')
            # print("-" * 10, "artic elements that has a staccato articulation", "-" * 10)

            for element in element_artic_list:
                flash('Element address:')
                flash(element)
                flash("is in measure:")
                flash(get_measure(element))
                flash('-------------------------------------')


        else:
            flash('All the form fields are required. ')

    return render_template('frontend_search_test.html', form=form)


if __name__ == "__main__":
    app.run()