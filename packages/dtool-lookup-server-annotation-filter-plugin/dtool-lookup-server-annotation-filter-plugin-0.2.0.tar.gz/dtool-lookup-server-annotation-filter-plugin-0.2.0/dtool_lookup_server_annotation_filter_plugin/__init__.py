from flask import (
    Blueprint,
    abort,
    request,
    jsonify,
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from dtool_lookup_server import (
    AuthenticationError
)

from dtool_lookup_server.utils import get_user_obj

from dtool_lookup_server_annotation_filter_plugin.utils import (
    get_annotation_key_info_by_user,
    get_annotation_value_info_by_user,
    get_num_datasets_by_user,
    get_datasets_by_user,
)


__version__ = "0.2.0"


annotation_filter_bp = Blueprint(
    'annotation_filter_plugin',
    __name__,
    url_prefix="/annotation_filter_plugin"
)


@annotation_filter_bp.route('/version', methods=["GET"])
@jwt_required
def version():

    # Authorize the user's request.
    try:
        username = get_jwt_identity()
        get_user_obj(username)
    except AuthenticationError:
        abort(401)

    return jsonify(__version__)


@annotation_filter_bp.route('/annotation_keys', methods=["POST"])
@jwt_required
def annotation_keys():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_annotation_key_info_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)


@annotation_filter_bp.route('/annotation_values', methods=["POST"])
@jwt_required
def annotation_values():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_annotation_value_info_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)


@annotation_filter_bp.route('/num_datasets', methods=["POST"])
@jwt_required
def num_datasets():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_num_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)


@annotation_filter_bp.route('/datasets', methods=["POST"])
@jwt_required
def datasets():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)
