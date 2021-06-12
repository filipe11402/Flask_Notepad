from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note
from . import db

#blue print to create the endpoints
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        user_id = current_user.id
        new_note = Note(text=note, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note Added successfuly', category='success')
    
    all_notes = Note.query.filter_by(user_id=current_user.id)

    return render_template('index.html', notes=all_notes)

@views.route('/delete-note/<string:id>', methods=['POST'])
@login_required
def delete_note(id):
    if request.method == 'POST':
        note_delete = Note.query.get(id)
        if note_delete:
            if note_delete.user_id == current_user.id:
                db.session.delete(note_delete)
                db.session.commit()

    return redirect(url_for('views.index'))