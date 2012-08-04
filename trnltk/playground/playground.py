# coding=utf-8

def parse_context_free(word_str, syntactic_category=None, secondary_syntactic_category=None):
    pass

# yapacagimi, yapacagimi -> true
def concordance_full_word(full_word, syntactic_category=None, secondary_syntactic_category=None):
    pass

# kitabimi, kitab -> true
def concordance_root(root, syntactic_category=None, secondary_syntactic_category=None):
    pass

# kitabimi, kitap -> true
def concordance_lemma(lemma, syntactic_category=None, secondary_syntactic_category=None):
    pass

# yapacagimi, yapacak -> true
def concordance_transition_word(transition_word, syntactic_category=None, secondary_syntactic_category=None):
    pass

# yapacagimi, yapacag => true
def concordance_transition_matched_word(transition_matched_word, syntactic_category=None, secondary_syntactic_category=None):
    pass



def print_concordance(word_list, offsets, width=75, lines=25):
    if offsets:
        half_width = (width - len(word_list[offsets[0]].str) - 2) / 2
        context = width/4 # approx number of words of context

        lines = min(lines, len(offsets))
        print "Displaying %s of %s matches:" % (lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join([word.str for word in word_list[i-context:i]]))
            right = ' '.join([word.str for word in word_list[i+1:i+context]])
            word = word_list[i].str
            left = left[-half_width:]
            right = right[:half_width]
            sum = left + u' ' + word + u' ' + right
            sum = sum[0:width] if len(sum)>=width else sum
            print sum
            lines -= 1
    else:
        print "No matches"