from pathlib import Path
import yaml
import argparse

def source_to_slisp(input_yaml):
   return '\n'.join(
           filter(lambda x: x, 
                  [f'(func {i[0]} "#{i[1]}")' 
                  if i[0][0] == 'b' else None
                  for i in input_yaml.items()]
                  ))
def load_yaml(input_path):
    return yaml.load(input_path.open(), yaml.FullLoader)

def build_scheme(input_path, output_path):
    output_path.write_text(
            source_to_slisp(
                load_yaml(input_path)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?')
    args = parser.parse_args()
    inputs = Path(args.input_file)
    outputs = Path(args.output_file)
    if inputs.is_dir():
        if outputs.exists() and outputs.is_file():
            exit(2)
        if not outputs.exists():
            outputs.mkdir(exist_ok = True, parents=True)
        for input_file in inputs.rglob('**/*'):
            build_scheme(
             input_file,
             outputs / input_file.with_suffix('.slisp').parts[-1])
