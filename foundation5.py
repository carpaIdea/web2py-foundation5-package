#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Developed by Paolo Caruccio ( paolo.caruccio66@gmail.com )
Released under web2py license
version 1 rev.201403191600

Description
-----------
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

Package content and requirements
----------------------------------
The package includes:
    - foundation5.py
    - web2py-foundation5.css
    - web2py-foundation5.js
    - example of layout.html (inspired to web2py welcome application)

The bundle doesn't include the framework files. You must download them from
http://foundation.zurb.com/

Installation and usage
------------------------
1. put the python module in "modules" folder of your w2p-app (you should
   restart web2py to load the module)
2. in "static" folder of your w2p-app put 'web2py-foundation5.css' in "css"
   sub-folder and 'web2py-foundation5.js' in the "js" folder
3. replace the 'layout.html' in views folder of your w2p-app with that found in
   this package
4. download and uncompress the framework files in the static folder of your
   w2p-app
5. in a model add the following code lines:

    # foundation5 theme for web2py
    from gluon import current
    current.auth = auth
    import foundation5 as zf5

6. code your views by using the foundation5 framework guidelines
   (see more at http://foundation.zurb.com/docs/)
7. call menu with "zf5.menu()" and auth_navbar with "zf5.navbar()", set the
   SQLFORM formstyle to "zf5.form()"

Auth navbar
-------------
The navbar is fully customizable: you can change the text and icon for auth
items, add dividers and add your own items, set the order of the items
to your need and taste.
You can call it in your view or controller simply with:

                           zf5.navbar()

It's possible to dynamically add items passing to the function a list of tuples
like the following:

        ['divider',('fi-star', 'Kitchen Sink', URL('kitchen_sink'))]

each tuple has 3 values: 1st is the icon class, 2nd is the text and 3d is the
url. Instead a tuple you could use a string for rendering a simple text but the
'divider' word will render exactly a divider.

Menu navigation
---------------
If you want a response.menu navbar use in your view or controller:

                            zf5.menu()

If instead you want a navbar with your custom items, you can pass a list (build
like response.menu) as 'menu_list' argument:

      my_nav = [['Home', True, URL('index')],['Page', False, URL('link')]]
      zf5.menu(menu_list=my_nav)

If you need to add Zurb Foundation 5 classes to the menu you can use the
argument 'menu_class' of the function.

Forms
-----
To render a SQLFORM as a Zurb Foundation 5 form you can set its formstyle
argument to:

                            zf5.form()

In this case the label will be over the input:

                            label |
                            input

For a label on the left side of the input line you can pass 'horizontal' or
'inline' as first argument.

        zf5.form(layout='horizontal') or zf5.form(layout='inline')

                         label | input

In the 'inline' layout, unlike the 'horizontal' layout, the label will be
vertically centered against the input.

The second argument of the function is for the styling checkboxes and radio
widgets (default is 'inline'):

                  zf5.form(rc_mode='inline')

           checkbox 1 | checkbox 2 | checkbox 3

                  zf5.form(rc_mode='stacked')

                       checkbox 1 |
                       checkbox 2 |
                       checkbox 3

for example:

                zf5.form('inline','stacked')

returns a form where the labels are inline with their control and the
checkboxes/radioboxes widget has stacked inputs.
Function's third argument is important to define the grid classes for the
'horizontal' and 'inline' forms. The default is 'medium-3' and it sets the
label column width. The column width of the control is calculated by the
function.
To add buttons to the form in runtime, you should use the function:

                  zf5.add_button(form, value, url, _class)

The mandatory arguments of the above function are:
    - form (the form to which append the button)
    - value (the button text)
    - url (the action's url)

The last argument is optional. You might want to only set it if you need a
different class than 'button small'.
If you need to insert dynamically into the form an extra row, you should use:

      zf5.build_row(id, label, control, comment, form, layout, rc_mode,
                    horizontal_form_label_class)

The mandatory arguments of the above function are:
    - id (the row id)
    - label (the row label)
    - control (the row widget)
    - comment (the row comment)

'layout', 'rc_mode' and horizontal_form_label_class arguments are optional.

To apply the Zurb Foundation 5 formstyle to auth forms you should set:

            auth.settings.formstyle = zf5.form()

Flash Message position
----------------------
For default the flash message is positioned on the right. If you want to center
it you can add the class 'centered' to the div.flash in the layout.html

License
-------
foundation5.py is released under web2py license
(http://www.web2py.com/init/default/license), while
web2py-foundation5.css and web2py-foundation5.js are released under the MIT
license (a copy is included in the package).

Acknowledgements
----------------
I wish to thank the following people for their suggestions and bug fixes:
Annet Vermeer for the flash message position fix
Dmitry Rodetsky for the implementation of reCaptcha

"""

from gluon import *
from gluon.languages import lazyT
from numbers import Number
from gluon.tools import Recaptcha


def navbar(additional_items=None, dropdown_class='dropdown',
           toggle_class=None):
    ''' full customizable auth navbar
    '''
    bar = current.auth.navbar(mode='bare')
    [li_login, li_register, li_request_reset_password, li_retrieve_username,
     li_logout, li_profile, li_change_password] = [None for n in xrange(7)]
    # text and icons for auth items in the drop-down
    ## text for dropdown toggle
    default_text = current.T('Login')
    ## login
    ico_login = "fi-power"
    txt_login = current.T('Login')
    ## register
    ico_register = "fi-torso"
    txt_register = current.T('Register')
    ## password reset
    ico_request_reset_password = "fi-lock"
    txt_request_reset_password = current.T('Lost password?')
    ## username retrieve
    ico_retrieve_username = "fi-lock"
    txt_retrieve_username = current.T('Forgot username?')
    ## logout
    ico_logout = "fi-power"
    txt_logout = current.T('Logout')
    ## profile
    ico_profile = "fi-torso"
    txt_profile = current.T('Profile')
    ## password change
    ico_change_password = "fi-lock"
    txt_change_password = current.T('Password')
    # divider
    li_divider = LI(_class='divider')
    # not auth items (add your own)
    ## below some examples
    ico0 = "fi-info"
    txt0 = current.T('About')
    href0 = URL(current.request.controller, 'about')
    li_about = LI(A(I(_class=ico0), ' ', txt0, _href=href0, _rel="nofollow"))
    ## ----------------
    ico1 = "fi-book"
    txt1 = current.T('Help')
    href1 = URL(current.request.controller, 'help')
    li_help = LI(A(I(_class=ico1), ' ', txt1, _href=href1, _rel="nofollow"))
    ## items added dynamically
    dynamic_items = []
    if additional_items and isinstance(additional_items, list):
        for item in additional_items:
            if not item:
                item = 'divider'
            if isinstance(item, (list, tuple)):
                aiico = item[0]
                aitxt = item[1]
                aihref = item[2]
                dynamic_items.append(LI(A(I(_class=aiico), ' ', aitxt,
                                        _href=aihref, _rel="nofollow")))
            elif isinstance(item, basestring):
                dynamic_items.append(item if item != 'divider' else li_divider)
            else:
                pass
    # auth items builder
    for k, v in bar.iteritems():
        if k == 'user':
            welcome_text = "%s %s" % (bar['prefix'], bar['user'])
            toggletext = default_text if v is None else welcome_text
        elif k == 'login':
            ico = ico_login
            txt = txt_login
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_login = res
        elif k == 'register':
            ico = ico_register
            txt = txt_register
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_register = res
        elif k == 'request_reset_password':
            ico = ico_request_reset_password
            txt = txt_request_reset_password
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_request_reset_password = res
        elif k == 'retrieve_username':
            ico = ico_retrieve_username
            txt = txt_retrieve_username
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_retrieve_username = res
        elif k == 'logout':
            ico = ico_logout
            txt = txt_logout
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_logout = res
        elif k == 'profile':
            ico = ico_profile
            txt = txt_profile
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_profile = res
        elif k == 'change_password':
            ico = ico_change_password
            txt = txt_change_password
            res = LI(A(I(_class=ico), ' ', txt, _href=v, _rel="nofollow"))
            li_change_password = res
    # dropdown toggle
    tc = "has-dropdown %s" % (toggle_class) if toggle_class else "has-dropdown"
    toggle = A(toggletext,
               _href="#",
               _class=tc,
               _rel="nofollow",
               data=dict(dropdown="w2p-auth-bar"))
    # set the order of items in the drop-down and add dividers
    ul = [li_register,
          li_profile,
          li_request_reset_password,
          li_change_password,
          li_retrieve_username,
          li_divider,
          li_login,
          li_logout,
          li_divider,
          li_about,
          li_help
          ]
    if dynamic_items:
        for di in dynamic_items:
            ul.append(di)
    # dropdown
    dropdown = UL(*[li for li in ul if li is not None],
                  _class=dropdown_class, _id='w2p-auth-bar',
                  **{'_data-dropdown-content': ''})
    # navbar
    navbar = LI(toggle, dropdown, _class="has-dropdown",
                **{'_data-w2pmenulevel': 'l0'})
    return navbar


def menu(menu_class='left', menu_list=None, menu_id=None):
    current_menu = current.response.menu if not menu_list else menu_list
    menu = MENU(current_menu,
                _class=menu_class,
                _id=menu_id,
                li_class='has-dropdown not-click',
                ul_class='dropdown')
    return menu


def add_button(form, value, url, _class='button small'):
    ''' add buttons to the zf5 form
        This function overrides that one in gluon/html.py
    '''
    REDIRECT_JS = 'window.location="%s";return false'
    submit = form.element(_type='submit')
    submit.parent.append(
        CAT(TAG['button'](value, _class=_class, _type='button',
                          _onclick=url if url.startswith('javascript:') else
                          REDIRECT_JS % url), XML('&nbsp;')))


def build_row(id, label, control, comment, form,
              layout=None, rc_mode='inline',
              horizontal_form_label_class='medium-3'):
    ''' form row builder
    '''
    fh_label_class = horizontal_form_label_class
    fh_label_class_prefix, fh_label_class_columns = (fh_label_class.split('-'))
    fh_offest_class = '%s-offset-%s' % (fh_label_class_prefix,
                                        fh_label_class_columns)
    fh_control_class = '%s-%s' % (fh_label_class_prefix,
                                  12-int(fh_label_class_columns))
    if not id.startswith('submit_record'):  # form controls
        if isinstance(label, (basestring, lazyT)):  # string label
            clabel = LABEL(label)
            if not label and layout != 'horizontal':
                clabel = CAT('')
            label = clabel
        if control is None:  # make the control as an empty string
            control = ''
        if isinstance(control, (basestring, lazyT)):  # text control (string)
            control = P(control, _class='form-control-static')
        elif isinstance(control, Number):  # text control (number)
            control = P(str(control), _class='form-control-static')
        elif isinstance(control, INPUT):  # widget
            ctrl_cls = None
            control_type = control.attributes.get('_type')
            if control_type not in ('checkbox', 'radio', 'file'):
                ctrl_cls = 'form-control'
                if isinstance(control, TEXTAREA):  # textarea
                    control['_rows'] = '3'
            elif control_type == 'file':  # file input
                if layout == 'inline':
                    ctrl_cls = 'form-control-static'
            elif control_type in ('checkbox', 'radio'):  # checkbox/radio input
                if form.readonly:
                    control['_disabled'] = 'disabled'
                clabel = label[0]
                label = LABEL('') if layout == 'horizontal' else CAT('')
                control = CAT(control, LABEL(clabel, _for=control['_id'],
                                             data=dict(w2p_form_element="rc")))
            if ctrl_cls:
                control.add_class(ctrl_cls)
        elif isinstance(control, SPAN):  # static text
            control = P(control[0])
            control.add_class('form-control-static')
        elif isinstance(control, A):  # link
            if layout == 'horizontal':
                label = LABEL(label)
            control.add_class('button secondary tiny')
            control['_role'] = 'button'
        elif isinstance(control, Recaptcha):
            # print out ReCaptcha as is
            control = XML(control, sanitize=False)
        elif (isinstance(control[0], UL)   # listwidget
              and control[0]['_class'] == 'w2p_list'):
            control = control[0]
            for c in control:
                if isinstance(c[0], INPUT):
                    c[0].add_class('form-control')
            control.add_class('no-bullet')
        elif (isinstance(control[0], INPUT)  # autocompletewidget
              and control[0]['_autocomplete'] == 'off'
              and control[-1]['_id'].startswith('_autocomplete_')):
            control[0].add_class('form-control')
            control = P(control, _class='w2p-autocomplete-widget')
        elif (isinstance(control,  # radiowidget/checkboxeswidget
                        (TABLE, DIV)) and
              control.attributes.get('_class') and
             ('web2py_radiowidget' in control['_class'] or
              'web2py_checkboxeswidget' in control['_class'])):
            labels = [l for l in control.elements('label')]
            mode = rc_mode if rc_mode == 'stacked' else 'inline'
            group = []
            for n, input in enumerate(control.elements('input')):
                itype = input.attributes.get('_type')
                if itype in ('checkbox', 'radio'):
                    if form.readonly:
                        input['_disabled'] = 'disabled'
                    rc_data = dict(w2p_form_element="rc")
                    if mode == 'inline':
                        group_element = CAT(input,
                                            LABEL(labels[n][0],
                                                  _for=input['_id'],
                                                  data=rc_data))
                    else:
                        group_element = LI(input,
                                           LABEL(labels[n][0],
                                                 _for=input['_id'],
                                                 data=rc_data),
                                           _class="rc-stacked")
                else:
                    group_element = input
                group.append(group_element)
            control = (UL(*group, _class='rc_container no-bullet')
                       if mode != 'inline'
                       else CAT(DIV(*group, _class='rc_container')))
        elif (isinstance(control, DIV) and  # UploadWidget
              isinstance(control[0], INPUT) and
              '_type' in control[0].attributes and
              control[0]['_type'] == 'file' and
              isinstance(control[1], SPAN) and
              isinstance(control[1][1], A)):
            file_inp = control[0]
            file_inp['_style'] = 'display:none;'
            file_link = control[1][1]
            delete_box = False
            has_image = False
            if control[1][2] == '|':
                delete_box = True
                del_inp = control[1][3]
                del_inp['_style'] = 'opacity:0;'
                delete_lbl = control[1][4]
            if isinstance(control[-1], IMG):
                has_image = True
                image_preview = control[-1]
            if has_image:
                file_repr = IMG(_src=image_preview['_src'],
                                _alt='thumbnail',
                                _id='image-thumb',
                                _class='th')
            else:
                file_repr = SPAN(file_link[0])
            file_link = CAT(A(file_repr,
                              _href=file_link['_href'],
                              _class='w2p-file-preview'),
                            SPAN(current.T('no file'),
                                 _id='no-file',
                                 _style='display:none;'))
            edit_btn_class = 'button secondary tiny dropdown'
            edit_btn = TAG['button'](current.T('edit'),
                                     _type='button',
                                     _class=edit_btn_class,
                                     **{'_data-dropdown': 'drop'})
            drop_down = UL(LI(A(current.T(delete_lbl[0]),
                                _href='#',
                                _id='delete-file-option')),
                           LI(A(current.T('change'),
                                _href='#',
                                _id='change-file-option')),
                           _class='f-dropdown',
                           _role='menu',
                           _id="drop")
            edit_btn_dd = SPAN(edit_btn,
                               drop_down,
                               _id='edit-btn-dd',
                               _class='btn-group')
            file_reset_btn = TAG['button'](current.T('reset'),
                                           _id='file-reset-btn',
                                           _type='button',
                                           _class='button secondary tiny',
                                           _style='display:none;')
            control = CAT(DIV(file_inp,
                              file_link,
                              del_inp,
                              edit_btn_dd,
                              file_reset_btn,
                              _class='w2p-uploaded-file'))
        else:  # widget not implemented
            print "row '%s': widget not implemented" % id
        if comment:  # comment
            comment = SPAN(comment, _class='comment')
            control.add_class("has-comment")
        if layout == 'horizontal':  # control for horizontal form
            label.add_class('right')
            label = DIV(label, _class='%s columns' % fh_label_class)
            control = DIV(CAT(control, comment or ''),
                          _class='%s columns' % fh_control_class)
            comment = ''
        elif layout == 'inline':  # control for inline form
            label.add_class('right inline')
            label = DIV(label, _class='%s columns' % fh_label_class)
            control = DIV(CAT(control, comment or ''),
                          _class='%s columns' % fh_control_class)
            comment = ''
        else:
            pass
        form_row = DIV(label, control, comment, _id=id, _class='row')
    else:  # form buttons
        if not len(control):
            # if the buttons are not wrapped in a DIV
            # then we have to wrap them
            control = CAT(control)
        inputs = []
        first_btn = True
        for n, input in enumerate(control):
            btn_class = 'small' if first_btn else 'secondary small'
            input_type = input.attributes.get('_type')
            if isinstance(input, INPUT):  # input tag
                if input_type in('button', 'submit', 'reset'):
                    first_btn = False
                    btn_id = input.attributes.get('_id')
                    js_click = input.attributes.get('_onclick')
                    input.add_class('zf5-form-btn button %s' % btn_class)
                    button = TAG['button'](input['_value'],
                                           _type=input_type,
                                           _onclick=js_click,
                                           _class=input['_class'],
                                           _id=btn_id)
                elif input_type == 'image':
                    first_btn = False
                    input.add_class('zf5-form-btn btn %s' % btn_class)
                    button = input
                else:  # it isn't a button
                    input.add_class('form-control')
                    button = input
            elif input_type in ('button', 'submit', 'reset'):  # 'button' tag
                first_btn = False
                input.add_class('zf5-form-btn btn %s' % btn_class)
                button = input
            elif isinstance(input, A):  # anchor tag as a button
                first_btn = False
                input.add_class('zf5-form-btn btn %s' % btn_class)
                input['_role'] = 'button'
                button = input
            else:
                button = input
            inputs.extend([button, XML('&nbsp;')])
        buttons = (CAT(*inputs)
                   if layout not in ['horizontal', 'inline']
                   else DIV(CAT(*inputs),
                            _class='%s %s columns' % (fh_control_class,
                                                      fh_offest_class)))
        form_row = DIV(buttons, _class='row', _id=id)
    return form_row


def form(layout=None, rc_mode='inline',
         horizontal_form_label_class='medium-3'):
    ''' formstyle for SQLFORM
    '''
    def style(form, fields):
        parent = CAT()
        form_group = None
        for id, label, widget, comment in fields:
            form_group = build_row(id, label, widget, comment,
                                   form, layout, rc_mode,
                                   horizontal_form_label_class)
            parent.append(form_group)
        form_classes = ('zf5-form form-%s' % layout if layout in ('horizontal',
                                                                  'inline')
                        else 'zf5-form')
        form.add_class(form_classes)
        form['_role'] = 'form'
        if layout in ('horizontal', 'inline'):
            form['_data-form-label-class'] = horizontal_form_label_class
        return parent
    return style
