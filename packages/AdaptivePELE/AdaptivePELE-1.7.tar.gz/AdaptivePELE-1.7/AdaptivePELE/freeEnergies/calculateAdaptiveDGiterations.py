from __future__ import absolute_import, division, print_function, unicode_literals
from six import reraise as raise_
import sys
import os
import argparse
import shutil
import glob
import itertools
from AdaptivePELE.freeEnergies import estimateDGAdaptive, prepareMSMFolders


def parse_arguments():
    """
        Create command-line interface
    """
    desc = "Plot information related to an MSM"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("nTrajs", type=int, help="Number of trajectories")
    parser.add_argument("-c", "--clusters", type=int, nargs="*", help="Number of clusters to analyse")
    parser.add_argument("-l", "--lagtimes", type=int, nargs="*", help="Lagtimes to analyse")
    parser.add_argument("--nRuns", type=int, default=10, help="Number of independent calculations")
    parser.add_argument("--resume", action='store_true', help="Whether to continue previous calculations")
    args = parser.parse_args()
    return args.nTrajs, args.clusters, args.lagtimes, args.nRuns, args.resume


def isfinished(folders):
    if not folders:
        return False
    for folder_it in folders:
        if not os.path.exists(os.path.join(folder_it, "results_summary.txt")):
            return False
    return True


def move(listFiles, dest):
    for element in listFiles:
        shutil.move(element, dest)


def main(trajsPerEpoch, clusters, lagtimes, nruns, resume=False):
    runFolder = os.getcwd()
    print("Running from " + runFolder)
    for tau, k in itertools.product(lagtimes, clusters):
        destFolder = "%dlag/%dcl" % (tau, k)
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)
        os.chdir(destFolder)
        folders_MSM = glob.glob("MSM_*")
        if isfinished(folders_MSM):
            print("Skipping run with lagtime %d, clusters %d" % (tau, k))
            os.chdir(runFolder)
            continue
        if not resume:
            for folder in folders_MSM:
                shutil.rmtree(folder)
        prepareMSMFolders.main(trajsPath=runFolder)
        print("***************")
        print("Estimating dG value in folder" + os.getcwd())
        try:
            estimateDGAdaptive.main(trajsPerEpoch, tau, k, nruns=nruns, resuming=resume)
        except Exception as err:
            if "distribution contains entries smaller" in str(err):
                print("Caught exception in step with lag %d and k %d, moving to next iteration" % (tau, k))
                with open("error.txt", "w") as fe:
                    fe.write("Caught exception in step with lag %d and k %d, moving to next iteration\n" % (tau, k))
            else:
                raise_(*sys.exc_info())
        os.chdir(runFolder)

if __name__ == "__main__":
    ntrajs, clusters_list, lagtimes_list, nRuns, resuming = parse_arguments()
    main(ntrajs, clusters_list, lagtimes_list, nRuns, resume=resuming)
