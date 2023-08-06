from __future__ import absolute_import, division, print_function, unicode_literals
import os
import ast
import sys
import glob
import json
import errno
import socket
import shutil
import string
from builtins import range
import six
from six import reraise as raise_
import numpy as np
import mdtraj as md
from scipy import linalg
try:
    import cPickle as pickle
except ImportError:
    import pickle
from AdaptivePELE.atomset import RMSDCalculator, atomset
from AdaptivePELE.freeEnergies import utils
try:
    import multiprocessing as mp
    PARALELLIZATION = True
except ImportError:
    PARALELLIZATION = False


class UnsatisfiedDependencyException(Exception):
    __module__ = Exception.__module__


class RequiredParameterMissingException(Exception):
    __module__ = Exception.__module__


class ImproperParameterValueException(Exception):
    __module__ = Exception.__module__


class UnspecifiedPELECrashException(Exception):
    __module__ = Exception.__module__


class Topology(object):
    """
        Container object that points to the topology used in each trajectory
    """
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.topologies = []
        # the topologyMap maps each trajectory to its corresponding topology
        # {0: [t1, t2.. tM], 1: [t2, t3, t4, t4...]}
        self.topologyMap = {}
        self.topologyFiles = []

    def __getitem__(self, key):
        return self.topologies[key]

    def __iter__(self):
        for top in self.topologies:
            yield top

    def cleanTopologies(self):
        """
            Remove the written topology files
        """
        files = glob.glob(os.path.join(self.path, "topology*.pdb"))
        for f in files:
            os.remove(f)

    def writeTopologyObject(self):
        """
            Dump the contents of the topology object using pickle
        """
        writeObject(os.path.join(self.path, "topologies.pkl"), self, protocol=2)

    def setTopologies(self, topologyFiles, cleanFiles=True):
        """
            Set the topologies for the simulation. If topologies were set
            before they are deleted and set again

            :param topologyFiles: List of topology files
            :type topologyFiles: list
            :param cleanFiles: Flag wether to remove previous files
            :type cleanFiles: bool
        """
        if self.topologies:
            self.topologies = []
            self.topologyFiles = []
            if cleanFiles:
                self.cleanTopologies()
        for top in topologyFiles:
            self.topologies.append(getTopologyFile(top))
            self.topologyFiles.append(os.path.abspath(top))

    def topologyFilesIterator(self):
        for top_file in self.topologyFiles:
            yield top_file

    def mapEpochTopologies(self, epoch, trajectoryMapping):
        """
            Map the trajectories for the next epoch and the used topologies

            :param epoch: Epoch of the trajectory selected
            :type epoch: int
            :param trajectoryMapping: Mapping of the trajectories and the corresponding topologies
            :type trajectoryMapping: list
        """
        mapping = trajectoryMapping[1:]+[trajectoryMapping[0]]
        self.topologyMap[epoch] = [self.topologyMap[i_epoch][i_traj-1] for i_epoch, i_traj, _ in mapping]

    def getTopology(self, epoch, trajectory_number):
        """
            Get the topology for a particular epoch and trajectory number

            :param epoch: Epoch of the trajectory of interest
            :type epoch: int
            :param trajectory_number: Number of the trajectory to select
            :type trajectory_number: int

            :returns: list -- List with topology information
        """
        return self.topologies[self.topologyMap[epoch][trajectory_number-1]]

    def getTopologyFile(self, epoch, trajectory_number):
        """
            Get the topology file for a particular epoch and trajectory number

            :param epoch: Epoch of the trajectory of interest
            :type epoch: int
            :param trajectory_number: Number of the trajectory to select
            :type trajectory_number: int

            :returns: str -- Path to the topology file
        """
        return self.topologyFiles[self.topologyMap[epoch][trajectory_number-1]]

    def getTopologyFromIndex(self, index):
        """
            Get the topology for a particular index

            :param index: Index of the trajectory of interest
            :type index: int

            :returns: list -- List with topology information
        """
        return self.topologies[index]

    def getTopologyIndex(self, epoch, trajectory_number):
        """
            Get the topology index for a particular epoch and trajectory number

            :param epoch: Epoch of the trajectory of interest
            :type epoch: int
            :param trajectory_number: Number of the trajectory to select
            :type trajectory_number: int

            :returns: int -- Index of the corresponding topology
        """
        return self.topologyMap[epoch][trajectory_number-1]

    def writeMappingToDisk(self, epochDir, epoch):
        """
            Write the topology mapping to disk

            :param epochDir: Name of the folder where to write the
                mapping
            :type epochDir: str
        """
        with open(epochDir+"/topologyMapping.txt", "w") as f:
            f.write("%s\n" % ':'.join(map(str, self.topologyMap[epoch])))

    def readMappingFromDisk(self, epochDir, epoch):
        """
            Read the processorsToClusterMapping from disk

            :param epochDir: Name of the folder where to write the
                processorsToClusterMapping
            :type epochDir: str
        """
        try:
            with open(epochDir+"/topologyMapping.txt") as f:
                self.topologyMap[epoch] = list(map(int, f.read().rstrip().split(':')))
        except IOError:
            sys.stderr.write("WARNING: topologyMapping.txt not found, you might not be able to recronstruct fine-grained pathways\n")


