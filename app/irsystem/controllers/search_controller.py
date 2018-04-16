from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.jaccard import input_to_tags

project_name = "How to Get More Likes"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('/', methods=['GET', 'POST'])
def search():
	query = request.args # TODO: change to appropriate input names and concatanate query for inputs filled
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		location = form.location.data
		date = form.date.data
		time = form.time.data
		people = form.people.data
		content = form.content.data
		output = input_to_tags(location, [date.strftime('%m-%d-%y'), time, people, content])
		return render_template('search.html', name=project_name, netids=netids, form=form, output=output)
	return render_template('search.html', name=project_name, netids=netids, form=form)

class InputForm(Form):
	location = StringField("Where is the picture taken?")
	date = DateField("When was the picture taken?")
	time = StringField("At what time was the picture taken?")
	people = StringField("Who's in the picture?")
	content = StringField("What's happening in the picture?")
