from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import ast
import glob
import heapq
import numpy as np
from scipy import stats
from builtins import range
from six import reraise as raise_
from AdaptivePELE.constants import blockNames
from AdaptivePELE.utilities import utilities
from AdaptivePELE.atomset import SymmetryContactMapEvaluator as sym
from AdaptivePELE.atomset import RMSDCalculator
from AdaptivePELE.atomset import atomset
from AdaptivePELE.clustering import clusteringTypes
from AdaptivePELE.clustering import thresholdcalculator
from AdaptivePELE.freeEnergies import extractCoords as coord
from AdaptivePELE.freeEnergies import getRepresentativeStructures as getRepr
try:
    import networkx as nx
    NETWORK = True
except ImportError:
    NETWORK = False

try:
    import multiprocessing as mp
    PARALELLIZATION = True
except ImportError:
    PARALELLIZATION = False

try:
    from AdaptivePELE.freeEnergies import cluster as pyemma_cluster
    from AdaptivePELE.freeEnergies.estimateDG import getCentersInfo
    import pyemma.coordinates as coor
    PYEMMA = True
except ImportError:
    PYEMMA = False


class Clusters(object):
    def __init__(self):
        self.clusters = []

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"clusters": self.clusters}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.clusters = state['clusters']

    def __len__(self):
        return len(self.clusters)

    def addCluster(self, cluster):
        """
            Add a new cluster

            :param cluster:  Cluster object to insert
            :type cluster: :py:class:`.Cluster`
        """
        self.clusters.append(cluster)

    def insertCluster(self, index, cluster):
        """
            Insert a cluster in a specified index

            :param index: Positions at which insert the cluster
            :type index: int
            :param cluster:  Cluster object to insert
            :type cluster: :py:class:`.Cluster`
        """
        self.clusters.insert(index, cluster)

    def getNumberClusters(self):
        """
            Get the number of clusters contained

            :returns: int -- Number of clusters contained
        """
        return len(self.clusters)

    def getCluster(self, clusterNum):
        """
            Get the cluster at position clusterNum

            :param clusterNum: Index of the cluster to retrieve
            :type clusterNum: int
            :returns: :py:class:`.Cluster` -- Cluster at position clusterNum
        """
        return self.clusters[clusterNum]

    def printClusters(self, verbose=False):
        """
            Print clusters information

            :param verbose: Flag to control the verbosity of the code (default is False)
            :type verbose: bool
        """
        for i, cluster in enumerate(self.clusters):
            print("--------------")
            print("CLUSTER #%d" % i)
            print("--------------")
            cluster.printCluster(verbose)
            print("")

    def __getitem__(self, key):
        return self.clusters[key]

    def __setitem__(self, key, value):
        self.clusters[key] = value

    def __delitem__(self, key):
        del self.clusters[key]

    def __eq__(self, other):
        return self.clusters == other.clusters

    def __iter__(self):
        for cluster in self.clusters:
            yield cluster


class ConformationNetwork(object):
    """
        Object that contains the conformation network, a network with clusters as
        nodes and edges representing trantions between clusters. The network is
        stored using the networkx package[1]

        References
        ----------
        .. [1] Networkx python package https://networkx.github.io
    """
    def __init__(self):
        if NETWORK:
            self.network = nx.DiGraph()
        else:
            self.network = None

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"network": self.network}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.network = state['network']
        if NETWORK and int(nx.__version__.split(".")[0]) > 1 and 'adj' in self.network.__dict__:
            for attr in ['node', 'adj', 'graph', 'pred', 'succ']:
                self.network.__dict__["_"+attr] = self.network.__dict__.pop(attr)

    def add_node(self, node, **kwargs):
        """
            Add a node to the network (wrapper for networkx method)

            :param node: Name of the node
            :type node: int
            :param kwargs: Set or change attributes using key=value.
            :type kwargs: keyword arguments, optional
        """
        if not NETWORK:
            return
        self.network.add_node(node, attr_dict=kwargs)

    def add_edge(self, source, target):
        """
            Add an edge to the network (wrapper for networkx method)

            :param source: Name of the source node
            :type source: int
            :param target: Name of the target node
            :type target: int
        """
        if not NETWORK:
            return
        if self.network.has_edge(source, target):
            self.network[source][target]['transition'] += 1
        else:
            self.network.add_edge(source, target, transition=1)

    def writeConformationNetwork(self, path):
        """
            Write the conformational network to file to visualize it

            :param path: Path where to write the network
            :type path: str
        """
        if not NETWORK:
            sys.stderr.write("Package networkx not found! Could not write network\n")
            return
        nx.write_edgelist(self.network, path)

    def writeFDT(self, path):
        """
            Write the first discovery tree to file in edgelist format to
            visualize it

            :param path: Path where to write the network
            :type path: str
        """
        if not NETWORK:
            sys.stderr.write("Package networkx not found! Could not write network\n")
            return
        with open(path, "w") as fw:
            for node, data in self.network.nodes(data=True):
                if data['parent'] != 'root':
                    fw.write("%d\t%d\n" % (data['parent'], node))

    def createPathwayToCluster(self, clusterLeave):
        """
            Retrace the FDT from a specific cluster to the root where it was
            discovered

            :param clusterLeave: End point of the pathway to reconstruct
            :type clusterLeave: int
            :returns: list -- List of snapshots conforming a pathway
        """
        pathway = []
        nodeLabel = clusterLeave
        while nodeLabel != "root":
            pathway.append(nodeLabel)
            nodeLabel = self.network.node[nodeLabel]['parent']
        return pathway[::-1]


class AltStructures(object):
    """
        Helper class, each cluster will have an instance of AltStructures that
        will maintain a priority queue (pq) of alternative structures to spawn
        from encoded as tuples (priority, PDB).
    """
    def __init__(self):
        self.altStructPQ = []
        self.limitSize = 10
        self.index = -1

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"altStructPQ": self.altStructPQ, "limitSize": self.limitSize, "index": self.index}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.limitSize = state['limitSize']
        self.altStructPQ = [(el[0], i, el[-1]) for i, el in enumerate(state['altStructPQ'])]
        self.index = state.get('index', len(self.altStructPQ)-1)

    def altSpawnSelection(self, centerPair):
        """
            Select an alternative PDB from the cluster center to spawn from

            :param centerPair: Tuple with the population of the representative structure
                and the PDB of said structure
            :type centerPair: int, :py:class:`.PDB`
            :returns: :py:class:`.PDB`, tuple -- PDB of the strucutre selected to spawn and tuple
                consisting of (epoch, trajectory, snapshot)

        """
        subpopulations = [i[0] for i in self.altStructPQ]
        totalSubpopulation = sum(subpopulations)
        # Create a list of the population distributed between the cluster
        # center and the alternative structures
        weights = 1.0/np.array([centerPair[0]-totalSubpopulation]+subpopulations)
        weights /= weights.sum()
        # This function only works on numpy >= 1.7, on life we have 1.6
        # ind = np.random.choice(range(len(self.altStructPQ)), p=weights)
        # Add one to account for the cluster representative
        r = stats.rv_discrete(values=(range(self.sizePQ()+1), weights))
        ind = r.rvs(size=10)[0]
        # The first value of the distribution is always the cluster center
        if ind == 0:
            print("cluster center")
            return centerPair[1], None
        else:
            # pick an alternative structure from the priority queue
            # The first element corresponds to the cluster center
            ind -= 1
            print("alternative structure")
            return self.altStructPQ[ind][2].pdb, self.altStructPQ[ind][2].trajPosition

    def cleanPQ(self):
        """
            Ensure that the alternative structures priority queue has no more
            elements than the limit in order to ensure efficiency
        """
        if len(self.altStructPQ) < self.limitSize:
            return
        limit = len(self.altStructPQ)
        del self.altStructPQ[self.limitSize-limit:]

    def addStructure(self, PDB, threshold, resname, resnum, resChain, contactThreshold, similarityEvaluator, trajPosition):
        """
            Perform a subclustering, with sub-clusters of size threshold/2

            :param PDB: Structure to cluster
            :type PDB: :py:class:`.PDB`
            :param threshold: Size of the cluster
            :type threshold: float
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param contactThreshold: Distance at which to atoms are considered in contact
            :type contactThreshold: float
            :param similarityEvaluator: Object that determinates the similarity between two structures
            :type similarityEvaluator: :py:class:`.SimilarityEvaluator`
            :param trajPosition: Tuple of (epoch, trajectory, snapshot) that permit
                identifying the structure added
            :type trajPosition: int, int, int

        """
        i = 0
        for _, _, subCluster in self.altStructPQ:
            _, distance = similarityEvaluator.isElement(PDB, subCluster, resname, resnum, resChain, contactThreshold)
            if distance < subCluster.threshold/2.0:
                subCluster.addElement([])
                del self.altStructPQ[i]
                heapq.heappush(self.altStructPQ, (subCluster.elements, self.updateIndex(), subCluster))
                if len(self.altStructPQ) > 2*self.limitSize:
                    self.cleanPQ()
                return
            i += 1
        newCluster = Cluster(PDB, thresholdRadius=threshold, contactThreshold=contactThreshold, contactMap=similarityEvaluator.contactMap, trajPosition=trajPosition)
        heapq.heappush(self.altStructPQ, (1, self.updateIndex(), newCluster))
        if len(self.altStructPQ) > 2*self.limitSize:
            self.cleanPQ()

    def updateIndex(self):
        """
            Update the index which represents chronological order of entries in
            the priority queue

            :returns: int -- Index of the following element
        """
        self.index += 1
        return self.index

    def sizePQ(self):
        """
            Get the number of sub-clusters stored in the priority queue

            :returns: int -- Number of sub-clusters stored in the priority queue
        """
        return len(self.altStructPQ)


