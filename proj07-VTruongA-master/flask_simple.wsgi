import sys
import os


APP_DIR = "/home/ec2-user/flask_simple/"

# why doesn't WSGI set this up automatically?  I find the next two steps
# fairly annoying!
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)


from flask_simple import app as application
