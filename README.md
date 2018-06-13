# Insight DevOps Engineering Systems Puzzle

# Note: the mentioned bugs are numbered 

# My notes and thoughts 


1) switched 80:8080 to 8080:80 correcting the porting of the nginx to a request

A slight improvement over “This site can’t be reached, localhost refused to connect.” which led me to a “502 Bad gateway” instead. When I printed out the container list for db,nginx and the flask app; In the log list for nginx there was a “failed (111: No route to host) while connecting to upstream” which suggested to me some connection/port issue was between the the nginx container (which depends upon the flaskapp.conf file) or app.py itself. I initially tried to tweek the flaskapp.conf trying to use the “upstream option” but was not successful. At face value the flask app.conf file was aware of where to send incoming requests by the line “proxy_pass http://flaskapp:5001;”, but there has to be something which accepts such requests. After some web surfing, I noticed that no port was specified in app.py . Looking at example applications I saw where the port needed to be specified (app.run(host='0.0.0.0', port=5001, debug=True)). This corrected the second bug.

2) changed app.run(host='0.0.0.0') to app.run(host='0.0.0.0', port=5001, debug=True)

Now entering localhost:8080 into the browser led me to the next step —> I could now interact with the flaskapp and enter items to be saved to the database. When I press “Enter Item” I am rerouted to success page which should display the contents of the database but instead displays an empty list. A new bug has emerged…My initial thought was that the output was not coded correctly and that upon rerouting, a NEW html file needed to be specified to properly display the contents of the database. In order to implement this I attempted a simple routine I found in an online resource which seemed to give a reasonable solution. I opened a new html file in templates/results.html . This would be the new html file I mentioned a moment ago. I pip installed a library called flask_table (just added to the requirement.txt file) which would allow me to generate a nice and neat table for displaying the contents of the database with NO nice features like edit/delete etc. This new library and table class are in tables.py which just contains
from flask_table import Table, Col

class Results(Table):
    type_of_item = Col('Item')
    number_items = Col('# of items')
    description = Col('description')
    date_added =('Date added')

In app.py  header I added #from tables import Results I  added the following below @app.route("/success")

    table = Results(results)
    table.border = True
    return render_template('results.html', table=table)

This generates an instance of the Results class which organizes each entry into the appropriate column. Despite this optimism I did not gain anything from this and was again greeted by “This site can’t be reached, localhost refused to connect.” For some strange reason (of which I can not yet resolve ) the flaskapp container was not generated. Back to square one…. I am suspecting that the data base is not sending its contents up the ladder …. that is either

db —x—> flaskapp ——> nginx
db ——> flaskapp —x—> nginx
db —x—> flaskapp —x—> nginx

Since I expect the list to look something like 

[  (item1.name, item1.quantity, item1.description, date_added), 
   (item2.name, item2.quantity, item2.description, date_added), 
   (item3.name, item3.quantity, item3.description, date_added),
(………)  ] 

but instead get an empty list which still accounts for the proper number of items 

[, , , , , , , , , , , ,]

The source code of the html file gives

[<models.Items object at 0x7fbc2c37a438>, <models.Items object at 0x7fbc2c37a4e0>, <models.Items object at 0x7fbc2c37a588>, <models.Items object at 0x7fbc2c37a630>,. . . . .]

So lets traceback and see how the items are being entered from which file and passed along until it is finally in models.Items

First the code initializes a ItemForm() object which is basically the homepage of the application

Next we call the Items object which basically reads in what was entered in ItemForm(). for example id which is a class member of ‘Items’ takes the value of a string which was entered in ItemForm. This is why in the Items object we have name=form.name.data. Basically we just created an instance of the Class Items where each of the members take on a value we specified on the home page.


