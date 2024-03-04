import psutil
import GPUtil
import time
import matplotlib.pyplot as plt
import numpy as np


# На разных размерах файлов


def example_function():
    result = 0
    for i in range(1000000):
        result += i
    return result

def monitor(CPUkernels=False):
    # Resident Set Size (RSS), объем оперативной памяти, занятый текущим процессом
    RSS = psutil.Process().memory_info().rss / (1024 ** 2)
    RAM = psutil.virtual_memory().percent
    CPU = psutil.cpu_percent()
    GPU, GPUmb = [], []
    print(f"\nRSS : {RSS:.2f} МБ \nИспользование RAM: {RAM}% \nОбщая загрузка CPU: {CPU}%", )
    if CPUkernels:
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            print(f"Ядро {i}: {percentage}%")
    for i, gpu in enumerate(GPUtil.getGPUs()):
        GPU.append(gpu.load * 100)
        GPUmb.append(gpu.memoryUsed)
        print(f"GPU {i + 1} Испоользуется: {GPU[i]}%")
        print(f"GPU {i + 1} Используемая память: {GPUmb[i]} MB из {gpu.memoryTotal} MB")
    return (RSS, RAM, CPU), GPU, GPUmb


def test_function(inp_func, N=10, *args, **kwargs):
    timestamps, RSS, RAM, CPU, GPU, GPUmb = [], [], [], [], [], []
    start_time = time.time()
    for i in range(N+1):
        current_time = time.time() - start_time
        timestamps.append(current_time)
        if i:
            inp_func(*args, **kwargs)
        res1, resGPU, resGPUmb = monitor()
        for elem, lst in zip(res1, (RSS, RAM, CPU)):
            lst.append(elem)
        if GPU == []:
            GPU, GPUmb = [[] for _ in range(len(resGPU))], [[] for _ in range(len(resGPUmb))]
        for i in range(len(resGPU)):
            GPU[i].append(resGPU[i])
            GPUmb[i].append(resGPUmb[i])
        time.sleep(1)  # Пауза на 1 секунду (может потребоваться изменение)
    print(f"\nЗатраченное на {N} повторов время: {time.time() - start_time:.5f} сек")

    return timestamps, RSS, RAM, CPU, GPU, GPUmb

def plot_graph(timestamps, RSS, RAM, CPU, GPU, GPUmb):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, RSS, label='RSS')
    for i, gpumb in enumerate(GPUmb):
        plt.plot(timestamps, gpumb, label=f'GPUmb {i + 1}')
    plt.xlabel('Время, сек')
    plt.ylabel('Значения, Мб')
    plt.yticks(np.arange(0, 1025, 64))
    plt.legend()
    plt.title('Мониторинг (RSS)')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, RAM, label='RAM')
    plt.plot(timestamps, CPU, label='CPU')
    for i, gpu in enumerate(GPU):
        plt.plot(timestamps, gpu, label=f'GPU {i + 1}')
    plt.xlabel('Время, сек')
    plt.ylabel('Значения, %')
    plt.yticks(np.arange(0, 101, 5))
    plt.legend()
    plt.title('Мониторинг (RAM, CPU, GPU)')
    plt.show()


if __name__ == "__main__":
    timestamps, RSS, RAM, CPU, GPU, GPUmb = test_function(example_function)
    plot_graph(timestamps, RSS, RAM, CPU, GPU, GPUmb)





