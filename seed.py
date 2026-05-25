import random
from datetime import datetime
from faker import Faker
from models import Session, Group, Teacher, Subject, Student, Grade

# Ініціалізуємо Faker для створення українських імен
fake = Faker('uk_UA')

def seed_database():
    # Відкриваємо сесію для роботи з базою даних
    session = Session()

    try:
        # 1. Створюємо 3 групи
        group_names = ['Група А', 'Група Б', 'Група В']
        groups = [Group(name=name) for name in group_names]
        session.add_all(groups)
        
        # 2. Створюємо 5 викладачів
        teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
        session.add_all(teachers)
        
        # Тимчасово зберігаємо, щоб отримати ID груп та викладачів
        session.commit()

        # 3. Створюємо 6 предметів і прив'язуємо до випадкових викладачів
        subject_names = [
            'Вища математика', 'Програмування Python', 'Дискретна математика', 
            'Англійська мова', 'Фізика', 'Історія України'
        ]
        subjects = [Subject(name=name, teacher=random.choice(teachers)) for name in subject_names]
        session.add_all(subjects)

        # 4. Створюємо 40 студентів і розкидаємо їх по 3 групах
        students = [Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(40)]
        session.add_all(students)
        
        # Знову зберігаємо, щоб студенти та предмети отримали свої ID
        session.commit()

        # 5. Додаємо оцінки (робимо кожному студенту від 15 до 20 оцінок)
        for student in students:
            for _ in range(random.randint(15, 20)):
                random_date = fake.date_this_year()
                
                grade = Grade(
                    grade=random.randint(4, 12),
                    date_received=random_date,
                    student=student,
                    subject=random.choice(subjects)
                )
                session.add(grade)

        # Фінально зберігаємо всі оцінки в базу даних
        session.commit()
        print("Успіх! Базу даних успішно заповнено за допомогою SQLAlchemy ORM!")

    except Exception as e:
        print(f"Ой, щось пішло не так: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()