#from app import *
#from main import *
from waitress import serve
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
    #app.run()
from main import *
