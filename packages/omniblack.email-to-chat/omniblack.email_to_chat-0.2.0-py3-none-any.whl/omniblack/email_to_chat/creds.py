from os import environ
from pathlib import Path
from .async_utils import run_in_executor


@run_in_executor
def load_cred(cred_name):
    if 'CREDENTIALS_DIRECTORY' in environ:
        path = Path(environ['CREDENTIALS_DIRECTORY'])/cred_name

        try:
            with path.open() as file_obj:
                return file_obj.read()
        except FileNotFoundError:
            pass

    if cred_name in environ:
        return environ[cred_name]
    else:
        raise RuntimeError(f'Credential {cred_name} could not be loaded.')
