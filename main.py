# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess

import psutil
import platform
import pymongo


def get_os_type():
    try:

        # print('inside os type')

        # os_type_raw = psutil.Popen(["systemd-detect-virt"])

        os_type_raw = subprocess.Popen(['systemd-detect-virt'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        os_type_encode, stderr = os_type_raw.communicate()

        # os_type_encode, _ = os_type_raw.communicate()[0]

        # print(os_type_encode)

        os_type = os_type_encode.decode('utf-8')

        return os_type.strip()

    except Exception as ex:

        print("Exception = " + ex)

        # _logger.error()

        return None


class CPUMetric:

    def _get_all_cpu_percent(self, result):

        try:
            result['cpu.core.perc'] = psutil.cpu_percent(percpu=True)

        except Exception as ex:

            self.error_message = str(ex)

    def _get_cpu_metrics(self, result):

        try:

            data_cpu_stats = {}

            cpu_stats = psutil.cpu_stats()

            cpu_freq = psutil.cpu_freq()

            data_cpu_stats["context.switches"] = cpu_stats.ctx_switches

            data_cpu_stats["interrupts"] = cpu_stats.interrupts

            if platform.system() == "Linux":
                # _logger.info("Collecting only linux data")

                data_cpu_stats["soft.interrupts"] = cpu_stats.soft_interrupts

            if platform.system() == "Windows":
                # _logger.info("Collecting only Windows data")

                data_cpu_stats["syscalls"] = cpu_stats.syscalls

            result['cpu.stats'] = data_cpu_stats

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()

    def _get_cpu_load_metrics(self, result):

        cpu_avg_load = {}

        try:

            cpu_load = psutil.getloadavg()

            if platform.system() != "Windows":
                # _logger.info("Collecting only Windows data CPU Load")

                cpu_avg_load['cpu.load.avg1.min'] = cpu_load[0]

                cpu_avg_load['cpu.load.avg5.min'] = cpu_load[1]

                cpu_avg_load['cpu.load.avg15.min'] = cpu_load[2]

                result["cpu.load"] = cpu_avg_load

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()

    def _get_cpu_times(self, result):

        cpu_times_metric = {}

        try:

            cpu_times = psutil.cpu_times(percpu=False)

            # print('checking os = ')
            os = get_os_type()
            # print('checking os = ' + os)

            if os is not None:
                print("inside")
                cpu_times_metric["guest"] = cpu_times[5]  # guest
                cpu_times_metric["guest.nice"] = cpu_times[6]  # guest nice

            else:

                cpu_times_metric["nice"] = cpu_times[0]

                cpu_times_metric["iowait"] = cpu_times[1]
                cpu_times_metric["irq"] = cpu_times[2]
                cpu_times_metric["softirq"] = cpu_times[3]
                cpu_times_metric["steal"] = cpu_times[4]

            result["cpu.times"] = cpu_times_metric

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()

    def _get_cpu_times_core(self, cpu_core_metric):

        cpu_core_list = {}
        core = 0

        try:

            cpu_times_list = psutil.cpu_times(percpu=True)

            os = get_os_type()

            for cpu_times in cpu_times_list:

                if os == "oracle":

                    cpu_core_list["guest"] = cpu_times[5]  # guest
                    cpu_core_list["guest.nice"] = cpu_times[6]  # guest nice

                else:

                    cpu_core_list["nice"] = cpu_times[0]
                    cpu_core_list["iowait"] = cpu_times[1]
                    cpu_core_list["irq"] = cpu_times[2]
                    cpu_core_list["softirq"] = cpu_times[3]
                    cpu_core_list["steal"] = cpu_times[4]

                cpu_core_metric["cpu.times.core." + str(core)] = cpu_core_list

                core += 1

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()

    def cpu_metric_func(self):

        cpu_metric_data = {}

        try:

            self._get_all_cpu_percent(result=cpu_metric_data)

            self._get_cpu_metrics(result=cpu_metric_data)

            self._get_cpu_load_metrics(result=cpu_metric_data)

            self._get_cpu_times(result=cpu_metric_data)

            self._get_cpu_times_core(cpu_metric_data)

            print("CPU metric")

            print(cpu_metric_data)

            return cpu_metric_data

            # _logger.debug("Collected CPU metric information = " + str(cpu_metric_data))

        except Exception as ex:

            print("Exception = " + ex)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    result = {}

    cpu_metric = CPUMetric()

    result = cpu_metric.cpu_metric_func()

#     Adding mongodb connections

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["netmos"]

    hostname = platform.node()

    mycol = mydb[hostname]

    x = mycol.insert_one(result)

    dblist = myclient.list_database_names()
    if "netmos" in dblist:
        print("The database exists.")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
