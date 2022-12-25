from flask import request, redirect, url_for, make_response, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
)

from .models import Users, Task, user_task
from ..app import db

blueprint = Blueprint(
    'auth_blueprint',
    __name__,
    url_prefix=''
)


@blueprint.route('/')
def route_default():
    return redirect(url_for('auth_blueprint.login'))


@blueprint.route('/signup', methods=['POST'])
@cross_origin()
def registration():
    try:
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not username:
            return new_server_error('missing username', 400)
        if not email:
            return new_server_error('missing email', 400)
        if not password:
            return new_server_error('missing password', 400)

        password_hash = generate_password_hash(password)
        user = Users(username=username, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()

        return {"msg": "user successfully registered"}, 201
    except IntegrityError:
        db.session.rollback()
        return new_server_error('user already exists', 400)
    except AttributeError as e:
        return new_server_error(f'provide an username, email and password in json format in the request body: {e}', 400)


@blueprint.route('/signin', methods=['POST'])
@cross_origin()
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return new_server_error('missing username', 400)
        if not password:
            return new_server_error('missing password', 400)

        user = Users.query.filter_by(username=username).first()
        if not user:
            return new_server_error('user not found!', 404)

        if check_password_hash(user.password, password):
            access_token = create_access_token(identity={"id": user.id})
            return {"access_token": access_token}, 200
        else:
            return new_server_error('invalid password!', 400)
    except AttributeError as e:
        return new_server_error(f'provide an email and password in json format in the request body: {e}', 400)


@blueprint.route('/tasks', methods=['GET'])
@jwt_required()
@cross_origin()
def get_users_tasks():
    try:
        user = get_jwt_identity()
        user_id = user['id']
        response = [x.serialize for x in Users.query.filter_by(id=user_id).first().tasks]
        return response, 200
    except Exception as e:
        return new_server_error(f'unable to get tasks: {e}', 400)


@blueprint.route('/tasks', methods=['POST'])
@jwt_required()
@cross_origin()
def add_task_to_user():
    try:
        user = get_jwt_identity()
        user_id = user['id']

        title = request.json.get('title', None)
        description = request.json.get('description', " ")
        status = request.json.get('status', None)

        if not title:
            return new_server_error('missing title', 400)
        if not description:
            return new_server_error('missing description', 400)
        if not status:
            status = 0

        user = Users.query.filter_by(id=user_id).first()
        task = Task(title=title, description=description, status=status)
        user.tasks.append(task)
        db.session.add(user)
        db.session.commit()

        return {"msg": "task successfully added"}, 201
    except Exception as e:
        return new_server_error(f'unable to add task: {e}', 400)


@blueprint.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_user_task(task_id: int):
    try:
        user = get_jwt_identity()
        user_id = user['id']

        q = db.session.query(Task).filter_by(task_id=task_id).join(user_task).filter_by(user_id=user_id)
        res = db.session.execute(q).first()
        if not res:
            return new_server_error(f'no task with id = {task_id}', 404)

        task = res[0]
        return task.serialize, 200
    except Exception as e:
        return new_server_error(f'unable to get task: {e}', 400)


@blueprint.route('/tasks/<int:task_id>', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_task(task_id: int):
    try:
        title = request.json.get('title', None)
        description = request.json.get('description', None)
        status = request.json.get('status', None)

        if not title and not description and not status:
            return new_server_error("at least one field must be set", 400)

        user = get_jwt_identity()
        user_id = user['id']

        q = db.session.query(Task).filter_by(task_id=task_id).join(user_task).filter_by(user_id=user_id)
        res = db.session.execute(q).first()
        if not res:
            return new_server_error(f'no task with id = {task_id}', 404)

        task = res[0]
        task.title = title if title else task.title
        task.description = description if description else task.description
        task.status = status if status is not None else task.status
        db.session.commit()
        return {"msg": "task successfully updated"}, 200
    except Exception as e:
        return new_server_error(f'unable to update task: {e}', 400)


@blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_task(task_id: int):
    try:
        user = get_jwt_identity()
        user_id = user['id']

        Task.query.filter_by(task_id=task_id).delete()
        db.session.commit()
        return {"msg": "task successfully deleted"}, 200
    except Exception as e:
        return new_server_error(f'unable to delete task: {e}', 400)


def new_server_error(err_msg: str, code: int) -> tuple[dict[str, str], int]:
    return {"err_msg": err_msg}, code
