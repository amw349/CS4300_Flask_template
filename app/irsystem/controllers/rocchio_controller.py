from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.good_cosinesim import input_to_tags, statistics_top_hashtags
from app.irsystem.models.parsers_and_TFidf_setup import process_list_of_jsons

@irsystem.route('rocchio', methods=['GET', 'POST'])
def rocchio():
    print ("Rocchio...........")
    form = request.form
    form_submitted = False
    print (request.data)
    if request.method == 'POST':
        print ("Form submitted...")
        form_submitted = True
        input_query = request.form['input_query']
        # rochio(input_query,list_of_disliked_hashtags, list_of_liked_hashtags, word_to_int_dict, tag_inv_idx)
        print ("Seach input:", input_query)
        output = [("testing1", .90), ("testing2", .84), ("testing3", .73), ("testing4", .64), ("testing5", .56), ("testing6", .53), ("testing7", .3), ("testing8", .21), ("testing9", .1), ("testing10", .08)]
        # output = input_to_tags(input_query, TF_IDF_matrix, word_to_int_dict, post_dict, int_to_word_dict, good_tags)
        # statistics = statistics_top_hashtags(output)
        return render_template('search.html', name=project_name, netids=netids, form=form, form_submitted_status=form_submitted, output=output)
    return render_template('search.html', name=project_name, netids=netids, form=form)
