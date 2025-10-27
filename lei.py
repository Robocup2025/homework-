class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    def personInfo(self):
        print(f"姓名：{self.name}，年龄：{self.age}，性别：{self.gender}")
class Student(Person):
    def __init__(self, name, age, gender, college, class_):
        super().__init__(name, age, gender)
        self.college = college
        self.class_ = class_
    def personInfo(self):
        super().personInfo()
        print(f"学院：{self.college}，班级：{self.class_}")
    def __str__(self):
        return f"学生{self.name}，{self.age}岁，{self.gender}，{self.college} {self.class_}班"
