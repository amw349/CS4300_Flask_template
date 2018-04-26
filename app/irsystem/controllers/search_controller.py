from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.cosinesim import input_to_tags
from app.irsystem.models.parsers_and_TFidf_setup import process_list_of_jsons
from numpy import linalg as LA
from scipy.sparse.linalg import svds
import os

def serve_jsons():
    path_to_json_dir = os.path.dirname(os.path.abspath(__file__))+'/../../static/json'
    for _, _, filenames in os.walk(path_to_json_dir):
        json_files = [ f for f in filenames if f.endswith("json") ]
        return json_files

profile_lst = serve_jsons()
word_to_int_dict, tag_to_int_dict, int_to_word_dict, int_to_tag_dict, word_TDF,\
tag_TDF, word_inv_idx, tag_inv_idx, post_dict = process_list_of_jsons(profile_lst)

project_name = "#yourPhoto"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('/', methods=['GET', 'POST'])
def search():
	form = request.form
	if request.method == 'POST':
		# location = form.location.data
		# date = form.date.data
		# time = form.time.data
		# people = form.people.data
		content = form["input_query"].content.data
		output = input_to_tags(content)
		# print ("output:", output)
		return render_template('search.html', name=project_name, netids=netids, form=form, output=output)
	return render_template('search.html', name=project_name, netids=netids, form=form)
