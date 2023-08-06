import json

from . import Logger


class Config():
    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).getLogger()

        try:
            with open("/opt/config.json") as config_file:
                try:
                    config = json.load(config_file)
                except Exception as e:
                    raise Exception(
                        "Failed to parse config file. {}".format(e))

                if len(config["trigger"]) == 0:
                    raise Exception(
                        "No trigger defined! Please check config file.")

                triggerCount = 0
                for triggerGroup in config["trigger"]:
                    triggerCount += len(triggerGroup)
                if triggerCount == 0:
                    raise Exception(
                        "No trigger defined! Please check config file.")

                if len(config["action"]) == 0:
                    self.logger.warn(
                        "You have no actions defined."
                        " Please check config file.")

                for triggerGroup in config["trigger"]:
                    for trigger in triggerGroup:
                        if not "action" in trigger or len(trigger["action"]):
                            self.logger.warn(
                                "You have no actions defined in trigger {}."
                                " Please check config file.".format(
                                    trigger["name"]))

                self.config = config
        except OSError:
            raise Exception("Can't find config file please check mount point")

        self.logger.info("Successfully loaded config.json")

    def getConfig(self):
        return self.config
