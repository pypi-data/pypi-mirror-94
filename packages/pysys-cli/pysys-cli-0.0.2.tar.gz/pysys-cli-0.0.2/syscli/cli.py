import platform

import click
import psutil


@click.command()
@click.option("-c", "--cpu", default=False, is_flag=True)
@click.option("-m", "--memroy", default=False, is_flag=True)
@click.option("-d", "--disk", default=False, is_flag=True)
def cli(cpu, memroy, disk):
    if cpu:
        res = "{:.2f}".format(psutil.cpu_freq().current / 1000) + " GHz "
        res += f"{psutil.cpu_count(logical=False)}核"
        res += f" {psutil.cpu_count()}线程"
        print(res)
        return
    if memroy:
        mem = psutil.virtual_memory()
        total = "{:.2f}".format(mem.total / 1073741824)
        available = "{:.2f}".format(mem.available / 1073741824)
        print(f"total: {total}G\navailable: {available}G")
        return
    if disk:
        usage = psutil.disk_usage("/")
        if platform.system() == "Darwin":
            unit = 10 ** 9
        else:
            unit = 1073741824
        total = "{:.2f}".format(usage.total / unit)
        free = "{:.2f}".format(usage.free / unit)
        print(f"total: {total}G\nfree: {free}G")
        return
