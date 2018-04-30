from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "#yourPhoto"
netids = ["Jake Bareket (jhb334)", "Anya Chopra (ac948)", "Michael Herbstman (mh856)", "David Miron (dm585)", "Alexandra Ward (amw349)"]

@irsystem.route('/', methods=['GET', 'POST'])
def index():
	print ("splash")
	return render_template('splash.html', name=project_name, netids=netids)
