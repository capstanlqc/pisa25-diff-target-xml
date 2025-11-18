import pandas as pd
from pathlib import Path
from typing import List, Tuple, Dict
from pprint import pprint as pp
import os
# from xml.dom.pulldom import parse
from xml.dom.minidom import parse, parseString
from lxml import etree
import diff_match_patch as dmp_module
from html_diff import diff
# from Levenshtein import distance as levenshtein_distance
# from rich import print as print
from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from bs4 import BeautifulSoup


def get_locale_counts(locale: str, data: Dict) -> Dict:
    counts = {}
    batches = ["01_COS_SCI-A_N", "02_COS_SCI-B_N", "03_COS_SCI-C_N", "04_QQS_N", "05_QQA_N", "06_COS_LDW_N", "07_COS_XYZ_N", "08_CGA_SCI_N", "11_COS_MAT-A_T", "12_COS_MAT-B_T", "13_COS_REA-A_T", "14_COS_REA-B_T", "15_COS_SCI-A_T", "16_COS_SCI-B_T"]
    for batch in batches:
        counts[batch] = len(data[batch]) if batch in data else 0

    return {
        "locale": locale,
        "total": sum(counts.values()),
        **counts
    }


def export_locale_to_excel(data: Dict, locale: str, output_path: str = None):
    if output_path is None:
        output_path = f"{locale}.xlsx"

    batches = list(data.keys())

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for batch, entries in data.items():

            # convert list of dicts into DataFrame
            df = pd.DataFrame(entries)

            # convert lists (like dmp_diff) to strings for readability
            if "dmp_diff" in df.columns:
                df["dmp_diff"] = df["dmp_diff"].astype(str)

            # clean sheet name to max 31 chars
            safe_name = batch[:31]

            # Write sheet
            df.to_excel(writer, sheet_name=safe_name, index=False)

    print(f"Saved: {output_path}")



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


def get_key_label_pairs(fpath: Path):
    """ Build a dictionary of key-value pairs from XML using lxml. """

    if not fpath.is_file():
        raise FileNotFoundError(f"{fpath} does not exist")

    # lxml parser that recovers from undefined entities
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(fpath, parser)
    root = tree.getroot()

    # find all <text> elements
    node_list = root.findall(".//text")

    result = {}
    for i, node in enumerate(node_list):
        parent = node.getparent()
        key_attr = parent.get("key") if parent is not None else f"unknown_{i}"
        key = f"{key_attr}/{i}"

        # get all text content, join into a single string
        text_content = "".join(node.itertext())
        result[key] = text_content
    # for i, node in enumerate(node_list):
    #     parent = node.getparent()
    #     key_attr = parent.get("key")
    #     key = f"{key_attr}/{i}"

    #     # get inner XML of node (children only)
    #     parts = []

    #     if node.text:
    #         parts.append(node.text)

    #     for child in node:
    #         parts.append(etree.tostring(child, encoding="unicode"))

    #         # include tail text after child
    #         if child.tail:
    #             parts.append(child.tail)

    #     inner_xml = "".join(parts)
    #     result[key] = inner_xml

    return result


def list_xml_files_in_folder(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".xml")]


def get_labels_metadata(common_repo_dpath: Path, batches: List[str]) -> list:

    labels_metadata = []

    for batch in batches:
        batch_dpath = os.path.join(common_repo_dpath, "source", batch)
        for xml_fname in list_xml_files_in_folder(batch_dpath):

            xml_fpath = os.path.join(batch_dpath, xml_fname)
            doc = parse(xml_fpath)
            labels = doc.getElementsByTagName("label")

            for label in labels:
                labels_metadata.append({
                    "file": f"{batch}/{os.path.basename(xml_fname)}",
                    "key": label.getAttribute("key"),
                    "locale_list": label.getAttribute("its:localeFilterList").split(","),
                    "filter_type": label.getAttribute("its:localeFilterType")
                })

    return labels_metadata


def is_included(batch, file, key, locale):

    # iterate through the labels
    label = next((entry for entry in labels_metadata if 
                  entry.get("file") == f"{batch}/{file}" and 
                  entry.get("key") == key), 
                None)

    if label:
        # get the locale filter list and type attributes
        locale_list = label["locale_list"]
        filter_type = label["filter_type"]

        # determine if the locale is included based on the filter type
        if filter_type == 'include':
            return locale in locale_list
        elif filter_type == 'exclude':
            return locale not in locale_list

    # return False if the key is not found
    return False


def check_key_uniqueness(keys):
    pass