class Cluster(object):
    """
        A cluster contains a representative structure(pdb), the number of
        elements, its density, threshold, number of contacts,
        a contactMap(sometimes) and a metric
    """
    def __init__(self, pdb, thresholdRadius=None, contactMap=None,
                 contacts=None, metrics=None, metricCol=None, density=None,
                 contactThreshold=8, altSelection=False, trajPosition=None):
        """
            :param pdb: Pdb of the representative structure
            :type pdb: :py:class:`.PDB`
            :param thresholdRadius: Threshold of the cluster
            :type thresholdRadius: float
            :param contactMap:  The contact map of the ligand and the protein
            :type contactMap: numpy.Array
            :param contacts: Ratio of the number of alpha carbons in contact with the ligand
            :type contacts: float
            :param metrics: Array of the metrics corresponding to the cluster
            :type metrics: numpy.Array
            :param metricCol: Column of the prefered metric
            :type metricCol: int
            :param density: Density of the cluster
            :type density: float
            :param contactThreshold: Distance between two atoms to be considered in contact (default 8)
            :type contactThreshold: float
            :param altSelection: Flag that controls wether to use the alternative structures (default 8)
            :type altSelection: bool
            :param trajPosition: Tuple of (epoch, trajectory, snapshot) that permit
                identifying the structure added
            :type trajPosition: int, int, int

        """
        self.pdb = pdb
        self.altStructure = AltStructures()
        self.elements = 1
        self.threshold = thresholdRadius
        self.density = density
        self.contacts = contacts
        self.contactMap = contactMap
        if metrics is None:
            metrics = []
        self.metrics = metrics
        self.originalMetrics = metrics
        self.metricCol = metricCol
        self.contactThreshold = contactThreshold
        self.altSelection = altSelection
        self.trajPosition = trajPosition

        if self.threshold is None:
            self.threshold2 = None
        else:
            self.threshold2 = thresholdRadius*thresholdRadius

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"pdb": self.pdb, "altStructure": self.altStructure,
                 "elements": self.elements, "threshold": self.threshold,
                 "densitiy": self.density, "contacts": self.contacts,
                 "contactMap": self.contactMap, "metrics": self.metrics,
                 "metricCol": self.metricCol, "threshold2": self.threshold2,
                 "contactThreshold": self.contactThreshold,
                 "altSelection": self.altSelection,
                 "originalMetrics": self.originalMetrics,
                 "trajPosition": self.trajPosition}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.pdb = state['pdb']
        self.altStructure = state.get('altStructure', AltStructures())
        self.elements = state['elements']
        self.threshold = state.get('threshold')
        self.density = state.get('density')
        self.contacts = state.get('contacts')
        self.contactMap = state.get('contactMap')
        self.metrics = state.get('metrics', [])
        self.originalMetrics = state.get('originalMetrics', [])
        self.metricCol = state.get('metricCol')
        self.threshold2 = state.get('threshold2')
        self.contactThreshold = state.get('contactThreshold', 8)
        self.altSelection = state.get('altSelection', False)
        self.trajPosition = state.get('trajPosition')

    def __len__(self):
        return self.elements

    def getMetric(self):
        """
            Get the value of the prefered metric if present, otherwise return None

            :returns: float -- Value of the prefered metric
        """
        if self.metricCol is not None and len(self.metrics) > self.metricCol:
            return self.metrics[self.metricCol]
        else:
            return None

    def getMetricFromColumn(self, numcol):
        """
            Get the value of the metric in column numcol if present, otherwise return None

            :param numcol: Column of the desired metric
            :type numcol: int
            :returns: float -- Value of the prefered metric
        """
        if len(self.metrics):
            return self.metrics[numcol]
        else:
            return None

    def addElement(self, metrics):
        """
            Add a new element to the cluster

            :param metrics: Array of metrics of the new structure
            :type metrics: numpy.Array
        """
        self.elements += 1
        if self.metrics is None:
            # Special case where cluster in created during clustering of
            # initial structures
            self.metrics = metrics
            return
        if self.originalMetrics is None:
            self.originalMetrics = metrics
        if len(metrics) and len(self.metrics):
            # Set all metrics to the minimum value
            self.metrics = np.minimum(self.metrics, metrics)

    def printCluster(self, verbose=False):
        """
            Print cluster information

            :param verbose: Flag to control the verbosity of the code (default is False)
            :type verbose: bool
        """
        if verbose:
            print(self.pdb.printAtoms())
        print("Elements: ", self.elements)
        print("Metrics: ", self.metrics)
        if self.threshold != 0:
            print("Radius threshold: ", self.threshold)
        print("Number of contacts: %.2f" % self.contacts)

    def __str__(self):
        return "Cluster: elements=%d, threshold=%.3f, contacts=%.3f, density=%.3f" % (self.elements, self.threshold, self.contacts, self.density or 0.000)

    def writePDB(self, path):
        """
            Write the pdb of the representative structure to file

            :param path: Filename of the file to write
            :type path: str
        """
        self.pdb.writePDB(path)

    def getContacts(self):
        """
            Get the contacts ratio of the cluster

            :returns: float -- contact ratio of the cluster
        """
        return self.contacts

    def writeSpawningStructure(self, path):
        """
            Write the pdb of the chosen structure to spawn

            :param path: Filename of the file to write
            :type path: str

            :returns int, int, int: Tuple of (epoch, trajectory, snapshot) that permit
                identifying the structure added
        """
        if not self.altSelection or self.altStructure.sizePQ() == 0:
            print("cluster center")
            self.pdb.writePDB(path)
            return self.trajPosition
        else:
            spawnStruct, trajPosition = self.altStructure.altSpawnSelection((self.elements, self.pdb))
            spawnStruct.writePDB(path)
            if trajPosition is None:
                trajPosition = self.trajPosition
            return trajPosition

    def __eq__(self, other):
        return (self.pdb, self.elements, self.threshold, self.contacts) == (other.pdb, other.elements, other.threshold, other.contacts) and np.allclose(self.metrics, other.metrics)


class ClusteringEvaluator(object):
    def __init__(self):
        self.contactMap = None
        self.contacts = None

    def cleanContactMap(self):
        """
            Clean the attributes to prepare for next iteration
        """
        self.contactMap = None
        self.contacts = None


class ContactsClusteringEvaluator(ClusteringEvaluator):
    def __init__(self, RMSDCalculator_object):
        """
            Helper object to carry out the RMSD clustering

            :param RMSDCalculator: object that calculates the RMSD between two
                conformations
            :type RMSDCalculator: :py:class:`.RMSDCalculator`
        """
        ClusteringEvaluator.__init__(self)
        self.RMSDCalculator = RMSDCalculator_object
        self.contacts = None
        # Only here for compatibility purpose
        self.contactMap = None

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"RMSDCalculator": self.RMSDCalculator,
                 "contacts": self.contacts, "contactMap": self.contactMap}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.RMSDCalculator = state.get('RMSDCalculator', RMSDCalculator.RMSDCalculator())
        self.contacts = state.get('contacts')
        self.contactMap = state.get('contactMap')

    def isElement(self, pdb, cluster, resname, resnum, resChain, contactThresholdDistance):
        """
            Evaluate wether a conformation is a member of a cluster

            :param pdb: Structure to compare
            :type pdb: :py:class:`.PDB`
            :param cluster: Cluster to compare
            :type cluster: :py:class:`.Cluster`
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param contactThreshold: Distance between two atoms to be considered in contact (default 8)
            :type contactThreshold: float
            :returns: bool, float -- Whether the structure belong to the cluster and the distance between them
        """
        dist = self.RMSDCalculator.computeRMSD(cluster.pdb, pdb)
        return dist < cluster.threshold, dist

    def checkAttributes(self, pdb, resname, resnum, resChain, contactThresholdDistance):
        """
            Check wether all attributes are set for this iteration

            :param pdb: Structure to compare
            :type pdb: :py:class:`.PDB`
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param contactThreshold: Distance between two atoms to be considered in contact (default 8)
            :type contactThreshold: float
        """
        if self.contacts is None:
            self.contacts = pdb.countContacts(resname, contactThresholdDistance, resnum, resChain)

    def getInnerLimit(self, cluster):
        """
            Return the threshold of the cluster

            :param cluster: Cluster to compare
            :type cluster: :py:class:`.Cluster`
            :returns: float -- Threshold of the cluster
        """
        return cluster.threshold2