class TopologyCompat(object):
    def __init__(self, pdb_file):
        self.topologyFiles = os.path.abspath(pdb_file)
        self.path = os.path.split(self.topologyFiles)[0]
        self.topologies = [getTopologyFile(self.topologyFiles)]

    def getTopologyFile(self, epoch, trajectory_number):
        return self.topologyFiles

    def topologyFilesIterator(self):
        yield self.topologyFiles

    def getTopologyIndex(self, epoch, trajectory_number):
        """
            Get the topology index for a particular epoch and trajectory number

            :param epoch: Epoch of the trajectory of interest
            :type epoch: int
            :param trajectory_number: Number of the trajectory to select
            :type trajectory_number: int

            :returns: int -- Index of the corresponding topology
        """
        return 0

    def getTopology(self, epoch, trajectory_number):
        """
            Get the topology for a particular epoch and trajectory number

            :param epoch: Epoch of the trajectory of interest
            :type epoch: int
            :param trajectory_number: Number of the trajectory to select
            :type trajectory_number: int

            :returns: list -- List with topology information
        """
        return self.topologies[0]


def cleanup(tmpFolder):
    """
        Remove folder if exists

        :param tmpFolder: Folder to remove
        :type tmpFolder: str
    """
    try:
        shutil.rmtree(tmpFolder)
    except OSError as exc:
        # If another process deleted the folder between the glob and the
        # actual removing an OSError is raised
        if exc.errno != errno.ENOENT:
            raise


def makeFolder(outputDir):
    """
        Makes folder

        :param outputDir: Folder filename
        :type outputDir: str
    """
    try:
        os.makedirs(outputDir)
    except OSError as exc:
        # if at this point another process has created the folder we are already
        # happy. If not, we complain
        if exc.errno != errno.EEXIST or not os.path.isdir(outputDir):
            print(exc.args)
            raise


