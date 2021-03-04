# Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


# httpsstackoverflow.comquestions8211128multiple-distinct-pages-in-one-html-file
# httpsstackoverflow.comquestions902408how-to-use-variables-in-sql-statement-in-python
# httpsstackoverflow.comquestions1081750python-update-multiple-columns-with-python-variables
# httpsstackoverflow.comquestions7478366create-dynamic-urls-in-flask-with-url-for
# httpsgithub.comvimallocflask-jwt-extendedissues175


from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector

app = Flask(__name__, static_url_path='')

# connect to database
conn = mysql.connector.connect(user='root', password='',
                               host='127.0.0.1',
                               database='zipcodes',
                               buffered=True)
cursor = conn.cursor()
#Search zipcode database
@app.route('/searchZIP/<searchzip>')
def searchzip(searchzip):
    # Get data from database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchzip])
    test = cursor.rowcount
    if test != 1:
        return searchzip + "was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go %s' % searched

#update zip database Population for a specified zip
@app.route('/updatezipPopulation/<updateZIP> <updatePOPULATION>')
def updatezipPopulation(updateZIP, updatePOPULATION):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZIP])
    test = cursor.rowcount
    if test != 1:
        return updateZIP + " was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", [updatePOPULATION,updateZIP])
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Population=%s", [updateZIP,updatePOPULATION])
        test1 = cursor.rowcount
        if test1 != 1:
            return updateZIP + "  failed to update"
        else:
            return 'Population has been updated successfully for zip: %s' % updateZIP

#update webpage
@app.route('/update',methods = ['POST'])
def update():
       user = request.form['uzip']
       user2 = request.form['uPopulation']
       return redirect(url_for('updatezipPopulation', updateZIP=user, updatePOPULATION=user2))

#search page
@app.route('/search', methods=['GET'])
def search():
       user = request.args.get('szip')
       return redirect(url_for('searchzip', searchzip=user))


#root of web server and gots to template (login.html)
@app.route('/')
def root():
   return render_template('login.html')

#main
if __name__ == '__main__':
   app.run(debug = True)
