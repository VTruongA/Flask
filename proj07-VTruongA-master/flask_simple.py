from flask import Flask, request, render_template, url_for, redirect, make_response
import MySQLdb
import passwords
import random
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():
        if request.method =="GET":
                conn = MySQLdb.connect(host=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWD,db="proj07")
                cursor = conn.cursor()
                user = request.cookies.get("username")
                if not user:
                        return render_template("landing.html")
                cursor.execute("SELECT * FROM sessions where NOW() < expire and user = '"+user+"';".encode())
                results = cursor.fetchall()
                cursor.close()
                if not results:
                        return render_template("landing.html")
                else:
                        return render_template("game.html",usr=user)
        else:
                if "opponent" not in request.form:
                        user = request.form["username"]
                        idInt = random.randint(0,16**64)
                        idStr = "%064x" % idInt
                        conn = MySQLdb.connect(host=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWD,db="proj07")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO sessions(id,user,expire) values('"+idStr+"','"+user+"',ADDTIME(NOW(),100));".encode())
                        conn.commit()
                        cursor.close()
                        resp = make_response(render_template("game.html",usr=user))
                        resp.set_cookie("username",user)
                        return resp
                else:
                        oppo = request.form["opponent"]
                        user = request.cookies.get("username")
                        conn = MySQLdb.connect(host=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWD,db="proj07")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO games(p1ID,p2ID,p1Name,p2Name) values((SELECT id from sessions WHERE user = '"+user+"'), (SELECT id from sessions WHERE user = '"+oppo+"'),(SELECT user from sessions WHERE user ='"+user+"'),(SELECT user from sessions WHERE user = '"+oppo+"'))".encode())                        conn.commit()
                        conn.commit()
                        cursor.close()
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM games WHERE (p1ID=(SELECT id from sessions WHERE user = '"+user+"') and (p2ID=(SELECT id from sessions WHERE user = '"+oppo+"'))) or (p1ID=(SELECT id from sessions WHERE user = '"+oppo+"') and (p2ID=(SELECT id from sessions WHERE user = '"+user+"')))".encode())                 
                        results = cursor.fetchall()
                        cursor.close()
                        return render_template("oppo.html",opp = oppo,usr=user,result=results)
