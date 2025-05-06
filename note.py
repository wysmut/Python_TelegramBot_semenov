#приложение заметок
import os

def build_note(note_text, note_name):
    with open(f"{note_name}.txt", 'w', encoding='utf-8') as f:
        f.write(note_text)

def create_note():
    note_name = input("Введите название заметки: ").strip()
    note_text = input("Введите текст заметки: ").strip()
    build_note(note_text, note_name)
    print(f"Заметка '{note_name}' создана.")

def read_note():
    note_name = input("Введите название заметки для чтения: ").strip()
    if os.path.isfile(f"{note_name}.txt"):
        with open(f"{note_name}.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Заметка '{note_name}':\n{content}")
    else:
        print(f"Заметка '{note_name}' не найдена.")

def edit_note():
    note_name = input("Введите название заметки для редактирования: ").strip()
    if os.path.isfile(f"{note_name}.txt"):
        with open(f"{note_name}.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Текущая заметка '{note_name}':\n{content}")
        
        new_text = input("Введите новый текст заметки: ").strip()
        build_note(new_text, note_name)
        print(f"Заметка '{note_name}' обновлена.")
    else:
        print(f"Заметка '{note_name}' не найдена.")

def delete_note():
    note_name = input("Введите название заметки для удаления: ").strip()
    if os.path.isfile(f"{note_name}.txt"):
        os.remove(f"{note_name}.txt")
        print(f"Заметка '{note_name}' удалена.")
    else:
        print(f"Заметка '{note_name}' не найдена.")

def display_notes(reverse=False):
    notes = [f for f in os.listdir() if f.endswith('.txt')]
    notes.sort(key=lambda x: os.path.getsize(x), reverse=reverse)
    for note in notes:
        print(note.replace('.txt', ''))

def main():
    while True:
        print("\nМеню:")
        print("1. Создать заметку")
        print("2. Читать заметку")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Показать все заметки (короткие в начале)")
        print("6. Показать все заметки (длинные в начале)")
        print("0. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            create_note()
        elif choice == '2':
            read_note()
        elif choice == '3':
            edit_note()
        elif choice == '4':
            delete_note()
        elif choice == '5':
            display_notes(reverse=False)
        elif choice == '6':
            display_notes(reverse=True)
        elif choice == '0':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
