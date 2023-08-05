collective.pfg.signup
=====================

|CI| |Coverage|

|Workflows|

.. |CI| image:: https://github.com/collective/collective.pfg.signup/workflows/CI/badge.svg
.. |Coverage| image:: https://coveralls.io/repos/github/collective/collective.pfg.signup/badge.svg?branch=master
   :target: https://coveralls.io/github/collective/collective.pfg.signup
.. |Workflows| image:: http://github-actions.40ants.com/collective/collective.pfg.signup/matrix.svg
   :target: https://github.com/collective/collective.pfg.signup/actions

.. contents::

Introduction
------------

Flexible member registration, membership workflow and membership management in Plone.

Features:

- Customisable user registration forms (via PloneFormGen);
- different registration forms for certain areas of the site;
- user approval workflow and user management based on groups;
- collecting additional information about members.

This plugin provides a PloneFormGen save adapter that uses the details from the 
submitted form to add Plone members.

It can be configured to:

- put the user in a predefined group, and
- allow members of a group to approve users before they are added. 
- The destination group or the group of approvers can be predefined, or
- polcies of groups based on naming conventions by using python expressions

Use Cases
------------

There are 3 use cases for adding users:

- User is automatically created with the password supplied in the form.
- User is created, password is randomly generated, and a password reset email is sent.
- User is held within the adaptor, pending approval.


Destination group
~~~~~~~~~~~~~~~~~


Once someone is signed up, they are added to a *destination group*.
The id of the destination group is determined by the **destination group id template**
in your signup adapter.

If you enter `Members` into the **destination group id template** field, all
users will be added to the `Members` group.

Dynamic Destination Group
~~~~~~~~~~~~~~~~~~~~~~~~~

You can vary the group that a user gets added to by using variable substitution
in your **destination group id template** TAL expression.

For example, if you 
- create a registration form 
- with a selection box called **organisation** 
- with the values `IBM`, `APPLE`, `GOOGLE`, 
- configure the adapter **destination group id template** to ```Members_${organisation}```
- Users will be added to `Members_APPLE`, `Members_IBM`, `Members_GOOGLE` based on the registration form

The substitutions need to correspond to fields on your registration form
and the groups need to exist

If the group doesn't exist the registrations will be held
for approval and an error email sent to the portal administrator.

Registration Approval Workflow
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

To hold registrations temporarily before the user accounts are added you can set a 
**Approval Group** on your adapter. This specifies the policy on which group manages 
users being added to another group.

**Approval Group** is a python expression returning a dict of ```python:{manager_group: [group1, group2, ...]}```

- Create a registration form
- Set adapter **Approval Group** to ```python:{'Administrators': ['*']}```
- Upon registration the user is emailed to say their registration is pending approval
- and email of the group is sent an email to notify that a registration needs to approved
    - if the group has no email, every memeber of group will be notified
- Someone from the adminstrators group can login, view a list of waiting registrations
- Once approved they are able to be edited or deactivated by the manager

Note if the approval group doesn't exist then email will be sent to the portal administrator instead.

Post approval actions
~~~~~~~~~~~~~~~~~~~~~

If you want to store the information entered into a signup form,
or take any other actions based on this information,
you can configure an additional PFG save action adapter.
Instead of directly activating that on the form, 
configure it as the **approved save action adapter** in the signup adapter
and this adapter will be activated only once the user has finally been approved.
You can use this with a scriptable adapter for example to do scriptable actions
on user approval.

Membership management view
~~~~~~~~~~~~~~~~~~~~~~~~~~

This plugin adds the `@@user_search_view` browser view, which improves upon the 
default Plone **Users and Groups** settings page for member management.

User profile pages are filtered by the **Manage Group Template** field.
Members have the fields **Access approved by**, **Access approved
date**, **Access last updated by** and **Access last updated date** to have a
record of membership management actions.

There are **activate** and **deactivate** buttons to disable user for accessing
the site.
