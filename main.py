import argparse
from models import Session, Teacher, Group, Student, Subject

session = Session()

# Універсальні функції для CRUD операцій
def create_record(model, name, teacher_id=None, group_id=None):
    if model == Teacher:
        record = model(fullname=name)
    elif model == Group:
        record = model(name=name)
    elif model == Student:
        if not group_id:
            print("Помилка: Для створення студента обов'язково потрібен параметр --group_id")
            return
        record = model(fullname=name, group_id=group_id)
    elif model == Subject:
        if not teacher_id:
            print("Помилка: Для створення предмета обов'язково потрібен параметр --teacher_id")
            return
        record = model(name=name, teacher_id=teacher_id)
    
    session.add(record)
    session.commit()
    print(f"Успіх: Запис у моделі {model.__name__} створено з ID: {record.id}")

def list_records(model):
    records = session.query(model).all()
    print(f"\n--- Список для моделі {model.__name__} ---")
    for r in records:
        # У студентів та викладачів поле називається fullname, у груп та предметів - name
        name_value = r.fullname if hasattr(r, 'fullname') else r.name
        print(f"ID: {r.id} | {name_value}")

def update_record(model, id_, new_name):
    record = session.query(model).filter(model.id == id_).first()
    if record:
        if hasattr(record, 'fullname'):
            old_name = record.fullname
            record.fullname = new_name
        else:
            old_name = record.name
            record.name = new_name
        session.commit()
        print(f"Успіх: Запис ID {id_} у моделі {model.__name__} змінено з '{old_name}' на '{new_name}'")
    else:
        print(f"Помилка: Запис з ID {id_} у моделі {model.__name__} не знайдено.")

def delete_record(model, id_):
    record = session.query(model).filter(model.id == id_).first()
    if record:
        session.delete(record)
        session.commit()
        print(f"Успіх: Запис з ID {id_} у моделі {model.__name__} успішно видалено.")
    else:
        print(f"Помилка: Запис з ID {id_} у моделі {model.__name__} не знайдено.")

def main():
    parser = argparse.ArgumentParser(description="Повноцінні CRUD операції з базою даних через SQLAlchemy")
    
    # Головні аргументи: дія (-a) та модель (-m)
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'delete'], required=True, help="Дія")
    parser.add_argument('-m', '--model', choices=['Teacher', 'Group', 'Student', 'Subject'], required=True, help="Модель")
    
    # Додаткові параметри
    parser.add_argument('--id', type=int, help="ID запису для дій update/delete")
    parser.add_argument('--name', type=str, help="Ім'я або назва для дій create/update")
    parser.add_argument('--teacher_id', type=int, help="ID викладача (тільки для створення предметів)")
    parser.add_argument('--group_id', type=int, help="ID групи (тільки для створення студентів)")

    args = parser.parse_args()

    # Словник для мапінгу текстового аргументу на реальний клас моделі
    model_mapping = {
        'Teacher': Teacher,
        'Group': Group,
        'Student': Student,
        'Subject': Subject
    }
    
    current_model = model_mapping[args.model]

    if args.action == 'create':
        if not args.name:
            print("Помилка: Для створення потрібен параметр --name")
        else:
            create_record(current_model, args.name, args.teacher_id, args.group_id)
            
    elif args.action == 'list':
        list_records(current_model)
        
    elif args.action == 'update':
        if not args.id or not args.name:
            print("Помилка: Для оновлення потрібні параметри --id та --name")
        else:
            update_record(current_model, args.id, args.name)
            
    elif args.action == 'delete':
        if not args.id:
            print("Помилка: Для видалення потрібен параметр --id")
        else:
            delete_record(current_model, args.id)

    session.close()

if __name__ == "__main__":
    main()