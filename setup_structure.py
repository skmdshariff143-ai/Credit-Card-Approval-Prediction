import os

def create_structure():
    dirs = [
        "config",
        "data/raw",
        "data/processed",
        "data/external",
        "docs",
        "models/trained",
        "models/artifacts",
        "notebooks",
        "reports/figures",
        "src/data",
        "src/features",
        "src/models",
        "src/pipeline",
        "src/utils",
        "flask_app/static/css",
        "flask_app/static/js",
        "flask_app/static/images",
        "flask_app/templates",
        "tests",
        "deployment/ibm_cloud",
        "screenshots"
    ]
    
    for d in dirs:
        os.makedirs(os.path.join("e:\\Credit-Card-Approval-Prediction", d), exist_ok=True)
        print(f"Created directory: {d}")
        
    init_files = [
        "config/__init__.py",
        "src/__init__.py",
        "src/data/__init__.py",
        "src/features/__init__.py",
        "src/models/__init__.py",
        "src/pipeline/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for f in init_files:
        path = os.path.join("e:\\Credit-Card-Approval-Prediction", f)
        if not os.path.exists(path):
            with open(path, "w") as file:
                file.write("# Initializer\n")
            print(f"Created file: {f}")

if __name__ == "__main__":
    create_structure()
