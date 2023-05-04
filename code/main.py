from pprint import pprint as pp
import os
# from xml.dom.pulldom import parse
from xml.dom.minidom import parse, parseString
import diff_match_patch as dmp_module
from html_diff import diff
from Levenshtein import distance as levenshtein_distance

# constants

locale = "fr-ZZ"

namespaces = {
	"": "http://www.imsglobal.org/xsd/imsqti_v2p2",
	"qti": "http://www.imsglobal.org/xsd/imsqti_v2p2",
	"its": "http://www.w3.org/2005/11/its",
	"xsi": "http://www.w3.org/2001/XMLSchema-instance",
	"m": "http://www.w3.org/1998/Math/MathML",
	"qh5": "http://www.imsglobal.org/xsd/imsqtiv2p2_html5_v1p0",
	"xi": "http://www.w3.org/2001/XInclude"
}

# functions

def calculate_levenshtein_distance(str_1, str_2):
    """
    The Levenshtein distance is a string metric for measuring the difference
    between two sequences. It is calculated as the minimum number of
	single-character edits necessary to transform one string into another.
    """
    pass


def get_key_label_pairs(fpath):
	""" Build a list of key-value dictionaries """

	document = parse(fpath) # xml.dom.minidom method

	# getElementsByTagNameNS if namespaces
	node_list = document.getElementsByTagName("text")

	return {
		node.parentNode.getAttribute("key"): "".join(child.toxml()
		for child in node.childNodes) for node in node_list
	}


def check_key_uniqueness(keys):
	pass



if __name__ == "__main__":

	# input arguments
	omtprj0_dpath = "repos/pisa_2025ft_translation_common" # @todo: abs path
	omtprj1_dpath = "repos/pisa_2025ft_translation_fr-ZZ_reconciliation"
	omtprj2_dpath = "repos/pisa_2025ft_translation_fr-ZZ_lead-reconciliation-review"
	batch = "03_COS_SCI1_N"

	source_dpath = os.path.join(omtprj0_dpath, "source", batch)
	tgt_orig_dpath = os.path.join(omtprj1_dpath, "target", batch)
	tgt_edit_dpath = os.path.join(omtprj2_dpath, "target", batch)

	source_files = [f for f in os.listdir(source_dpath) if f.endswith(".xml")]

	for file in source_files:

		source_fpath 	  	= os.path.join(source_dpath, file)
		target_orig_fpath	= os.path.join(tgt_orig_dpath, file.replace(".xml", f"_{locale}.xml"))
		target_edit_fpath 	= os.path.join(tgt_edit_dpath, file.replace(".xml", f"_{locale}.xml"))

		source_strings 		= get_key_label_pairs(source_fpath)
		target_orig_strings = get_key_label_pairs(target_orig_fpath)
		target_edit_strings = get_key_label_pairs(target_edit_fpath)

		# shall we check that keys are unique?
		keys = source_strings.keys()

		dmp = dmp_module.diff_match_patch()
		#diff = dmp.diff_main(target_orig_strings[key], target_edit_strings[key])
		# Result: [(-1, "Hell"), (1, "G"), (0, "o"), (1, "odbye"), (0, " World.")]
		# dmp.diff_cleanupSemantic(diff)
		# Result: [(-1, "Hello"), (1, "Goodbye"), (0, " World.")]
		#print(diff)

		result = [
			{	"key": key,
				"source_text": source_strings[key],
				"target_orig": target_orig_strings[key],
				"target_edit": target_edit_strings[key],
				"dmp_diff": dmp.diff_main(target_orig_strings[key], target_edit_strings[key]),
				"html_diff": diff(target_orig_strings[key], target_edit_strings[key]),
				"file": file
			}
			for key in keys
			if key in target_edit_strings.keys() and key in target_orig_strings.keys()
		]

		# pp(result) # pretty print
		print(result)
