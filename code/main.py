from pprint import pprint as pp
import os
# from xml.dom.pulldom import parse
from xml.dom.minidom import parse, parseString
import diff_match_patch as dmp_module
from html_diff import diff
# from Levenshtein import distance as levenshtein_distance
from rich import print as print

# constants

locale = "zh-CN"

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


def is_included(file, key, locale):

    # parse the XML file
    doc = parse(file)

    # find all <label> elements
    labels = doc.getElementsByTagName("label")

    # iterate through the labels
    for label in labels:
        # check if the 'key' attribute matches
        if label.getAttribute("key") == key:
            # get the locale filter list and type attributes
            locale_list = label.getAttribute("its:localeFilterList").split(",")
            filter_type = label.getAttribute("its:localeFilterType")

            # determine if the locale is included based on the filter type
            if filter_type == 'include':
                return locale in locale_list
            elif filter_type == 'exclude':
                return locale not in locale_list

    # return False if the key is not found
    return False


def check_key_uniqueness(keys):
    pass

if __name__ == "__main__":

    # input arguments
    orig_dname = "pisa_2025ms_translation_common" # @todo: abs path
    xlat_dname = "pisa_2025ms_translation_zh-CN_qqs-prepare-files"
    edit_dname = "pisa_2025ms_translation_zh-CN_qqs-verification"

    batches = ["04_QQS_N"]
    # parent_dpath = ["/", "home", "souto", "Repos", "ACER-PISA-2025-FT"]
    parent_dpath = "/media/souto/257-FLASH/dev/capstanlqc/pisa25-diff-target-xml/data".split("/")
    parent_dpath[0] = "/"

    for batch in batches:
        source_dpath      = os.path.join(*parent_dpath, orig_dname, "source", batch)
        target_orig_dpath = os.path.join(*parent_dpath, xlat_dname, "target", batch)
        target_edit_dpath = os.path.join(*parent_dpath, edit_dname, "target", batch)

        if not os.path.exists(source_dpath):
            print(f"{batch=} not found")
            continue

        source_files = [f for f in os.listdir(source_dpath) if f.endswith(".xml")]

        for file in source_files:

            source_fpath           = os.path.join(source_dpath, file)
            target_orig_fpath    = os.path.join(target_orig_dpath, file.replace(".xml", f"_{locale}.xml"))
            target_edit_fpath     = os.path.join(target_edit_dpath, file.replace(".xml", f"_{locale}.xml"))

            if not os.path.exists(target_orig_fpath) or not os.path.exists(target_edit_fpath):
                continue

            source_strings         = get_key_label_pairs(source_fpath)
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
                {    "key": key,
                    "source_text": source_strings[key],
                    "target_orig": target_orig_strings[key],
                    "target_edit": target_edit_strings[key],
                    "dmp_diff": dmp.diff_main(target_orig_strings[key], target_edit_strings[key]),
                    "html_diff": diff(target_orig_strings[key], target_edit_strings[key]),
                    "file": file
                }
                for key in keys
                if key in target_edit_strings.keys() and key in target_orig_strings.keys()
                # add to results only if there has been a change
                and target_orig_strings[key] != target_edit_strings[key]
                # add to results only if the label is included for this locale
                and is_included(os.path.join(source_dpath, file), key, locale)
            ]

            print(result)