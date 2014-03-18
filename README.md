web2py-foundation5-package
==========================
This package applies to some standard elements of web2py the Zurb Foundation 5
theme.  
The current version covers: the auth navbar, the menus and SQLFORM  
Supported version of Zurb Foundation framework: 5.0.3+  
Working since Version 2.8.2-stable+timestamp.2013.12.17.16.49.17 of web2py  
Tested with python 2.7.6 and the following browsers:  
    - Chrome 31.0.1650.63  
    - Firefox 26.0  
    - Opera 12.16 Build 1860  
    - IE 10  
    - IE 9  

Zurb Foundation 5 doesn't support IE7 and IE8
(http://foundation.zurb.com/learn/faq.html)

##Package content and requirements  
The package includes:  
    - foundation5.py  
    - web2py-foundation5.css  
    - web2py-foundation5.js  
    - example of layout.html (inspired to web2py welcome application)  

The bundle doesn't include the framework files. You must download them from
http://foundation.zurb.com/

##Installation and usage
1. put the python module in "modules" folder of your w2p-app (you should restart web2py to load the module)
2. in "static" folder of your w2p-app put 'web2py-foundation5.css' in "css" sub-folder and 'web2py-foundation5.js' in the "js" folder
3. replace the 'layout.html' in views folder of your w2p-app with that found in this package
4. download and uncompress the framework files in the static folder of your w2p-app  
5. in a model add the following code lines:

  ```python
  # foundation5 theme for web2py  
    from gluon import current  
    current.auth = auth  
    import foundation5 as zf5  
  ```
6. code your views by using the foundation5 framework guidelines
 (see more at http://foundation.zurb.com/docs/)
7. call menu with "zf5.menu()" and auth_navbar with "zf5.navbar()", set the SQLFORM formstyle to "zf5.form()"

##Detailed istructions
###Auth navbar
The navbar is fully customizable: you can change the text and icon for auth items, add dividers and add your own items, set the order of the items to your need and taste.  
You can call it in your view or controller simply with:  
```python
zf5.navbar()
```
It's possible to dynamically add items passing to the function a list of tuples like the following:  
```python
['divider',('fi-star', 'Kitchen Sink', URL('kitchen_sink'))]
```
each tuple has 3 values: 1st is the icon class, 2nd is the text and 3d is the url. Instead a tuple you could use a string for rendering a simple text but the 'divider' word will render exactly a divider.  
###Menu navigation
If you want a response.menu navbar use in your view or controller:
```python
zf5.menu()
```
If instead you want a navbar with your custom items, you can pass a list (build like response.menu) as 'menu_list' argument:
```python
my_nav = [['Home', True, URL('index')],['Page', False, URL('link')]]
zf5.menu(menu_list=my_nav)
```
If you need to add Zurb Foundation 5 classes to the menu you can use the argument 'menu_class' of the function.  
###Forms
To render a SQLFORM as a Zurb Foundation 5 form you can set its formstyle argument to:
```python
zf5.form()
```
In this case the label will be over the input:  

    label |  
    input

For a label on the left side of the input line you can pass 'horizontal' or 'inline' as first argument.    
By
```python
zf5.form(layout='horizontal')
```
or  
```python
zf5.form(layout='inline')
```
we will have  

    label | input

In the 'inline' layout, unlike the 'horizontal' layout, the label will be vertically centered against the input.  
The second argument of the function is for the checkboxes and radio widgets styling (default is 'inline'):
```python
zf5.form(rc_mode='inline')

checkbox 1 | checkbox 2 | checkbox 3

zf5.form(rc_mode='stacked')

checkbox 1 |
checkbox 2 |
checkbox 3
```
for example:
```python
zf5.form('inline','stacked')
```
returns a form where the labels are inline with their control and the checkboxes/radioboxes widget has stacked inputs.  
Function's third argument is important to define the grid classes for the 'horizontal' and 'inline' forms. The default is 'medium-3' and it sets the label column width. The column width of the control is calculated by the function.  
To add buttons to the form in runtime, you should use the function:   
```python
zf5.add_button(form, value, url, _class)
```
The mandatory arguments of the above function are:  
- form (the form to which append the button)
- value (the button text)
- url (the action's url)

The last argument is optional. You might want to only set it if you need a different class than 'button small'.  
If you need to insert dynamically into the form an extra row, you should use:  
```python
zf5.build_row(id, label, control, comment, form, layout, rc_mode,
              horizontal_form_label_class)
```
The mandatory arguments of the above function are:  
- id (the row id)
- label (the row label)
- control (the row widget)
- comment (the row comment)

'layout', 'rc_mode' and horizontal_form_label_class arguments are optional.  
To apply the Zurb Foundation 5 formstyle to auth forms you should set:
```python
auth.settings.formstyle = zf5.form()
```
###Flash Message position
For default the flash message is positioned on the right. If you want to center it you can add the class 'centered' to the div.flash in the layout.html  
