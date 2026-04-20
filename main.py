from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from modules import *

@app.route('/')
def main():
    return render_template('index.html')




app.run(debug=True)


