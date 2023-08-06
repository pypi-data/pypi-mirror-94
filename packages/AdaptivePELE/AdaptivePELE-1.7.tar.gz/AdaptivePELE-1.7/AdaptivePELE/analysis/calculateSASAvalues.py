from __future__ import absolute_import, division, print_function, unicode_literals
import os
import glob
import time
import argparse
import numpy as np
import mdtraj as md
import multiprocessing as mp
from AdaptivePELE.utilities import utilities
from AdaptivePELE.analysis import analysis_utils


def parseArguments():
    """
        Parse the command-line options

        :returns: object -- Object containing the options passed
    """
    desc = "Program that caculates the relative SASA of a ligand."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("resname", type=str, help="Ligand resname")
    parser.add_argument("--path", type=str, default=".", help="Path where the simulation is stored")
    parser.add_argument("--top", type=str, default=None, help="Topology file for non-pdb trajectories or path to Adaptive topology object")
    parser.add_argument("--out_name", type=str, default="fixedReport", help="Name of the modified report files (default is fixedReport)")
    parser.add_argument("--out_folder", type=str, default=None, help="Path where to store the report files (default is fixedReport)")
    parser.add_argument("-n", type=int, default=1, help="Number of processors to parallelize")
    parser.add_argument("--fmt_str", type=str, default="%.4f", help="Format of the output file (default is .4f which means all floats with 4 decimal points)")
    parser.add_argument("--new_report", action="store_true", help="Whether to create new report files instead of modifying existing ones")
    parser.add_argument("--traj_to_process", nargs="*", type=int, default=None, help="Number of the trajectories to filter, if not specified all of them will be processed")
    args = parser.parse_args()

    return args.resname, args.path, args.top, args.out_name, args.fmt_str, args.n, args.out_folder, args.new_report, args.traj_to_process


def calculateSASA(trajectory, topology, res_name):
    """
        Calculate the SASA of a ligand in a trajectory

        :param trajectory: Name of the trajectory file
        :type trajectory: str
        :param topology: Topology of the trajectory (needed for non-pdb trajs)
        :type topology: str
        :param res_name: Ligand resname
        :type res_name: str
    """
    utilities.print_unbuffered("Processing", trajectory)
    t = md.load(trajectory, top=topology)
    t.remove_solvent(inplace=True)
    res_atoms = t.top.select("resname '%s'" % res_name)
    if not len(res_atoms):
        raise ValueError("Nothing found using resname %s" % res_name)
    t2 = t.atom_slice(res_atoms)
    for atom in t2.top.atoms:
        # mdtraj complains if the ligand residue index is not 0 when
        # isolated
        atom.residue.index = 0
    res_index = t.top.atom(res_atoms[0]).residue.index
    sasa = md.shrake_rupley(t, mode="residue")
    sasa_empty = md.shrake_rupley(t2, mode="residue")
    return sasa[:, res_index]/sasa_empty[:, 0]


def process_file(traj, top_file, resname, report, outputFilename, format_out, new_report, epoch):
    start = time.time()
    sasa_values = calculateSASA(traj, top_file, resname)
    header = ""
    if not new_report:
        try:
            reportFilename = glob.glob(report)[0]
        except IndexError:
            raise IndexError("File %s not found" % report)
        if outputFilename != reportFilename:
            reportFilename = outputFilename

        with open(reportFilename) as f:
            header = f.readline().rstrip()
            if not header.startswith("#"):
                header = ""
            reportFile = utilities.loadtxtfile(f)

        fixedReport = analysis_utils.extendReportWithRmsd(reportFile, sasa_values)
    else:
        indexes = np.array(range(sasa_values.shape[0]))
        fixedReport = np.concatenate((indexes[:, None], sasa_values[:, None]), axis=1)

    with open(outputFilename, "w") as fw:
        if header:
            fw.write("%s\tSASA\n" % header)
        else:
            fw.write("# Step\tSASA\n")
        np.savetxt(fw, fixedReport, fmt=format_out, delimiter="\t")
    end = time.time()
    print("Took %.2fs to process" % (end-start), traj)


def main(resname, folder, top, out_report_name, format_out, nProcessors, output_folder, new_report, trajs_to_select):
    """
        Calculate the relative SASA values of the ligand

        :param resname: Ligand resname
        :type resname: str
        :param folder: Path the simulation
        :type folder: str
        :param top: Path to the topology
        :type top: str
        :param out_report_name: Name of the output file
        :type out_report_name: str
        :param format_out: String with the format of the output
        :type format_out: str
        :param nProcessors: Number of processors to use
        :type nProcessors: int
        :param output_folder: Path where to store the new reports
        :type output_folder: str
        :param new_report: Whether to create new reports
        :type new_report: bool
        :param trajs_to_select: Number of the reports to read, if don't want to select all
        :type trajs_to_select: set
    """
    # Constants
    if output_folder is not None:
        out_report_name = os.path.join(output_folder, out_report_name)
    outputFilename = "_".join([out_report_name, "%d"])
    trajName = "*traj*"
    reportName = "*report*_%d"
    if nProcessors is None:
        nProcessors = utilities.getCpuCount()
    nProcessors = max(1, nProcessors)
    print("Calculating SASA with %d processors" % nProcessors)
    epochs = utilities.get_epoch_folders(folder)
    if top is not None:
        top_obj = utilities.getTopologyObject(top)
    else:
        top_obj = None
    files = []
    if not epochs:
        # path does not contain an adaptive simulation, we'll try to retrieve
        # trajectories from the specified path
        files = analysis_utils.process_folder(None, folder, trajName, reportName, os.path.join(folder, outputFilename), top_obj, trajs_to_select)
    for epoch in epochs:
        print("Epoch", epoch)
        files.extend(analysis_utils.process_folder(epoch, folder, trajName, reportName, os.path.join(folder, epoch, outputFilename), top_obj, trajs_to_select))
    print("Starting to process files!")
    pool = mp.Pool(nProcessors)
    results = [pool.apply_async(process_file, args=(info[0], info[2], resname, info[1], info[4], format_out, new_report, info[3])) for info in files]
    pool.close()
    pool.join()
    for res in results:
        res.get()

if __name__ == "__main__":
    lig_name, path, topology_path, out_name, fmt_str, n_proc, out_folder, new_reports, traj_filter = parseArguments()
    if traj_filter is not None:
        traj_filter = set(traj_filter)
    main(lig_name, path, topology_path, out_name, fmt_str, n_proc, out_folder, new_reports, traj_filter)
