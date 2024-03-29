from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    uni = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=True)

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User %r>' % self.uni


class Course(db.Model):
    # for reference
    # http://www.columbia.edu/cu/bulletin/uwb/subj/COMS/_Fall2019_text.html
    number = db.Column(db.String(10), nullable=False)
    section = db.Column(db.Integer, nullable=False)
    call = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    points = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    dept_short = db.Column(db.String(4), nullable=False)
    day = db.Column(db.String(3), nullable=False)
    time = db.Column(db.String(80), nullable=False)
    faculty = db.Column(db.String(80), nullable=False)
    seat_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Course {}{}-{} {}>'.format(self.dept_short, self.number, str(self.section).zfill(3), self.title)

    # def __init__(**kwargs):
    #     super(Course, self).__init__(**kwargs)
    #     for i in range(seat_count):
    #         s = Seat(course=self)
    #         db.session.add(s)
    #     db.session.commit()
    #     return 0

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.call'), nullable=False)
    course = db.relationship('Course', backref=db.backref('seats', lazy=True))
    student_id = db.Column(db.String(10), db.ForeignKey('user.uni'), nullable=True)
    student = db.relationship('User', backref=db.backref('classes', lazy=True))

    def __repr__(self):
        return str(self.course)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.call'))
    course = db.relationship('Course', uselist=False)
    student_id = db.Column(db.String(10), db.ForeignKey('user.uni'),nullable=False)
    student = db.relationship('User', backref=db.backref('orders', lazy=True))
    price = db.Column(db.Integer, nullable=False)
    side = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return '<{} {} {}>'.format(self.side, self.price, self.course)
