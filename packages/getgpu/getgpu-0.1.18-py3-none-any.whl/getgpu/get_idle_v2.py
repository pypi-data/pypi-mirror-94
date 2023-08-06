import os
import re
import pickle
from datetime import datetime
from icecream import ic

def get_profile_name(memory_total):
    total = int(memory_total)
    if total < 5500:
        return 'MIG 1g.5gb'
    elif total < 11000:
        return 'MIG 2g.10gb'
    elif total < 22000:
        return 'MIG 4g.20gb'
    else:
        return 'MIG 7g.40gb'

def update_history(gpu_info, history_filename='/home/seilna/.gpu_history.pkl'):

    if not os.path.exists(history_filename):
        with open(history_filename, 'wb') as f:
            pickle.dump({}, f)

    with open(history_filename, 'rb') as f:
        history = pickle.load(f)

    # 각 gpu 마다 사용 히스토리를 업데이트
    for gpu_name, gpu_status in gpu_info.items():
        if gpu_name not in history:
            history[gpu_name] = {}

        # 해당 gpu (mig device 포함) 를 사용중인 유저를 수집
        users = set()
        for process in gpu_status['processes']:
            users.append(process['user'])

        for mig_name, mig_status in gpu_status['mig'].items():
            for process in mig_status['processes']:
                users.add(process['user'])

        # 유저의 최근 사용 시각을 업데이트
        for user in users:
            history[gpu_name][user] = datetime.now()

    with open(history_filename, 'wb') as f:
        pickle.dump(history, f)

    return history

def get_gpu_info():
    gpu_info = {}
    smi = os.popen('nvidia-smi').read().split('\n')

    mode='gpu'

    mig_id = 0
    device_names = os.popen('nvidia-smi -L').read().split('\n')
    mig_names = [name for name in device_names if 'MIG' in name]
    gpu_names = [name for name in device_names if 'A100-SXM4-40GB' in name]

    for line in smi:
        if 'MIG devices:' in line:
            mode = 'mig'

        elif 'Processes:' in line:
            mode = 'process'

        if mode == 'gpu':
            # gpu 정보를 파싱
            if 'A100-SXM4-40GB' in line:
                line = line.replace('|', '').split()
                gpu_id = line[0]

            if line.count('W') == 2:
                memory = re.findall('([0-9]+)MiB', line)
                uuid = re.findall('UUID: (GPU-[0-9a-z\-\/]+)', gpu_names[int(gpu_id)])[0]
                name = 'GPU %d: A100-SXM4-40GB' % int(gpu_id)
                if len(memory) > 0:
                    used, total = memory[0], memory[1]
                    gpu_info[name] = {'used': used, 'total': total, 'mig': {}, 'uuid': gpu_id, 'processes': []}

                else:
                    gpu_info[name] = {'used': 'N/A', 'total': 'N/A', 'mig': {}, 'uuid': gpu_id, 'processes': []}

        # mig instance 정보를 파싱
        elif mode == 'mig':
            memory = re.findall('([0-9]+)MiB', line)
            if len(memory) == 0:
                continue

            line = line.replace('|', '').split()
            if len(line) < 12:
                continue

            gpu_name = 'GPU %d: A100-SXM4-40GB' % int(line[0])
            used, total = memory[0], memory[1]
            name = mig_names[mig_id].split(':')[0].strip()
            uuid = re.findall('UUID: (MIG-GPU-[0-9a-z\-\/]+)', mig_names[mig_id])[0]
            mig_id += 1

            gpu_info[gpu_name]['mig'][name] = {
                'used': used,
                'total': total,
                'uuid': uuid,
                'processes': []
            }

        elif mode == 'process':

            # nvidia-smi 를 파싱해서 프로세스 정보 얻어오기
            process_line = re.findall('[0-9]+MiB', line)
            if len(process_line) == 0:
                continue

            line = line.replace('|', '').split()
            gpu_id, gi_id, ci_id, pid, process_name, used_memory = \
                line[0], line[1], line[2], line[3], line[5], line[6].replace('MiB', '')

            # process pid 로 소유자 계정 조회
            user = os.popen('ps -u -p {} | awk "NR>1"'.format(pid)).read().split()[0]

            gpu_name = [name for name in gpu_info.keys() if 'GPU {}'.format(gpu_id) in name][0]

            mig_name =  [
                name for name, status in gpu_info[gpu_name]['mig'].items() \
                if '{}/{}'.format(gi_id, ci_id) in status['uuid']
            ]

            # mig device 위에서 도는 프로세스 정보 입력
            if len(mig_name) > 0:
                gpu_info[gpu_name]['mig'][mig_name[0]]['processes'].append(
                    {'user': user, 'name': process_name, 'used_memory': used_memory}
                )

            # gpu device 위에서 도는 프로세스 정보 입력
            else:
                gpu_info[gpu_name]['processes'].append(
                    {'user': user, 'name': process_name, 'used_memory': used_memory}
                )


    # mig 활성화된 device 가 있는 경우,
    # 활성화되지 않은 device 에서는 job 을 돌릴 수 없음
    if mode == 'mig':
        for gpu_name, gpu_status in gpu_info.items():
            gpu_info[gpu_name]['used'] = 'N/A'
            gpu_info[gpu_name]['total'] = 'N/A'

    return gpu_info

