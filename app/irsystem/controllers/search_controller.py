from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.cosinesim import input_to_tags

project_name = "#yourPhoto"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('/', methods=['GET', 'POST'])
def search():
	print ("here")
	form = request.form
	if request.method == 'POST':
		print ("Search function called.........")
		print ("request:", request)
		print ("request form:", request.form)
		print ("request form input:", request.form['input_query'])
		input_query = request.form['input_query']
		output = input_to_tags("", input_query)
		return render_template('search.html', name=project_name, netids=netids, form=form, output=output)
	return render_template('search.html', name=project_name, netids=netids, form=form)
