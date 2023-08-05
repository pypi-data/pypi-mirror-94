# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON: 2021/1/21 4:20 PM
# LAST MODIFIED ON:
# AIM:

import unittest
from sentence_spliter.spliter import cut_to_sentences_en
from sentence_spliter.logic_graph_en import long_cuter_en
from sentence_spliter.automata.sequence import EnSequence
from sentence_spliter.automata.state_machine import StateMachine


class test_spliter(unittest.TestCase):
    @unittest.skip('pass')
    def test_white_list(self):
        sentence = "He was a private in the U.S. Army."
        out = cut_to_sentences_en(sentence)
        expected = ["He was a private in the U.S. Army."]
        self.assertEqual(expected, out)

        sentence = "He was a private in the U.S. Army. AHAH!"
        out = cut_to_sentences_en(sentence)
        expected = ['He was a private in the U.S. Army.', ' AHAH!']
        self.assertEqual(expected, out)

        sentence = "Notice that U.S.A. can also be written USA, but U.S. is better with the periods. Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.)."
        out = cut_to_sentences_en(sentence)
        expected = [
            "Notice that U.S.A. can also be written USA, but U.S. is better with the periods.",
            " Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.)."]
        self.assertEqual(expected, out)

        sentence = "U.S.A is the ency of the world"
        out = cut_to_sentences_en(sentence)
        expected = ['U.S.A is the ency of the world']
        self.assertEqual(expected, out)
        sentence = "Notice that U.S.A. can also be written USA."
        out = cut_to_sentences_en(sentence)
        expected = ["Notice that U.S.A. can also be written USA."]
        self.assertEqual(expected, out)

        sentence = "Notice that U.S.A. can also be written USA, but U.S. is better with the periods. Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.)."
        out = cut_to_sentences_en(sentence)
        expected = ['Notice that U.S.A. can also be written USA, but U.S. is better with the periods.',
                    ' Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.).']
        self.assertEqual(expected, out)

        sentence = "Mrs. Gibson, meanwhile, counting her stitches aloud with great distinctness and vigour."
        out = cut_to_sentences_en(sentence)
        expected = ["Mrs. Gibson, meanwhile, counting her stitches aloud with great distinctness and vigour."]
        self.assertEqual(expected, out)

        sentence = "Dr. Who and Who Dr. aren't same person."
        out = cut_to_sentences_en(sentence)
        expected = ["Dr. Who and Who Dr. aren't same person."]
        self.assertEqual(expected, out)

        sentence = ""

    @unittest.skip('pass')
    def test_bracket_quota(self):
        sentence = ' "keep forawrd !!", said he. (but he already tired..)'
        out = cut_to_sentences_en(sentence)
        expected = [' "keep forawrd !!", said he. (but he already tired..)']
        self.assertEqual(expected, out)

        sentence = '“Which, if true, will have been recorded in the muster returns. Does it require a general to inspect the books? A clerk could do that.”'
        out = cut_to_sentences_en(sentence)
        expected = [
            '“Which, if true, will have been recorded in the muster returns. Does it require a general to inspect the books? A clerk could do that.”']
        self.assertEqual(expected, out)

    @unittest.skip('pass')
    def test_dialogue(self):
        sentence = '"you are all lying !" "I am won!!!","Joe, you know I won!!!"'
        out = cut_to_sentences_en(sentence)
        expected = ['"you are all lying !" "I am won!!!","Joe, you know I won!!!"']
        self.assertEqual(expected, out)

        sentence = '"you are all lying !""I am won!!!","Joe, you know I won!!!"'
        out = cut_to_sentences_en(sentence)
        expected = ['"you are all lying !""I am won!!!","Joe, you know I won!!!"']
        self.assertEqual(expected, out)

        sentence = '"you are all lying lying lying and lying!"     "I am won!!!","Joe, you know I won!!!"'
        out = cut_to_sentences_en(sentence)
        expected = ['"you are all lying lying lying and lying!"     ', '"I am won!!!","Joe, you know I won!!!"']
        self.assertEqual(expected, out)

        sentence = '"you are all lying lying lying and lying!""I am won!!!","Joe, you know I won!!!"'
        out = cut_to_sentences_en(sentence)
        expected = ['"you are all lying lying lying and lying!"', '"I am won!!!","Joe, you know I won!!!"']
        self.assertEqual(expected, out)

        sentence = '“This presupposes that you have disposed of the enemy’s shore battery?” “It does, sir.” “A joint attack, eh?”'
        out = cut_to_sentences_en(sentence)
        expected = ['“This presupposes that you have disposed of the enemy’s shore battery?” ',
                     '“It does, sir.” “A joint attack, eh?”']
        self.assertEqual(expected, out)

    @unittest.skip('pass')
    def test_short_stence(self):
        sentence = '1. 2 3 4. 1 2 3 4 5 6. 1 2 3 4 5 6 7 8.'
        out = cut_to_sentences_en(sentence)
        expected = ['1. 2 3 4. 1 2 3 4 5 6.', ' 1 2 3 4 5 6 7 8.']
        self.assertEqual(expected, out)

    @unittest.skip('pass')
    def test_long_cutter(self):
        # __long_machine_en = StateMachine(long_cuter_en(max_len=9))
        #
        # sentence = '"1 2 3 4 5 6 7?" cried Henry'
        # m_input = EnSequence(sentence)
        # __long_machine_en.run(m_input)
        # out = m_input.sentence_list()
        # m_input.sentence_list()
        # expected = ['"1 2 3 4 5 6 7?"', ' cried Henry']
        # self.assertEqual(expected, out)
        #
        # sentence = '1 3 5 6 7 8 9 10, where 1 2 3 4.'
        # m_input = EnSequence(sentence)
        # __long_machine_en.run(m_input)
        # out = m_input.sentence_list()
        # m_input.sentence_list()
        # expected = ['1 3 5 6 7 8 9 10, ', 'where 1 2 3 4.']
        # self.assertEqual(expected, out)

        sentence = "\"What would a stranger do here, Mrs. Price?\" he inquired angrily, remembering, with a pang, that certain new, unaccountable, engrossing emotions had quite banished Fiddy from his thoughts and notice, when he might have detected the signs of approaching illness, met them and vanquished them before their climax."
        __long_machine_en = StateMachine(long_cuter_en(max_len=9, min_len=3))
        m_input = EnSequence(sentence)
        __long_machine_en.run(m_input)
        for v in m_input.sentence_list():
            print(v)

    @unittest.skip('pass')
    def test_sample2(self):
        # sentence = '. . . . We now commend you to the Supream being Sincerely praying him to preserve you and the Forces under your Command in health and safety, & Return you Crowned with Victory and Laurels.'
        #
        # out = cut_to_sentences_en(sentence)
        # for v in out:
        #     print(v + "\n")

        sentence = '978-0-06-196963-8 EPub Edition © 2010 ISBN: 9780062013842 10 11 12 13 14 OFF/RRD 10 9 8 7 6 5 4 3 2 1 About the Publisher Australia HarperCollins Publishers (Australia) Pty. Ltd. 25 Ryde Road (PO Box 321) Pymble, NSW 2073, Australia http://www.harpercollinsebooks.com.au Canada HarperCollins Canada 2 Bloor Street East - 20th Floor Toronto, ON, M4W, 1A8, Canada http://www.harpercollinsebooks.ca New Zealand HarperCollinsPublishers (New Zealand) Limited P.O. Box 1 Auckland, New Zealand'

        __long_machine_en = StateMachine(long_cuter_en(max_len=9))
        m_input = EnSequence(sentence)
        out = __long_machine_en.run(m_input)
        for v in out:
             print(v + "\n")

    @unittest.skip('pass')
    def test_demo(self):
        # paragraph = "A long time ago. there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
        # __long_machine_en = StateMachine(long_cuter_en(min_len=4))
        # m_input = EnSequence(paragraph)
        # __long_machine_en.run(m_input)
        # print(m_input.sentence_list())

        paragraph = "A long time ago. There is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
        __long_machine_en = StateMachine(long_cuter_en(max_len=11, min_len=3))
        m_input = EnSequence(paragraph)
        __long_machine_en.run(m_input)
        print(m_input.sentence_list())