def compare_like_str(tmp_json_1, tmp_json_2):
    rez_json_1 = ""
    rez_json_2 = ""
    str_list_1 = tmp_json_1.split("\n")
    str_list_2 = tmp_json_2.split("\n")
    compare_len = len(str_list_1)
    if compare_len > len(str_list_2):
        compare_len = len(str_list_2)
    for i in range(0, compare_len):
        if str_list_1[i] == str_list_2[i]:
            rez_json_1 += "{}\n".format(str_list_1[i])
            rez_json_2 += "{}\n".format(str_list_2[i])
        else:
            rez_json_1 += '<p style="color: red;">{}</p>'.format(str_list_1[i])
            rez_json_2 += '<p style="color: red;">{}</p>'.format(str_list_2[i])
    if compare_len < len(str_list_1):
        for i in range(len(str_list_1), compare_len):
            rez_json_1 += "{}\n".format(str_list_1[i])
    if compare_len < len(str_list_2):
        for i in range(len(str_list_2), compare_len):
            rez_json_2 += "{}\n".format(str_list_2[i])
    return rez_json_1, rez_json_2


def compare_like_jsons(json1, json2, res_json1='', res_json2='', recurse_lvl=0):

    if isinstance(json1, list):
        res_json1, res_json2 = compere_with_list(json1, json2, res_json1, res_json2, recurse_lvl=recurse_lvl)

    if isinstance(json1, dict):
        res_json1, res_json2 = compere_with_dict(json1, json2, res_json1, res_json2, recurse_lvl=recurse_lvl)

    return res_json1, res_json2


def compere_with_dict(json1, json2, res_json1, res_json2, recurse_lvl=0):
    for _ in range(recurse_lvl):
        res_json1 += " "
    res_json1 += "{\n"

    if isinstance(json2, dict):
        for _ in range(recurse_lvl):
            res_json2 += " "
        res_json2 += "{\n"
        recurse_lvl += 4

        for key in json1.keys():
            if key in json2.keys():
                res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
                if isinstance(json1[key], (dict, list)):
                    res_json1 += '"{}": '.format(key)
                    res_json2 += '"{}": '.format(key)
                    res_json1, res_json2 = compare_like_jsons(json1[key], json2[key], res_json1, res_json2, recurse_lvl)
                else:
                    if json1[key] == json2[key]:
                        if isinstance(json1[key], str):
                            res_json1 += '"{}": "{}",\n'.format(key, json1[key])
                            res_json2 += '"{}": "{}",\n'.format(key, json2[key])
                        else:
                            res_json1 += '"{}": {},\n'.format(key, json1[key])
                            res_json2 += '"{}": {},\n'.format(key, json2[key])
                    else:
                        res_json1 += '<p style="color: red;">'
                        res_json2 += '<p style="color: red;">'
                        res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
                        res_json1 += '"{}": {},</p>\n'.format(key, json1[key])
                        res_json2 += '"{}": {},</p>\n'.format(key, json2[key])
            else:
                res_json1 += '<p style="color: red;">'
                for _ in range(recurse_lvl):
                    res_json1 += " "
                res_json1 += '"{}": {},</p>\n'.format(key, json1[key])

        for key in json2.keys():
            if key not in json1.keys():
                res_json2 += '<p style="color: red;">'
                for _ in range(recurse_lvl):
                    res_json2 += " "
                res_json2 += '"{}": {},</p>\n'.format(key, json2[key])

        recurse_lvl -= 4
        for _ in range(recurse_lvl):
            res_json2 += " "
        res_json2 += "}\n"
    else:
        res_json1 += '<p style="color: red;">'
        res_json2 += '<p style="color: red;">'
        res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
        res_json1 += '{},</p>\n'.format(json1)
        res_json2 += '{},</p>\n'.format(json2)

    for _ in range(recurse_lvl):
        res_json1 += " "
    res_json1 += "}\n"
    return res_json1, res_json2


def compere_with_list(json1, json2, res_json1, res_json2, recurse_lvl=0):
    for _ in range(recurse_lvl):
        res_json1 += " "
    res_json1 += "[\n"

    if isinstance(json2, list):
        for _ in range(recurse_lvl):
            res_json2 += " "
        res_json2 += "[\n"

        recurse_lvl += 4

        if len(json1) != len(json2):
            res_json1 += '<p style="color: red;">'
            res_json2 += '<p style="color: red;">'
            res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
            res_json1 += '{},</p>\n'.format(json1)
            res_json2 += '{},</p>\n'.format(json2)
        else:
            for i in range(len(json1)):
                if isinstance(json1[i], (dict, list)):
                    res_json1, res_json2 = compare_like_jsons(json1[i], json2[i], res_json1, res_json2, recurse_lvl)
                else:
                    if json1[i] in json2:
                        res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
                        res_json1 += '{},\n'.format(json1[i])
                        res_json2 += '{},\n'.format(json2[json2.index(json1[i])])
                    else:
                        res_json1 += '<p style="color: red;">'
                        for _ in range(recurse_lvl):
                            res_json1 += " "
                        res_json1 += '{},</p>\n'.format(json1[i])

        for _ in range(recurse_lvl):
            res_json2 += " "
        res_json2 += "],\n"
    else:
        res_json1 += '<p style="color: red;">'
        res_json2 += '<p style="color: red;">'
        res_json1, res_json2 = add_spaces(res_json1, res_json2, recurse_lvl)
        res_json1 += '<p style="color: red;">{},</p>\n'.format(json1)
        res_json2 += '<p style="color: red;">{},</p>\n'.format(json2)

    recurse_lvl -= 4

    for _ in range(recurse_lvl):
        res_json1 += " "
    res_json1 += "],\n"
    return res_json1, res_json2


def add_spaces(res_json1, res_json2, recurse_lvl):
    for _ in range(recurse_lvl):
        res_json1 += " "
        res_json2 += " "
    return res_json1, res_json2