class CMClusteringEvaluator(ClusteringEvaluator):
    limitSlope = {8: 6, 6: 15, 4: 60, 10: 3}
    limitMax = {8: 2, 6: 0.8, 4: 0.2, 10: 4}

    def __init__(self, similarityEvaluator, symmetryEvaluator):
        """
            Helper object to carry out the RMSD clustering

            :param similarityEvaluator: object that calculates the similarity
                between two contact maps
            :type similarityEvaluator: :py:class:`.CMSimilarityEvaluator`
            :param symmetryEvaluator: object to introduce the symmetry  in the
                contacts maps
            :type symmetryEvaluator: :py:class:`.SymmetryContactMapEvaluator`
        """
        ClusteringEvaluator.__init__(self)
        self.similarityEvaluator = similarityEvaluator
        self.symmetryEvaluator = symmetryEvaluator
        self.contacts = None
        self.contactMap = None

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"similarityEvaluator": self.similarityEvaluator,
                 "symmetryEvaluator": self.symmetryEvaluator,
                 "contacts": self.contacts, "contactMap": self.contactMap}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.similarityEvaluator = state.get('similarityEvaluator')
        self.symmetryEvaluator = state.get('symmetryEvaluator')
        self.contacts = state.get('contacts')
        self.contactMap = state.get('contactMap')

    def isElement(self, pdb, cluster, resname, resnum, resChain, contactThresholdDistance):
        """
            Evaluate wether a conformation is a member of a cluster

            :param pdb: Structure to compare
            :type pdb: :py:class:`.PDB`
            :param cluster: Cluster to compare
            :type cluster: :py:class:`.Cluster`
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param contactThreshold: Distance between two atoms to be considered in contact (default 8)
            :type contactThreshold: float
            :returns: bool, float -- Whether the structure belong to the cluster and the distance between them
        """
        if self.contactMap is None:
            self.contactMap, self.contacts = self.symmetryEvaluator.createContactMap(pdb, resname, contactThresholdDistance, resnum, resChain)
            # self.contactMap, foo = self.symmetryEvaluator.createContactMap(pdb, resname, contactThresholdDistance)
            # self.contacts = pdb.countContacts(resname, 8)  # contactThresholdDistance)
        distance = self.similarityEvaluator.isSimilarCluster(self.contactMap, cluster.contactMap, self.symmetryEvaluator)
        return distance < cluster.threshold, distance

    def checkAttributes(self, pdb, resname, resnum, resChain, contactThresholdDistance):
        """
            Check wether all attributes are set for this iteration

            :param pdb: Structure to compare
            :type pdb: :py:class:`.PDB`
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param contactThreshold: Distance between two atoms to be considered in contact (default 8)
            :type contactThreshold: float
        """
        if self.contactMap is None:
            self.contactMap, self.contacts = self.symmetryEvaluator.createContactMap(pdb, resname, contactThresholdDistance, resnum, resChain)
            # self.contactMap, foo = self.symmetryEvaluator.createContactMap(pdb, resname, contactThresholdDistance)
            # self.contacts = pdb.countContacts(resname, 8)  # contactThresholdDistance)

    def getInnerLimit(self, cluster):
        """
            Return the threshold of the cluster

            :param cluster: Cluster to compare
            :type cluster: :py:class:`.Cluster`
            :returns: float -- Threshold of the cluster
        """
        # if cluster.contacts > self.limitMax[cluster.contactThreshold]:
        #     return 4.0
        # else:
        #     return 16-self.limitSlope[cluster.contactThreshold]*cluster.contacts

        # if cluster.contacts > 2.0:
        #     return 4.0
        # elif cluster.contacts <= 0.5:
        #     return 25.0
        # else:
        #     return 25-14*(cluster.contacts-0.5)

        if cluster.contacts > 2.0:
            return 4.0
        elif cluster.contacts < 0.5:
            return 25.0
        else:
            return 16-8*(cluster.contacts-0.5)

        # if cluster.contacts > 1.0:
        #     return 4.0
        # elif cluster.contacts > 0.75:
        #     return 9.0
        # elif cluster.contacts > 0.5:
        #     return 16.0
        # else:
        #      return 25


