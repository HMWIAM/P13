from flask import Flask, request, render_template
import pickle
import numpy as np

# Create an app object using the pickle class
app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))


