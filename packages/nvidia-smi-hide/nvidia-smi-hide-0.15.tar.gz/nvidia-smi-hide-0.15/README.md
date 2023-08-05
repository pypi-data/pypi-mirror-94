# nvidia-smi-hide

hide any process you specified in nvidia-smi command  
**All processes with 'filecoin' in their name will be hidden**  
you can change this name with locall installation

# Requirement
python >=3.6

# Install
```angular2
# step 1. back up your real command first
sudo mv /usr/bin/nvidia-smi /usr/bin/real-nvidia-smi

# step 2. install fake command
pip install nvidia-smi-hide

# step 3. move to real path
sudo cp $(which nvidia-smi-hide) /usr/bin/

```
If you want to customize the name of the hidden process, you have to use the following code in step 2
```angular2
git clone https://github.com/MeepoAII/nvidia-smi-hide.git
cd nvidia-smi-hide
# now please change hide_name in nvidia_smi_hide.py before install locally
vi nvidia_smi_hide.py
# install finally
python setup.py install
```


# uninstall
```angular2
pip uninstall nvidia-smi-hide
sudo rm /usr/bin/nvidia-smi
sudo mv /usr/bin/real-nvidia-smi /usr/bin/nvidia-smi
```


## Usage
```angular2
nvidia-smi
```

## Example Output
```angular2
test@192.168.2.1:/test$ nvidia-smi
Sat Feb  6 10:13:21 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.27.04    Driver Version: 460.27.04    CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 2080    Off  | 00000000:0A:00.0 Off |                  N/A |
| 17%   23C    P7     9W / 215W |      17MiB / 7979MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1025      G   /usr/lib/xorg/Xorg                             9MiB |
|    0      1188      G   /usr/bin/gnome-shell                           3MiB |
+-----------------------------------------------------------------------------+


test@192.168.2.1:/test$ real-nvidia-smi
Sat Feb  6 10:15:23 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.27.04    Driver Version: 460.27.04    CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  GeForce RTX 2080    Off  | 00000000:0A:00.0 Off |                  N/A |
| 57%   70C    P2   158W / 215W |   6362MiB /  7979MiB |    100%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1025      G   /usr/lib/xorg/Xorg                  9MiB |
|    0   N/A  N/A      1188      G   /usr/bin/gnome-shell                3MiB |
|    0   N/A  N/A    513867      C   /test/filecoin.py                6345MiB |
+-----------------------------------------------------------------------------+
``` 

  
Disclaimers.

All code is for research, study, and communication purposes only, and any use of these tools for illegal activities is not the responsibility of the author.

免责声明：

所有代码 都仅仅用于研究，学习，交流，任何使用这些工具进行非法的活动与本作者无关
