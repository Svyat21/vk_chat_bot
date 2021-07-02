def date_str(dates):
    result = ''
    for index, i in enumerate(dates):
        result += f'{index + 1}. {i.strftime("%d-%m-%Y")}\n'
    return result


def cities_str(sites):
    result = ', '.join(sites)
    return result