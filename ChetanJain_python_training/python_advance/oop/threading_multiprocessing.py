

import os
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List
from python_advance.constants import (
    THREAD_SLEEP_DURATION,
    NUMBER_RANGE_START,
    NUMBER_RANGE_END,
    THREAD_COUNT,
    PROCESS_COUNT,
)


def print_numbers_in_thread(thread_identifier: str, upper_limit: int) -> None:
    """
    Print numbers from 1 to upper_limit tagged with thread_identifier.
    """
    for number in range(1, upper_limit + 1):
        print(f"[Thread {thread_identifier}] Number: {number}")


def create_two_threads_printing_numbers() -> None:

    first_thread = threading.Thread(
        target=print_numbers_in_thread, args=("A", 5)
    )
    second_thread = threading.Thread(
        target=print_numbers_in_thread, args=("B", 5)
    )
    first_thread.start()
    second_thread.start()
    first_thread.join()
    second_thread.join()


def compute_sum_in_thread(start: int, end: int) -> None:

    total_sum: int = sum(range(start, end + 1))
    print(f"Sum from {start} to {end} = {total_sum}")


def demonstrate_thread_join() -> None:
    """
    Demonstrate the join() method ensuring main thread waits for child threads.
    """
    sum_thread = threading.Thread(
        target=compute_sum_in_thread,
        args=(NUMBER_RANGE_START, NUMBER_RANGE_END)
    )
    sum_thread.start()
    sum_thread.join()
    print("Main thread continues after sum_thread completes.")


def simulate_file_download(file_name: str, download_duration: float) -> None:

    print(f"Starting download: {file_name}")
    time.sleep(download_duration)
    print(f"Completed download: {file_name}")


def create_download_simulation_threads() -> None:
    """
    Create multiple threads simulating file downloads using time.sleep().
    """
    file_download_tasks: List[tuple] = [
        ("report.pdf", 2.0),
        ("image.png", 1.0),
        ("video.mp4", 3.0),
    ]
    download_threads: List[threading.Thread] = []
    for file_name, duration in file_download_tasks:
        download_thread = threading.Thread(
            target=simulate_file_download, args=(file_name, duration)
        )
        download_threads.append(download_thread)
        download_thread.start()

    for download_thread in download_threads:
        download_thread.join()


def print_process_id(process_label: str) -> None:

    print(f"[Process {process_label}] PID: {os.getpid()}")


def create_two_processes_printing_pids() -> None:

    first_process = multiprocessing.Process(
        target=print_process_id, args=("One",)
    )
    second_process = multiprocessing.Process(
        target=print_process_id, args=("Two",)
    )
    first_process.start()
    second_process.start()
    first_process.join()
    second_process.join()


def compute_square_of_number(number: int) -> int:

    square: int = number ** 2
    print(f"Square of {number} = {square}")
    return square


def compute_squares_with_multiprocessing(number_list: List[int]) -> None:

    process_list: List[multiprocessing.Process] = []
    for number in number_list:
        computation_process = multiprocessing.Process(
            target=compute_square_of_number, args=(number,)
        )
        process_list.append(computation_process)
        computation_process.start()

    for computation_process in process_list:
        computation_process.join()


def execute_with_thread_pool(number_list: List[int]) -> List[int]:

    with ThreadPoolExecutor() as thread_executor:
        results: List[int] = list(
            thread_executor.map(compute_square_of_number, number_list)
        )
    return results


def execute_with_process_pool(number_list: List[int]) -> List[int]:

    with ProcessPoolExecutor() as process_executor:
        results: List[int] = list(
            process_executor.map(compute_square_of_number, number_list)
        )
    return results