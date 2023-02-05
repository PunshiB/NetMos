import subprocess
import psutil
import platform


class MemoryMetric:

    def __init__(self):

        # Util.set_metric_agent_configuration()

        # self.config = Util.get_metric_agent_configuration()

        # _logger.set_log_level(int(self.config["metric.agent"]["log.level"]))

        # self.error_message = None

        # self.exception = None
        pass

    def _get_memory_metrics(self, result):

        try:

            virt_memory = psutil.virtual_memory()

            swap_memory = psutil.swap_memory()

            result["memory.byte"] = virt_memory.total

            result["available.byte"] = virt_memory.available

            result["used.byte"] = virt_memory.used

            result["free.byte"] = virt_memory.free

            result["buffers.byte"] = virt_memory.buffers

            result["cached.byte"] = virt_memory.cached

            result["available.percent"] = round(((virt_memory.available/virt_memory.total)*100),2)

            result["used.percent"] = round(virt_memory.percent,2)

            result["swap.memory.byte"] = swap_memory.total

            result["swap.memory.perc"] = round(swap_memory.percent,2)

            result["free.swap.memory.byte"] = swap_memory.free

            result["used.swap.memory.byte"] = swap_memory.used

        except Exception as ex:

            self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()

    def memory_metric_func(self):

        memory_metric_data = {}

        try:

            self._get_memory_metrics(memory_metric_data)

            print(memory_metric_data)
            # _logger.debug("Collected Memory metric data = " + str(memory_metric_data))

        except Exception as ex:

            # self.error_message = str(ex)

            # self.exception = _logger.get_error_stack_trace()

            # _logger.error()
            pass


if __name__ == '__main__':

    mem_metric = MemoryMetric()

    mem_metric.memory_metric_func()
