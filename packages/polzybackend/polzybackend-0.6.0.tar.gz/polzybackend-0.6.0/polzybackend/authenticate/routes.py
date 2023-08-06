from flask import jsonify, request, current_app
from datetime import date
from polzybackend.authenticate import bp
from polzybackend.utils.import_utils import all_stages, permissions
from polzybackend.models import User
from polzybackend import auth


@bp.route('/stages')
def stages():
    #
    # returns list of all available stages for login
    #

    try:
        # get all stages
        stages = all_stages()()
        current_app.logger.debug(f"Value of stages: {stages}")

    except Exception as e:
        current_app.logger.warning(f'Failed to get All Stages: {e}')
        stages = []

    return jsonify(stages), 200


@bp.route('/login', methods=['POST'])
def login():
    # get request data
    data = request.get_json()
    
    # check for required fields in data
    required_fields = [
        'email',
        'stage',
        'language',
    ]
    for field in required_fields:
        value = data.get(field)  
        if value is None:
            return {'error': f'User data does not contain {field}'}, 400

    # get user from db
    email = data['email']
    user = User.query.filter_by(email=email).first()
    # check if user found
    if user is None:
        return {'error': f'User {email} does not exist'}, 404

    # update current stage and language
    user.set_stage(data['stage'])
    user.set_language(data['language'])

    return jsonify(user.to_json()), 200


@bp.route('/permissions', methods=['POST'])
@auth.login_required
def user_permissions():
    # get request data
    try:
        data = request.get_json()

        # get company id
        company_id = data.get('id')
        if company_id is None:
            current_app.logger.warning(f'Payload does not contain company id. Payload: {data}')
            raise Exception('Payload does not contain company id')

        # update company
        user = auth.current_user()
        company_details = user.set_company(company_id=company_id)
        
        return jsonify({
            'permissions': permissions(user),
            'company': company_details,
        }), 200

    except Exception as e:
        return {'error': f'Failed to set company: {e}'}, 400
