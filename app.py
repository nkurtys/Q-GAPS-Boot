from flask import Flask, render_template, request, redirect

import sqlite3
from assets.scripts import functions

app = Flask(__name__)

@app.route('/')
def index():
#Access Database of fav tables
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

#Delete Datatable
    to_delete_tablename = request.args.get("button-id", "")
    if to_delete_tablename:
        functions.deleteTable(to_delete_tablename)

#Display all mastodon tables in tab
    names = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()
    listOfTables = []
    if len(names) == 0 :
        return render_template('index.html', title='Home',tablenames=False, 
                            listOfTables=listOfTables)
    else:
        for tablename in names:
            listOfLists = []
            listOfLists.append(tablename[0])
            listOfLists.append(cursor.execute("SELECT * FROM " + tablename[0]).fetchall())
            listOfTables.append(listOfLists)

#Display all livivo tables in tab
    namesL = cursor.execute("SELECT name FROM sqlite_schema WHERE type='tableL' ORDER BY name").fetchall()
    listOfLTables = []
    if len(namesL) == 0 :
        return render_template('index.html', title='Home',tablenames=False, 
                            listOfTables=listOfTables, listOfLTables=listOfLTables)
    else:
        for tablenameL in namesL:
            # if tablename[0] == "qfever":
            #     continue
            listOfLLists = []
            listOfLLists.append(tablenameL[0])
            listOfLLists.append(cursor.execute("SELECT * FROM " + tablenameL[0]).fetchall())
            listOfLTables.append(listOfLLists)
        cursor.close()
        connection.close()


    return render_template('index.html', title='Home',tablenames=names, 
                                listOfTables=listOfTables)


@app.route('/search')
def search():
    #change sdave to save 60 toots 

    #search toots for query and display it on the website
    query = request.args.get("query", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    #save keyword as table
    tablename = request.args.get("tablename", "")
    checkMastodon = request.args.get("btncheckM", "")
    checkLivivo = request.args.get("btncheckL", "")

    if query:
        #search toots for query and display it on the website
        result = functions.searchInstance(instance="mastodon.social", query=query, start_date=start_date, end_date=end_date)
    elif tablename:
        #setup new table in database
        result = functions.saveDatabase(table=tablename, query=tablename, M=bool(checkMastodon), L=bool(checkLivivo))
    else:
        result = False
        print("No query")

    return render_template('search.html', title='Search', posts=result, query=query)
        

#generate page showing tablesd
@app.route("/tables/")
@app.route("/tables/<tablename>")
def make_page(tablename):
    #Access Database of fav tables
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    #fetch all posts relating to tablename
    try: 
        posts = cursor.execute("SELECT * FROM " + tablename).fetchall()
    except: 
        posts = False
    try:
        postsL = cursor.execute("SELECT * FROM " + tablename + "L").fetchall()
    except:
        postsL = False

    cursor.close()
    connection.close()
    return render_template("page.html", tablename=tablename, posts=posts, postsL=postsL)


@app.route("/create")
def create():
    return redirect("/search")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
 #flag debug False in production
