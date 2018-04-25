from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.cosinesim import input_to_tags
from app.irsystem.models.parsers_and_TFidf_setup import process_list_of_jsons
from numpy import linalg as LA
from scipy.sparse.linalg import svds
import os

def json_list():
    path_to_json_dir = os.path.dirname(os.path.abspath(__file__))+'/../../static/json'
    for _, _, filenames in os.walk(path_to_json_dir):
        return filenames

profile_lst = json_list()
word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(profile_lst)

project_name = "How to Get More Likes"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('/', methods=['GET', 'POST'])
def search():
	query = request.args # TODO: change to appropriate input names and concatanate query for inputs filled
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		# location = form.location.data
		# date = form.date.data
		# time = form.time.data
		# people = form.people.data
		content = form.content.data
		output = input_to_tags("", content, word_to_int_dict, post_dict, word_TDF)
		return render_template('search.html', name=project_name, netids=netids, form=form, output=output)
	return render_template('search.html', name=project_name, netids=netids, form=form)

class InputForm(Form):
	location = StringField("Where is the picture taken?")
	date = DateField("When was the picture taken?")
	time = StringField("At what time was the picture taken?")
	people = StringField("Who's in the picture?")
	content = StringField("What's happening in the picture?")
