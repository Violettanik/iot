# flask-admin
import flask_admin
import flask_login as login
from flask import url_for, redirect, request, abort
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
# flask-login
from flask_login import current_user

from app import db, security
from app.initial import app
from app.models import User

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        print(f'{current_user.username}: current_user.is_active: ')
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


# Переадресация страниц (используется в шаблонах)
class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    # @login.login_required
    # @auth_required
    def index(self):
        print(f'is_authenticated: {current_user.is_authenticated}')
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


# Create admin
admin = flask_admin.Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html',
                          template_mode='bootstrap3')
# Add view
admin.add_view(MyModelView(User, db.session))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )

