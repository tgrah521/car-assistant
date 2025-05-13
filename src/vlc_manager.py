import psutil

def get_vlc():
    vlc_processes = []
    for proc in psutil.process_iter(['name','pid']):
        if proc.info['name'] == 'vlc':
            vlc_processes.append(proc)
    return vlc_processes
    

def close_all_vlc():
    vlc_processes = get_vlc()
    for proc in vlc_processes:
        proc.terminate()