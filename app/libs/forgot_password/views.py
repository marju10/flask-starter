from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    url_for
)
from app.models.user import User
from .forms import (
    ForgotPasswordForm,
    ResetPasswordForm
)
from . import (
    forgot_password as forgot_password_util,
    decode,
    InvalidTokenException
)

bp = Blueprint('forgot_password', __name__, template_folder='templates')


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        forgot_password_util(
            email,
            sender=__sender)

    return render_template(
        'forgot.html',
        form=form
    )


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()

    if form.validate_on_submit():
        try:
            user = decode(token)
            password = form.new_password.data
            user.update(
                password=User.hash_password(password).decode('utf-8')
            )
            flash('Password reset!', 'success')
        except InvalidTokenException:
            flash('The link is invalid or expired', 'error')
            return redirect(url_for('main.index'))

    return render_template(
        'reset.html',
        form=form,
        token=token
    )


def __sender(token, user):
    raise Exception(
        'Add a sender function to forgot_password_util call \n'
        'Token: {}'.format(token)
    )