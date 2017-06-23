def uniqueLetters(cabin):
    '''Input list of unique Cabin numbers and output unique letters from entire list'''
    uniq_letters = set()
    for e in cabin:
        if type(e) is not str:
            next
        else:
            f = list(set(e))
            f = list(filter(lambda i: not str.isdigit(i), f))
            uniq_letters.update(f)
    uniq_letters.discard(" ") 
    return uniq_letters