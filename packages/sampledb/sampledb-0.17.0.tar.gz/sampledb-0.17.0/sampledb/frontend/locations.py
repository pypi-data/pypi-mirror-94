# coding: utf-8
"""

"""

import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length
import typing

from . import frontend
from ..logic import errors
from ..logic.locations import Location, create_location, get_location, get_locations_tree, update_location, get_object_location_assignment, confirm_object_responsibility
from ..logic.security_tokens import verify_token
from ..logic.notifications import mark_notification_for_being_assigned_as_responsible_user_as_read
from .utils import check_current_user_is_not_readonly


class LocationForm(FlaskForm):
    name = StringField(validators=[Length(min=1, max=100)])
    description = StringField()
    parent_location = SelectField()


@frontend.route('/locations/')
@flask_login.login_required
def locations():
    locations_map, locations_tree = get_locations_tree()
    return flask.render_template(
        'locations/locations.html',
        locations_map=locations_map, locations_tree=locations_tree,
        sort_location_ids_by_name=_sort_location_ids_by_name
    )


@frontend.route('/locations/<int:location_id>', methods=['GET', 'POST'])
@flask_login.login_required
def location(location_id):
    try:
        location = get_location(location_id)
    except errors.LocationDoesNotExistError:
        return flask.abort(404)
    mode = flask.request.args.get('mode', None)
    if mode == 'edit':
        if flask.current_app.config['ONLY_ADMINS_CAN_MANAGE_LOCATIONS'] and not flask_login.current_user.is_admin:
            flask.flash('Only administrators can edit locations.', 'error')
            return flask.abort(403)
        check_current_user_is_not_readonly()
        return _show_location_form(location, None)
    locations_map, locations_tree = get_locations_tree()
    ancestors = []
    parent_location = location
    while parent_location.parent_location_id is not None:
        parent_location = get_location(parent_location.parent_location_id)
        ancestors.insert(0, (parent_location.id, parent_location.name))
    for ancestor_id, ancestor_name in ancestors:
        locations_tree = locations_tree[ancestor_id]
    locations_tree = locations_tree[location_id]
    return flask.render_template(
        'locations/location.html',
        locations_map=locations_map, locations_tree=locations_tree,
        location=location, ancestors=ancestors,
        sort_location_ids_by_name=_sort_location_ids_by_name
    )


@frontend.route('/locations/new/', methods=['GET', 'POST'])
@flask_login.login_required
def new_location():
    if flask.current_app.config['ONLY_ADMINS_CAN_MANAGE_LOCATIONS'] and not flask_login.current_user.is_admin:
        flask.flash('Only administrators can create locations.', 'error')
        return flask.abort(403)
    check_current_user_is_not_readonly()
    parent_location = None
    parent_location_id = flask.request.args.get('parent_location_id', None)
    if parent_location_id is not None:
        try:
            parent_location_id = int(parent_location_id)
        except ValueError:
            parent_location_id = None
    if parent_location_id:
        try:
            parent_location = get_location(parent_location_id)
        except errors.LocationDoesNotExistError:
            flask.flash('The requested parent location does not exist.', 'error')
    return _show_location_form(None, parent_location)


