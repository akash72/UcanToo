from flask import Flask
from flask import jsonify
from flask import request

import model_interface as ModelInterface
import sys, os
import _pickle as pickle
import gzip
import numpy as np


app = Flask(__name__)




if __name__ == '__main__':
 app.run()