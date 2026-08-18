from sqlalchemy import create_engine, text, Column, Integer, String, Float, select
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///Students.db")

Session = sessionmaker(bind=engine)

sessionlocal = Session()

sessionlocal.execute(text("SELECT 1"))

Base = declarative_base()

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    nat_id_num = Column(Integer)
    courses = Column(String)
    score = Column(Float)

Base.metadata.create_all(engine)

#-----------------------Create---------------------------
def add_student(name, surname, age, nat_id_num, courses, score):
    new_student = Students(
        name=name,
        surname=surname,
        age=int(age),
        nat_id_num=int(nat_id_num),
        courses=courses,
        score=float(score)
    )
    sessionlocal.add(new_student)
    sessionlocal.commit()
    return new_student
#--------------------------------------------------------

#------------------------Update--------------------------
def update_student(student_id, field, new_value):
    student = sessionlocal.get(Students, int(student_id))
    
    if student is None:
        return None
    
    if field == "name":
        student.name = new_value
    elif field == "surname":
        student.surname = new_value
    elif field == "age":
        student.age = int(new_value)
    elif field == "nat_id_num":
        student.nat_id_num = int(new_value)
    elif field == "courses":
        student.courses = new_value
    elif field == "score":
        student.score = float(new_value)
    else:
        return "invalid_field"
    
    sessionlocal.commit()
    return student
#--------------------------------------------------------

#------------------------Delete--------------------------
def del_by_id(id):
    user = sessionlocal.get(Students, int(id))
    
    if user is None:
        return None
    
    sessionlocal.delete(user)
    sessionlocal.commit()
    return show_list()
#--------------------------------------------------------

#-------------------------Read---------------------------
def show_list():
    show_all = sessionlocal.scalars(select(Students)).all()
    result = "📋 لیست دانشجویان\n\n"

    for show in show_all:
        result += f"👤 دانشجو\n"
        result += f"🆔 شناسه: {show.id}\n"
        result += f"نام: {show.name}\n"
        result += f"نام خانوادگی: {show.surname}\n"
        result += f"کد ملی: {show.nat_id_num}\n"
        result += "━━━━━━━━━━━━━━\n"

    return result

def show_by_id(id):
    student = sessionlocal.query(Students).filter(Students.id == int(id)).first()
    return student

def show_by_nat_id_num(nat_num):
    return sessionlocal.query(Students).filter(Students.nat_id_num == int(nat_num)).first()
#--------------------------------------------------------