def getSnapshots(trajectoryFile, verbose=False, topology=None, use_pdb=False):
    """
        Gets the snapshots

        :param trajectoryFile: Trajectory filename
        :type trajectoryFile: str
        :param verbose: Add verbose to snapshots
        :type verbose: bool

        :returns: iterable -- Snapshots with information
    """
    # topology parameter is ignored, just here for compatibility purposes
    ext = getFileExtension(trajectoryFile)
    if ext == ".pdb" or use_pdb:
        with open(trajectoryFile, "r") as inputFile:
            inputFileContent = inputFile.read()

        snapshots = inputFileContent.split("ENDMDL")
        if len(snapshots) > 1:
            snapshots = snapshots[:-1]
        if not verbose:
            return snapshots

        remarkInfo = "REMARK 000 File created using PELE++\nREMARK source            : %s\nREMARK original model nr : %d\nREMARK First snapshot is 1, not 0 (as opposed to report)\n%s"
        snapshotsWithInfo = [remarkInfo % (trajectoryFile, i+1, snapshot) for i, snapshot in enumerate(snapshots)]
    elif ext == ".xtc":
        with md.formats.XTCTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _, _, _ = f.read()
        # formats xtc and trr are by default in nm, so we convert them to A
        snapshotsWithInfo *= 10
    elif ext == ".trr":
        with md.formats.TRRTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _, _, _, _ = f.read()
        snapshotsWithInfo *= 10
    elif ext == ".dcd":
        with md.formats.DCDTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _, _ = f.read()
    elif ext == ".dtr":
        with md.formats.DTRTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _, _ = f.read()
    elif ext == ".mdcrd":
        with md.formats.MDCRDTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _ = f.read()
    elif ext == ".nc":
        with md.formats.NetCDFTrajectoryFile(trajectoryFile) as f:
            snapshotsWithInfo, _, _, _ = f.read()
    else:
        raise ValueError("Unrecongnized file extension for %s" % trajectoryFile)
    return snapshotsWithInfo


def getTrajNum(trajFilename):
    """
        Gets the trajectory number

        :param trajFilename: Trajectory filename
        :type trajFilename: str

        :returns: int -- Trajectory number
    """
    return int(trajFilename.split("_")[-1][:-4])


def getFileSuffix(filename, separator="_"):
    """
        Gets the suffix appendend to a file name

        :param filename: filename
        :type filename: str
        :param separator: character used as separator for the suffix
        :type separator: str

        :returns: int -- Trajectory number
    """
    name, _ = os.path.splitext(filename)
    return name.split(separator)[-1]

def isReport(reportFilename):
    """
        Checks whether the file is a PELE report

        :param reportFilename: Trajectory filename
        :type reportFilename: str

        :returns: bool -- Whether the file is a PELE report
    """
    return getFileSuffix(reportFilename).isdigit()

def getReportNum(reportFilename):
    """
        Gets the report number

        :param reportFilename: Trajectory filename
        :type reportFilename: str

        :returns: int -- Report number
    """
    return int(getFileSuffix(reportFilename))


def getPrmtopNum(prmtopFilename):
    """
        Gets the prmtop number

        :param trajFilename: prmtop filename
        :type trajFilename: str

        :returns: int -- prmtop number
    """
    return int(prmtopFilename.split("_")[-1][:-7])


def calculateContactMapEigen(contactMap):
    """
        Calculates eigenvectors and values of an extended contact map

        :param contactMap: Contact map
        :type contactMap: np.array

        :returns: (numpy.ndarray, numpy.ndarray) -- eigenvalues, eigenvectors
    """
    nLig, nCA = contactMap.shape
    extendedCM = np.zeros((nLig+nCA, nLig+nCA))
    extendedCM[nCA:, :nCA] = contactMap
    extendedCM[:nCA, nCA:] = contactMap.T
    assert (extendedCM == extendedCM.T).all(), "Extended ContactMap not symmetric"
    eiv, eic = np.linalg.eigh(extendedCM)
    return eiv, eic


def assertSymmetriesDict(symmetries, PDB):
    """
        Asserts the symmetry list in a PDB

        :param symmetries: List of symmetry groups
        :type symmetries: list of str
        :param PDB: PDB object to check symmetry list against
        :type PDB: :py:class:`.PDB`

        :raise AssertionError: If an atom is not found in the structure
    """
    for group in symmetries:
        for key in group:
            assert key in PDB.atoms, "Symmetry atom %s not found in initial structure" % key
    if symmetries:
        print("Symmetry dictionary correctly defined!")


