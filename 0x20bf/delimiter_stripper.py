def delimiter_stripper(string):
    # avoid incorrect hashes
    # TODO: add chars as needed
    string.strip(":")
    string.strip(".")
    return string.strip(":")
