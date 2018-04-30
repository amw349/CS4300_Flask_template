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
	print ("index/search")
	form = request.form
	if request.method == 'POST':
		print ("form submitted.........")
		print ("request:", request)
		print ("request form:", request.form)
		print ("request form input:", request.form['input_query'])
		input_query = request.form['input_query']
		# output = input_to_tags(input_query, word_TDF, word_to_int_dict, post_dict)
		return render_template('search.html', name=project_name, netids=netids, form=form, output=["#1", "#1", "#3", "#4", "#5","#6", "#7", "#8", "#9", "#10"])
	return render_template('search.html', name=project_name, netids=netids, form=form)
