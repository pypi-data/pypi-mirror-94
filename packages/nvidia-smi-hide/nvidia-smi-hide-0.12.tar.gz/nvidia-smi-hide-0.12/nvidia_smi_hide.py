import subprocess
import time
import random
from pynvml import *

hide_name = "filecoin"
real_cmd_path = "/usr/bin/nvidia-smi"

filterd_arg = ['-i', '--id', '-f', '--filename', '-l', '--loop',
               '-q', '--query', '-x', '--xml-format',
               '-l', '--loop', '-lms', '--loop-ms', 'dmon', 'pmon']


def default_print(id="all", filename="none"):
    nvmlInit()

    localtime = time.asctime(time.localtime(time.time()))

    driver_version = nvmlSystemGetDriverVersion().decode()

    # todo
    # get the right cuda version on different system
    cuda_version = "10.0"

    gpu_list = []
    process_list = []
    gpuDeviceCount = nvmlDeviceGetCount()
    for i in range(gpuDeviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)

        hide_used_memory = 0
        # sum hide process used per gpu, and substract finally

        # processes:
        process_compute_list = nvmlDeviceGetComputeRunningProcesses(handle)
        process_graph_list = nvmlDeviceGetGraphicsRunningProcesses(handle)
        for process in process_compute_list:
            try:
                pid = process.pid
            except:
                pid = "N/A"
            try:
                process_name = nvmlSystemGetProcessName(pid).decode()
            except:
                continue
            if len(process_name) > 40:
                process_name = "..." + process_name[-37:]
            if hide_name not in process_name:
                pass
            else:
                hide_used_memory += process.usedGpuMemory
                continue

            try:
                process_gpu_usage = int(process.usedGpuMemory / 1024 / 1024)
                process_gpu_usage = str(process_gpu_usage) + "MiB"
            except:
                process_gpu_usage = "N/A"

            this = {"gpu": str(i), "PID": str(pid), "Type": "C",
                    "Process name": process_name, "memory": process_gpu_usage}
            process_list.append(this)

        for process in process_graph_list:
            # just for test
            # test end
            try:
                pid = process.pid
            except:
                pid = "N/A"
            try:
                process_name = nvmlSystemGetProcessName(pid).decode()
            except:
                continue
            if len(process_name) > 40:
                process_name = "..." + process_name[-37:]
            if hide_name not in process_name:
                pass
            else:
                hide_used_memory += process.usedGpuMemory
                continue

            try:
                process_gpu_usage = int(process.usedGpuMemory / 1024 / 1024)
                process_gpu_usage = str(process_gpu_usage) + "MiB"
            except:
                process_gpu_usage = "N/A"

            this = {"gpu": str(i), "PID": str(pid), "Type": "G",
                    "Process name": process_name, "memory": process_gpu_usage}
            process_list.append(this)


        # the first line
        id = str(i)

        name = str(nvmlDeviceGetName(handle).decode())
        if len(name) >= 18:
            name = name[:15] + "..."

        try:
            persistence = nvmlDeviceGetPersistenceMode(handle)
            if persistence == 0:
                persistence = "Off"
            else:
                persistence = "on"
        except Exception:
            persistence = "N/A"

        bus_id = "0000" + nvmlDeviceGetPciInfo(handle).busId.decode()

        try:
            disp_A = nvmlDeviceGetDisplayActive(handle)
            if disp_A == 0:
                disp_A = "Off"
            else:
                disp_A = "On"
        except Exception:
            disp_A = "N/A"

        ecc = 0
        try:
            ecc = nvmlDeviceGetTotalEccErrors(handle)
        except Exception:
            ecc = "N/A"

        # second line

        memory_info = nvmlDeviceGetMemoryInfo(handle)
        memory_total = int(memory_info.total / (1024 * 1024))

        # start make fake info
        # based on fake_ratio = memory_used / memory_total

        # 1. fake memory use
        memory_used = int((memory_info.used - hide_used_memory) / (1024 * 1024))
        memory = str(memory_used) + "MiB / " + str(memory_total) + "MiB"

        fake_ratio = float(memory_used) / float(memory_total)

        # 2. fake fan speed
        # make sure the fan speed is 15-80, so the formula is
        # fake_fan = 15 + (80-15) * fake_ratio
        try:
            fan = nvmlDeviceGetFanSpeed(handle)
            base_fan = random.randint(15, 20)
            fan = int(base_fan + (80-base_fan) * fake_ratio)
            fan = str(fan) + "%"
        except:
            fan = "N/A"

        # 3. fake temperature
        # make sure the temp is 25-70, so the formula is
        # fake_temp = 25 + (70-25) * fake_ratio
        try:
            Temp = str(nvmlDeviceGetTemperature(handle, 0))
            base_Temp = random.randint(21, 25)
            Temp = int(base_Temp + (70-base_Temp) * fake_ratio)
            Temp = str(Temp) + "C"
        except:
            Temp = "N/A"

        # 4. fake performance
        # p0-p7, based on fake_ratio
        try:
            power_status = nvmlDeviceGetPowerState(handle)
            base_power_status = 0
            power_status = 7 - int(base_power_status + (7-base_power_status) * fake_ratio)
            power_status = "P" + str(power_status)
        except:
            power_status = "N/A"

        # 5. fake power
        # similar to the above
        power_limited = int(nvmlDeviceGetPowerManagementLimit(handle)/1000)
        base_power = random.randint(3, 20)
        power_used = int(base_power + (power_limited - base_power) * fake_ratio)
        power = str(power_used) + "W / " + str(power_limited) + "W"

        # 6. fake gpu-utilization
        volatile_gpu_end = int(fake_ratio * 100)
        volatile_gpu_start = volatile_gpu_end // 2
        volatile_gpu = str(random.randint(volatile_gpu_start, volatile_gpu_end)) + "%"

        compute_m = "Default"

        this = {"gpu": id, "name": name, "persistence": persistence,
                "bus_id": bus_id, "disp_a": disp_A, "ecc": ecc, "fan": fan,
                "Temp": Temp, "power_state": power_status, "power": power,
                "memory": memory, "volatile": volatile_gpu, "compute": compute_m}

        gpu_list.append(this)

    # output format string
    print(localtime)
    print("+-----------------------------------------------------------------------------+") #79
    print("| NVIDIA-SMI {0:13}Driver Version: {1:13}CUDA Version: {2:9}|".format(driver_version,
            driver_version, cuda_version))
    print("|-------------------------------+----------------------+----------------------+")
    print("| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |")
    print("| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |")
    # todo
    # new feature MIG M. (Multiple Instance GPU)
    print("|===============================+======================+======================|")

    for gpu in gpu_list:
        # gpu info first line
        print("|{0:>4}  {1:18}{2:>5}  | {3} {4} |{5:>21} |".format(gpu['gpu'],
            gpu['name'], gpu['persistence'], gpu['bus_id'], gpu['disp_a'], gpu['ecc']))
        # gpu info second line
        print("|{0:>4}{1:>6}{2:>6}{3:>14} |{4:>21} |{5:>8}{6:>13} |".format(gpu['fan'],
                gpu['Temp'], gpu['power_state'], gpu['power'], gpu['memory'], gpu['volatile'], gpu['compute']))
        print("+-------------------------------+----------------------+----------------------+")

    print("")
    print("+-----------------------------------------------------------------------------+")
    print("| Processes:                                                       GPU Memory |")
    print("|  GPU       PID   Type   Process name                             Usage      |")
    print("|=============================================================================|")



    if len(process_list) == 0:
        print("|  No running processes found                                                 |")

    for process in process_list:
        print('|{0:>5}{1:>10}{2:>7}   {3}{4}{5:>10} |'.format(process['gpu'],
            process['PID'], process['Type'], process['Process name'],
            " "*(41-len(process['Process name'])), process['memory']))
    print("+-----------------------------------------------------------------------------+")


    nvmlShutdown()