class Clustering(object):
    def __init__(self, resname="", resnum=0, resChain="", reportBaseFilename=None,
                 columnOfReportFile=None, contactThresholdDistance=8,
                 altSelection=False):
        """
            Base class for clustering methods, it defines a cluster method that
            contacts and accumulative inherit and use

            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param reportBaseFilename: Name of the file that contains the metrics of the snapshots to cluster
            :type reportBaseFilename: str
            :param columnOfReportFile: Column of the report file that contain the metric of interest
            :type columnOfReportFile: int
            :param contactThresholdDistance: Distance at wich a ligand atom and a protein atom are
                considered in contact(default 8)
            :type contactThresholdDistance: float
        """
        self.type = "BaseClass"

        self.clusters = Clusters()
        if reportBaseFilename:
            self.reportBaseFilename = reportBaseFilename + "_%d"
        else:
            self.reportBaseFilename = None
        self.resname = resname
        self.resnum = resnum
        self.resChain = resChain
        self.col = columnOfReportFile
        self.contactThresholdDistance = contactThresholdDistance
        self.symmetries = []
        self.altSelection = altSelection
        self.conformationNetwork = ConformationNetwork()
        self.epoch = -1

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"type": self.type, "clusters": self.clusters,
                 "reportBaseFilename": self.reportBaseFilename,
                 "resname": self.resname, "resnum": self.resnum,
                 "resChain": self.resChain, "col": self.col,
                 "epoch": self.epoch, "symmetries": self.symmetries,
                 "conformationNetwork": self.conformationNetwork,
                 "contactThresholdDistance": self.contactThresholdDistance,
                 "altSelection": self.altSelection}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.type = state['type']
        self.clusters = state['clusters']
        self.reportBaseFilename = state.get('reportBaseFilename')
        self.resname = state.get('resname', "")
        self.resnum = state.get('resnum', 0)
        self.resChain = state.get('resChain', "")
        self.col = state.get('col')
        self.contactThresholdDistance = state.get('contactThresholdDistance', 8)
        self.symmetries = state.get('symmetries', [])
        self.altSelection = state.get('altSelection', False)
        self.conformationNetwork = state.get('conformationNetwork', ConformationNetwork())
        self.epoch = state.get('epoch', -1)

    def __str__(self):
        return "Clustering: nClusters: %d" % len(self.clusters)

    def __len__(self):
        return len(self.clusters)

    def __iter__(self):
        for cluster in self.clusters:
            yield cluster

    def __getitem__(self, key):
        return self.clusters[key]

    def __setitem__(self, key, value):
        self.clusters[key] = value

    def __delitem__(self, key):
        del self.clusters[key]

    def setCol(self, col):
        """
            Set the column of the prefered column to col

            :param col: Column of the prefered column
            :type col: int
        """
        self.col = col

        for cluster in self.clusters.clusters:
            cluster.metricCol = col

    def updateRepeatParameters(self, repeat, steps):
        """
            Update parameters that should be extracted from the simulation object

            :param repeat: Whether to avoid repeating steps (False for PELE, True for md)
            :type repeat: bool
            :param steps: steps per epoch
            :type steps: int
        """
        pass

    def getClusterListForSpawning(self):
        """
            Return the clusters object to be used in the spawning

            :returns: :py:class:`.Clusters` -- Container object for the clusters
        """
        return self.clusters

    def getCluster(self, clusterNum):
        """
            Get the cluster at index clusterNum

            :returns: :py:class:`.Cluster` -- Cluster at clusterNum
        """
        return self.clusters.getCluster(clusterNum)

    def setProcessors(self, processors):
        pass

    def emptyClustering(self):
        """
            Delete previous results of clustering object
        """
        self.clusters = Clusters()
        self.conformationNetwork = ConformationNetwork()
        self.epoch = -1

    def clusterIterator(self):
        """
            Iterator over the clusters
        """
        # TODO: may be interesting to add some condition to filter, check
        # itertools module, its probably implemented
        for cluster in self.clusters.clusters:
            yield cluster

    def getNumberClusters(self):
        """
            Get the number of clusters

            :returns: int -- Number of clusters
        """
        return self.clusters.getNumberClusters()

    def __eq__(self, other):
        return (self.clusters, self.reportBaseFilename, self.resname, self.resnum, self.resChain, self.col) == (other.clusters, other.reportBaseFilename, other.resname, other.resnum, other.resChain, other.col)

    def filterClustersAccordingToBox(self, simulationRunnerParams):
        """
            Filter the clusters to select only the ones whose representative
            structures will fit into the selected box

            :param simulationRunnerParams: :py:class:`.SimulationParameters` Simulation parameters object
            :type simulationRunnerParams: :py:class:`.SimulationParameters`

            :returns list, list: -- list of the filtered clusters, list of bools flagging wether the cluster is selected or not

        """
        box_center = ast.literal_eval(simulationRunnerParams.boxCenter)
        box_radius = simulationRunnerParams.boxRadius
        clustersFiltered = []
        clustersSelected = []
        for cluster in self.clusters:
            if utilities.distanceCOM(box_center, cluster.pdb.getCOM()) < (box_radius-1):
                clustersFiltered.append(cluster)
                clustersSelected.append(True)
            else:
                clustersSelected.append(False)
        return clustersFiltered, clustersSelected

    def filterClustersAccordingToMetric(self, clustersFiltered, filter_value, condition, col_filter):
        """
            Filter the clusters to select only the ones whose metric fits an
            specific criterion

            :param clustersFiltered: List of clusters to be processed
            :type clustersFiltered: list
            :param filter_value: Value to use in the filtering
            :type filter_value: float
            :param condition: Whether to use > or < condition in the filtering
            :type condition: str
            :param col_filter: Column of the report to use
            :type col_filter: int

            :returns list, list: -- list of the filtered clusters, list of bools flagging whether the cluster is selected or not

        """
        metrics = self.getMetricsFromColumn(col_filter)
        if None in metrics:
            raise utilities.RequiredParameterMissingException("Metrics not found in clusters and required for filtering!!")
        if condition == blockNames.SpawningParams.minValue:
            tmp_selection = metrics < filter_value
        elif condition == blockNames.SpawningParams.maxValue:
            tmp_selection = metrics > filter_value
        selection = np.array(clustersFiltered) & tmp_selection
        if not selection.any():
            # if no clusters match the given filtering criteria, bussiness as
            # usual
            selection = clustersFiltered
        return [cl for i, cl in enumerate(self.clusters) if selection[i]], selection

    def getMetricsFromColumn(self, col):
        """
            Get the metric of the clusters

            :param col: Column to select the metric
            :type col: int

            :returns: np.array -- Array containing the metric of the clusters
        """
        return np.array([cl.getMetricFromColumn(col) for cl in self.clusters])

    def cluster(self, paths, ignoreFirstRow=False, topology=None, epoch=None, outputPathConstants=None):
        """
            Cluster the snaptshots contained in the paths folder

            :param paths: List of folders with the snapshots
            :type paths: list
            :param ignoreFirstRow: Flag wether to ignore the first snapshot of a trajectory
            :type ignoreFirstRow: bool
            :param topology: Topology object containing the set of topologies needed for the simulation
            :type topology: :py:class:`.Topology`
            :param epoch: Epoch number
            :type epoch: int
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
        """
        if epoch is None:
            self.epoch += 1
        else:
            self.epoch = epoch
        trajectories = getAllTrajectories(paths)
        for trajectory in trajectories:
            trajNum = utilities.getTrajNum(trajectory)
            # origCluster = processorsToClusterMapping[trajNum-1]
            origCluster = None
            snapshots = utilities.getSnapshots(trajectory, True)
            if topology is not None:
                top = topology.getTopology(self.epoch, trajNum)
            else:
                top = None
            if self.reportBaseFilename:
                reportFilename = os.path.join(os.path.split(trajectory)[0],
                                              self.reportBaseFilename % trajNum)
                metrics = loadReportFile(reportFilename)

                for num, snapshot in enumerate(snapshots):
                    if ignoreFirstRow and num == 0:
                        continue
                    try:
                        origCluster = self.addSnapshotToCluster(trajNum, snapshot, origCluster, num, metrics[num], self.col, topology=top)
                    except IndexError as e:
                        message = (" in trajectory %d. This is usually caused by a mismatch between report files and trajectory files"
                                   " which in turn is usually caused by some problem in writing the files, e.g. quota")

                        # raise a new exception of the same type, with the same
                        # traceback but with an added message
                        raise_(IndexError, (str(e) + message % trajNum), sys.exc_info()[2])
            else:
                for num, snapshot in enumerate(snapshots):
                    if ignoreFirstRow and num == 0:
                        continue
                    origCluster = self.addSnapshotToCluster(trajNum, snapshot, origCluster, num, topology=top)
        for cluster in self.clusters.clusters:
            cluster.altStructure.cleanPQ()

    def writeOutput(self, outputPath, degeneracy, outputObject, writeAll):
        """
            Writes all the clustering information in outputPath

            :param outputPath: Folder that will contain all the clustering information
            :type outputPath: str
            :param degeneracy: Degeneracy of each cluster. It must be in the same order
                as in the self.clusters list
            :type degeneracy: list
            :param outputObject: Output name for the pickle object
            :type outputObject: str
            :param writeAll: Wether to write pdb files for all cluster in addition
                of the summary
            :type writeAll: bool
        """
        utilities.cleanup(outputPath)
        utilities.makeFolder(outputPath)

        summaryFilename = os.path.join(outputPath, "summary.txt")
        with open(summaryFilename, 'w') as summaryFile:
            summaryFile.write("#cluster size degeneracy contacts threshold density metric\n")

            for i, cluster in enumerate(self.clusters.clusters):
                if writeAll:
                    outputFilename = "cluster_%d.pdb" % i
                    outputFilename = os.path.join(outputPath, outputFilename)
                    cluster.writePDB(outputFilename)

                metric = cluster.getMetric()
                if metric is None:
                    metric = "-"
                else:
                    metric = "%.3f" % metric
                degeneracy_cluster = 0
                if degeneracy is not None:
                    # degeneracy will be None if null spawning is used
                    degeneracy_cluster = degeneracy[i]

                writeString = "%d %d %d %.2f %.4f %.1f %s\n" % (i, cluster.elements,
                                                                degeneracy_cluster,
                                                                cluster.contacts,
                                                                cluster.threshold,
                                                                cluster.density or 1.0,
                                                                metric)
                summaryFile.write(writeString)

        utilities.writeObject(outputObject, self, protocol=2)

    def addSnapshotToCluster(self, trajNum, snapshot, origCluster, snapshotNum, metrics=None, col=None, topology=None):
        """
            Cluster a snapshot using the leader algorithm

            :param trajNum: Trajectory number
            :type trajNum: int
            :param snapshot: Snapshot to add
            :type snapshot: str
            :param origCluster: Cluster found in the previos snapshot
            :type origCluster: int
            :param snapshotNum: Number of snapshot in its trajectory
            :type snapshotNum: int
            :param metrics: Array with the metrics of the snapshot
            :type metrics: numpy.Array
            :param col: Column of the desired metrics
            :type col: int
            :returns: int -- Cluster to which the snapshot belongs
            :param topology: Topology for non-pdb trajectories
            :type topology: list
        """
        if metrics is None:
            metrics = []
        pdb = atomset.PDB()
        pdb.initialise(snapshot, resname=self.resname, resnum=self.resnum, chain=self.resChain, topology=topology)
        self.clusteringEvaluator.cleanContactMap()
        for clusterNum, cluster in enumerate(self.clusters.clusters):
            scd = atomset.computeSquaredCentroidDifference(cluster.pdb, pdb)
            if scd > self.clusteringEvaluator.getInnerLimit(cluster):
                continue

            isSimilar, dist = self.clusteringEvaluator.isElement(pdb, cluster,
                                                                 self.resname, self.resnum,
                                                                 self.resChain, self.contactThresholdDistance)
            if isSimilar:
                if dist > cluster.threshold/2.0:
                    cluster.altStructure.addStructure(pdb, cluster.threshold, self.resname, self.resnum, self.resChain, self.contactThresholdDistance, self.clusteringEvaluator, trajPosition=(self.epoch, trajNum, snapshotNum))
                cluster.addElement(metrics)
                if origCluster is None:
                    origCluster = clusterNum
                self.conformationNetwork.add_edge(origCluster, clusterNum)
                return clusterNum

        # if made it here, the snapshot was not added into any cluster
        # Check if contacts and contactMap are set (depending on which kind
        # of clustering)
        self.clusteringEvaluator.checkAttributes(pdb, self.resname, self.resnum,
                                                 self.resChain, self.contactThresholdDistance)
        contacts = self.clusteringEvaluator.contacts
        numberOfLigandAtoms = pdb.getNumberOfAtoms()
        contactsPerAtom = contacts/numberOfLigandAtoms

        threshold = self.thresholdCalculator.calculate(contactsPerAtom)
        cluster = Cluster(pdb, thresholdRadius=threshold,
                          contacts=contactsPerAtom,
                          contactMap=self.clusteringEvaluator.contactMap,
                          metrics=metrics, metricCol=col,
                          contactThreshold=self.contactThresholdDistance,
                          altSelection=self.altSelection, trajPosition=(self.epoch, trajNum, snapshotNum))
        self.clusters.addCluster(cluster)
        clusterNum = self.clusters.getNumberClusters()-1
        if clusterNum == origCluster or origCluster is None:
            origCluster = clusterNum
            # The clusterNum should only be equal to origCluster when the first
            # cluster is created and the clusterInitialStructures function has
            # not been called, i.e. when usind the compareClustering script
            self.conformationNetwork.add_node(clusterNum, parent='root', epoch=self.epoch)
        else:
            self.conformationNetwork.add_node(clusterNum, parent=origCluster, epoch=self.epoch)
        self.conformationNetwork.add_edge(origCluster, clusterNum)
        # If a new cluster is discovered during a trajectory, the next step in
        # the same trajectory will be considered to start from these new
        # cluster, thus resulting in a more precise conformation network and
        # smoother pathways
        return clusterNum

    def writeClusterMetric(self, path, metricCol):
        """
            Write the metric of each node in the conformation network in a
            tab-separated file

            :param path: Path where to write the network
            :type path: str
            :param metricCol: Column of the metric of interest
            :type metricCol: int
        """
        with open(path, "w") as f:
            for i, cluster in enumerate(self.clusters.clusters):
                metric = cluster.getMetricFromColumn(metricCol)
                if metric is None:
                    f.write("%d\t-\n" % i)
                else:
                    f.write("%d\t%.4f\n" % (i, metric))

    def writeConformationNodePopulation(self, path):
        """
            Write the population of each node in the conformation network in a
            tab-separated file

            :param path: Path where to write the network
            :type path: str
        """
        with open(path, "w") as f:
            for i, cluster in enumerate(self.clusters.clusters):
                f.write("%d\t%d\n" % (i, cluster.elements))

    def getOptimalMetric(self, column=None, simulationType="min"):
        """
            Find the cluster with the best metric

            :param column: Column of the metric that defines the best cluster,
                if not specified, the cluster metric is chosen
            :type column: int
            :param simulationType: Define optimal metric as the maximum or minimum, max or min
            :type simulationType: str

            :returns: int -- Number of cluster with the optimal metric
        """
        metrics = []
        for _, cluster in enumerate(self.clusters.clusters):
            if column is None:
                metric = cluster.getMetric()
            else:
                metric = cluster.getMetricFromColumn(column)
            metrics.append(metric)
        if None in metrics:
            raise utilities.RequiredParameterMissingException("Metrics not found in clusters and required for filtering!!")
        if simulationType.lower() == "min":
            optimalMetricIndex = np.argmin(metrics)
        elif simulationType.lower() == "max":
            optimalMetricIndex = np.argmax(metrics)
        else:
            raise ValueError("Unrecognized type simulation parameter!!! Possible values are max or min")

        return optimalMetricIndex

    def writePathwayTrajectory(self, pathway, filename):
        """
            Write a list of cluster forming a pathway into a trajectory pdb file

            :param pathway: List of clusters that form the pathway
            :type pathway: list
            :param filename: Path where to write the trajectory
            :type filename: str
        """
        with open(filename, "w") as pathwayFile:
            pathwayFile.write("REMARK 000 File created using PELE++\n")
            pathwayFile.write("REMARK 000 Pathway trajectory created using the FDT\n")
            pathwayFile.write("REMARK 000 List of cluster belonging to the pathway %s\n" % ' '.join(map(str, pathway)))
            for i, step_cluster in enumerate(pathway):
                cluster = self.clusters.clusters[step_cluster]
                pathwayFile.write("MODEL    %4d\n" % (i+1))
                pdbStr = cluster.pdb.get_pdb_string()
                pdbList = pdbStr.split("\n")
                for line in pdbList:
                    line = line.strip()
                    # Avoid writing previous REMARK block
                    if line.startswith("REMARK ") or line.startswith("MODEL ") or line == "END":
                        continue
                    elif line:
                        pathwayFile.write(line+"\n")
                pathwayFile.write("ENDMDL\n")

    def writePathwayOptimalCluster(self, filename):
        """
            Extract the pathway to the cluster with the best metric as a
            trajectory and  write it to a PDB file

            :param filename: Path where to write the trajectory
            :type filename: str
        """
        optimalCluster = self.getOptimalMetric()
        pathway = self.createPathwayToCluster(optimalCluster)
        self.writePathwayTrajectory(pathway, filename)


