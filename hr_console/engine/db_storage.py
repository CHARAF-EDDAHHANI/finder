from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from employee import Employee
from jobopening import JobOpening
from company import Company
from engine.filestorage import FileStorage
import basemodel

classes = {"Employee": Employee, "JobOpening": JobOpening, "Company": Company}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        HR_ENV = getenv('HR_ENV')
        self.__engine = create_engine('sqlite:///hr_console.db')
        if HR_ENV == "test":
            basemodel.Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        basemodel.Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        self.__session.remove()

    def get(self, cls, id):
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        all_class = classes.values()

        if not cls:
            count = sum(len(self.all(clas).values()) for clas in all_class)
        else:
            count = len(self.all(cls).values())

        return count

    def save_to_json(self, class_type, filename):
        objects = self.all(class_type)
        FileStorage.save_to_json(objects, filename)

    def load_from_json(self, class_type, filename):
        objects = FileStorage.load_from_json(class_type, filename)
        for obj in objects:
            self.new(obj)
        self.save()
