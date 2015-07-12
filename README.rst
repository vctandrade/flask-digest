############
Flask Digest
############

|license| |pypi|

.. |license| image:: https://img.shields.io/pypi/l/Flask-Digest.svg?style=flat-square
      :target: https://github.com/vctandrade/flask-digest/blob/master/LICENSE.txt
.. |pypi| image:: https://img.shields.io/pypi/v/Flask-Digest.svg?style=flat-square
      :target: https://pypi.python.org/pypi/Flask-Digest

Flask Digest provides a RESTful way of authenticating users using a Flask application.
To achieve that, it uses the Digest Access Authentication protocol and most optional
features described in `RFC 2617`_.

In a simplified manner, Flask Digest allows you to make your resources available only
to those registered in your system, while taking care of security issues by following
well known protocols.

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

Responses
=========

**Unauthorized - 401**
   When the user provides an invalid combination of username/password, uses a
   ``nonce`` created for another IP or provides a wrong ``nc``, the server will
   deny access and return this.

**Challenge - 401**
   When the user does not provide an ``Authorization`` header or uses a stale ``nonce``,
   the server will request authentication through an ``WWW-Authenticate`` header, which
   includes everything he needs to provide a valid response.

**BadRequest - 400**
   If the user's ``Authorization`` header is missing a field, does not use the requested
   ``qop`` value or provides the wrong URI in the header, the server will deny access and
   return this.

Features
========

This implementation of the Digest Authentication scheme uses the **Quality of Protection (qop)**
optional feature. More specifically, it forces you to use the ``auth`` variation of it, since
it makes the protocol much more secure.

On top of that, it discards the ``nonce`` tokens after half an hour, automatically giving
another one to the user, and it makes sure those tokens are only used from the IP for whom
they were created.

Finally, it prevents you from storing the passwords in plaintext, offering instead an
already hashed form of it when you call the method marked by the ``register`` decorator.

The result is that, using Flask Digest, you'll be protected against the following attacks:

* **Replay**: the request is intercepted and reproduced in the future.
* **Reflection**: attacker repasses the server's challenge to the user.
* **Criptoanalysis**:

   * **Chosen plaintext**: malicious server chooses the ``nonce``.
   * **Precomputed dictionary**: precomputed version of the above.
   * **Batch brute force**: chosen plaintext on multiple users at once.

**Man-in-the-middle attacks**, ie. intercept and modify requests, are also prevented regarding
the request URIs, but until ``auth-int`` is implemented entity bodies CAN be modified.
So ``POST`` and ``PUT`` methods are still vunerable.

Recommendations
===============

Even thought Flask Digest doesn't allow you to store plaintext passwords, it's still a
good idea to encrypt the file in some way. Also, if maintaining multiple realms, make
sure their names differ, so that a security breach in one doesn't affect the other.

To avoid **online dictionary attacks**, ie. brute force using a list of common passwords,
do not permit your users to choose easy passwords. And to avoid **spoofing** tell them
not to trust any server whose ``qop`` value is not ``auth``.

What the future holds
=====================

* Logging of possible attacks
* Implementation of ``auth-int``
* Adition of ``Authentication-Info`` header
* Per user/resource authentication
* Support Werkzeug's ``views`` and ``blueprints``
