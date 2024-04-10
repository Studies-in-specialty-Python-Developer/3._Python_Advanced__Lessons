""" Урок 7, завдання 2
Створіть два класи Directory (тека) і File (файл) з типами (анотацією).
Клас Directory має мати такі поля:
• назва (name типу str);
• батьківська тека (root типу Directory);
• список файлів (список типу files, який складається з екземплярів File);
• список підтек (список типу sub_directories, який складається з екземплярів Directory).
Клас Directory має мати такі поля:
• додавання теки до списку підтек (add_sub_directory, який приймає екземпляр Directory
та присвоює поле root для приймального екземпляра);
• видалення теки зі списку підтек (remove_sub_directory, який приймає екземпляр
Directory та зануляє поле root. Метод також видаляє теку зі списку sub_directories);
• додавання файлу в теку (add_file, який приймає екземпляр File і присвоює йому поле
directory – див. клас File нижче);
• видалення файлу з теки (remove_file, який приймає екземпляр File та зануляє у нього
поле directory. Метод видаляє файл зі списку files).
Клас File має мати такі поля:
• назва (name типу str);
• тека (Directory типу Directory).
"""


class File:
    name: str
    directory: 'Directory'

    def __init__(self, name: str):
        self.name = name


class Directory:
    name: str
    root: 'Directory'
    files: list[File]
    sub_directories: list['Directory']

    def __init__(self, name: str):
        self.name = name
        self.files = []
        self.sub_directories = []

    def add_sub_directory(self, sub_dir: 'Directory'):
        sub_dir.root = self
        self.sub_directories.append(sub_dir)

    def remove_sub_directory(self, sub_dir: 'Directory'):
        # Предполагается, что sub_dir содержится в списке
        # Иначе надо делать обработку возможного исключения
        sub_dir.root = None
        self.sub_directories.remove(sub_dir)

    def add_file(self, file: File):
        file.directory = 'Directory'
        self.files.append(file)

    def remove_file(self, file: File):
        # Предполагается, что file содержится в списке
        # Иначе надо делать обработку возможного исключения
        file.directory = None
        self.files.remove(file)

    def print_structure(self):
        for sub_dir in self.sub_directories:
            print(sub_dir.name)
        for file in self.files:
            print(file.name)


dir_0 = Directory('dir_0')
dir_1 = Directory('dir_1')
dir_2 = Directory('dir_2')
file_1 = File('file_1')
file_2 = File('file_2')

dir_0.add_sub_directory(dir_1)
dir_0.add_sub_directory(dir_2)
dir_0.add_file(file_1)
dir_0.add_file(file_2)

dir_0.print_structure()
print()

dir_0.remove_sub_directory(dir_2)
dir_0.remove_file(file_1)

dir_0.print_structure()
