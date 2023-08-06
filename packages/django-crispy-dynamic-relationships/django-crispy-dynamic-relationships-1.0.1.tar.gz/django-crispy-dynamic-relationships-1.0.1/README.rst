django-crispy-dynamic-relationships
===================================

Add dynamic one-to-many relationships to your crispy forms with easy model declaration. It handles saving, updating and deleting automatically.

Installation
---------------

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install django-crispy-dynamic-relationships


Edit your `settings.py` file to include `'django-crispy-dynamic-relationships'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django-crispy-dynamic-relationships',
    ]

Subclass ModelFormCrispy to build forms similar to ModelForm. Add an extra field for the one-to-many relationship. Multiple fields supported.

.. code-block:: python

    from django-crispy-dynamic-relationships.factory import ModelFormCrispy

    class Child1Form(ModelFormCrispy):
        class Meta:
            model = models.Child1
            fields ='__all__'

    class ParentForm(ModelFormCrispy):
        class Meta:
            model = models.Parent
            fields ='__all__'

        children = [Child1Form]

Instantiate Forms with the parent class (ParentForm in this example) and a model instance if updating. Then pass the instance to the view context.

.. code-block:: python

    from django_crispy_forms_dynamic.factory import Forms

    context['parent_instance'] = Forms(parent_class=ParentForm, parent_instance=parent_instance)


Load 'dynamic_modelform_tags' in your template and apply the filter to the parent_instance.


.. code-block:: html

    {% load dynamic_modelform_tags %}
    <form method="post">
        {% csrf_token %}
        {{ forms_factory|form_dynamic }}
        <button type="submit" id="id_submit">Submit</button>
    </form>

Finally, save your form by calling is_valid() and save() methods in your POST method of your view.

.. code-block:: python

    def post(self,request,pk=None):
        print(request.POST)
        try:
            parent_instance = Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            parent_instance = None
        factory= Forms(parent_class=ParentForm, parent_instance=parent_instance, form_data=request.POST)
        if factory.is_valid():
            factory.save()
            return redirect('success')

Docs & Source
-------------

* Source: https://github.com/angelgm/django-crispy-dynamic-relationships
* PyPI: https://pypi.org/project/django-crispy-dynamic-relationships
