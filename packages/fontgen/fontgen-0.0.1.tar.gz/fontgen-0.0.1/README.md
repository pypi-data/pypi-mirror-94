
# fontgen  
  
Python package for generating fonts.   
  
## Installation  
  
This is one time process.  
  
Fontgen requires Python 3.8 or later.  
  
### First you need to create a virtual environment for python  
  
On macOS and Linux:  
  
`python3 -m venv venv`  
  
On Windows:  
  
`py -m venv venv`  
  
### Activating a virtual environment  
  
On macOS and Linux:  
  
`source env/bin/activate`  
  
On Windows:  
  
`.\env\Scripts\activate`  
  
### Downloading fontgen  
  
If you have SSH access, you can download it directly using this command  
  
`git clone git@github.com:itfoundry/fontgen.git`  
  
If you don't have SSH access, you can simpaly download the zip file and extract it to the working directory.  
  
Rename the zip extracted directory to "fontgen"  
  
### Installing fontgen  
  
`pip install ./fontgen`  
  
`rm -rf fontgen`  
  
## Usage  
  
Make sure the virtual environment is activated.  
  
Refer to [Activating a virtual environment](https://github.com/itfoundry/fontgen#activating-a-virtual-environment)  
  
Example:  
  
`fontgen -f "Font Family Name" -o var`  
  
For italic version you will have to type "Font Family Name Italic"  
  
For detailed usage, type:  
   
 `fontgen -h`
 
 ## Directory structure
 
 / Base Directory (Name of the Directory = Font family name)
    
    / sxasd
           