def default_print_2(id="all", filename="none"):
    return



def default_print_filtered(id="all", filename="none", loop="none"):
    if loop is not "none":
        while True:
            try:
                default_print()
                time.sleep(loop)
            except:
                return
    else:
        default_print()
        pass
    return


def isInter(a, b):
    result = list(set(a)&set(b))
    if result:
        return True
    else:
        return False

def preprocess_arg(arg):
    for i, a in enumerate(arg):
        if '=' in a:
            arg_1, arg_2 = a.split('=')
            del arg[i]
            arg.insert(i, arg_1)
            arg.insert(i+1, arg_2)

    return arg

def main():
    arg = sys.argv
    arg[0] = real_cmd_path
    cmd = ""
    for a in arg:
        cmd += a
        cmd += " "


    # 1.check argument valid start
    ps_call = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        ps_call.communicate(timeout=0.08)
    except:
        pass

    returncode = ps_call.returncode
    if returncode == 0 or returncode is None:
        pass
    else:
        print("Invalid combination of input arguments. Please run 'nvidia-smi -h' for help.")
        return

    # 1.check argument valid end

    # so far, argument is absolutely valid
    # 2.split special argument and normal argument start
    arg = preprocess_arg(arg)

    if len(arg) == 1:
        default_print()


    elif isInter(arg[1:], filterd_arg) and '-h' not in arg and '--help' not in arg:
        # to fake print out

        arg = arg[1:]

        if 'dmon' in arg:
            # todo
            print("Unsupported arguments")
        elif 'pmon' in arg:
            # todo
            print("Unsupported arguments")
        elif '-lms' in arg or '--loop-ms' in arg:
            # todo
            print("Unsupported arguments")
        elif '-q' in arg or '--query' in arg:
            # todo
            print("Unsupported arguments")
        else:
            # may be loop or -i or -f
            loop = "none"
            id = "none"
            filename = "none"
            if '-l' in arg:
                loop = 5
                index = arg.index('-l')
                try:
                    loop = int(arg[index+1])
                except:
                    pass
            elif '--loop' in arg:
                loop = 5
                index = arg.index('--loop')
                try:
                    loop = int(arg[index+1])
                except:
                    pass

            if '-i' in arg:
                id = 0
                index = arg.index('-i')
                try:
                    id = arg[index+1].split(',')
                except:
                    pass
            elif '--id' in arg:
                id = [0,]
                index = arg.index('--id')
                try:
                    id = arg[index+1].split(',')
                except:
                    pass

            if '-f' in arg:
                filename = "none"
                index = arg.index('-f')
                try:
                    filename = arg[index+1]
                except:
                    pass
            elif '--filename' in arg:
                filename = "none"
                index = arg.index('--filename')
                try:
                    filename = arg[index+1]
                except:
                    pass

            default_print_filtered(id, filename, loop)

    else:
        # to real nvidia-smi
        proc = subprocess.Popen(cmd, shell=True)
        try:
            outs, errs = proc.communicate()
        except:
            proc.kill()
            outs, errs = proc.communicate()
    # 2.split special argument and normal argument end


if __name__ == '__main__':
    main()
