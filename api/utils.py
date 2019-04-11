
def clear_input(input):
    dictionary = {}
    for key in input:
        if input[key] != None:
            dictionary[key] = input[key]
    return dictionary
