# `getgpu`

Python CLI for getting idle gpu device.

---
## Installation
```
$ pip install getgpu
```
---
## Usage
```python
# test_getgpu.py
gpu_devices = [0,1,2,3]
available_device = getgpu.wait_until_available(device_ids=gpu_devices, timeout=10000)
```
---
## Examples
```shell
# run_multiple_processes_on_gpu.sh
learning_rates=(
  1e-1 1e-2 1e-3 1e-4 1e-5 1e-6 1e-7 1e-8
)

for learning_rate in $learning_rates; do
    gpu_device=$(python -c "import getgpu; getgpu.wait_until_available(device_ids=[0,1,2,3]))
    CUDA_VISIBLE_DEVICES=$gpu_device python main.py --learning_rate=$learning_rate
done
```

