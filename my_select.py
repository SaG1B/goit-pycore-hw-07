from sqlalchemy import func, desc
from models import Session, Student, Grade, Group, Subject, Teacher

# Відкриваємо сесію для виконання запитів
session = Session()

def select_1():
    """1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Student)\
    .join(Grade)\
    .group_by(Student.id)\
    .order_by(desc('avg_grade'))\
    .limit(5)\
    .all()

def select_2(subject_id):
    """2. Знайти студента із найвищим середнім балом з певного предмета."""
    return session.query(
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Student)\
    .join(Grade)\
    .filter(Grade.subject_id == subject_id)\
    .group_by(Student.id)\
    .order_by(desc('avg_grade'))\
    .first()

def select_3(subject_id):
    """3. Знайти середній бал у групах з певного предмета."""
    return session.query(
        Group.name, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Group)\
    .join(Student)\
    .join(Grade)\
    .filter(Grade.subject_id == subject_id)\
    .group_by(Group.id)\
    .all()

def select_4():
    """4. Знайти середній бал на потоці (по всій таблиці оцінок)."""
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).scalar()

def select_5(teacher_id):
    """5. Знайти які курси читає певний викладач."""
    return session.query(Subject.name)\
    .filter(Subject.teacher_id == teacher_id)\
    .all()

def select_6(group_id):
    """6. Знайти список студентів у певній групі."""
    return session.query(Student.fullname)\
    .filter(Student.group_id == group_id)\
    .all()

def select_7(group_id, subject_id):
    """7. Знайти оцінки студентів у окремій групі з певного предмета."""
    return session.query(Student.fullname, Grade.grade)\
    .select_from(Student)\
    .join(Grade)\
    .filter(Student.group_id == group_id, Grade.subject_id == subject_id)\
    .all()

def select_8(teacher_id):
    """8. Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Teacher)\
    .join(Subject)\
    .join(Grade)\
    .filter(Subject.teacher_id == teacher_id)\
    .scalar()

def select_9(student_id):
    """9. Знайти список курсів, які відвідує певний студент."""
    return session.query(Subject.name)\
    .select_from(Subject)\
    .join(Grade)\
    .filter(Grade.student_id == student_id)\
    .distinct()\
    .all()

def select_10(student_id, teacher_id):
    """10. Список курсів, які певному студенту читає певний викладач."""
    return session.query(Subject.name)\
    .select_from(Subject)\
    .join(Grade)\
    .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)\
    .distinct()\
    .all()

def select_11(student_id, teacher_id):
    """11. Середній бал, який певний викладач ставить певному студенту."""
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Grade)\
    .join(Subject)\
    .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)\
    .scalar()

def select_12(group_id, subject_id):
    """12. Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    subquery = session.query(func.max(Grade.date_received))\
        .join(Student)\
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)\
        .scalar_subquery()

    return session.query(Student.fullname, Grade.grade, Grade.date_received)\
    .select_from(Student)\
    .join(Grade)\
    .filter(
        Student.group_id == group_id, 
        Grade.subject_id == subject_id, 
        Grade.date_received == subquery
    )\
    .all()

if __name__ == "__main__":
    print("--- 1. Топ 5 студентів ---")
    print(select_1())
    
    print("\n--- 2. Найкращий студент з предмета №1 ---")
    print(select_2(1))
    
    print("\n--- 3. Середній бал у групах з предмета №1 ---")
    print(select_3(1))
    
    print("\n--- 4. Загальний середній бал на потоці ---")
    print(select_4())
    
    print("\n--- 11. Середній бал від викладача №1 студенту №1 ---")
    print(select_11(1, 1))

    print("\n--- 12. Оцінки групи №1 з предмета №1 на останньому занятті ---")
    print(select_12(1, 1))

    # Закриваємо сесію після завершення роботи скрипта
    session.close()