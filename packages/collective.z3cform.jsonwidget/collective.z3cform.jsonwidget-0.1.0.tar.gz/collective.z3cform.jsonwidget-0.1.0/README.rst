.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=============================
collective.z3cform.jsonwidget
=============================

z3c.form widget to manage a json field.

Features
--------

- Customizable schema

Usage
-----

You need to set the widget to needed fields into your form instance::

    from collective.z3cform.jsonwidget.browser.widget import JSONFieldWidget
    from zope.interface import Interface
    from zope import schema


    class IMyJsonSchema(Interface):
        first = schema.TextLine(
            title='first field',
            required=True,
        )
        second = schema.List(
            title="second field",
            required=False,
            value_type=schema.TextLine(),
        )

    class IFormSchema(Interface):
        my_json_field = schema.SourceText(
            title="The field with some stored json values"
        )

    class MyForm(Form):

        ...
        schema = IFormSchema
        fields = field.Fields(IFormSchema)
        fields["my_json_field"].widgetFactory = JSONFieldWidget

        def updateWidgets(self):
            """
            """
            super(MyForm, self).updateWidgets()
            self.widgets["my_json_field"].schema = IMyJsonSchema


With this configuration, we are setting **JSONFieldWidget** widget to **my_json_field** field and
setting the fields schema defined in **IMyJsonSchema** interface.

In the field are stored a list of json objects where each object has a set of fields defined in the schema.

For example for the given configuration, we are going to store into the field something like::

    [
        {
            "first": "a string",
            "second": [1,2,3,4]
        },
        {
            "first": "another string",
            "second": ["a", "b", "c"]
        },
    ]


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install collective.z3cform.jsonwidget by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.z3cform.jsonwidget


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.z3cform.jsonwidget/issues
- Source Code: https://github.com/collective/collective.z3cform.jsonwidget


Credits
-------

Developed with the support of `Regione Emilia Romagna`__;

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
-------

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
