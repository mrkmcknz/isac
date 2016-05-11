def most_common(lst):

    return max(set(lst), key=lst.count)


def least_common(lst):

    return min(set(lst), key=lst.count)
