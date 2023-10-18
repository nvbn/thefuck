import json
import thefuck.const as const


class CommandRecords(object):
    """Object to interact with 'records.json' data"""
    def __init__(self):
        """Opens 'records.json' if available"""
        try:
            with open("records.json", "r") as records_file:
                self.statistics = json.load(records.file)
        except:
            self.statistics = const.DEFAULT_RECORDS_DICT

    
    def add_records(self, category, **kwargs):
        """Creates new records from arguments
        and dumps information to 'records.json'
        
        :type commands: Iterable[thefuck.types.CorrectedCommand]
        :type category: Const string
        """
        if category == const.APPLIED_RULES:
            for command in kwargs['command_list']:
                try:
                    self.statistics[const.APPLIED_RULES][command.script] +=1
                except KeyError:
                    self.statistics[const.APPLIED_RULES].update({command.script: 1})

        elif category == const.SELECTED_RULES:
            command = kwargs['command_single']
            try:
                self.statistics[const.SELECTED_RULES][command.script] += 1
            except KeyError:
                self.statistics[const.SELECTED_RULES].update({command.script: 1})

        elif category == const.NO_FUCKS_GIVEN:
            self.statistics[const.NO_FUCKS_GIVEN] += 1

    def clear_records(self):
        self.statistics = const.DEFAULT_RECORDS_DICT
        self.save()

    def save(self):
        with open("records.json", "w") as records_file:
            json.dump(self.statistics, records_file)