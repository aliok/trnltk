"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
class TextTokenizer(object):
    """
    Splits the text into words.
    """

    PUNC_CHARS = [u'.', u',', u',', u'..', u'...', u'-', u'!', u'?', u':', u'-', u'"', u'(', u')']     #  " ' " is not included

    def tokenize(self, text):
        """
        @type text: str or unicode
        @rtype list or None
        """

        text = text.strip()

        text = self._insert_spaces_for_punc_chars(text)

        text = self._replace_all_space_with_whitespace(text)

        tokens = text.split(u' ')

        tokens = filter(lambda x : x, tokens)

        return tokens

    def _insert_spaces_for_punc_chars(self, text):
        # insert space before punc chars. except:

        # 1. Dot comes after number : "3."
        # 2. Punc char comes after punc char : "..." (except comma after dot)
        # 3. The apostrophe used in a proper name : "Ahmet'in"  # apostrophe is not a punc char anymore
        # 4. The quoted stuff for emphasis : 'Cok "aptal"di o adam' #TODO
        # 5. Punc chars between numbers : "5:20", "5.123.456", "5,12" (but not "5, 6, 7")

        # use a string builder(?). add chars directly, except we need to insert space in front of them.
        # with a random access list(string builder), we can check the last char for the exception cases described above

        builder = u''
        for char_index, char in enumerate(text):
            if not char in self.PUNC_CHARS:
                builder = builder + char
            else:
                if not builder:
                    continue

                prev_char = builder[-1]
                next_char = None if char_index+1>=len(text) else text[char_index+1]

                add_space = True

                # check case #1
                if prev_char and prev_char.isdigit() and char == u'.':
                    add_space = False

                # check case #2
                elif prev_char in self.PUNC_CHARS:
                    if char==u',' and prev_char==u'.':
                        add_space = True
                    else:
                        add_space = False

                # check case #5
                elif prev_char.isdigit() and next_char and next_char.isdigit():
                    add_space = False

                if add_space:
                    builder += u' '
                builder = builder + char

        return builder

    def _replace_all_space_with_whitespace(self, text):

        """
        @type text: str or unicode
        """
        text = text.replace(u'\n', u' ')
        text = text.replace(u'\t', u' ')
        text = text.replace(u'\r', u' ')

        return text