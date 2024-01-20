import json

class FileStorage:
    @staticmethod
    def save_to_json(objects, filename):
        with open(filename, 'w') as file:
            data = [obj.to_dict() for obj in objects]
            json.dump(data, file, indent=2)

    @staticmethod
    def load_from_json(class_type, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return [class_type.from_dict(obj) for obj in data]
