from app import db
from models import User, Course, Order, Seat


def make_courses():
    c1 = Course(number="W4111",section=1,call=35949,points=3,title="INTRODUCTION TO DATABASES",department="Computer Science",dept_short="COMS",day="TR",time="1:10pm-2:25pm",faculty="Luis Gravano",seat_count=155)

    c2 = Course(number="W4111",section=2,call=35950,points=3,title="INTRODUCTION TO DATABASES",department="Computer Science",dept_short="COMS",day="F",time="10:10am-12:40pm",faculty="Donald F Ferguson",seat_count=272)

    c3 = Course(number="W4118",section=1,call=35918,points=3,title="OPERATING SYSTEMS I",department="Computer Science",dept_short="COMS",day="MW",time="8:40am-9:55am",faculty="Jason Nieh",seat_count=120)

    c4 = Course(number="W4995",section=1,call=35925,points=3,title="HACKING 4 DEFENSE",department="Computer Science",dept_short="COMS",day="T",time="4:10pm-6:40pm",faculty="Paul S Blaer",seat_count=30)

    c5 = Course(number="W4995",section=1,call=10586,points=3,title="DEEP LRNG FOR COMP VISION",department="Computer Science",dept_short="COMS",day="TR",time="2:40pm-3:55pm",faculty="Peter Belhumeur",seat_count=60)

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.commit()

def make_seats():
    courses = Course.query.all()
    for course in courses:
        for i in range(course.seat_count):
            seat = Seat(course=course)
            db.session.add(seat)
        db.session.commit()

def main():
    db.create_all()
    make_courses()
    make_seats()

if __name__ == '__main__':
    main()
