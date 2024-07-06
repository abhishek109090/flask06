from flask import Flask,redirect,url_for,jsonify,request
import psycopg2
from psycopg2 import Error,extras
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def con():
    connection=None
    try:
        connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="root",
    dbname="postgres",
    port=5432  
        )
    except Error as e:
        print(f"the error is '{e}")
    return connection



@app.route('/item',methods=["GET"])
def fun():
    connection= con()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('select * from student')
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    if items:
        x1=[]
        for item in items:
            x={
                "name":item[1],
                "mail_id" :item[2],
                "course" :item[3],
                "id" : item[0]
            
            }
            x1.append(x)
            
        return jsonify(x1)
    else:
        return jsonify({"error":"item not found"})
    
@app.route('/items/<int:id>', methods=['PUT'])
def updateitem(id):
    data = request.get_json()
    name=data.get('name')
    mail_id=data.get('mail_id')
    course=data.get('course')
    connection= con()
    cursor= connection.cursor()
    cursor.execute('update student set name=%s, mail_id= %s,course= %s where id = %s',(name,mail_id,course,id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item update to the database"})

@app.route('/del/<int:id>',methods=["DELETE"])
def delitem(id):
    connection= con()
    cursor = connection.cursor()
    cursor.execute("delete from student where id = %s",(id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item deleted"})

 
@app.route('/postitem',methods=["POST"])
def createitem():
    data = request.get_json()
    name=data.get('name')
    mail_id=data.get('mail_id')
    course=data.get('course')
    connection=con()
    cursor= connection.cursor()
    cursor.execute("insert into student (name,mail_id,course) values (%s,%s,%s)",(name,mail_id,course))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item inserted to the database"})


@app.route('/home/<name>')
def myfun(name):
    return 'welcome %s to the python class' % name

@app.route('/one/<var>')
def myfun1(var):
    if var=='mrv':
        return redirect(url_for('myfun',name=var))
    else:
        return redirect(url_for('fun'))

if __name__=="__main__":
    app.run()
