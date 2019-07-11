import yaml
import os
from DS-Logger import yamlloader

# Use this class to load YAML file into object
# Author: nzvincent@gmail.com
# Usage: obj = ClassYamlLoader
#        obj.load_yaml('file.yaml')

class dsYamlLoader:
  logger = dsLogger()
  
  def __init__(self):
    #bsLog("Initiating class" +  self.__class__.__name__, "INFO" )
    pass
  
  def load_yaml(self, input_file): 
    if os.path.isfile(input_file):
      with open(input_file, 'r') as stream:
        try:
          self.logger.log("YAML file loaded successful:  " +  input_file, "INFO")
          output = yaml.load(stream)
          return output
        except yaml.YAMLError as exc:
          self.logger.log("Errro loading YAML file: " +  exc , "ERROR")
