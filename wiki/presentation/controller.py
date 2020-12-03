import datetime
import functools
import flask
import werkzeug
from ..services import *
from ..core.application.getusers import *
from ..core.application.adduser import *
from ..core.application.updateuser import *
from ..core.application.removeuser import *
from ..core.application.login import *
from ..core.application.loadpage import *
from ..core.application.savepage import *
from ..core.application.loadprofile import *
from ..core.application.saveprofile import *
from ..core.models.page import *
from ..core.models.user import *
from ..core.models.session import *


app = flask.Flask(
    __name__,
    template_folder='views/templates',
    static_folder='views/static'
)


def login_required(api:bool=False, redirect:str=''):
    def decorator(f):
        @functools.wraps(f)
        def decorated_func(*args, **kwargs):
            if flask.g.user is None:
                if api:
                    raise werkzeug.exceptions.NotAuthorized()
                else:
                    return flask.redirect(flask.url_for('page', path=redirect))
            return f(*args, **kwargs)
        return decorated_func
    return decorator


@app.before_request
def before_request():
    session_repository = Dependency.resolve(ISessionRepository)
    user_repository = Dependency.resolve(IUserRepository)
    session_id = SessionId(flask.request.cookies.get('session_id', ''))
    session = session_repository.load(session_id)
    flask.g.user = None if session is None \
        else user_repository.load(session.user_id)


@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        user_id = UserId(flask.request.form['user_id'])
        password = UserPassword(flask.request.form['password'])
        request = LoginRequest(user_id=user_id, password=password)
        response = Service.call(request)
        return flask.jsonify({
            'session_id': response.session_id.value,
            'expires': response.expires.value.timestamp(),
        })
    except (KeyError, ValueError, TypeError):
        raise werkzeug.exceptions.BadRequest()


@app.route('/api/profile', methods=['GET', 'POST'])
@login_required(api=True)
def api_profile():
    if flask.request.method == 'POST':
        try:
            name = UserName(flask.request.form['name'])
            password = UserPassword(flask.request.form['password'])
            retypepassword = UserPassword(flask.request.form['retypepassword'])
            request = SaveProfileRequest(
                user_id=flask.g.user.user_id,
                name=name,
                password=password,
                retypepassword=retypepassword
            )
            response = Service.call(request)
        except (KeyError, ValueError, TypeError) as e:
            raise werkzeug.exceptions.BadRequest()
    request = LoadProfileRequest(flask.g.user.user_id)
    response = Service.call(request)
    return flask.jsonify({
        'user_id': response.user.user_id.value,
        'name': response.user.name.value,
        'password': '',
        'retypepassword': ''
    })


@app.route('/api/users', methods=['GET'])
@login_required(api=True)
def api_users():
    request = GetUsersRequest(user=flask.g.user)
    response = Service.call(request)
    return flask.jsonify({
        'users': [
            {
                'user_id': user.user_id.value,
                'name': user.name.value,
                'role': user.role.value,
                'role_name': user.role.name.capitalize()
            } for user in response.users
        ],
        'roles': [
            {
                'name': role.name.capitalize(),
                'value': role.value
            } for role in response.roles
        ]
    })


@app.route('/api/user', methods=['PUT'])
@login_required(api=True)
def api_user():
    try:
        request = AddUserRequest(
            requestor=flask.g.user,
            user_id=UserId(flask.request.form['user_id']),
            name=UserName(flask.request.form['name']),
            password=UserPassword(flask.request.form['password']),
            role=UserRole(int(flask.request.form['role']))
        )
        response = Service.call(request)
        return api_users()
    except (KeyError, ValueError, TypeError):
        raise werkzeug.exceptions.BadRequest()


@app.route('/api/user/<string:user_id>', methods=['POST', 'DELETE'])
@login_required(api=True)
def api_user_user_id(user_id: str):
    try:
        if flask.request.method == 'POST':
            request = UpdateUserRequest(
                requestor=flask.g.user,
                user_id=UserId(user_id),
                name=UserName(flask.request.form['name']),
                role=UserRole(int(flask.request.form['role']))
            )
            response = Service.call(request)
        elif flask.request.method == 'DELETE':
            request = RemoveUserRequest(
                requestor=flask.g.user,
                user_id=UserId(user_id)
            )
            response = Service.call(request)
    except (KeyError, ValueError, TypeError):
        raise werkzeug.exceptions.BadRequest()
    return api_users()


@app.route('/api/page/', methods=['GET'], defaults={'path': 'index'})
@app.route('/api/page/<string:path>', methods=['GET', 'POST'])
@login_required(api=True)
def api_page(path: str):
    if flask.request.method == 'POST':
        try:
            page_id = PageId(path)
            title = PageTitle(flask.request.form['title'])
            body = PageBody(flask.request.form['body'])
            lastmodified = PageLastModified(
                datetime.datetime.now(datetime.timezone.utc))
            version = PageVersion(int(flask.request.form['version']))
            page = Page(
                page_id=page_id,
                title=title,
                body=body,
                lastmodified=lastmodified,
                version=version
            )
            request = SavePageRequest(page=page)
            response = Service.call(request)
        except (KeyError, ValueError, TypeError):
            raise werkzeug.exceptions.BadRequest()
    request = LoadPageRequest(PageId(path))
    response = Service.call(request)
    return flask.jsonify({
        'page_id': response.page.page_id.value,
        'title': response.page.title.value,
        'body': response.page.body.value,
        'lastmodified': response.page.lastmodified.value.timestamp(),
        'version': response.page.version.value
    })


@app.route('/login', methods=['GET'])
def login():
    if flask.g.user is not None:
        return flask.redirect(flask.url_for('page', path=''))
    return flask.render_template('page.html',
        view='login', user=flask.g.user)


@app.route('/profile', methods=['GET'])
@login_required(redirect='')
def profile():
    return flask.render_template('page.html',
        view='profile', user=flask.g.user)


@app.route('/manage', methods=['GET'])
@login_required(redirect='')
def manage():
    return flask.render_template('page.html',
        view='manage', user=flask.g.user)


@app.route('/', methods=['GET', 'POST'], defaults={'path': 'index'})
@app.route('/<string:path>', methods=['GET', 'POST'])
def page(path: str):
    request = LoadPageRequest(PageId(path))
    response = Service.call(request)
    if 'edit' in flask.request.values:
        if flask.g.user is None:
            return flask.redirect(flask.url_for('page', path=path))
        return flask.render_template(
            'page.html', view='edit', user=flask.g.user, page=response.page)
    return flask.render_template(
        'page.html', view='page', user=flask.g.user, page=response.page)
