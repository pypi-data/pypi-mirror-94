'''The scheduler manages cron-like actions being programmed and automatically
   executed by the Appy server, as "virtual" requests.'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2021 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import time

from appy.server.handler import VirtualHandler

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
MIN_KO   = 'Config attribute "jobs.minutes" must be an integer being higher ' \
           'or equal to 1.'
MISSING  = 'Missing %s for a job.'
WRONG_TD = 'Wrong timedef "%s".'
TD_KO    = '%s. Must be of the form "m h dom mon dow".' % WRONG_TD
TD_P_KO  = '%s. Every part must be char "*" or an integer.' % WRONG_TD

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Job:
    '''Represents a job that must be executed in the context of the scheduler'''

    def __init__(self, method):
        # Running a job consists in executing a method as defined on the tool.
        # m_method is the name of this method.
        method = method.strip() if method else method
        if not method: raise Exception(MISSING % 'method')
        self.method = method
        # This instance will also hold more information, stored by the Appy
        # server itself. For example, if this job is scheduled at regular
        # intervals, the date of the last execution will be stored on this Job
        # instance. Consequently, do not reuse the same job instance for several
        # config entries. In order to avoid name clashes, any attribute added by
        # Appy will start with an underscore.
        # ~~~
        # By default, the job will lead to a database commit. As for any other
        # method executed in the context of a UI request, if m_method must not
        # lead to a commit (either because the job, intrinsically, dos not
        # update any data in the database, or because an error occurred), the
        # method can access the currently running handler and set its "commit"
        # attribute, ie:
        # 
        #                      tool.H().commit = False

    def run(self, scheduler):
        '''Runs this job'''
        server = scheduler.server
        # Create a Virtual handler for that
        handler = VirtualHandler(server)
        # Run the job
        server.database.run(self.method, handler, scheduler.logger)
        # Unregister the virtual handler
        VirtualHandler.remove()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Scheduler configuration, defining the list of planned jobs.'''

    def __init__(self):
        # The scheduler will be run every "minutes" minutes. It is not advised
        # to change this value, at the risk of being unable to conform to the
        # crontab semantics.
        # ~~~
        # For example, if you decide to set the value to 5, every timeDef entry
        # where the "minutes" part is not a multiple of 5 will never match.
        self.minutes = 1
        # Attribute "all" lists all the planned jobs. Every entry in this list
        # must be a tuple (timeDef, Job).
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # timeDef | Refers to a string defining when the job must be executed.
        #         | It must be a string conforming to the crontab syntax, the
        #         | last element excepted. Let's explain it with an example. The
        #         | following crontab entry executes a script everyday, at
        #         | 00:30:
        #         |
        #         |    # m h dom mon dow command
        #         |    30 0 * * * /some/path/to/a/script
        #         |
        #         | The corresponding timeDef entry for a Appy job would be:
        #         | 
        #         |    "30 0 * * *"
        #         |
        #         | Instead of executing a script as defined in a standard
        #         | crontab entry, a Job instance must be specified, as
        #         | described hereafter.
        #         |
        #         | Currently, only a subset of the crontab syntax is
        #         | implemented: any entry can be the star (*) or a integer
        #         | number. Entries like */3, 2-3, 5,8 or 2-5/3 are not
        #         | implemented yet.
        #         |
        #         | Moreover, in the future, the syntax will be extended to
        #         | incorporate load-related definitions. The goal is to
        #         | implement behaviours like this one: "execute this job
        #         | if the system load was low during the last hour".
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Job     | A Job instance (see class Job hereabove), defining the
        #         | method to execute.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Method m_add below may be used to easily add a job to this list.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.all = []

    def check(self):
        '''Ensures the Scheduler config is correct'''
        # Check attribute "minutes"
        minutes = self.minutes
        if not isinstance(minutes, int) or (minutes < 1):
            raise Exception(MIN_KO)
        # Check timeDefs
        for timeDef, job in self.all:
            timeDef = timeDef.strip() if timeDef else timeDef
            if not timeDef: raise Exception(MISSING % 'timeDef')
            parts = timeDef.split()
            if len(parts) != 5:
                raise Exception(TD_KO % timeDef)
            for part in parts:
                if (part != '*') and not part.isdigit():
                    raise Exception(TD_P_KO % timeDef)

    def add(self, timeDef, method):
        '''Adds a job to p_self.all, or running this m_method according to this
           p_timeDef.'''
        self.all.append( (timeDef, Job(method)) )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Scheduler:
    '''The Appy scheduler'''

    # Mapping between the parts of a timeDef and the names of the corresponding
    # parts in the struct returned by time.localtime():
    #
    # - each key is the index of the value in the timeDef ;
    # - each value is a tuple (j, delta, ifNegative):
    #
    #   * "j" is the index of the corresponding part in the data structure
    #     returned by time.localtime() ;
    #
    #   * "delta" is an optional value to add to the value as returned by
    #     time.localtime(). Indeed, Python values may differ from those defined
    #     by the crontab syntax. For example, according to Python, 0 is the
    #     number for Monday; according to cron, it is the number for Sunday
    #     (together with 7). By applying a delta of -1 to the Python value, a
    #     correct comparison may de done ;
    #
    #   * "ifNegative" is the number to add to the Python value, if negative,
    #     after the "delta" has been applied to it. In the previous example, if
    #     0 (Sunday) is specified, applying -1 produces -1, being negative.
    #     Adding 7 produces the correct corresponding Python value.
    codeMap = {
      4: (6, -1, 7), # Day of the week - Monday is 0 (Python) or 1 (cron)
      3: (1,  0, 0), # Month number    - from 1 to 12
      2: (2,  0, 0), # Day number      - from 1 to 31
      1: (3,  0, 0), # Hour            - from 0 to 23
      0: (4,  0, 0)  # Minutes         - from 0 to 59
    }

    def __init__(self, server):
        '''A unique Scheduler instance is created per Appy server'''
        # The Server instance
        self.server = server
        self.logger = server.loggers.app
        # The scheduler will run every "minutes" minutes. The minimum is 1.
        self.config = server.config.jobs
        self.minutes = self.config.minutes if self.config else None
        # Store, in attribute "last", the last minute corresponding to the last
        # scheduler execution. It allows to prevent several executions of the
        # same job(s) at the same minute.
        # ~~~
        self.last = time.localtime().tm_min
        # This attribute is initialised to the current minute. It means that, as
        # soon as the Appy server is started, the scheduler will not be able to
        # run until a minute elapses. This is very important in the context of
        # an automatic Appy server restart. Imagine a job that automatically
        # restarts the server. If the job takes less than one minute to execute,
        # the Appy server restarts, and, if "last" is empty, the job is executed
        # again... and again, as many times as it can within a minute.

    def mustRun(self, job, now, timeDef):
        '''Must this p_job be run, according to this p_timeDef(inition) ?'''
        parts = timeDef.split()
        # Walk parts from the last (dow) to the first part (minutes)
        for i, info in Scheduler.codeMap.items():
            part = parts[i]
            # Part "*" always matches
            if part == '*': continue
            j, delta, ndelta = info
            # Update the current part with the delta. Currently, every part must
            # be an integer number.
            part = int(part) + delta
            if part < 0:
                part += ndelta
            # Values can now be compared
            if part != now[j]:
                return
        return True

    def runJobs(self):
        '''It's time to check if jobs must be run. Scan p_self.all and run
           jobs defined in it that must be run right now.'''
        jobs = self.config.all
        if not jobs: return
        now = time.localtime()
        for timeDef, job in jobs:
            if self.mustRun(job, now, timeDef):
                job.run(self)

    def scanJobs(self):
        '''This method is called by the server's infinite loop and checks
           whether jobs must be ran.'''
        # This method is called every "config.server.pollInterval" seconds. This
        # is too much: perform a real execution every "self.minutes" minutes.
        if not self.minutes: return
        current = time.localtime().tm_min
        if (current % self.minutes) or (current == self.last): return
        # Run jobs that must be run
        self.last = current
        self.runJobs()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
