import re
import nltk
import string
import collections
nltk.download

'''
Via from https://github.com/MANU-CHAUHAN/text_format_checker
'''

pattern_web_url = re.compile(
    r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")

pattern_email = re.compile(r'([a-zA-Z]+[a-zA-Z0-9_.]*@[a-zA-Z._]+?\.(?:com|net|org|edu|gov))')

ignore_words = set(['iPad', 'iPhone'])


def named_entity_checker(text):
    entities = set()
    for entity in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
        if isinstance(entity, nltk.tree.Tree):
            etext = " ".join([word for word, tag in entity.leaves()])
            # label = entity.label()
            entities.add(etext)
    return entities


def get_email_url_ignore_word_indices(txt):
    span_set = set()

    r = pattern_email.finditer(txt)
    if r:
        for item in r:
            span_set.add(item.span())

    r = pattern_web_url.finditer(txt)
    if r:
        for item in r:
            span_set.add(item.span())
    nums = set()

    # check for named entities, which needs to be removed, and update ignore words set
    ignore_words.update(named_entity_checker(text=txt))

    r = [re.finditer(r'\b{}\b'.format(w.lower()), txt.lower()) for w in ignore_words]

    for i in r:
        for j in i:
            s, e = j.span()
            if e - s > 0:
                span_set.add((s, e))
    for start, end in span_set:
        if txt[start - 1] == ' ':
            nums.add((start - 1, end))
        else:
            nums.add((start, end))
    return {i for s, e in nums for i in range(s, e)}


end_states = set('.?!')
capital_letters = set(string.ascii_uppercase)
small_letters = set(string.ascii_lowercase)
punctuations = set(string.punctuation)
digits = set(string.digits)
[punctuations.remove(x) for x in ['.', '?', '!']]


def check_text_format(texts):
    final_data = []
    over_all_count = 0
    flag = False
    for text in texts:
        if text:
            mistakes = {}
            count = 0
            # check if the text starts and contains only email/url
            email = pattern_email.match(text)
            url = pattern_web_url.match(text)
            if email:
                s, e = email.span()
                if e - s == len(text):
                    flag = True
            if url:
                s, e = url.span()
                if e - s == len(text):
                    flag = True
            if not flag:
                first = text[0]
                last = text[-1]

                if (first < 'A' or first > 'Z') and (first < '0' or first > '9'):
                    mistakes['start_not_proper'] = True
                    count += 1
                if last not in ['.', '?', '!']:
                    mistakes['end_not_proper'] = True
                    count += 1

                mistakes['extra_spaces'] = []
                mistakes['space_used_before_.?!'] = []
                mistakes['no_space_after_.?!'] = []
                mistakes['capital_letter_missed_after_.?!_space'] = []
                mistakes['capital_letter_missed_after_.?!'] = []
                mistakes['capital_case_after_small_case'] = []

                chars_dict = collections.defaultdict(int)
                previous_to_previous_state = previous_state = current_state = 0

                index = 1
                chars_dict[text[0]] += 1
                length = len(text)
                indices_to_ignore = get_email_url_ignore_word_indices(text)

                while index < length:
                    char = text[index]
                    chars_dict[char] += 1

                    if char in capital_letters:
                        current_state = 0

                    if char == ' ':
                        current_state = 1

                    if char in small_letters:
                        current_state = 2

                    if char in end_states:
                        current_state = 3

                    if char in digits:
                        current_state = 4

                    if char in punctuations:
                        current_state = 5

                    if index in indices_to_ignore:
                        index += 1
                        previous_to_previous_state = previous_state
                        previous_state = current_state
                        continue

                    '''checks for states'''

                    # check if space before '.'
                    if current_state == 3 and previous_state == 1:
                        mistakes['space_used_before_.?!'].append(index - 1)
                        count += 1

                    # check if space after space -> extra space used
                    elif previous_state == current_state == 1:
                        mistakes['extra_spaces'].append(index)
                        count += 1

                    # wrong case usage: abC, 'C' is capital case after small case.
                    elif current_state == 0 and previous_state == 2:
                        mistakes['capital_case_after_small_case'].append(index)
                        count += 1

                    # ...blah. abc -> small case after '.' and space
                    if previous_to_previous_state == 3 and previous_state == 1 and current_state == 2:
                        mistakes['capital_letter_missed_after_.?!_space'].append(index)
                        count += 1

                    # no space after '.'
                    if current_state in [0, 2] and previous_state == 3:
                        mistakes['no_space_after_.?!'].append(index)
                        count += 1

                    # small letter after .
                    if current_state == 2 and previous_state == 3:
                        mistakes['capital_letter_missed_after_.?!'].append(index)
                        count += 1

                    index += 1
                    previous_to_previous_state = previous_state
                    previous_state = current_state

                # while ends

                ''' check the number of pairs for '(' & ')', '{' & '}', '[' & ']', '<' & '>'   '''
                if chars_dict['('] != chars_dict[')']:
                    mistakes['(_)_mismatch'] = True
                    count += 1

                if chars_dict['{'] != chars_dict['}']:
                    mistakes['{_}_mismatch'] = True
                    count += 1

                if chars_dict['['] != chars_dict[']']:
                    mistakes['[_]_mismatch'] = True
                    count += 1

                if chars_dict['<'] != chars_dict['>']:
                    mistakes['<_>_mismatch'] = True
                    count += 1

                if count > 0:
                    over_all_count += count
                    final_data.append(
                        {'count': count,
                         'mistakes': {x: y for x, y in mistakes.items() if y},
                         'text': text})

    return final_data, over_all_count


# if __name__ == '__main__':
#     s1 = "hello .hoW are you www.xyz.com? i hope all  good. iPhone is working now."
#     s2 = "I work at Google. where do you work?"
#     s3 = "abc@xyz.com"

#     data, total_mistakes = check_text_format([s1, s2, s3])
#     print('\nTotal mistakes: ', total_mistakes, '\n')
#     [print('Text number: {0}    Info dict: {1}'.format(i, x)) for i, x in enumerate(data)]