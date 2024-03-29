from format_otr.utils import get_json_from_file, parse_html, get_all_timestamps, get_syllable_count
from pathlib import Path
import sys


def get_text_between(start, end):
    text = ""
    tag = start.next_element.next_element
    while tag != end:
        if tag.name is None:
            text += tag.text
        tag = tag.next_element
    return text


def get_text_till_end(start):
    text = ""
    tag = start.next_element.next_element
    while tag:
        if tag.name is None:
            text += tag.text
        tag = tag.next_element
    return text


def get_txt(file_path_to_otr):
    otr_file = Path(file_path_to_otr)
    json_otr = get_json_from_file(otr_file)
    soup = parse_html(json_otr["text"])
    timestamps = get_all_timestamps(soup)
    txt = ""
    for start, end in zip(timestamps, timestamps[1:]):
        txt += f"{start.string}, {get_syllable_count(get_text_between(start, end).strip())}, {get_text_between(start, end).strip()}\n"
    txt += f"{timestamps[-1].string}, {get_syllable_count(get_text_till_end(timestamps[-1]).strip())}, {get_text_till_end(timestamps[-1]).strip()}"
    # \xa0 is non-breaking space. Replace it with space.
    txt = txt.replace("\xa0", " ")
    return txt


def main_cli():
    if len(sys.argv) > 1 and sys.argv[1][-4:] == ".otr":
        print(get_txt(sys.argv[1]))
