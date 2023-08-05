# nvidia-smi-hide

hide any process you specified in nvidia-smi command  
**All processes with 'filecoin' in their name will be hidden**  
you can change this name with locall installation

# Install
```angular2
git clone https://github.com/MeepoAII/nvidia-smi-hide.git
cd nvidia-smi-hide
pip install .
```


# uninstall
`pip uninstall nvidia-smi-hide`


## Usage
just:
```angular2
nvidia-smi-hide
```
if you want to change the default hide name, first uninstall it, 
and change hide_name in nvidia_smi_hide.py, then  
 `pip install .`

You can move the command to /usr/bin/ to make it easier to use this  
command even when the python virtual environment is not activated  
`sudo mv $(which nvidia-smi-hide) /usr/bin/`
