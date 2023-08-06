import os
import inspect


class Autograder(object):
    '''Autograders test suite'''

    def setup(self):
        '''Setup method that is called before all defined tests'''
        pass

    def before_each(self):
        '''Method that is called before each defined test'''
        pass

    def after_each(self):
        '''Method that is called after each defined test'''
        pass

    def tear_down(self):
        '''Tear down method that is called after all defined tests'''
        pass

    def check(self):
        '''Checks all defined test

        Parameters
        ----------
        cwd: str
            Current working directory

        Returns
        -------
        dict
            Submit result
        '''
        details = {}
        stdouts = ''
        stderrs = ''
        total = 0

        # setup tests
        self.setup()

        # get all _test defined methods
        for (name, method) in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.lower().strip().endswith('_test'):
                self.before_each()
                note, message, stdout, stderr = method()
                name = method.__doc__ or method.__name__
                total += note
                details[method.__name__[:-5]] = {
                    'name': name,
                    'grade': note,
                    'message': message
                }
                # append stdout
                if stdout:
                    stdouts += f'{name}:stdout' + (os.linesep * 2)
                    stdouts += stdout + (os.linesep * 2)
                # append stderr
                if stderr:
                    stderrs += f'{name}:stderr' + (os.linesep * 2)
                    stderrs += stderr + (os.linesep * 2)
                self.after_each()

        # tear down test suite
        self.tear_down()

        # convert details to array
        finalDetails = []
        if getattr(self, 'order', None) is not None:
            for key in self.order:
                finalDetails.append(details[key])
        else:
            finalDetails = list(details.values())

        return {
            'grade': min(round(total), 100),
            'details': finalDetails,
            'stdout': stdouts.rstrip(),
            'stderr': stderrs.rstrip()
        }