class ContactsClustering(Clustering):
    def __init__(self, thresholdCalculator, resname="", resnum=0, resChain="",
                 reportBaseFilename=None, columnOfReportFile=None,
                 contactThresholdDistance=8, symmetries=None, altSelection=False):
        """
            Cluster together all snapshots that are closer to the cluster center
            than certain threshold. This threshold is assigned according to the
            ratio of number of contacts over the number of heavy atoms of the ligand

            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param thresholdCalculator: ThresholdCalculator object that calculate the
                threshold according to the contacts ratio
            :type thresholdCalculator: :py:class:`.ThresholdCalculator`
            :param reportBaseFilename: Name of the file that contains the metrics of
                the snapshots to cluster
            :type reportBaseFilename: str
            :param columnOfReportFile: Column of the report file that contain the
                metric of interest
            :type columnOfReportFile: int
            :param contactThresholdDistance: Distance at wich a ligand atom and a protein atom are
                considered in contact(default 8)
            :type contactThresholdDistance: float
            :param symmetries: List of symmetric groups
            :type symmetries: list
            :param altSelection: Flag that controls wether to use the alternative structures (default 8)
            :type altSelection: bool
        """
        Clustering.__init__(self, resname=resname, resnum=resnum, resChain=resChain,
                            reportBaseFilename=reportBaseFilename,
                            columnOfReportFile=columnOfReportFile,
                            contactThresholdDistance=contactThresholdDistance,
                            altSelection=altSelection)
        self.type = clusteringTypes.CLUSTERING_TYPES.rmsd
        self.thresholdCalculator = thresholdCalculator
        if symmetries is None:
            symmetries = []
        self.symmetries = symmetries
        self.clusteringEvaluator = ContactsClusteringEvaluator(RMSDCalculator.RMSDCalculator(symmetries))

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"type": self.type, "clusters": self.clusters,
                 "reportBaseFilename": self.reportBaseFilename,
                 "resname": self.resname, "resnum": self.resnum,
                 "resChain": self.resChain, "col": self.col,
                 "epoch": self.epoch,
                 "symmetries": self.symmetries,
                 "conformationNetwork": self.conformationNetwork,
                 "contactThresholdDistance": self.contactThresholdDistance,
                 "altSelection": self.altSelection,
                 "thresholdCalculator": self.thresholdCalculator,
                 "clusteringEvaluator": self.clusteringEvaluator}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.type = state['type']
        self.clusters = state['clusters']
        self.reportBaseFilename = state.get('reportBaseFilename')
        self.resname = state.get('resname', "")
        self.resnum = state.get('resnum', 0)
        self.resChain = state.get('resChain', "")
        self.col = state.get('col')
        self.contactThresholdDistance = state.get('contactThresholdDistance', 8)
        self.symmetries = state.get('symmetries', [])
        self.altSelection = state.get('altSelection', False)
        self.conformationNetwork = state.get('conformationNetwork', ConformationNetwork())
        self.epoch = state.get('epoch', -1)
        self.thresholdCalculator = state.get('thresholdCalculator', thresholdcalculator.ThresholdCalculatorConstant())
        if isinstance(self.symmetries, dict):
            self.symmetries = [self.symmetries]
        self.clusteringEvaluator = state.get('clusteringEvaluator', ContactsClusteringEvaluator(RMSDCalculator.RMSDCalculator(self.symmetries)))


class ContactMapAccumulativeClustering(Clustering):
    def __init__(self, thresholdCalculator, similarityEvaluator, resname="",
                 resnum=0, resChain="",
                 reportBaseFilename=None, columnOfReportFile=None,
                 contactThresholdDistance=8, symmetries=None, altSelection=False):
        """ Cluster together all snapshots that have similar enough contactMaps.
            This similarity can be calculated with different methods (see similariyEvaluator documentation)

            :param thresholdCalculator: ThresholdCalculator object that calculate the
                threshold according to the contacts ratio
            :type thresholdCalculator: :py:class:`.ThresholdCalculator`
            :param similarityEvaluator: object that calculates the similarity
                between two contact maps
            :type similarityEvaluator: object
            :param resname: String containing the three letter name of the ligand in the pdb
            :type resname: str
            :param resnum: Integer containing the residue number of the ligand in the pdb
            :type resnum: int
            :param resChain: String containing the chain name of the ligand in the pdb
            :type resChain: str
            :param reportBaseFilename: Name of the file that contains the metrics of
                the snapshots to cluster
            :type reportBaseFilename: str
            :param columnOfReportFile: Column of the report file that contain the
                metric of interest
            :type columnOfReportFile: int
            :param contactThresholdDistance: Distance at wich a ligand atom and a protein atom are
                considered in contact(default 8)
            :type contactThresholdDistance: float
            :param symmetries: List of symmetric groups
            :type symmetries: list
            :param altSelection: Flag that controls wether to use the alternative structures (default 8)
            :type altSelection: bool
        """
        if symmetries is None:
            symmetries = []
        Clustering.__init__(self, resname=resname, resnum=resnum, resChain=resChain,
                            reportBaseFilename=reportBaseFilename,
                            columnOfReportFile=columnOfReportFile,
                            contactThresholdDistance=contactThresholdDistance,
                            altSelection=altSelection)
        self.type = clusteringTypes.CLUSTERING_TYPES.contactMap
        self.thresholdCalculator = thresholdCalculator
        self.similarityEvaluator = similarityEvaluator
        self.symmetryEvaluator = sym.SymmetryContactMapEvaluator(symmetries)
        self.clusteringEvaluator = CMClusteringEvaluator(similarityEvaluator, self.symmetryEvaluator)

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"type": self.type, "clusters": self.clusters,
                 "reportBaseFilename": self.reportBaseFilename,
                 "resname": self.resname, "resnum": self.resnum,
                 "resChain": self.resChain, "col": self.col,
                 "epoch": self.epoch, "symmetries": self.symmetries,
                 "conformationNetwork": self.conformationNetwork,
                 "contactThresholdDistance": self.contactThresholdDistance,
                 "altSelection": self.altSelection,
                 "thresholdCalculator": self.thresholdCalculator,
                 "similariyEvaluator": self.similarityEvaluator,
                 "symmetryEvaluator": self.symmetryEvaluator,
                 "clusteringEvaluator": self.clusteringEvaluator}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.type = state['type']
        self.clusters = state['clusters']
        self.reportBaseFilename = state.get('reportBaseFilename')
        self.resname = state.get('resname', "")
        self.resnum = state.get('resnum', 0)
        self.resChain = state.get('resChain', "")
        self.col = state.get('col')
        self.contactThresholdDistance = state.get('contactThresholdDistance', 8)
        self.symmetries = state.get('symmetries', [])
        self.altSelection = state.get('altSelection', False)
        self.conformationNetwork = state.get('conformationNetwork', ConformationNetwork())
        self.epoch = state.get('epoch', -1)
        self.thresholdCalculator = state.get('thresholdCalculator', thresholdcalculator.ThresholdCalculatorConstant(value=0.3))
        self.similarityEvaluator = state.get('similariyEvaluator', CMSimilarityEvaluator(blockNames.ClusteringTypes.Jaccard))
        self.symmetryEvaluator = state.get('symmetryEvaluator', sym.SymmetryContactMapEvaluator(self.symmetries))
        self.clusteringEvaluator = state.get('clusteringEvaluator', CMClusteringEvaluator(self.similarityEvaluator, self.symmetryEvaluator))


