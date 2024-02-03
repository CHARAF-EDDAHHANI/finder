#!/usr/bin/env python3

import json

class FileStorage:
    @staticmethod
    def save_to_json(objects, filename):
        with open(filename, 'w') as file:
            data = [obj.to_dict() for obj in objects]
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")

    @staticmethod
    def load_from_json(class_type, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                objects = [class_type.from_dict(obj) for obj in data]
            print(f"Data loaded from {filename}")
            return objects
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []
        except Exception as e:
            print(f"Error loading data from {filename}: {e}")
            return []
