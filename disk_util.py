
import psutil
import platform


## _logger = Logger(component="Metric Agent/Disk")


class DiskMetric:

    def __init__(self):

        # Util.set_metric_agent_configuration()

        # self.config = Util.get_metric_agent_configuration()

        # # _logger.set_log_level(int(self.config["metric.agent"]["log.level"]))

        self.error_message = None

        self.exception = None

    def _get_disk_partition(self, flag, result):

        device_list = []

        try:

            disk_part = psutil.disk_partitions(all=flag)  # False: Only physically connected.

            for device in disk_part:
                device_list.append(device.device)

            result['disk.partitions'] = device_list

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = # _logger.get_error_stack_trace()

            # _logger.error()

    '''
        The below function get_disk_usage() collects the data of every partition except specified
        in agent.json.
    '''

    def _get_disk_usage_metrics(self, status, exclude_disk, result):

        disk_usg = {}

        total = 0

        free = 0

        used = 0

        percent = 0

        try:

            if status == "on":

                disk_list = psutil.disk_partitions(all=False)

                # # _logger.debug("Inside disk usage status = " + status)

                # Check whether given partition exists or not.
                for disk in disk_list:

                    # # _logger.debug("Checking list of disks = " + str(disk))

                    if disk.mountpoint in exclude_disk:

                        # _logger.debug("Excluding Disk = " + str(disk.device))

                        full_device_name = disk.device

                        split_device_name = full_device_name.split("/")

                        device_name = split_device_name[-1]

                        disk_usg['disk.' + device_name.lower()] = "off"
                        # Specified partition will not be considered.

                    else:

                        disk_usage = psutil.disk_usage(disk.mountpoint)

                        full_device_name = disk.device

                        split_device_name = full_device_name.split("/")

                        device_name = split_device_name[-1]

                        disk_usg['disk.' + device_name.lower()] = {

                            "total.byte": disk_usage.total,

                            "used.byte": disk_usage.used,

                            "free.byte": disk_usage.free,

                            "percent": round(disk_usage.percent,2),

                            "mount.path": disk.mountpoint
                        }

                        # _logger.debug("Disk details = " + str(disk_usg['disk.' + device_name.lower()]))

                        total += disk_usage.total

                        used += disk_usage.used

                        free += disk_usage.free

                        percent = ((used / total) * 100)

                result["disk.capacity.byte"] = total

                result["used.disk.byte"] = used

                result["free.disk.byte"] = free

                result["disk.perc"] = round(percent,2)

                result["disk.volume"] = disk_usg

            elif status == "off":

                result["disk.usage"] = "off"

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = # _logger.get_error_stack_trace()

            # _logger.error()

    '''
        The below function get_disk_stats() collects the data of every partition except specified
        in agent.json.
    '''

    def _get_disk_io_metrics(self, status, exclude_disk, result):

        disk_stats = {}

        try:

            if status == "on":

                disk_io = psutil.disk_io_counters(perdisk=False, nowrap=True)

                result["disk.read.byte"] = disk_io[2]

                result["disk.write.byte"] = disk_io[3]

                result["disk.read.time.sec"] = round((disk_io[4] / 1000),2)

                result["disk.write.time.sec"] = round((disk_io[5] / 1000),2)

                disk_list = psutil.disk_partitions(all=False)

                # Check whether given partition exists or not.
                for disk in disk_list:

                    if disk.mountpoint in exclude_disk:

                        # _logger.debug("Excluding Disk = " + str(disk.device).lower())

                        full_device_name = disk.device

                        split_device_name = full_device_name.split("/")

                        device_name = split_device_name[-1]

                        disk_stats['disk.stats.' + device_name.lower()] = "off"
                        # Specified partition will not be considered.

                    else:

                        disk_io = psutil.disk_io_counters(perdisk=True, nowrap=True)

                        if platform.system() == "Linux":

                            full_device_name = disk.device

                            split_device_name = full_device_name.split("/")

                            device_name = split_device_name[-1]

                            disk_stats['disk.stats.' + device_name.lower()] = {

                                "read.byte": disk_io[device_name][2],

                                "write.byte": disk_io[device_name][3],

                                "read.time.sec": round((disk_io[device_name][4] / 1000),2),

                                "write.time.sec": round((disk_io[device_name][5] / 1000),2),
                            }

                            # _logger.debug(
                            #     "Getting disk stats = " + str(disk_stats['disk.stats.' + device_name.lower()]))

                        else:

                            windows_disk_list = disk_io.keys()

                            for disk_name in windows_disk_list:
                                disk_stats['disk.stats.' + disk_name.lower()] = {

                                    "read.byte": disk_io[disk_name][2],

                                    "write.byte": disk_io[disk_name][3],

                                    "read.time.sec": round((disk_io[disk_name][4] / 1000),2),

                                    "write.time.sec": round((disk_io[disk_name][5] / 1000),2),
                                }

                                # _logger.debug(
                                #     "Getting disk stats = " + str(disk_stats['disk.stats.' + disk_name.lower()]))

                result["partition.stats"] = disk_stats

                # _logger.debug("Collected Disk stats details = " + str(result["partition.stats"]))

            elif status == "off":

                result["disk.stats"] = "off"

                # _logger.debug("Collected Disk stats details = " + str(result["disk.stats"]))

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = # _logger.get_error_stack_trace()

            # _logger.error()

    '''
       The below function get_interface_stats() only collects the data of interface specified
       in agent.json.
    '''

    # ----------------------------------------Disk---------------------------------------------

    def disk_metric_func(self):

        disk_metric_data = {}

        # _logger.info("Collecting disk metric data ...")

        try:

            # 'flag = self.config["metric.agent"]["disk.metric.status"]
            flag = Util.get_disk_metric_status()

            exclude_disk_list = Util.get_list_of_disks()
            # 'exclude_disk_list = self.config["metric.agent"]["disks"]

            self._get_disk_partition(flag=False, result=disk_metric_data)

            self._get_disk_usage_metrics(flag, exclude_disk_list, disk_metric_data)

            self._get_disk_io_metrics(flag, exclude_disk_list, disk_metric_data)

            # Print will be replaced by zmq_publisher_method. print(disk_metric_data)
            print(disk_metric_data)

            # _logger.debug("Collected Disk metric data = " + str(disk_metric_data))

            return True

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = # _logger.get_error_stack_trace()

            # _logger.error()

            return False


if __name__ == '__main__':

    disk_metric = DiskMetric()

    DiskMetric.disk_metric_func()