def html_to_runs(html_text):
    """Parse <del> and <ins> into runs for openpyxl rich text."""
    runs = []
    soup = BeautifulSoup(html_text, "html.parser")

    for elem in soup.recursiveChildGenerator():
        if elem.name is None:  # text node
            text = elem.string
            if not text or text.strip() == "":
                continue

            parent = elem.parent.name if elem.parent else None

            if parent == "del":
                runs.append({
                    "text": text,
                    "strike": True,
                    "color": "FF0000"
                })
            elif parent == "ins":
                runs.append({
                    "text": text,
                    "color": "00AA00"
                    # underline not supported
                })
            else:
                runs.append({"text": text})
    return runs

def make_rich_text(runs):
    """Convert parsed runs into CellRichText. Only strike and color supported."""
    rich = CellRichText()
    for r in runs:
        font = InlineFont(
            color=r.get("color"),
            strike=r.get("strike", False)
        )
        rich.append(TextBlock(
            text=r["text"],
            font=font
        ))
    return rich

def apply_html_formatting_excel(xlsx_path, column_name="html_diff"):
    """Apply <del> and <ins> formatting (strike/color only) to all sheets."""
    wb = load_workbook(xlsx_path)
    for ws in wb.worksheets:
        # find column index
        headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        if column_name not in headers:
            continue
        col_idx = headers.index(column_name) + 1

        for row in ws.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx):
            cell = row[0]
            val = cell.value
            if not isinstance(val, str) or "<del>" not in val and "<ins>" not in val:
                continue

            runs = html_to_runs(val)
            rich = make_rich_text(runs)
            cell.value = rich

    wb.save(xlsx_path)


if __name__ != "__main__":
    exit("This module is not meant to be imported")

common_dpath = Path("/home/souto/Repos/acer/pisa_2025ms_translation_common")
final_dpath = Path("/home/souto/Repos/acer/pisa_2025ms_translation_final")

not_locales = ["ui-translations", ".git", "translations", "z-qq-keys"]
locale_dpaths = final_dpath.glob("*/") # gebnerator
locales = sorted([d.name for d in locale_dpaths if d.name not in not_locales])

reports = {}
reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
aggregate_data = []

for locale in locales:

    target_locale_dpath = final_dpath / locale
    edited_locale_dpath = final_dpath / "translations" / locale / "batch1"
    
    if not common_dpath.is_dir() or not target_locale_dpath.is_dir() or not edited_locale_dpath.is_dir():
        continue

    batch_dpaths = target_locale_dpath.glob("*") # generator
    batches = sorted([d.name for d in batch_dpaths if d.is_dir()])

    # get labels data outside of looping
    labels_metadata = get_labels_metadata(common_dpath, batches)

    for batch in batches:
        print(f"=== {locale} / {batch} ===")

        batch_dpath = target_locale_dpath / batch
        target_fpaths = batch_dpath.glob("*") # generator
        
        source_dpath = common_dpath / "source" / batch

        for target_fpath in target_fpaths:

            base_fname = target_fpath.name.replace(f"_{locale}", "")
            final_fpath = edited_locale_dpath / base_fname
            source_fpath = common_dpath / "source" / batch / base_fname
            
            if not source_fpath.is_file() or not target_fpath.is_file() or not final_fpath.is_file():
                continue

            source_strings      = get_key_label_pairs(source_fpath)
            target_orig_strings = get_key_label_pairs(target_fpath)
            target_edit_strings = get_key_label_pairs(final_fpath)


            keys = source_strings.keys()

            dmp = dmp_module.diff_match_patch()

            result = [
                {   "key": key,
                    "source_text": source_strings[key],
                    "target_orig": target_orig_strings[key],
                    "target_edit": target_edit_strings[key],
                    # "dmp_diff": dmp.diff_main(target_orig_strings[key], target_edit_strings[key]),
                    "html_diff": diff(target_orig_strings[key], target_edit_strings[key]),
                    "file": base_fname
                }
                for key in keys
                if key in target_edit_strings.keys() and key in target_orig_strings.keys()
                # add to results only if there has been a change
                and target_orig_strings[key] != target_edit_strings[key]
            ]

            if result:
                if locale not in reports:
                    reports[locale] = {}

                reports[locale].update({batch: result})

    if locale in reports:

        data = get_locale_counts(locale, reports[locale])
        aggregate_data.append(data)

        export_locale_to_excel(reports[locale], locale, output_path=reports_dir / f"{locale}_diff.xlsx")
        apply_html_formatting_excel(reports_dir / f"{locale}_diff.xlsx")
                


# for locale, data in reports.items():
#     export_locale_to_excel(data, locale, output_path=f"{locale}_diff.xlsx")
#     apply_html_formatting_excel(f"{locale}_diff.xlsx")


totals_df = pd.DataFrame(aggregate_data)
totals_df.to_excel(reports_dir / "_diff_totals.xlsx", index=False)
print("Saved: _diff_totals.xlsx")