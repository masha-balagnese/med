from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import CORS
import sqlite3 as sql
import face_recognition

app = Flask(__name__)

CORS(app)

@app.route("/")
def index():
    return "This is root!!!!"


@app.route('/test', methods = ['GET'])
def test_picture():
    with sql.connect('test.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from Pictures where id = 1')
        me = cur.fetchall()[0][1]
        with open('me.jpg', 'wb') as f:
            f.write(me)

        picture_of_me = face_recognition.load_image_file("me.jpg")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        cur.execute('select * from Pictures where id = 2')
        unknown = cur.fetchall()[0][1]
        with open('unknown.jpg', 'wb') as f:
            f.write(unknown)

        unknown_picture = face_recognition.load_image_file("unknown.jpg")
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

        if results[0] == True:
            print("It's a picture of me!")
        else:
            print("It's not a picture of me!")


        return jsonify({'1': 1})

if __name__ == '__main__':
    app.run()
    # app.run(host='medicine_balagnese.com', port=5000, debug=True)
    # app.run(host='192.168.0.255', port=88, debug=True)
