import sys
import json 
import os
import shlex 

import importlib.resources

# WARNING !!! SPAGHETTI CODE !

# Creates buck-data path 
with importlib.resources.path("src","data.json") as haar_resource:
    
  file = os.path.abspath(haar_resource)
  file = file[:-18]
  file = file + "buck-data/"
  
  if os.path.isdir(file):
    i = 0
    
  else:
    os.mkdir(file)
    data = file + "data.json"
    f = open(data,"a+")
    
# Creates the Bucket class 
class Bucket: 
  def __init__(self,name,executor,commandList,description):
    self.name = name
    self.executor = executor
    self.commandList = commandList
    self.description = description
    self.count = 0
    
  #Increments the count property 
  def increment(self):
    self.count += 1
   
# Intetacts with Db 

def middleMan(arg,data): 
  try :
    #Fetch data from data file 
    with importlib.resources.path("src","data.json") as haar_resource:
      dataFile = os.path.abspath(haar_resource)
      dataFile = dataFile[:-18]
      dataFilePath = dataFile + "buck-data/data.json"
      if arg == "r":
        with open (dataFilePath, 'r') as f:
          data = f.read()
          f.close()
          
        return data
      
      elif arg == "a":
        data = json.dumps(data)
        with open(dataFilePath,"a") as f: 
          data = '\n'+data+', \n'
          f.write(data)
          f.close()
      else: 
        return dataFilePath

  except FileNotFoundError:
    print(">> Cannot locate data file :  " + dataFilePath )
  except Exception as e:
    print (">> Error")
# Creates a New Bucket
def createBucket():
  try :   
    print(' >> Howdy! Create A New Bucket ')
    # Accept inputs from User
    name = input("\n Name : ")
    print ('\n >> Seperate commands with a comma')
    preCmds = input (" Commands : ")
    cmds = preCmds.split(',')
    executor = str(input("\n Executor : ")) 
  
    detail = str(input("""\n Description : """))
      
    # Instantiate an object of the class with data from input
    data = Bucket(name,executor,cmds,detail)
    # Load data object into a new object (spaghetti code❗)
    newData = {
      "name": data.name,
      "executor":data.executor,
      "buck_list":data.commandList,
      "description":data.description,
      "count":data.count
    }
  
    middleMan("a",newData)
    
    # Sucess Message
    print('\n >> yay! it is done ')
    for i in data.commandList:
      if '$' in i:
        print (f"\n >> Usage : 'buck {data.executor} [extra argument]' ")
      else:
        print (f"\n >> Usage : 'buck {data.executor}' ")
  
      # End Process
      sys.exit()
      
  except KeyboardInterrupt:
    print("\n >> KeyboardInterrupt :  Process terminated !")
#List out buckets
def listBucket():
  # fetch data from middleMan()
  data = middleMan("r","")
  
  modifiedData = '{ "bucket" : [' + data + '{} ] } '
  #Coverts Data To Json
  jsonData = json.loads(modifiedData)
  
  # Renders Data 
  print (' >> Here you go : \n')
  print(json.dumps(jsonData,indent=2))
  
# Check if command is cd
def is_cd(command: str) -> bool:
  command_split = shlex.split(command)
  return command_split[0] == "cd" 
  # this returns True if command is cd or False if not
# Runs commands if is_cd == True
def run_command(command: str) -> int:
  if is_cd(command):
    split_command = shlex.split(command)
    directory_to_change = ' '.join(split_command[1:])
    os.chdir(directory_to_change)
  else: 
    os.system(command)

#Run Commands From Bucket
def run(arg):
  
  # Fetch Data from middleMan()
  data = middleMan("r","")
  data = data[:-3]
  
  otherData = '{ "bucket" : [' + data + '] } '
  
  # Coverts modified data to json
  data = json.loads(otherData)
  
  
  # Logic
  for i in data['bucket']:
    response = i.get('executor')
    
    
    
    if arg[1] in response:
      
      buck = i.get('buck_list')
       
      
      if len(arg) > 2 :
        for i in buck:
         
          if '$' in i:
            
            cmd = i
            newCmd = cmd.replace('$',arg[2])
     
            for i in range(len(buck)):
              if buck[i] == cmd:
                buck[i] = newCmd
        for i in buck:
          run_command(i)
        
        if len(buck) == 1 :
          print('>> Done! executed 1 command.')
          
        else:
          print('>> Done! executed '+ str(len(buck)) + ' commands.')
          
      else:
        for i in buck:
        
          if '$' in i:
            print('>> Usage : buck ' + arg[1] + ' [extra argument] ' )
            sys.exit()
          
        for i in buck:
          run_command(i)
        
        if len(buck) == 1 :
          print('>> Done! executed 1 command.')
        else:
          print('>> Done! executed '+ str(len(buck)) + ' commands.')

# Wipes out data.json file
def eraseBucket():
  ans = input('\n>> This would wipe out your bucket data ! , "y" or "n" : ' )
  if ans == "y" or ans == "Y":
    file = middleMan("","")
    # Write Json to a Json Data Fi
    with open(file,"w") as f: 
      f.write("")
      f.close()
    # Sucess Message
    print('\n>> Your bucket is now empty.  ')
    # End Process
    sys.exit()
  elif ans == "n" or ans == "N":
    print("\n>> Process Terminated...")
  else:
    print("\n>> error :  You did not enter a valid input, try again !")
    sys.exit()


 
#Help message 
def helpMessage():
  print (" >> Howdy! Let's get you started. \n")
  
  print(" >> buck --create(-c) : Create a new Bucket \n  • Name(Optional) - Name of bucket \n  • Commands - List of commands you'd like to run all at once, add '$' in front of any of the commands to pass in a future value to the command in execution, e.g mkdir $, cd $, code . \n \n This would require an extra argument to replace the '$' sign in execution. SEPERATE MULTIPLE COMMANDS WITH A ','. \n \n • Executor - This is a keyword of your choice that runs all of the commands you inputed earlier. \n • Description(Optional) - This is a message that describes your bucket. \n • yay! You've successfully created your first bucket ^_^ \n \n  >> buck --list(-l) : This renders a json list of the buckets you've created. \n  >> buck --erase(-e) : Clears out all of your buckets, if needed . \n \n >> HOW DO YOU RUN YOUR BUCKET COMMANDS ? it's easy ! \n \n   ➡ ️️buck [executor] [extra arguments(if you added a '$' sign to any of your commands)] \n \n >> That was alot! Go ahead and create several buckets to increase your productivity in the CLI.  @Pleasanttech \n  ➡️ Docs | Project | Support : \n • Github - https://github.com/Pleasant-tech/Buck \n • YouTube - youtube.com/c/Pleasanttech \n >> Happy Hacking ! :) ")
  
  
# Main Function

  
def main(arg=sys.argv):
  
  args = ['--create','-c','--list','-l','--erase','-e','--help','-h']
  if len(arg) == 1:
    print (' >> Howdy :) Get started with buck today !\n   Usage : buck --help(-h)')
  elif arg[1] == '--create' or arg[1] == '-c':
    createBucket()
    
  elif arg[1] == '--list' or arg[1]=='-l':
    
    listBucket()
  elif arg[1] == '--erase' or arg[1]=='-e':
    
    eraseBucket()
 
  elif arg[1] == '--help' or arg[1]=='-h':
    helpMessage()
    
  
  
 
  elif arg[1] not in args:
    run(arg)
 
  

   
#if '__name__' == '__main__':
  
  