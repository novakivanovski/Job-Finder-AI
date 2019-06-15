

class InputProcessor:
    def __init__(self, user_input, job, callback):
        self.input = user_input
        self.job = job
        self.callback = callback

    def process(self):
        pass


class PassProcessor(InputProcessor):
    def __init__(self, user_input, job, callback):
        super().__init__(user_input, job, callback)

    def process(self):
        self.job.set_passed(True)


class FailProcessor(InputProcessor):
    def __init__(self, user_input, job, callback):
        super().__init__(user_input, job, callback)

    def process(self):
        self.job.set_passed(True)


class ExitProcessor(InputProcessor):
    def __init__(self, user_input, job, callback):
        super().__init__(user_input, job, callback)

    def process(self):
        print('Exiting...')
        return True


class InvalidProcessor(InputProcessor):
    def __init__(self, user_input, job, callback):
        super().__init__(user_input, job, callback)

    def process(self):
        print('Invalid input. Please try again.')
        return self.callback(self.job)


def get_processor(user_input, job, callback):
    input_processor = processor_map[user_input] if user_input in processor_map else InvalidProcessor
    return input_processor(user_input, job, callback)


processor_map = {'y': PassProcessor, 'n': FailProcessor, 'exit': ExitProcessor}
