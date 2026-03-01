from flask import Flask
import os
import importlib.util
from database.db_init import init_database

def import_pages(route, app):
    for root, _, files in os.walk(route):
        for file in files:
            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)
            module_name = os.path.splitext(os.path.relpath(path, route))[0]
            module_name = module_name.replace(os.sep, ".")

            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Failed to import {path}: {e}")
                continue

            if hasattr(module, "page"):
                print(f"{module_name}.page =", module.page)
                app.register_blueprint(module.page)


app = Flask(__name__, static_folder='static', static_url_path='')

init_database()
import_pages("routes", app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)