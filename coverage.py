import subprocess
result = subprocess.check_output("coverage report -m", shell=True, text=True)
result = result.replace("\n", "")
result = result.split(" ")
result = int(result[-1].replace("%", ""))

if(result < 100):
    raise ValueError("Coverage below 100, got {}".format(result))