def getRMSD(traj, nativePDB, resname, reschain, resnum, symmetries, topology=None):
    """
        Computes the RMSD of a trajectory, given a native and symmetries

        :param traj: Trajecotry filename
        :type traj: str
        :param nativePDB:  Native PDB object
        :type native PDB: :py:class:`.PDB`
        :param resname: Residue name of the ligand in the system pdb
        :type resname: str
        :param reschain: Chain name of the ligand in the system pdb
        :type reschain: str
        :param resnum: Residue number of the ligand in the system pdb
        :type resnum: int
        :param symmetries: Symmetries dictionary list with independent symmetry groups
        :type symmetries: list of dict
        :param topology: Topology for non-pdb trajectories
        :type topology: list

        :return: np.array -- Array with the rmsd values of the trajectory
    """

    snapshots = getSnapshots(traj)
    rmsds = np.zeros(len(snapshots))
    RMSDCalc = RMSDCalculator.RMSDCalculator(symmetries)
    for i, snapshot in enumerate(snapshots):
        snapshotPDB = atomset.PDB()
        snapshotPDB.initialise(snapshot, resname=resname, chain=reschain, resnum=resnum, topology=topology)

        rmsds[i] = RMSDCalc.computeRMSD(nativePDB, snapshotPDB)

    return rmsds


def readClusteringObject(clusteringObjectPath):
    """
        Reads and returns a clustering object

        :param clusteringObjectPath: Clustering object path
        :type clusteringObjectPath: str

        :raise EOFError: If the object is empty

        :returns: :py:class:`.Clustering` -- clusteringObject
    """
    with open(clusteringObjectPath, 'rb') as f:
        try:
            if six.PY2:
                return pickle.load(f)
            elif six.PY3:
                # make python3 able to read python2-written pickles
                return pickle.load(f, encoding="latin")
        except EOFError:
            t, v, tb = sys.exc_info()
            raise_(t, v, tb)


def ensure_connectivity_msm(msm):
    if msm.nstates_full == msm.nstates:
        return msm.stationary_distribution
    else:
        counts = msm.count_matrix_full
        counts += 1/counts.shape[0]
        trans = utils.buildRevTransitionMatrix(counts)
        _, eic = getSortedEigen(trans)
        return getStationaryDistr(eic[:, 0])


def getStationaryDistr(lowestEigenvector):
    absStationary = np.abs(lowestEigenvector)
    return absStationary / absStationary.sum()


def getSortedEigen(T):
    eigenvals, eigenvectors = linalg.eig(T, left=True, right=False)
    sortedIndices = np.argsort(eigenvals)[::-1]

    # reigenvals, reigenvectors = linalg.eig(T.T)
    # rsortedIndices = np.argsort(reigenvals)[::-1]
    return eigenvals[sortedIndices], eigenvectors[:, sortedIndices]


def get_epoch_folders(path):
    """
        List the folders belonging to an adaptive simulation and containing
        trajectories and reports

        :param path: Path where to check for the folders
        :type path: str

        :returns: list -- List of folders belonging to the simulation, sorted

    """
    allFolders = os.listdir(path)
    folders = [epoch for epoch in allFolders if epoch.isdigit()]
    folders.sort(key=int)
    return folders


