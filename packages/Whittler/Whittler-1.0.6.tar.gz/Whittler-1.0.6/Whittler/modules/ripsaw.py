from Whittler.classes.Result import Result
import json
import os

class RipsawResult(Result):

    FRIENDLY_NAME = "ripsaw"
    
    ATTRIBUTES = [
        "ruleset",
        "severity",
        "filename",
        "function_name",
        "suggested_replacements",
        "line_number",
        "line",
        "surrounding_lines",
        "surrounding_5_lines",
    ]

    _REBASE_PATH = ""

    _ORIGINAL_PATH_STRIP_NUM_CHARS = 0

    @staticmethod
    def give_result_dict_list(fname):
        with open(fname,"r") as f:
            output = json.loads(f.read())
        ret = []
        ruleset = output["metadata"]["ruleset"]["name"]
        for finding_type in ("errors","warnings"):
            if finding_type in output.keys():
                severity = finding_type[:-1] # chop off the "s" at the end
            else:
                continue
            for errorfile, errordata in output[finding_type].items():
                if RipsawResult._REBASE_PATH or RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS:
                    errorfile = f"{RipsawResult._REBASE_PATH}/{errorfile[RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS:]}"
                result = {"ruleset":ruleset, "severity":severity}
                result["filename"] = errorfile
                for funcname, errdetails in errordata.items():
                    result["function_name"] = funcname
                    result["suggested_replacements"] = ", ".join(sorted(errdetails["replacements"])) if "replacements" in errdetails else ""
                    try:
                        with open(errorfile,"r") as f:
                            filecontent = f.read()
                    except FileNotFoundError:
                        print(f"\nFailed to find the file {errorfile} .\n")
                        rebase = input("\nIf the repository is accessible from this machine, I can attempt to fix the references. Should I? (Y/n) ")
                        if not rebase.strip() or rebase.lower() == "y":
                            while True:
                                RipsawResult._REBASE_PATH = input("\nWhat is the base location for the repository? ").rstrip("/").rstrip("\\")
                                if not os.path.isdir(RipsawResult._REBASE_PATH):
                                    print("\nThat's not a folder I can open.")
                                else:
                                    break
                            RipsawResult._REBASE_PATH = RipsawResult._REBASE_PATH.replace("\\","/")
                            while True:
                                print(f"\nThe original filepath is {errorfile} .")
                                print(f"With the new base, the filepath will be {RipsawResult._REBASE_PATH}/{errorfile} .")
                                rebase = input("\nIs this OK, or do characters need to be stripped from the beginning of the original filepath? (y/N) ")
                                if not rebase.strip() or rebase.lower() == "n":
                                    try:
                                        with open(f"{RipsawResult._REBASE_PATH}/{errorfile}","r") as f:
                                            pass
                                    except FileNotFoundError:
                                        print("Couldn't open that file path.\n")
                                        continue
                                while True:
                                    RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS = input("How many characters do I need to strip from the beginning of the original filepath for the rebased filepath to be accurate? ")
                                    try:
                                        RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS = int(RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS)
                                    except ValueError:
                                        print("Failed to parse input as a number.\n")
                                        continue
                                    new_fpath = f"{RipsawResult._REBASE_PATH}/{errorfile[RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS:]}"
                                    print(f"\nThe new full filepath is {new_fpath} .")
                                    try:
                                        with open(new_fpath,"r") as f:
                                            errorfile = f"{RipsawResult._REBASE_PATH}/{errorfile[RipsawResult._ORIGINAL_PATH_STRIP_NUM_CHARS:]}"
                                            filecontent = f.read()
                                            break
                                    except FileNotFoundError:
                                        print("Couldn't open that file path.\n")
                                        continue
                                print(f"\nOK, rebasing all ripsaw results to {RipsawResult._REBASE_PATH} .")
                                break
                        else:
                            print("\nOK, but I won't be able to import the file contents for whittling.")
                            filecontent = ""
                            break
                        
                    filelines = filecontent.splitlines()
                    for lineno in set(errdetails["lines"]):
                        result["line_number"] = str(lineno)
                        result["line"] = filelines[lineno].strip()
                        result["surrounding_lines"] = "\n".join(filelines[lineno-1:lineno+1])
                        result["surrounding_5_lines"] = "\n".join(filelines[lineno-5:lineno+5])
                ret.append(result)
        return ret