class SequentialLastSnapshotClustering(Clustering):
    """
        Assigned  the last snapshot of the trajectory to a cluster.
        Only useful for PELE sequential runs
    """
    def __init__(self, resname="", resnum=0, resChain="", reportBaseFilename=None,
                 columnOfReportFile=None, contactThresholdDistance=8,
                 altSelection=False):
        Clustering.__init__(self, resname=resname, resnum=resnum, resChain=resChain,
                            reportBaseFilename=reportBaseFilename,
                            columnOfReportFile=columnOfReportFile,
                            contactThresholdDistance=contactThresholdDistance,
                            altSelection=altSelection)
        self.type = clusteringTypes.CLUSTERING_TYPES.lastSnapshot

    def cluster(self, paths, topology=None, epoch=None, outputPathConstants=None):
        """
            Cluster the snaptshots contained in the paths folder

            :param paths: List of folders with the snapshots
            :type paths: list
            :param topology: Topology object containing the set of topologies needed for the simulation
            :type topology: :py:class:`.Topology`
            :param epoch: Epoch number
            :type epoch: int
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
        """
        # Clean clusters at every step, so we only have the last snapshot of
        # each trajectory as clusters
        self.clusters = Clusters()
        trajectories = getAllTrajectories(paths)
        for trajectory in trajectories:
            trajNum = utilities.getTrajNum(trajectory)
            snapshots = utilities.getSnapshots(trajectory, True)
            if topology is not None:
                top = topology.getTopology(self.epoch, trajNum)
            else:
                top = None
            if self.reportBaseFilename:
                reportFilename = os.path.join(os.path.split(trajectory)[0],
                                              self.reportBaseFilename % trajNum)
                metrics = loadReportFile(reportFilename)
                # Pass as cluster metrics the minimum value for each metric,
                # thus the metrics are not valid to do any spawning, only to
                # check the exit condition
                metrics = metrics.min(axis=0)

                self.addSnapshotToCluster(snapshots[-1], metrics, self.col, topology=top)
            else:
                self.addSnapshotToCluster(snapshots[-1], topology=top)

    def addSnapshotToCluster(self, snapshot, metrics=None, col=None, topology=None):
        """
            Cluster a snapshot using the leader algorithm

            :param trajNum: Trajectory number
            :type trajNum: int
            :param snapshot: Snapshot to add
            :type snapshot: str
            :param metrics: Array with the metrics of the snapshot
            :type metrics: numpy.Array
            :param col: Column of the desired metrics
            :type col: int
            :returns: int -- Cluster to which the snapshot belongs
            :param topology: Topology for non-pdb trajectories
            :type topology: list
        """
        if metrics is None:
            metrics = []
        pdb = atomset.PDB()
        pdb.initialise(snapshot, resname=self.resname, resnum=self.resnum,
                       chain=self.resChain, topology=topology)
        contacts = pdb.countContacts(self.resname, self.contactThresholdDistance, self.resnum, self.resChain)
        numberOfLigandAtoms = pdb.getNumberOfAtoms()
        contactsPerAtom = contacts/numberOfLigandAtoms

        cluster = Cluster(pdb, thresholdRadius=0,
                          contacts=contactsPerAtom, metrics=metrics,
                          metricCol=col)
        self.clusters.addCluster(cluster)


class NullClustering(Clustering):
    """
        Don't generate any clustering, works essentially as a placeholder
        for simulation when no clustering is desired
    """
    def __init__(self):
        Clustering.__init__(self)
        self.type = clusteringTypes.CLUSTERING_TYPES.null

    def cluster(self, paths, topology=None, epoch=None, outputPathConstants=None):
        """
            Cluster the snaptshots contained in the paths folder

            :param paths: List of folders with the snapshots
            :type paths: list
            :param topology: Topology object containing the set of topologies needed for the simulation
            :type topology: :py:class:`.Topology`
            :param epoch: Epoch number
            :type epoch: int
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
        """
        pass

    def writeOutput(self, outputPath, degeneracy, outputObject, writeAll):
        """
            Writes all the clustering information in outputPath

            :param outputPath: Folder that will contain all the clustering information
            :type outputPath: str
            :param degeneracy: Degeneracy of each cluster. It must be in the same order
                as in the self.clusters list
            :type degeneracy: list
            :param outputObject: Output name for the pickle object
            :type outputObject: str
            :param writeAll: Wether to write pdb files for all cluster in addition
                of the summary
            :type writeAll: bool
        """
        utilities.cleanup(outputPath)
        utilities.makeFolder(outputPath)

        summaryFilename = os.path.join(outputPath, "summary.txt")
        with open(summaryFilename, 'w') as summaryFile:
            summaryFile.write("#cluster size degeneracy contacts threshold density metric\n")
            summaryFile.write("Using null clustering, no clusters available\n")

        utilities.writeObject(outputObject, self, protocol=2)


