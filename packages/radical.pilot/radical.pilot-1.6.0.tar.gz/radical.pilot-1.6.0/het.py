#!/usr/bin/env python

import random

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'debug.summit',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 1024 * 42
                  }
        pdesc = rp.PilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        tmgr  = rp.TaskManager(session=session)
        tmgr.add_pilots(pilot)

        n    = 1024 * 32
        tds = list()
        for i in range(0, n):

            td = rp.TaskDescription()
          # td.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            td.executable       = '/bin/sleep',
            td.arguments        = [random.randint(1, 30) * 1]
            td.gpu_processes    = random.choice([0, 0, 0, 0, 0, 1, 1, 2, 3])
            td.cpu_processes    = random.randint(1, 16)
            td.cpu_threads      = random.randint(1, 8)
            td.gpu_process_type = rp.MPI
            td.cpu_process_type = rp.MPI
            td.cpu_thread_type  = rp.OpenMP
            tds.append(td)

        tmgr.submit_tasks(tds)
        tmgr.wait_tasks()


# ------------------------------------------------------------------------------

