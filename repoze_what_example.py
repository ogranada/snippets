# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from functools import wraps

from werkzeug import (Response, Request, ClosingIterator, Template,
                      Local, LocalManager, script, redirect, Href)
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, Forbidden, Unauthorized
from repoze.what.plugins.quickstart import setup_sql_auth

from sqlalchemy import (MetaData, create_engine, Table, Column, Integer,
                        String, ForeignKey)
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base
from repoze.what.predicates import (NotAuthorizedError, not_anonymous,
                                    has_permission)


# sqlalchemy classes and instances
metadata = MetaData()
# a in-memory database for users
engine = create_engine('sqlite:///database.db')
session = scoped_session(sessionmaker(bind=engine))

# base class for models
ModelBase = declarative_base(metadata=metadata)


class User(ModelBase):
    """
    This class represents a single user.
    """
    # the primary key
    id = Column(Integer, primary_key=True)
    # the user name
    user_name = Column(String(100), index=True, nullable=False, unique=True)
    # the password.  Real world applications should use a safe hashing
    # algorithm like PBKDF2 to store password in hashed form only.
    password = Column(String(100))

    __tablename__ = 'users'

    def __init__(self, user_name, password=None):
        self.user_name = user_name
        self.password = password

    def validate_password(self, password):
        """
        Validates the given ``password`` and returns ``True``, if it matches
        :attr:`password`.
        """
        return self.password and self.password == password


class Permission(ModelBase):
    """
    Represents a single permission.
    """
    # the primary key
    id = Column(Integer, primary_key=True)
    # the permission name
    permission_name = Column(String(100), index=True, nullable=False, unique=True)

    __tablename__ = 'permissions'

    def __init__(self, permission_name):
        self.permission_name = permission_name


class Group(ModelBase):
    """
    Represents a group.
    """
    # the primary key
    id = Column(Integer, primary_key=True)
    # the group name
    group_name = Column(String(100), index=True, nullable=False, unique=True)

    __tablename__ = 'groups'

    def __init__(self, group_name):
        self.group_name = group_name


# helper tables for many-to-many relations
user_groups = Table('user_groups', metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('group_id', Integer, ForeignKey('groups.id')))

group_permissions = Table('group_permissions', metadata,
                          Column('group_id', Integer, ForeignKey('groups.id')),
                          Column('permission_id', Integer, ForeignKey('permissions.id')))

# relation attributes for users and groups
User.groups = relation(Group, secondary=user_groups, backref='users')
Group.permissions = relation(Permission, secondary=group_permissions, backref='groups')

# # create all tables
metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)

# create a permission, two users and a group
def _setup_users():
    admin = User('admin', 'password')
    user = User('user', 'password')
    administer = Permission('administer')
    admins = Group('admins')
    session.add(admin)
    session.add(user)
    session.add(admins)
    session.add(administer)
    admin.groups.append(admins)
    admins.permissions.append(administer)
    session.commit()
_setup_users()


# context-local objects
local = Local()
local_manager = LocalManager()
# a global request binding
request = local('request')
# the url routing map
url_map = Map([
    Rule('/dologin', endpoint='dologin', build_only=True),
    Rule('/logout', endpoint='logout', build_only=True)])


# the templates (using werkzeug minitemplates)
# provides the document outline
document = Template(u"""\
<html>
  <head>
    <title>${title}</title>
  </head>
  <body>
    <h1>${title}</h1>
    <div>
      ${body}
    </div>
  </body>
</html>""")

# provides the login form
login_form = Template(u"""\
<strong>Please log in.</strong>
<p>
  Two users are available, "admin" and "user".  The latter has no permissions.
  Use "password" as password ;)
</p>
<form action="${login_url}" method="post">
<table>
  <tr>
    <td><label for="login">Username: </label></td>
    <td><input id="login" name="login" type="text" /></td>
  </tr>
  <tr>
    <td><label for="password">Password: </label></td>
    <td><input id="password" name="password" type="password" /></td>
  </tr>
</table>
<input id="login_submit" name="submit" type="submit" value="Login" />
</form>""")

# provides the index site
index_document = Template(u"""\
<ul>
  <li><a href="${permission_url}">This link requires a permission</a></li>
  <li><a href="${logged_in_url}">This link requires a login</a></li>
  <% if logged_in %>
  <li><a href="${logout_url}">Logout!</a></li>
  <% else %>
  <li><a href="${login_url}">Login!</a></li>
  <% endif %>
</ul>""")


