import configparser

default = configparser.ConfigParser()
default.read('default.ini')
extension = default["extend"]["files"].split(",")[:-1]

for ini in extension:
    ini = ini.strip()
    default.read(ini)

# print(default.sections())  # for a list of config parameters
