#!/usr/bin/env python3

import random

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr = rp.PilotManager(session=session)
        umgr = rp.UnitManager(session)

        pds  = list()
        for i in range(3):
            pd  = rp.ComputePilotDescription({
                'resource'      : 'local.localhost',
                'runtime'       : 60,
                'exit_on_error' : True,
                'cores'         : 64 * (i + 1),
                'gpus'          :  8 * (i + 1),
            })
            pds.append(pd)

        pilots = pmgr.submit_pilots(pds)
        umgr.add_pilots(pilots)

        cuds = list()
        for _ in range(512):
            cud = rp.ComputeUnitDescription({
                'executable'      : '/tmp/hello_rp.sh',
                'arguments'       : [random.randint(1, 10)],
                'cpu_process_type': rp.MPI,
                'cpu_processes'   : random.randint(1, 4),
                'gpu_processes'   : random.choice([0] * 50 + [1] * 5 + [2] * 2),
                'pre_exec'        : ['sleep 1'],
                'post_exec'       : ['sleep 1'],
              # 'pre_launch'      : ['export RP_LAUNCH="launch"'],
              # 'pre_exec'        : ['export RP_EXEC="exec"'],
              # 'pre_rank'        : {0: ['export RP_RANK=foo'],
              #                      1: ['export RP_RANK=bar']},
            })
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


# ------------------------------------------------------------------------------