class MSMClustering(Clustering):
    """
        Cluster the trajectories to estimate a Markov State Model (MSM)
    """
    def __init__(self, n_clusters, tica=False, resname="", resnum=0, resChain="", symmetries=None, atom_Ids="", writeCA=False, sidechains=False, tica_lagtime=10, tica_nICs=3, tica_kinetic_map=True, tica_commute_map=False):
        if not PYEMMA:
            raise utilities.UnsatisfiedDependencyException("No installation of PyEMMA found. Please, install PyEMMA to use MSMClustering option.")
        Clustering.__init__(self, resname=resname, resnum=resnum, resChain=resChain)
        self.type = clusteringTypes.CLUSTERING_TYPES.MSMClustering
        self.nprocessors = None
        self.n_clusters = n_clusters
        self.tica = tica
        self.constantsExtract = coord.Constants()
        self.indexes = None
        self.atom_Ids = atom_Ids
        self.writeCA = writeCA
        self.sidechains = sidechains
        self.tica_lagtime = tica_lagtime
        self.tica_nICs = tica_nICs
        self.tica_kinetic_map = tica_kinetic_map
        self.tica_commute_map = tica_commute_map
        self.pyemma_clustering = None
        self.extract_params = coord.ParamsHandler("", self.atom_Ids, self.resname, 0, False, False, 0, self.writeCA, True, self.nprocessors, False, "", self.sidechains, "", False, False, "", False, False)

    def __getstate__(self):
        # Defining pickling interface to avoid problems when working with old
        # simulations if the properties of the clustering-related classes have
        # changed
        state = {"type": self.type, "clusters": self.clusters,
                 "reportBaseFilename": self.reportBaseFilename,
                 "resname": self.resname, "resnum": self.resnum,
                 "resChain": self.resChain, "col": self.col,
                 "epoch": self.epoch, "symmetries": self.symmetries,
                 "nprocessors": self.nprocessors, "n_clusters": self.n_clusters,
                 "tica": self.tica, "constantsExtract": self.constantsExtract,
                 "indexes": self.indexes, "atom_Ids": self.atom_Ids,
                 "writeCA": self.writeCA, "sidechains": self.sidechains,
                 "tica_lagtime": self.tica_lagtime, "tica_nICs": self.tica_nICs,
                 "tica_kinetic_map": self.tica_kinetic_map,
                 "tica_commute_map": self.tica_commute_map,
                 "pyemma_clustering": self.pyemma_clustering,
                 "extract_params": self.extract_params}
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.type = state['type']
        self.clusters = state['clusters']
        self.reportBaseFilename = state.get('reportBaseFilename')
        self.resname = state.get('resname', "")
        self.resnum = state.get('resnum', 0)
        self.resChain = state.get('resChain', "")
        self.col = state.get('col')
        self.epoch = state.get('epoch', -1)
        self.symmetries = state.get('symmetries', [])
        if isinstance(self.symmetries, dict):
            self.symmetries = [self.symmetries]
        self.nprocessors = state.get('nprocessors')
        self.n_clusters = state['n_clusters']
        self.tica = state.get('tica', False)
        self.constantsExtract = state.get('constantsExtract', coord.Constants())
        self.indexes = state.get('indexes')
        self.atom_Ids = state.get('atom_Ids', "")
        self.writeCA = state.get('writeCA', False)
        self.sidechains = state.get('sidechains', False)
        self.tica_lagtime = state.get('tica_lagtime', 10)
        self.tica_nICs = state.get('tica_nICs', 3)
        self.tica_kinetic_map = state.get('tica_kinetic_map', True)
        self.tica_commute_map = state.get('tica_commute_map', False)
        self.pyemma_clustering = state.get('pyemma_clustering')
        self.extract_params = state.get('extract_params', coord.ParamsHandler("", self.atom_Ids, self.resname, 0, False, False, 0, self.writeCA, True, self.nprocessors, False, "", self.sidechains, "", False, False, "", False, False))

    def updateRepeatParameters(self, repeat, steps):
        """
            Update parameters that should be extracted from the simulation object

            :param repeat: Whether to avoid repeating steps (False for PELE, True for md)
            :type repeat: bool
            :param steps: steps per epoch
            :type steps: int
        """
        self.extract_params.non_Repeat = repeat
        self.extract_params.numtotalSteps = steps

    def getClusterListForSpawning(self):
        """
            Return the clusters object to be used in the spawning

            :returns: :py:class:`.Clusters` -- Container object for the clusters
        """
        return self.pyemma_clustering

    def setProcessors(self, processors):
        self.nprocessors = processors

    def cluster(self, paths, topology=None, epoch=None, outputPathConstants=None):
        """
            Cluster the snaptshots contained in the paths folder

            :param paths: List of folders with the snapshots
            :type paths: list
            :param topology: Topology object containing the set of topologies needed for the simulation
            :type topology: :py:class:`.Topology`
            :param epoch: Epoch number
            :type epoch: int
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
        """
        if epoch is None:
            epoch = self.epoch + 1
        # clean clusters from previous iteration
        self.emptyClustering()
        # when cleaning the clusters, the epoch attribute is reset
        self.epoch = epoch

        utilities.makeFolder(outputPathConstants.allTrajsPath)
        utilities.makeFolder(os.path.join(outputPathConstants.allTrajsPath, "extractedCoordinates"))
        extractedFolder = self.constantsExtract.extractedTrajectoryFolder % outputPathConstants.epochOutputPathTempletized % self.epoch
        repeatedFolder = self.constantsExtract.outputTrajectoryFolder % outputPathConstants.epochOutputPathTempletized % self.epoch
        self.constantsExtract.gatherTrajsFilename = os.path.join(outputPathConstants.allTrajsPath, "traj_%s_%s.dat")
        self.constantsExtract.gatherNonRepeatedTrajsFilename = os.path.join(outputPathConstants.allTrajsPath, "extractedCoordinates", "traj_%s_%s.dat")
        utilities.makeFolder(extractedFolder)
        if not self.extract_params.non_Repeat:
            utilities.makeFolder(repeatedFolder)
        trajectories = getAllTrajectories(paths)
        self.extract_params.sidechain_folder = paths[0]
        self.extract_params.topology = topology
        # extract coordinates
        if PARALELLIZATION and self.nprocessors is not None:
            pool = mp.Pool(self.nprocessors)
            self.extract_params.parallelize = True
        else:
            self.extract_params.parallelize = False
            pool = None
        if self.sidechains:
            new_sidechains = coord.extractSidechainIndexes(self.extract_params, pool=pool)
            self.sidechains = list(set(self.sidechains).intersection(set(new_sidechains)))
        else:
            self.sidechains = []
        if self.indexes is None:
            if utilities.getFileExtension(trajectories[0]) in coord.MDTRAJ_FORMATS:
                self.indexes = []
                # select indexes for all topologies
                for top in topology.topologyFilesIterator():
                    self.indexes.append(coord.extractIndexesTopology(top, self.resname, self.atom_Ids, self.writeCA, self.sidechains))
            else:
                self.indexes = []

        workers = []
        for filename in trajectories:
            trajNum = utilities.getTrajNum(filename)
            if self.indexes:
                indexes_traj = self.indexes[topology.getTopologyIndex(self.epoch, trajNum)]
            else:
                indexes_traj = self.indexes
            if topology is not None:
                topology_traj = topology.getTopologyFile(self.epoch, trajNum)
            else:
                topology_traj = None
            if pool is None:
                # serial version
                coord.writeFilenameExtractedCoordinates(filename, self.extract_params, outputPathConstants.epochOutputPathTempletized % self.epoch, self.constantsExtract, topology=topology_traj, indexes=indexes_traj)
            else:
                # multiprocessor version
                workers.append(pool.apply_async(coord.writeFilenameExtractedCoordinates, args=(filename, self.extract_params, outputPathConstants.epochOutputPathTempletized % self.epoch, self.constantsExtract, topology_traj, indexes_traj)))
        for w in workers:
            w.get()
        if not self.extract_params.non_Repeat:
            coord.repeatExtractedSnapshotsInFolder(outputPathConstants.epochOutputPathTempletized % self.epoch, self.constantsExtract, self.extract_params.numtotalSteps)
        coord.gatherTrajs(self.constantsExtract, outputPathConstants.epochOutputPathTempletized % self.epoch, self.epoch, self.extract_params.non_Repeat, self.epoch)
        # apply tica
        if self.tica:
            trajectories = []
            trajs = glob.glob(os.path.join(outputPathConstants.allTrajsPath, self.constantsExtract.baseExtractedTrajectoryName+"*"))
            for trajectory in trajs:
                if "tica" in trajectory:
                    continue
                trajectories.append(utilities.loadtxtfile(trajectory))
            tica = coor.tica(data=trajectories, lag=self.tica_lagtime, kinetic_map=self.tica_kinetic_map, commute_map=self.tica_commute_map)
            projected = tica.get_output(dimensions=range(self.tica_nICs))
            for traj_name, projected_traj in zip(trajs, projected):
                auxArr = np.array(range(len(projected_traj)))
                np.savetxt("tica_%s" % traj_name, np.hstack(auxArr.reshape(-1, 1), projected_traj))
            base_traj_names = "tica_%s" % self.constantsExtract.baseGatheredFilename
        else:
            base_traj_names = self.constantsExtract.baseGatheredFilename

        # cluster the coordinates
        self.pyemma_clustering = pyemma_cluster.Cluster(self.n_clusters, outputPathConstants.allTrajsPath, base_traj_names, discretizedPath=os.path.join(outputPathConstants.allTrajsPath, "discretized"))
        self.pyemma_clustering.cleanDiscretizedFolder()
        self.pyemma_clustering.clusterTrajectories()

        # create Adaptive clusters from the kmeans result
        trajectory_files = glob.glob(os.path.join(outputPathConstants.allTrajsPath, "extractedCoordinates", base_traj_names))
        trajectories = [utilities.loadtxtfile(f)[:, 1:] for f in trajectory_files]
        # assign non-repeated trajectories to the clusters, in order to properly
        # assing the corresponding structures
        nonRepeatedDtrajs = self.pyemma_clustering.assignNewTrajectories(trajectories)
        centersInfo = getCentersInfo(self.pyemma_clustering.clusterCenters, trajectories, trajectory_files, nonRepeatedDtrajs)
        centersInfo_processed = []
        for cluster in centersInfo:
            try:
                epoch_num, traj_num, snapshot_num = centersInfo[cluster]["structure"]
            except TypeError:
                print("Structure not found for cluster %d" % cluster)
                raise
            centersInfo_processed.append([cluster, int(epoch_num), int(traj_num), int(snapshot_num)])
        extractInfo = getRepr.getExtractInfo(centersInfo_processed)
        # extractInfo is a dictionary organized as {[epoch, traj]: [cluster, snapshot]}

        # assign cluster dummies so that then clusters can be assigned in proper
        # order
        for _ in range(self.n_clusters):
            self.clusters.addCluster(Cluster(""))
        structureFolder = os.path.join(outputPathConstants.epochOutputPathTempletized, "*traj*_%d.*")
        for trajFile, extraInfo in extractInfo.items():
            try:
                pdbFile = glob.glob(structureFolder % trajFile)[0]
            except IndexError:
                raise ValueError("Structure %s not found" % (structureFolder % trajFile))
            try:
                snapshots = utilities.getSnapshots(pdbFile)
            except IOError:
                raise IOError("Unable to open %s, please check that the path to structures provided is correct" % pdbFile)
            for pair in extraInfo:
                pdb = atomset.PDB()
                if topology is not None:
                    top_traj = topology.getTopology(*trajFile)
                else:
                    top_traj = None
                pdb.initialise(snapshots[pair[1]], resname=self.resname, topology=top_traj)
                cluster = Cluster(pdb, trajPosition=(trajFile[0], trajFile[1], pair[1]))
                self.clusters[pair[0]] = cluster

    def writeOutput(self, outputPath, degeneracy, outputObject, writeAll):
        """
            Writes all the clustering information in outputPath

            :param outputPath: Folder that will contain all the clustering information
            :type outputPath: str
            :param degeneracy: Degeneracy of each cluster. It must be in the same order
                as in the self.clusters list
            :type degeneracy: list
            :param outputObject: Output name for the pickle object
            :type outputObject: str
            :param writeAll: Wether to write pdb files for all cluster in addition
                of the summary
            :type writeAll: bool
        """
        utilities.cleanup(outputPath)
        utilities.makeFolder(outputPath)

        summaryFilename = os.path.join(outputPath, "summary.txt")
        with open(summaryFilename, 'w') as summaryFile:
            summaryFile.write("#cluster degeneracy epoch trajectory snapshot cluster center\n")

            for i, cluster in enumerate(self.clusters.clusters):
                if writeAll:
                    outputFilename = "cluster_%d.pdb" % i
                    outputFilename = os.path.join(outputPath, outputFilename)
                    cluster.writePDB(outputFilename)

                degeneracy_cluster = 0
                if degeneracy is not None:
                    # degeneracy will be None if null spawning is used
                    degeneracy_cluster = degeneracy[i]
                center_str = " ".join(["%.3f" for _ in self.pyemma_clustering.clusterCenters[i]])
                writeString = "%d %d %d %d %d %s\n" % ((i, degeneracy_cluster) + cluster.trajPosition + (center_str % tuple(self.pyemma_clustering.clusterCenters[i]),))
                summaryFile.write(writeString)

        utilities.writeObject(outputObject, self, protocol=2)

    def filterClustersAccordingToBox(self, simulationRunnerParams):
        """
            Filter the clusters to select only the ones whose representative
            structures will fit into the selected box

            :param simulationRunnerParams: :py:class:`.SimulationParameters` Simulation parameters object
            :type simulationRunnerParams: :py:class:`.SimulationParameters`

            :returns list, list: -- list of the filtered clusters, list of bools flagging wether the cluster is selected or not

        """
        pass

    def filterClustersAccordingToMetric(self, clustersFiltered, filter_value, condition, col_filter):
        """
            Filter the clusters to select only the ones whose metric fits an
            specific criterion

            :param clustersFiltered: List of clusters to be processed
            :type clustersFiltered: list
            :param filter_value: Value to use in the filtering
            :type filter_value: float
            :param condition: Whether to use > or < condition in the filtering
            :type condition: str
            :param col_filter: Column of the report to use
            :type col_filter: int

            :returns list, list: -- list of the filtered clusters, list of bools flagging whether the cluster is selected or not

        """
        pass


