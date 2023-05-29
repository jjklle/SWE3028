# process string list
def process_string_list(string_list):
    if string_list=="":
        return ""
    string_list = string_list.replace("[", "").replace("]", "").replace("'", "")
    return ", ".join([item.strip() for item in string_list.split(",")])

