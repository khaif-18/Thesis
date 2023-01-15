from flask import render_template
class View:
    def show(self, data):
        return render_template("index.html",data=data)