class ClusteringBuilder(object):
    def buildClustering(self, clusteringBlock, reportBaseFilename=None, columnOfReportFile=None):
        """
            Builder to create the appropiate clustering object

            :param clusteringBlock: Parameters of the clustering process
            :type clusteringBlock: dict
            :param reportBaseFilename: Name of the file that contains the metrics of
                the snapshots to cluster
            :type reportBaseFilename: str
            :param columnOfReportFile: Column of the report file that contain the
                metric of interest
            :type columnOfReportFile: int
            :returns: :py:class:`.Clustering` -- Clustering object selected
        """
        paramsBlock = clusteringBlock[blockNames.ClusteringTypes.params]
        try:
            clusteringType = clusteringBlock[blockNames.ClusteringTypes.type]
        except KeyError as err:
            err.message += ": Need to provide mandatory parameter in clustering block"
            raise KeyError(err.message)
        contactThresholdDistance = paramsBlock.get(blockNames.ClusteringTypes.contactThresholdDistance, 8)
        altSelection = paramsBlock.get(blockNames.ClusteringTypes.alternativeStructure, False)
        resname = str(paramsBlock.get(blockNames.ClusteringTypes.ligandResname, "")).upper()
        resnum = int(paramsBlock.get(blockNames.ClusteringTypes.ligandResnum, 0))
        resChain = str(paramsBlock.get(blockNames.ClusteringTypes.ligandChain, "")).upper()
        if clusteringType == blockNames.ClusteringTypes.rmsd:
            symmetries = paramsBlock.get(blockNames.ClusteringTypes.symmetries, [])

            thresholdCalculatorBuilder = thresholdcalculator.ThresholdCalculatorBuilder()
            thresholdCalculator = thresholdCalculatorBuilder.build(clusteringBlock)
            return ContactsClustering(thresholdCalculator, resname=resname, resnum=resnum, resChain=resChain,
                                      reportBaseFilename=reportBaseFilename, columnOfReportFile=columnOfReportFile,
                                      contactThresholdDistance=contactThresholdDistance, symmetries=symmetries,
                                      altSelection=altSelection)
        elif clusteringType == blockNames.ClusteringTypes.lastSnapshot:

            return SequentialLastSnapshotClustering(resname=resname, resnum=resnum, resChain=resChain,
                                                    reportBaseFilename=reportBaseFilename,
                                                    columnOfReportFile=columnOfReportFile,
                                                    contactThresholdDistance=contactThresholdDistance)
        elif clusteringType == blockNames.ClusteringTypes.contactMap:
            symmetries = paramsBlock.get(blockNames.ClusteringTypes.symmetries, [])
            thresholdCalculatorBuilder = thresholdcalculator.ThresholdCalculatorBuilder()
            thresholdCalculator = thresholdCalculatorBuilder.build(clusteringBlock)
            try:
                similarityEvaluatorType = paramsBlock[blockNames.ClusteringTypes.similarityEvaluator]
            except KeyError:
                raise ValueError("No similarity Evaluator specified!!")
            similarityBuilder = similarityEvaluatorBuilder()
            similarityEvaluator = similarityBuilder.build(similarityEvaluatorType)
            return ContactMapAccumulativeClustering(thresholdCalculator, similarityEvaluator, resname=resname,
                                                    resnum=resnum, resChain=resChain,
                                                    reportBaseFilename=reportBaseFilename, columnOfReportFile=columnOfReportFile,
                                                    contactThresholdDistance=contactThresholdDistance, symmetries=symmetries, altSelection=altSelection)
        elif clusteringType == blockNames.ClusteringTypes.null:
            return NullClustering()
        elif clusteringType == blockNames.ClusteringTypes.MSMClustering:
            n_clusters = paramsBlock[blockNames.ClusteringTypes.nclusters]
            symmetries = paramsBlock.get(blockNames.ClusteringTypes.symmetries, [])
            tica = paramsBlock.get(blockNames.ClusteringTypes.tica, False)
            atom_Ids = paramsBlock.get(blockNames.ClusteringTypes.atom_Ids, "")
            writeCA = paramsBlock.get(blockNames.ClusteringTypes.writeCA, False)
            sidechains = paramsBlock.get(blockNames.ClusteringTypes.sidechains, False)
            tica_lagtime = paramsBlock.get(blockNames.ClusteringTypes.tica_lagtime, 10)
            tica_nICs = paramsBlock.get(blockNames.ClusteringTypes.tica_nICs, 3)
            tica_kinetic_map = paramsBlock.get(blockNames.ClusteringTypes.tica_kinetic_map, True)
            tica_commute_map = paramsBlock.get(blockNames.ClusteringTypes.tica_commute_map, False)
            return MSMClustering(n_clusters, tica, resname, resnum, resChain, symmetries, atom_Ids, writeCA, sidechains, tica_lagtime, tica_nICs, tica_kinetic_map, tica_commute_map)
        else:
            sys.exit("Unknown clustering method! Choices are: " +
                     str(clusteringTypes.CLUSTERING_TYPE_TO_STRING_DICTIONARY.values()))


class similarityEvaluatorBuilder(object):
    def build(self, similarityEvaluatorType):
        """
            Builder to create the appropiate similarityEvaluator

            :param similarityEvaluatorType: Type of similarityEvaluator chosen
            :type similarityEvaluatorType: str
            :returns: :py:class:`.SimilarityEvaluator` -- SimilarityEvaluator object selected
        """
        if similarityEvaluatorType in clusteringTypes.SIMILARITY_TYPES_NAMES:
            return CMSimilarityEvaluator(similarityEvaluatorType)
        else:
            sys.exit("Unknown threshold calculator type! Choices are: " + str(clusteringTypes.SIMILARITY_TYPES_TO_STRING_DICTIONARY.values()))


class CMSimilarityEvaluator(object):
    """
        Evaluate the similarity of two contactMaps by calculating the ratio of
        the number of differences over the average of elements in the contacts
        maps, their correlation or their Jaccard index, that is, the ratio
        between the intersection of the two contact maps and their union
    """
    def __init__(self, typeEvaluator):
        self.typeEvaluator = typeEvaluator

    def isSimilarCluster(self, contactMap, clusterContactMap, symContactMapEvaluator):
        """
            Evaluate if two contactMaps are similar or not, return True if yes,
            False otherwise

            :param contactMap: contactMap of the structure to compare
            :type contactMap: numpy.Array
            :param contactMap: contactMap of the structure to compare
            :type contactMap: numpy.Array
            :param symContactMapEvaluator: Contact Map symmetry evaluator object
            :type symContactMapEvaluator: :py:class:`.SymmetryContactMapEvaluator`
            :returns: float -- distance between contact maps
        """
        if self.typeEvaluator == blockNames.ClusteringTypes.correlation:
            return symContactMapEvaluator.evaluateCorrelation(contactMap, clusterContactMap)
        elif self.typeEvaluator == blockNames.ClusteringTypes.Jaccard:
            return symContactMapEvaluator.evaluateJaccard(contactMap, clusterContactMap)
        elif self.typeEvaluator == blockNames.ClusteringTypes.differenceDistance:
            return symContactMapEvaluator.evaluateDifferenceDistance(contactMap, clusterContactMap)
        else:
            raise ValueError("Evaluator type %s not found!!" % self.typeEvaluator)


def getAllTrajectories(paths):
    """
        Find all the trajectory files in the paths specified

        :param paths: The path where to find the trajectories
        :type paths: str
        :returns: list -- A list with the names of all th trajectories in paths
    """
    files = []
    for path in paths:
        files += glob.glob(path)
    # sort the files obtained by glob by name, so that the results will be the
    # same on all computers
    return sorted(files)


def filterRepeatedReports(metrics, column=2):
    """
        Filter the matrix containing the report information to avoid rejected
        steps

        :param metrics: Contents of the report file
        :type metrics: np.ndarray
        :param column: Column to check for repeats
        :type column: int
        :returns: np.ndarray -- Contents of the report file filtered
    """
    new_metrics = []
    accepted_steps = set()
    for row in metrics:
        if row[2] in accepted_steps:
            continue
        else:
            accepted_steps.add(row[2])
            new_metrics.append(row.tolist())
    return np.array(new_metrics)


def loadReportFile(reportFile):
    """
        Load a report file and filter it

        :param reportFile: Name of the report file
        :type reportFile: str
        :returns: np.ndarray -- Contents of the report file
    """
    metrics = utilities.loadtxtfile(reportFile)
    return filterRepeatedReports(metrics)
