# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang
# CREATED ON: 2020/8/7 3:54 PM
# LAST MODIFIED ON:
# AIM:
from abc import ABC
import re
from typing import Tuple
from loguru import logger

from .abc import Operation
from .sequence import StrSequence, EnSequence
from . import condition
from .weights_list import weights as cut_weights
import copy


class Indolent(Operation):
    def __init__(self, symbols: dict, name: str = None):
        super(Indolent, self).__init__('Indolent' if not name else name, symbols)

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_candidate()
        return state


class Normal(Operation):
    def __init__(self, symbols: dict):
        super(Normal, self).__init__('Normal', symbols)

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_sentence_list()
        return state


class CutPreIdx(Operation):
    def __init__(self, symbols: dict):
        super(CutPreIdx, self).__init__('CutPreIdx', symbols)

    def operate(self, state: StrSequence) -> StrSequence:

        if self.symbols['quotation_left'].match(state.current_value):
            state.quota_left = state.quota_left - 1 if state.quota_left > 0 else 1
        if self.symbols['quotation_en'].match(state.current_value):
            state.quota_en = state.quota_en - 1 if state.quota_en > 0 else 1
        state.v_pointer -= 1
        state.add_to_sentence_list()
        return state


class LongHandler(Operation):
    def __init__(self, symbols: dict, hard_max: int = 300):
        super(LongHandler, self).__init__('LongHandler', symbols)
        self.is_end_symbol = condition.IsEndSymbolCN(symbols)
        self.is_comma = condition.IsComma(symbols)
        self.is_book_close = condition.IsBookClose(symbols)
        self.is_barcket_close = condition.IsBracketClose(symbols)
        self.is_right_quota = condition.IsRightQuotaZH()

        self.hard_max = hard_max

    def operate(self, state: StrSequence) -> StrSequence:
        # new_candidate = []
        # - step 1. end_symbol 过滤
        temps_state = copy.copy(state)
        for i in range(temps_state.sentence_start, temps_state.v_pointer - 1)[::-1]:
            temps_state.v_pointer = i
            if self.is_right_quota(temps_state) or (
                    self.is_end_symbol(temps_state) and self.is_book_close(temps_state)):
                cut_id = i
                break
        else:
            temps_state = copy.copy(state)
            # - step 2. comma 过滤
            for i in range(temps_state.sentence_start, temps_state.v_pointer - 1)[::-1]:  # enumerate(state.candidate):
                temps_state.v_pointer = i
                if self.is_comma(temps_state):
                    cut_id = i
                    break
            else:
                cut_id = state.sentence_start + self.hard_max - 1
        if cut_id > state.v_pointer:
            # -- step 3. run forward -- #
            while state.v_pointer < state.length and not self.is_end_symbol(state):
                state.v_pointer += 1
        else:
            state.v_pointer = cut_id

        return state


class ShortHandler(Operation):

    def __init__(self, symbols: dict):
        super(ShortHandler, self).__init__('ShortHandler', symbols)

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_candidate()
        return state


class LongHandlerEN(Operation):
    def __init__(self, symbols: dict, min_sentence_length: int = 5):
        super(LongHandlerEN, self).__init__('LongHandlerEN', symbols)
        self.is_end_symbol = condition.IsEndSymbolCN(symbols)
        self.is_comma = condition.IsComma(symbols)
        self.is_book_close = condition.IsBookClose(symbols)
        self.is_barcket_close = condition.IsBracketClose(symbols)
        self.is_right_quota = condition.IsRightQuotaEn(symbols)
        self.not_in_white_list = condition.NotInWhitelistDotEn()
        self.is_next_with_space = condition.IsNextWithSpace(symbols)
        self.min_sentence_length = min_sentence_length
        self.space = self.symbols['all_symbols']
        self.blank = re.compile('\r')

        # --- build weigths dict -- #
        weights = cut_weights.splitlines()
        self.weights = dict()
        self.max_key_size = 1
        for v in weights:
            if not v:
                continue
            v = v.split()
            sym = v[0]
            word = ' '.join(v[1:-1])
            if (len(v) - 2) > self.max_key_size:
                self.max_key_size = len(v) - 2
            w = int(v[-1])
            w = int(w)
            self.weights[sym + ' ' + word] = w

        # self.weights = {k: i for k, i in sorted(self.weights.items(), key=lambda x: x[1])}

    def operate(self, state: EnSequence) -> EnSequence:
        temps_state = copy.copy(state)
        cut_id, dialog_success = self.dialog_handler(temps_state)
        if dialog_success:
            org_pointer = state.v_pointer
            state.v_pointer = min(cut_id + 1, state.length)
            state.add_to_sentence_list()
            state.v_pointer = org_pointer
            return state
        else:
            cut_id, comma_success = self.comma_weights(temps_state)
            if comma_success:
                org_pointer = state.v_pointer
                state.v_pointer = min(cut_id + 1, state.length)
                state.add_to_sentence_list()
                state.v_pointer = org_pointer
                return state
        return state

    def comma_weights(self, state: EnSequence) -> Tuple[int, bool]:
        # -- traverse all elements to find all comma -- #
        max_score = -1
        best_i = -1
        length = state.v_pointer - state.sentence_start
        half_len = length // 2
        sub_len = 0
        best_sub_len = 0
        for idx, i in enumerate(range(state.sentence_start + 1, state.v_pointer - 1)):
            value = state[i]
            if not self.space.match(state[i]):
                sub_len += 1
            if value in [':', '：'] and sub_len > self.min_sentence_length and self.blank.match(state[i + 1][0]):
                return i, True
            if value == ',':
                # -- 首字母大写优先切分 -- #
                if state[min(i + 2, length)][0].isupper():
                    best_i = i
                    max_score = 10
                    best_sub_len = sub_len
                else:
                    # -- 在权重层里寻找合理的切句位置 -- #
                    for n_words in range(self.max_key_size):
                        key = ' '.join([state[min(i + ii * 2, length)].lower() for ii in range(n_words + 2)])
                        postion_penalty = 1 - abs(idx - half_len) / half_len
                        weight = self.weights.get(key, 5) / 10 + postion_penalty
                        # weight = postion_penalty
                        if weight > max_score:
                            best_i = i
                            max_score = weight
                            best_sub_len = sub_len
        if max_score > 0 and best_sub_len > self.min_sentence_length:
            return best_i, True
        else:
            return best_i, False

    def dialog_handler(self, state: EnSequence) -> Tuple[int, bool]:
        org_pointer = state.v_pointer
        sub_len = 0
        for i in range(state.sentence_start + 1, state.v_pointer - 1):
            state.v_pointer = i
            if not self.space.match(state[i]):
                sub_len += 1
            if self.is_next_with_space(state) and self.is_end_symbol(state) and self.not_in_white_list(
                    state) and sub_len > self.min_sentence_length:
                state.v_pointer = org_pointer
                return i, True
            if self.is_right_quota(state):
                state.v_pointer = org_pointer
                return i, True
        else:
            state.v_pointer = org_pointer
            return -1, False


class EndState(Operation):
    def __init__(self, symbols: dict):
        super(EndState, self).__init__('EndState', symbols)

    def operate(self, state: StrSequence) -> StrSequence:
        if state.sentence_list and state.sentence_start >= state.length or state.length == 0:
            return state
        else:
            state.add_to_sentence_list()
            return state


# =========================== #
#      Special Condition      #
# =========================== #

class SpecialOperation(Operation, ABC):
    pass
