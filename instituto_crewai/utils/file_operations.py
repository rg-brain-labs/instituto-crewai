from pathlib import Path

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_templates(template_dir):
    return {
        file.stem: read_file(file)
        for file in Path(template_dir).glob('*.md')
    }