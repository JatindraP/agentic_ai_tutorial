
from dotenv import load_dotenv
from server import app
import uvicorn
import rag_utils as utils

load_dotenv()

UV_HOST = utils.get_config("uvicorn", "host")
UV_PORT = utils.get_config("uvicorn", "port")

def main():
    uvicorn.run(app, host=UV_HOST, port=UV_PORT)

main()