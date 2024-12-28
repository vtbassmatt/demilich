from io import BufferedReader
import tomllib


def load_from_resources(filename: str):
    from importlib import resources
    from demilich import data
    
    full_filename = resources.files(data) / filename
    return load_from_file(full_filename)


def load_from_file(filename: str):
    with open(filename, 'rb') as f:
        return load_from_stream(f)


def load_from_stream(stream: BufferedReader):
    data = tomllib.load(stream)
    return data


if __name__ == '__main__':
    print(load_from_resources('pb2024.toml'))