def gen_atom_name(index):
    # 6760 = 26*26*10
    # The maximum number of unique ids generated by this method is 175760 =
    # 26*26*26*10, however, remember that generally the maximum number of unique
    # atoms that can be used with vmd is around 32000
    ind1 = index//6760
    ind2 = (index % 6760)
    ind3 = ind2 % 260
    return chr(65+ind1)+chr(65+ind2//260)+chr(65+ind3//10)+str(ind3 % 10)


def join_coordinates_prob(coords, p):
    """
        Join a MxN numpy array representing some cluster center coordinates with
        an 1XN array representing some metric of the clusters

        :param coords: Coordinates of the clusters
        :type coords: np.array
        :param p: Metric of the clusters
        :type p: np.array
    """
    if len(p.shape) < 2:
        p = p[:, np.newaxis]
    return np.hstack((coords, p))


def write_PDB_clusters(pmf_xyzg, title="clusters.pdb", use_beta=False, elements=None):
    templateLine = "HETATM%s %s CLT L 502    %s%s%s  0.75%s          %s  \n"
    if elements is None:
        elements = ["H" for i in range(len(pmf_xyzg))]

    content = ""
    names = []
    for i, line in enumerate(pmf_xyzg):
        number = str(i).rjust(5)
        # number3 = str(i).ljust(3)
        number3 = gen_atom_name(i).ljust(4)
        names.append(number3)
        x = ("%.3f" % line[0]).rjust(8)
        y = ("%.3f" % line[1]).rjust(8)
        z = ("%.3f" % line[2]).rjust(8)
        element = elements[i].rjust(2)
        if use_beta:
            g = ("%.2f" % line[-1]).rjust(6)
        else:
            g = ("%.2f" % 0).rjust(6)
        content += templateLine % (number, number3, x, y, z, g, element)

    with open(title, 'w') as f:
        f.write(content)
    return names


def distanceCOM(coords1, coords2):
    coords1 = np.array(coords1)
    coords2 = np.array(coords2)
    return np.linalg.norm(coords1-coords2)


def sign(x, tol=1e-7):
    """
        Return the sign of a number

        :param x: Array of number to evaluate the sign
        :type x: numpy.array
        :param tol: Tolerance to define the zero
        :type tol: float

        :returns: int -- Sign of the number
    """
    x[abs(x) < tol] = 0
    return np.sign(x)


def getAtomNames(values):
    """
        Assign to each value an atomname, O for negatives, H for 0 and N for
        positives. This function is created for assign atomnames for custom pdbs

        :param values: Collection of numbers to assing an atom name for
        :type values: iterable

        :returns: list -- List of atom names
    """
    names = ["O", "H", "N"]
    values += 1
    return [names[int(value)] for value in values]


def getReportAndTrajectoryWildcard(JSONdict):
    """
        Extract the trajectory and report filename from the pele control file

        :param JSONdict: Dictionary containing a parsed PELE control file
        :type JSONdict: dict

        :returns: str, str -- Report and trajectory wildcards
    """
    reportWildcard = os.path.split(JSONdict["commands"][0]["PELE_Output"]['reportPath'])[1]
    trajWildcard = os.path.split(JSONdict["commands"][0]["PELE_Output"]['trajectoryPath'])[1]
    trajWildcard = '_%d'.join(os.path.splitext(trajWildcard))
    reportWildcard = '_%d'.join(os.path.splitext(reportWildcard))
    return reportWildcard, trajWildcard


def getPELEControlFileDict(templetizedControlFile):
    """
        Parse a PELE control file into a python dictionary
    """

    with open(templetizedControlFile) as fc:
        peleControlFile = fc.read()

    templateNames = {ele[1]: '"$%s"' % ele[1] for ele in string.Template.pattern.findall(peleControlFile)}
    templateNames.pop("OUTPUT_PATH", None)
    templateNames.pop("REPORT_NAME", None)
    templateNames.pop("TRAJECTORY_NAME", None)
    return json.loads(string.Template(peleControlFile).safe_substitute(templateNames)), templateNames


def getMetricsFromReportsInEpoch(reportName, outputFolder, nTrajs):
    """
        Extract the metrics in report file from an epoch to a numpy array
    """
    metrics = []
    for i in range(1, nTrajs):
        report = np.loadtxt(os.path.join(outputFolder, reportName % i))
        if len(report.shape) < 2:
            metrics.append(report.tolist()+[i, 0])
        else:
            traj_line = np.array([i] * report.shape[0])
            snapshot_line = np.array(range(report.shape[0]))
            metrics.extend(np.hstack((report, traj_line[:, np.newaxis], snapshot_line[:, np.newaxis])))
    return np.array(metrics)


def getSASAcolumnFromControlFile(JSONdict):
    for i, metricBlock in enumerate(JSONdict["commands"][0]["PeleTasks"][0]['metrics']):
        if 'sasa' in metricBlock['type'].lower():
            # Report files have 4 fixed columnts, task, steps, accepted steps
            # and energy
            return i+4
    raise ValueError("No SASA metric found in control file!!! Please add it in order to use the moving box feature")


def getTopologyFile(structure):
    """
        Extract the topology information to write structures from xtc format

        :param structure: Pdb file with the topology information
        :type structure: str

        :return: list of str -- The lines of the topology file
    """
    top = []
    with open(structure) as f:
        for line in f:
            if not (line.startswith("ATOM") or line.startswith("HETATM")):
                continue
            else:
                top.append("".join([line[:30], "%s%s%s", line[54:]]))
    return top


def write_mdtraj_object_PDB(conformation, output, topology):
    """
        Write a snapshot from a xtc trajectory to pdb

        :param conformation: Mdtraj trajectory object to write
        :type structure: str or Trajectory
        :param output: Output where to write the object
        :type output: str
        :param topology: Topology-like object
        :type topology: list
    """
    PDB = atomset.PDB()
    PDB.initialise(conformation, topology=topology)
    PDB.writePDB(output)


def get_mdtraj_object_PDBstring(conformation, topology):
    """
        Get the pdb string of a snapshot from a xtc trajectory to pdb

        :param conformation: Mdtraj trajectory object to write
        :type structure: str or Trajectory
        :param topology: Topology-like object
        :type topology: list

        :returns: str -- The pdb representation of a snapshot from a xtc
    """
    PDB = atomset.PDB()
    PDB.initialise(conformation, topology=topology)
    return PDB.get_pdb_string()


def write_xtc_to_pdb(filename, output_file, topology):
    """
        Get the pdb string of a snapshot from a xtc trajectory to pdb

        :param filename: Path to the xtc trajectory
        :type filename: str
        :param output_file: Output where to write the object
        :type output_file: str
        :param topology: Topology file object
        :type topology: str

        :returns: str -- The pdb representation of a snapshot from a xtc
    """
    topology_contents = getTopologyFile(topology)
    xtc_object = md.load(filename, top=topology)
    pdb = atomset.PDB()
    pdb.initialise(xtc_object, topology=topology_contents)
    pdb.writePDB(output_file)


def convert_trajectory_to_pdb(trajectory, topology, output, output_folder):
    """
        Write a trajectory from a non-pdb trajectory to pdb format

        :param trajectory: Trajectory to convert
        :type trajectory: str
        :param topology: Topology file
        :type topology: str
        :param output: Filename of the ouput file
        :type output: str
        :param output_folder: Folder where to store the output trajectory
        :type output_folder: str
    """
    output = os.path.join(output_folder, output)
    topology_contents = getTopologyFile(topology)
    snapshots = getSnapshots(trajectory)
    with open(output, "w") as fw:
        for i, conf in enumerate(snapshots):
            PDB = atomset.PDB()
            PDB.initialise(conf, topology=topology_contents)
            fw.write("MODEL     %4d\n" % (i+1))
            fw.write(PDB.pdb)
            fw.write("ENDMDL\n")
        fw.write("END\n")


def writeObject(filename, object_to_write, protocol=2):
    with open(filename, "wb") as f:
        pickle.dump(object_to_write, f, protocol)


def getCpuCount():
    if not PARALELLIZATION:
        raise UnsatisfiedDependencyException("Multiprocessing module not found, will not be able to parallelize")
    machine = socket.getfqdn()
    cores = None
    if "bsccv" in machine:
        # life cluster
        cores = os.getenv("SLURM_NTASKS", None)
    elif "mn.bsc" in machine or "power" in machine:
        # nord3
        cores = os.getenv("LSB_DJOB_NUMPROC", None)
    elif "bsc.mn" in machine or "bullx" in machine or "power" in machine:
        # MNIV, MinoTauro or CTE-Power
        cores = os.getenv("SLURM_NPROCS", None)
    try:
        cores = int(cores)
    except TypeError:
        cores = None
    # Take 1 less than the count of processors, to not clog the machine
    return cores or max(1, mp.cpu_count()-1)


def writeProcessorMappingToDisk(folder, filename, processorMapping):
    """
        Write the processorsToClusterMapping to disk

        :param folder: Name of the folder where to write the
            processorsToClusterMapping
        :type folder: str
        :param filename: Name of the file where to write the processorMapping
        :type filename: str
        :param processorMapping: Mapping of the trajectories to processors
        :type processorMapping: list
    """
    with open(os.path.join(folder, filename), "w") as f:
        f.write("%s\n" % ':'.join(map(str, processorMapping)))


def readProcessorMappingFromDisk(folder, filename):
    """
        Read the processorsToClusterMapping from disk

        :param folder: Name of the folder where to write the
            processorsToClusterMapping
        :type folder: str
        :param filename: Name of the file where to write the processorMapping
        :type filename: str
        :returns: list -- List with the mapping of the trajectories to processors
    """
    try:
        with open(os.path.join(folder, filename)) as f:
            return list(map(ast.literal_eval, f.read().rstrip().split(':')))
    except IOError:
        sys.stderr.write("WARNING: processorMapping.txt not found, you might not be able to recronstruct fine-grained pathways\n")


def print_unbuffered(*args):
    """
        Call print and immediately after flush the buffer
    """
    print(*args)
    sys.stdout.flush()


def getFileExtension(trajectoryFile):
    """
        Extract the extension of a trajectory

        :param trajectoryFile: Name of the trajectory file
        :type trajectoryFile: str

        :returns: str -- Extension of the trajectory
    """
    return os.path.splitext(trajectoryFile)[1]


def loadtxtfile(filename, usecols=None, postprocess=True, dtype=float):
    """
        Load a table file from a text file

        :param filename: Name of the file to load
        :type filename: str
        :param usecols: Which columns to read, with 0 being the first
        :type usecols: int
        :param postprocess: Whether to add an extra dimension if only one line present in the txt file
        :type postprocess: bool
        :param dtype: Data-type of the resulting array, (default float)
        :type dtype: data-type

        :returns: np.ndarray -- Contents of the text file
    """
    metrics = np.genfromtxt(filename, missing_values=str("--"), filling_values='0', usecols=usecols, dtype=dtype)
    if len(metrics.shape) < 2 and postprocess:
        metrics = metrics[np.newaxis, :]
    return metrics


def writeNewConstraints(folder, filename, constraints):
    """
        Write the constraints to disk

        :param folder: Name of the folder where to write the
            constraints
        :type folder: str
        :param filename: Name of the file where to write the constraints
        :type filename: str
        :param constraints: List of the constraints
        :type constraints: list
    """
    with open(os.path.join(folder, filename), "w") as f:
        for constraint in constraints:
            f.write("{x[0]} {x[1]} {x[2]}\n".format(x=constraint))


def readConstraints(folder, filename):
    """
        Read the new constraints from disk

        :param folder: Name of the folder where to write the constraints
        :type folder: str
        :param filename: Name of the file where to write the constraints
        :type filename: str
        :returns: list -- List with the new constraints
    """
    new_constraints = []
    with open(os.path.join(folder, filename)) as f:
        for line in f:
            line_split = line.rstrip().split()
            line_split[2] = float(line_split[2])
            new_constraints.append(line_split)
    return new_constraints


def generateRotationMatrixAroundAxis(axis, angle):
    # extracted from https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    c = np.cos(angle)
    s = np.sin(angle)
    x, y, z = axis
    return np.array([[c+(1-c)*x**2, x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [x*y*(1-c)+z*s, c+(1-c)*y**2, y*z*(1-c)-x*s],
                     [x*z*(1-c)-y*s, y*z*(1-c)+x*s, c+(1-c)*z**2]])


def getTopologyObject(topology_file):
    ext = getFileExtension(topology_file)
    if ext == ".pdb":
        return TopologyCompat(topology_file)
    elif ext == ".pkl":
        return readClusteringObject(topology_file)
    else:
        raise ValueError("The topology parameter needs to be the path to a pickled Topology object or a pdb!")


def get_available_backend():
    machine = socket.getfqdn()
    if "bsccv" in machine:
        # life cluster
        return "webagg"
    elif "mn.bsc" in machine:
        # nord3
        return "tkagg"
    elif "bsc.mn" in machine:
        # MNIV
        return "qt5agg"
    elif "bullx" in machine:
        # MinoTauro
        return "gtkagg"
    elif "power" in machine:
        # CTE-Power
        return "tkagg"


def get_workers_output(workers, wait_time=60):
    """
        Get the output of a pool of workers without serializing the program at the get.

        :param workers: List of AsyncResult objects created when passing work to the pool
        :type workers: list
        :param wait_time: Number of second to wait before checking if next worker is finished
        :type wait_time: int

        :returns: list -- List containing the output of all workers, if the function
            passed to the pool had no return value it will be a list of None objects
    """
    # fill the list of results with placeholder zeros
    results = [0 for _ in range(len(workers))]
    to_finish = list(range(len(workers)))
    # loop over all processes of the pool, waiting for a minute and checking
    # if they are finished, this allows to query and reraise exceptions
    # withiout waiting for previous succesfull workers to finish
    while to_finish:
        i = to_finish.pop(0)
        workers[i].wait(wait_time)
        if workers[i].ready():
            # mantain the order of the results in which they were submitted,
            # this is assumed in some places where multiprocessing is used
            results[i] = workers[i].get()
        else:
            # if worker is not done append it again at the end of the queue
            to_finish.append(i)
    return results


def glob_sorted(pattern, reverse=False, key=None):
    """
        Run glob and sort the output to ensure cross-platform compatibility

        :param pattern: pathname to match files
        :type pattern: str
        :param reverse: If set to True, then the list elements are sorted as if each comparison were reversed
        :type reverse: bool
        :param key: Function of one argument that is used to extract a comparison key from each list element
        :type key: function

        :returns: list -- List containing the output of all workers, if the function
            passed to the pool had no return value it will be a list of None objects
    """
    results = glob.glob(pattern)
    return sorted(results, reverse=reverse, key=key)


def get_string_from_array(array, sep=", ", decimals=None, remove_newlines=True):
    """
        Get a string representation of an array, specifiying separator and
        decimal rounding

        :param array: Input array
        :type array: ndarray or list
        :param sep: Separator
        :type sep: str
        :param decimals: Number of decimals to round the array
        :type decimals: int
        :param remove_newlines: Wheter to remove the newlines between dimensions
        :type remove_newlines: bool
    """
    # ensure input is a numpy array
    array = np.array(array)
    representation = np.array2string(array, precision=decimals, separator=sep)
    if remove_newlines:
        return representation.replace('\n', '')
    return representation


def get_file_name_extension(full_path):
    """
        Get the name and the extension of the file pointed by full_path

        :param full_path: Path to the file
        :type full_path: str
    """
    return os.path.splitext(os.path.split(full_path)[1])


def get_file_name(full_path):
    """
        Get the name of the file pointed by full_path

        :param full_path: Path to the file
        :type full_path: str
    """
    name, _ = get_file_name_extension(full_path)
    return name


def get_file_extension(full_path):
    """
        Get the extension of the file pointed by full_path

        :param full_path: Path to the file
        :type full_path: str
    """
    _, ext = get_file_name_extension(full_path)
    return ext
