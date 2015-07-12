############
Flask Digest
############

Flask Digest provides a RESTful way of authenticating users using a Flask application.
To achieve that, it uses the Digest Access Authentication protocol described in `RFC 2617`_.

.. _RFC 2617: https://www.ietf.org/rfc/rfc2617.txt

Quickstart
==========

This module is implementation independent from how the user database is handled and
accessed. So the first thing you need to do is set it up. Then, you need to create
the ``Stomach`` object and inform it of how to use the database you created.
The only thing left now is to decide which resources should be protected.

All the steps regarding the ``Stomach`` object are done with the use of three
decorator methods, similar to the ones used by Flask. Those are exemplified bellow,
where ``myRealm`` is a string of your choosing, used to describe the server:

.. code-block:: python

   from flask import Flask
   from flask_digest import Stomach

   app = Flask(__name__)
   stomach = Stomach('myRealm')

   db = dict()

   @stomach.register
   def add_user(username, password):
       db[username] = password

   @stomach.access
   def get_user(username):
       return db.get(username, None)

   @app.route('/')
   @stomach.protect
   def main():
       return '<h1> resource <h1>'

   add_user('admin', '12345')
   app.run()

Keep in mind that the ``protect`` decorator MUST be located after ``route``.

Also, the method for registering new users is expected to receive a username
as first parameter and a password as second. Other parameters are allowed as well.

As for the database access method, it should only have the username as required
parameter, while returning the stored password or ``None`` if the username was
not registered.