@frontend.route('/locations/confirm_responsibility')
@flask_login.login_required
def accept_responsibility_for_object():
    token = flask.request.args.get('t', None)
    if token is None:
        flask.flash('The confirmation token is missing.', 'error')
        return flask.redirect(flask.url_for('.index'))
    object_location_assignment_id = verify_token(token, salt='confirm_responsibility', secret_key=flask.current_app.config['SECRET_KEY'], expiration=None)
    if object_location_assignment_id is None:
        flask.flash('The confirmation token is invalid.', 'error')
        return flask.redirect(flask.url_for('.index'))
    try:
        object_location_assignment = get_object_location_assignment(object_location_assignment_id)
    except errors.ObjectLocationAssignmentDoesNotExistError:
        flask.flash('This responsibility assignment does not exist.', 'error')
        return flask.redirect(flask.url_for('.index'))
    if object_location_assignment.responsible_user_id != flask_login.current_user.id:
        flask.flash('This responsibility assignment belongs to another user.', 'error')
        return flask.redirect(flask.url_for('.index'))
    if object_location_assignment.confirmed:
        flask.flash('This responsibility assignment has already been confirmed.', 'success')
    else:
        confirm_object_responsibility(object_location_assignment_id)
        flask.flash('You have successfully confirmed this responsibility assignment.', 'success')
        mark_notification_for_being_assigned_as_responsible_user_as_read(
            user_id=flask_login.current_user.id,
            object_location_assignment_id=object_location_assignment_id
        )
    return flask.redirect(flask.url_for('.object', object_id=object_location_assignment.object_id))


def _sort_location_ids_by_name(location_ids: typing.Iterable[int], location_map: typing.Dict[int, Location]) -> typing.List[int]:
    location_ids = list(location_ids)
    location_ids.sort(key=lambda location_id: location_map[location_id].name)
    return location_ids


def _show_location_form(location: typing.Optional[Location], parent_location: typing.Optional[Location]):
    if location is not None:
        submit_text = "Save"
    elif parent_location is not None:
        submit_text = "Create"
    else:
        submit_text = "Create"
    locations_map, locations_tree = get_locations_tree()
    invalid_location_ids = []
    if location is not None:
        invalid_location_ids.append(location.id)
        ancestor_ids = []
        _parent_location = location
        while _parent_location.parent_location_id is not None:
            _parent_location = get_location(_parent_location.parent_location_id)
            ancestor_ids.insert(0, _parent_location.id)
        locations_subtree = locations_tree
        for ancestor_id in ancestor_ids:
            locations_subtree = locations_subtree[ancestor_id]
        locations_subtree = locations_subtree[location.id]
        unhandled_descendent_ids_and_subtrees = [(descendent_id, locations_subtree) for descendent_id in locations_subtree]
        while unhandled_descendent_ids_and_subtrees:
            descendent_id, locations_subtree = unhandled_descendent_ids_and_subtrees.pop(0)
            invalid_location_ids.append(descendent_id)
            locations_subtree = locations_subtree[descendent_id]
            for descendent_id in locations_subtree:
                unhandled_descendent_ids_and_subtrees.append((descendent_id, locations_subtree))

    location_form = LocationForm()
    location_form.parent_location.choices = [('-1', '-')] + [
        (str(location_id), locations_map[location_id].name)
        for location_id in locations_map
        if location_id not in invalid_location_ids
    ]
    if location_form.parent_location.data is None or location_form.parent_location.data == str(None):
        if location is not None and location.parent_location_id:
            location_form.parent_location.data = str(location.parent_location_id)
        elif parent_location is not None:
            location_form.parent_location.data = str(parent_location.id)
        else:
            location_form.parent_location.data = str(-1)

    form_is_valid = False
    if location_form.validate_on_submit():
        form_is_valid = True

    if location is not None:
        if location_form.name.data is None:
            location_form.name.data = location.name
        if location_form.description.data is None:
            location_form.description.data = location.description

    if form_is_valid:
        name = location_form.name.data
        description = location_form.description.data
        parent_location_id = location_form.parent_location.data
        try:
            parent_location_id = int(parent_location_id)
        except ValueError:
            parent_location_id = None
        if parent_location_id < 0:
            parent_location_id = None
        if location is None:
            location = create_location(name, description, parent_location_id, flask_login.current_user.id)
            flask.flash('The location was created successfully.', 'success')

        else:
            update_location(location.id, name, description, parent_location_id, flask_login.current_user.id)
            flask.flash('The location was updated successfully.', 'success')
        return flask.redirect(flask.url_for('.location', location_id=location.id))
    return flask.render_template(
        'locations/location_form.html',
        location_form=location_form,
        submit_text=submit_text
    )