def expose(rule, **kw):
    """
    Exposes the decorated function through the given ``rule`` in the url
    mal.  Shamelessly stolen from werkzeug tutorial ;)
    """
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate


def protect(predicate):
    """
    Protects the decorated function with the given ``predicate``.  If the
    predicate isn't met, a :exc:`Forbidden` error is raised, if the user is
    authenticated (but obviously not authorized), otherwise a
    :exc:`Unauthorized` error is raised (the user isn't authenticated)
    """
    def decorate(func):
        @wraps(func)
        def wrapped():
            try:
                predicate.check_authorization(request.environ)
            except NotAuthorizedError as err:
                reason = unicode(err)
                if request.environ.get('repoze.who.identity'):
                    # The user is authenticated.
                    raise Forbidden(reason)
                else:
                    # The user is not authenticated.  This error has the
                    # error code 401, which triggers the redirection to the
                    # login form in repoze!
                    raise Unauthorized(reason)
            else:
                return func()
        return wrapped
    return decorate


@expose('/')
def index():
    # display the index with some links to test authentication and
    # authorization
    body = index_document.render(
        permission_url=local.urls.build('need_permission'),
        logged_in_url=local.urls.build('need_login'),
        login_url=local.urls.build('login'),
        logout_url=local.urls.build('logout'),
        logged_in=not_anonymous().is_met(request.environ))
    html = document.render(title='Hello!', body=body)
    return Response(html, mimetype='text/html')


@expose('/login')
def login():
    # extract the url, the user came from, from the get parameters.
    came_from = request.args.get('came_from', local.urls.build('index'))
    # build the action url with the camefrom parameter
    url = Href(local.urls.build('dologin'))(came_from=came_from)
    # and render the form
    body = login_form.render(login_url=url)
    html = document.render(title='Login', body=body)
    return Response(html, mimetype='text/html')


# the user must have the administer permission to view this url
@protect(has_permission('administer'))
@expose('/need_permission')
def need_permission():
    return Response(
        document.render(body='You may administer the site!', title='Admin'),
        mimetype='text/html')


# the user must be logged in to view this url
@protect(not_anonymous())
@expose('/need_login')
def need_login():
    return Response(
        document.render(body='You are logged in.', title='User'),
        mimetype='text/html')


@expose('/post_login')
def post_login():
    # extract the url, the user came from
    came_from = request.args.get('came_from', local.urls.build('index'))
    if not_anonymous().is_met(request.environ):
        # the user authenticated successfully, redirect to where he came
        # from
        return redirect(came_from)
    else:
        # redirect to the login form
        url = local.urls.build('login')
        return redirect(Href(url)(came_from=came_from))


def application(environ, start_response):
    # create a request
    local.request = Request(environ)
    # bind urls to environment
    local.urls = urls = url_map.bind_to_environ(environ)
    try:
        # get endpoint and arguments and call the endpoint
        endpoint, args = urls.match()
        response = globals()[endpoint](*args)
    except HTTPException as err:
        # handle http exceptions gracefully
        response = err
    # return the response and dispose resources
    return ClosingIterator(response(environ, start_response),
                           [local_manager.cleanup, session.remove])


application = setup_sql_auth(
    # the wrapped application
    application,
    # sqlalchemy classes for users, groups and permissions.
    # the User class must have a "groups" attribute with all groups, the
    # user is member of, a "user_name" attribute containing the username,
    # and a "validate_password()" method to validate a password input.  The
    # Group class must have "group_name", "users" and "permissions"
    # attributes.  The Permission class must have a "permission_name" and a
    # "groups" attribute.
    User, Group, Permission,
    # the sqlalchemy scoped session
    session,
    # the secret key for the authticket cookie
    cookie_secret='Some very secret key',
    # the url providing the login form
    login_url='/login',
    # the url called by the login form
    login_handler='/dologin',
    # this url is being redirected to after a login
    post_login_url='/post_login',
    # this url is being redirected to after a logout
    #post_logout_url='/post_logout',
    # this url logs out
    logout_handler='/logout')


action_serve = script.make_runserver(lambda: application, use_reloader=True,
                                     use_debugger=True)


if __name__ == '__main__':
    script.run()
