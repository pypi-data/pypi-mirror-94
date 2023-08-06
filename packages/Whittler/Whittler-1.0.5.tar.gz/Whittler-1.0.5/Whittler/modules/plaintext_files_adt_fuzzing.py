from Whittler.classes.Result import Result

class AdtFuzzResult(Result):

    FRIENDLY_NAME = "plaintext_files_adt"
    
    ATTRIBUTES = ["output","input"]

    @staticmethod
    def give_result_dict_list(fname):
        result = {}
        with open(fname, "r") as f:
            result["output"] = f.read()
        with open(fname.replace("_output","_unpack"), "r") as f:
            result["input"] = f.read()
        return [result]