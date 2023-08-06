from Whittler.classes.Result import Result

class StackPepResult(Result):

    FRIENDLY_NAME = "stackpep"
    
    ATTRIBUTES = [
        "type",
        "fullname",
        "verb",
        "subject",
        "version",
        "fullmodule",
        "topmodule"
    ]

    @staticmethod
    def give_result_dict_list(fname):
        with open(fname,"r") as f:
            rawcontent = f.read()
        entries = list(filter(None, rawcontent.splitlines()))
        ret = []
        for entry in entries:
            e = {}
            funcinfo = list(filter(None,entry.split(" ")))
            typ,funcname,version,module = [funcinfo[i] if i<len(funcinfo) else "" for i in range(4)]
            e["type"] = typ
            e["fullname"] = funcname
            e["verb"] = funcname.split("-")[0]
            e["subject"] = funcname.split("-")[1]
            e["version"] = version
            e["fullmodule"] = module
            e["topmodule"] = module.split(".")[0]
            ret.append(e)
        return ret