import os
from dotenv import load_dotenv
from pathlib import Path

dir: Path = Path(__file__).resolve().parent.parent

dotenvPath = Path(f'{dir}/database.env')
load_dotenv(dotenv_path=dotenvPath)

host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
userdb = os.getenv('USERDB')
password = os.getenv('PASSWORD')

def printEnvironment():
    print(f'El host es: {host},\n'
          f'El puerto es: {port},\n'
          f'La base de datos es: {database},\n'
          f'El usuario es: {userdb},\n'
          f'La contraseñá es: {password}')


if __name__ == '__main__':
    printEnvironment()