def get_idle_v2(n_devices=1, device_name='A100-SXM4-40GB', memory_used_less_than=300):
    assert device_name in [
        'A100-SXM4-40GB',
        '1g.5gb',
        '2g.10gb',
        '3g.20gb',
        '4g.20gb',
        '7g.40gb'
    ], 'The value of `device_name` should be one of "A100-SXM4-40GB", "1g.5gb", "2g.10gb", "3g.20gb", "4g.20gb", "7g.40gb".'

    gpu_info = get_gpu_info()

    idle_devices = []
    idle_devices_group = []
    for gpu_name, gpu_status in gpu_info.items():
        if device_name in gpu_name and \
            gpu_status['total'] != 'N/A' and \
            int(gpu_status['used']) < memory_used_less_than:

            idle_devices_group.append(gpu_status['uuid'])

        if len(idle_devices_group) == n_devices:
            idle_devices.append(','.join(idle_devices_group))
            idle_devices_group = []

        for mig_name, mig_status in gpu_status['mig'].items():
            if device_name in mig_name and \
                int(mig_status['used']) < memory_used_less_than:
                idle_devices_group.append(mig_status['uuid'])

            if len(idle_devices_group) == n_devices:
                idle_devices.append(','.join(idle_devices_group))
                idle_devices_group = []

    return idle_devices

def to_pretty(gpu_info):
    history = update_history(gpu_info)

    from socket import gethostname


    ret = '{}\n'.format(gethostname())
    for gpu_name, gpu_status in gpu_info.items():
        used = '{memory: <5}MiB'.format(memory=gpu_status['used']) if gpu_status['used'] != 'N/A' else gpu_status['used']
        total = '{memory: <5}MiB'.format(memory=gpu_status['total']) if gpu_status['total'] != 'N/A' else gpu_status['used']

        # 사용 히스토리 보여주기 (현재 사용중인 유저의 히스토리는 제외)
        current_users = set()
        for process in gpu_status['processes']:
            current_users.add(process['user'])

        for mig_name, mig_status in gpu_status['mig'].items():
            for process in mig_status['processes']:
                current_users.add(process['user'])

        if used == 'N/A':
            ret += '{name: <25}'.format(name=gpu_name)
        else:
            ret += '{name: <25} | {used:9} / {total:9} | '.format(name=gpu_name, used=used, total=total)
            for process_info in gpu_status['processes']:
                ret += '{}({}MiB) '.format(process_info['user'], process_info['used_memory'])
        # history
        for user, last_used in history[gpu_name].items():
            if user in current_users:
                continue
            ret += '{}({:d}h ago)'.format(user, 1 + int((datetime.now() - last_used).total_seconds() // 3600))
        ret += '\n'

        for mig_name, mig_status in gpu_status['mig'].items():
            used = '{memory: <5}MiB'.format(memory=mig_status['used'])
            total = '{memory: <5}MiB'.format(memory=mig_status['total'])

            ret += '  {name: <23} | {used: <9} / {total: <9} | '.format(name=mig_name, used=used, total=total)
            for process_info in mig_status['processes']:
                ret += '{}({}MiB) '.format(process_info['user'], process_info['used_memory'])
            ret += '\n'


    return ret

if __name__ == '__main__':
    get_gpu_info()

    idle = get_idle_v2(
        n_devices=2,
        # device_name='2g.10gb'
    )
