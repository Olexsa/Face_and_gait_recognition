import psutil
import GPUtil
import concurrent.futures
import time



def example_function():
    result = 0
    for i in range(1000000):
        result += i
    return result


def monitor(interval=1, duration=5, CPUkernels=False):
    start_time = time.time()
    while time.time() - start_time < duration:
        st_time = time.time()
        # Resident Set Size (RSS), объем оперативной памяти, занятый текущим процессом
        print(f"RSS : {psutil.Process().memory_info().rss / 1024 ** 2:.2f} МБ")
        print(f"Использование RAM: {psutil.virtual_memory().percent}%")
        print(f"Общая загрузка CPU: {psutil.cpu_percent()}%")
        if CPUkernels:
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
                print(f"Ядро {i}: {percentage}%")
        for i, gpu in enumerate(GPUtil.getGPUs()):
            print(f"GPU {i+1} Испоользуется: {gpu.load * 100}%")
            print(f"GPU Используемая память: {gpu.memoryUsed} MB из {gpu.memoryTotal} MB")
        print(f"Затраченное на вывод время: {time.time() - st_time:.5f} сек", end='\n\n')

        time.sleep(interval)


if __name__ == "__main__":
    strattime = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        code_execution_future = executor.submit(example_function)
        monitor_cpu_future = executor.submit(monitor)
        code_execution_result = code_execution_future.result()
        monitor_cpu_future.result()
    print(f"Затраченное время: {time.time() - start_time:.5f} сек")

