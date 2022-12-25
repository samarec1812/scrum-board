from ..app import db

user_task = db.Table(
    'user_task',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.task_id', ondelete="CASCADE"), primary_key=True),
)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    tasks = db.relationship('Task', secondary=user_task)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
        }
