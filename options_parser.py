
def parse(html: str):
    temp_option = False
    temp_option_two = False
    result_dict = dict()
    pair = ['string', 'id']
    temp_word = str()
    for i, symbol in enumerate(html):
        if symbol == 'v' or temp_option:
            if html[i:i + 5] == 'value' or temp_option:
                temp_option = True
                temp_word += symbol
        if symbol == '>' and html[i - 6:i] != 'option':
            temp_option = False
            pair[1] = int(temp_word[temp_word.index('"'):-1].strip('"'))
            print(pair[1])
            temp_word = ""
            temp_option_two = True
        if symbol == '<' and html[i + 1:i + 2] == '/' and temp_option_two:
            pair[0] = temp_word[1:]
            print(pair[0])
            temp_word = ""
            result_dict.update({pair[0]: pair[1]})
            temp_option_two = False
        if temp_option_two:
            temp_word += symbol

    return result_dict
