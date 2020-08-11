# -*- coding: utf-8 -*-
# This code is copy and modify from https://github.com/keithito/tacotron.
"""Perform preprocessing and raw feature extraction."""

import re
import os

import numpy as np
import soundfile as sf

from tensorflow_tts.utils import cleaners

"""
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
"""

from jamo import h2j, j2h
from jamo.jamo import _jamo_char_to_hcj

from tensorflow_tts.utils.korean import symbols, _symbol_to_id, _id_to_symbol

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")


class KSSProcessor(object):
    """KSS processor."""

    def __init__(
        self, data_dir, cleaner_names, metadata_filename="transcript.v.1.2.txt"
    ):
        self.data_dir = data_dir
        self.cleaner_names = cleaner_names

        self.speaker_name = "kss"
        if data_dir:
            with open(os.path.join(data_dir, metadata_filename), encoding="utf-8") as f:
                self.items = [self.split_line(data_dir, line, "|") for line in f]

    def split_line(self, data_dir, line, split):
        wav_file, _, text_norm, _, _ = line.strip().split(split)
        wav_path = os.path.join(data_dir, wav_file)
        return text_norm, wav_path, self.speaker_name

    def get_one_sample(self, item):
        text, wav_file, speaker_name = item

        # normalize audio signal to be [-1, 1], soundfile already norm.
        audio, rate = sf.read(wav_file)
        audio = audio.astype(np.float32)

        # convert text to ids
        text_ids = np.asarray(self.text_to_sequence(text), np.int32)

        sample = {
            "raw_text": text,
            "text_ids": text_ids,
            "audio": audio,
            "utt_id": os.path.split(wav_file)[-1].split(".")[0],
            "speaker_name": speaker_name,
            "rate": rate,
        }

        return sample

    def text_to_sequence(self, text):
        global _symbol_to_id

        sequence = []
        # Check for curly braces and treat their contents as ARPAbet:
        while len(text):
            m = _curly_re.match(text)
            if not m:
                sequence += _symbols_to_sequence(
                    _clean_text(text, [self.cleaner_names])
                )
                break
            sequence += _symbols_to_sequence(
                _clean_text(m.group(1), [self.cleaner_names])
            )
            sequence += _arpabet_to_sequence(m.group(2))
            text = m.group(3)
        return sequence


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbols):
    return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(["@" + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != "_" and s != "~"
