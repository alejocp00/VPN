class LogManager:
    def __init__(self, log_file_path):
        self.__logs = []

    def add_log(self, log):
        self.__logs.append(log)

    def get_all_log(self):
        return self.__logs

    def print_logs(self):
        for log in self.__logs:
            print(log)
