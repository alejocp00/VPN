class LogManager:
    def __init__(self):
        self.__logs = []
        self.__new_log = False
        self.__logs_to_show = 10

    def add_log(self, log):
        self.__new_log = True
        self.__logs.append(log)

    def get_all_log(self):
        return "\n".join(self.__logs)

    def get_logs(self):
        """Return the amount of logs indicated by __logs_to_show

        Returns:
            string: logs formatted to be printed
        """

        # Update flag
        self.__new_log = False

        # Check if are enough logs
        if len(self.__logs) < self.__logs_to_show:
            return "\n".join(self.__logs)

        return "\n".join(self.__logs[-self.__logs_to_show])

    def new_logs(self):
        return self.__new_log
