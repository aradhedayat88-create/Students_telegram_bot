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
# user1 = Students(name = "tirdad", surname = "ershadi", age = 33,
#                 nat_id_num = 246957, courses = "Static, Dynamic", score = 20)
# sessionlocal.add(user1)
# sessionlocal.commit()
#--------------------------------------------------------

#------------------------Update--------------------------
# update_age = int(input("Enter your age in order to update it: "))
# user2 = sessionlocal.query(Students).filter(Students.age == int(update_age)).first()
# user2.age = int(input("Enter your new age in order to update it: "))
# sessionlocal.commit()
#--------------------------------------------------------

#------------------------Delete--------------------------
# del_by_id = int(input("Enter the id which is going to be deleted: "))
# user = sessionlocal.get(Students, int(del_by_id))
# sessionlocal.delete(user)
# sessionlocal.commit()
#--------------------------------------------------------

#-------------------------Read---------------------------
# show_all = sessionlocal.scalars(select(Students)).all()
# for show in show_all:
#     print(show.id, show.name, show.surname, show.nat_id_num)
#--------------------------------------------------------
