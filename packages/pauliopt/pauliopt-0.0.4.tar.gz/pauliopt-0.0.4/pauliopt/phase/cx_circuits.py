"""
    This module contains code to create CX circuits for the optimization
    of circuits of mixed phase gadgets.
"""

from typing import (cast, Collection, Dict, FrozenSet, Iterator, List,
                    Optional, overload, Sequence, Tuple, Union)
import numpy as np # type: ignore
from pauliopt.topologies import Coupling, Topology, Matching


GateLike = Union[List[int], Tuple[int, int]]


class CXCircuitLayer:
    """
        Container for a layer of CX gates constrained
        by a given qubit topology.

        It uses `pauliopt.topologies.Matching` to keep track of which
        couplings in the qubit topology are currently occupied by a CX gate,
        and to efficiently determine whether a CX gate can be added to the layer.
    """

    _topology: Topology
    _couplings_seq: Tuple[Coupling, ...]
    _gates: Dict[Coupling, Tuple[int, int]]
    _matching: Matching

    def __init__(self, topology: Topology,
                 gates: Collection[GateLike] = tuple()):
        if not isinstance(topology, Topology):
            raise TypeError(f"Expected Topology, found {type(topology)}.")
        if not isinstance(gates, Collection):
            raise TypeError(f"Expected collection of ordered pairs, found {gates}")
        self._topology = topology
        self._gates = {}
        self._couplings_seq = tuple(sorted(topology.couplings))
        self._matching = Matching(topology)
        self._num_flippable_cxs = 2*len(self.topology.couplings)
        for gate in gates:
            if not isinstance(gate, (list, tuple)) or len(gate) != 2 or len(set(gate)) != 2:
                raise TypeError(f"Expected gates to be pairs of distinct integers, found {gate}.")
            ctrl, trgt = gate
            self.flip_cx(ctrl, trgt)

    @property
    def topology(self) -> Topology:
        """
            Readonly property exposing the qubit topology
            constraining this CX circuit layer.
        """
        return self._topology

    @property
    def num_gates(self) -> int:
        """
            Readonly property returning the number of gates in this
            CX circuit layer.
        """
        return len(self._gates)

    @property
    def gates(self) -> FrozenSet[Tuple[int, int]]:
        """
            Readonly property returning the collection of gates in this
            CX circuit layer.

            This collection is freshly generated at every call.
        """
        return frozenset(self._gates.values())

    @property
    def num_flippable_cxs(self) -> int:
        """
            Readonly property returning the number of CX gates in this
            CX circuit layer that can be flipped.
        """
        return self._num_flippable_cxs

    @property
    def flippable_cxs(self) -> FrozenSet[Tuple[int, int]]:
        """
            Readonly property returning the collection of CX gates that
            that can be currently flipped in this layer, namely:

            - all gates currently in the layer (will be removed by flip);
            - all gates with both qubits currently not covered by a gate
              already in the layer (will be added by flip).

            This collection is freshly generated at every call.
        """
        return frozenset(self._iter_flippable_cxs())

    def incident(self, qubit: int) -> Optional[Tuple[int, int]]:
        """
            Returns the CX gate incident to the given qubit in this layer,
            or `None` if there is no gate incident to the qubit.
        """
        incident_coupling = self._matching.incident(qubit)
        if incident_coupling is None:
            return None
        return self._gates[incident_coupling]

    def has_cx(self, ctrl: int, trgt: int) -> bool:
        """
            Checks whether the given CX gate is in the layer:
        """
        gate = (ctrl, trgt)
        coupling = Coupling(ctrl, trgt)
        return self._gates.get(coupling, None) == gate

    def is_cx_flippable(self, ctrl: int, trgt: int) -> bool:
        """
            Checks whether the given CX gate can be flipped in this layer.
            This is true if:

            - the gate is present (gate can be removed);
            - the gate is not present, and neither the control nor the
              target are already covered by some other gate (gate can be added).
        """
        gate = (ctrl, trgt)
        coupling = Coupling(ctrl, trgt)
        if coupling in self._gates:
            return self._gates[coupling] == gate
        if (self._matching.incident(ctrl) is None
                and self._matching.incident(trgt) is None):
            return True
        return False

    def random_flip_cx(self, rng: np.random.Generator) -> Tuple[int, int]:
        """
            Returns a randomly selected flippable CX gate in this CX circuit layer,
            using the given random number generator.
        """
        cx_idx = rng.integers(self._num_flippable_cxs)
        for i, cx in enumerate(self._iter_flippable_cxs()):
            if i == cx_idx:
                return cx
        raise Exception("Cannot get here!")

    def flip_cx(self, ctrl: int, trgt: int) -> "CXCircuitLayer":
        """
            Adds/removes a CX gate with given control and target to/from the layer.
            Raises `ValueError` if the gate cannot be added/removed.

            The layer is modified in-place and then returned, as per the
            [fluent API pattern](https://en.wikipedia.org/wiki/Fluent_interface).
        """
        # pylint: disable = too-many-branches
        if not isinstance(ctrl, int):
            raise TypeError(f"Expected integer, found {ctrl}.")
        if not isinstance(trgt, int):
            raise TypeError(f"Expected integer, found {trgt}.")
        gate = (ctrl, trgt)
        if not self._matching.is_flippable(gate):
            raise ValueError(f"Cannot add CX gate {gate} to the layer: "
                             f"gate is not present, but one of control or target "
                             f"is already involved in some other gate.")
        coupling = Coupling(ctrl, trgt)
        if coupling in self._gates:
            if self._gates[coupling] == gate:
                # CX gate already there, gets removed from the layer:
                del self._gates[coupling]
                self._matching.flip(coupling)
                self._num_flippable_cxs += 1
                for q in self._topology.adjacent(ctrl):
                    if q != trgt and self.incident(q) is None:
                        self._num_flippable_cxs += 2
                for q in self._topology.adjacent(trgt):
                    if q != ctrl and self.incident(q) is None:
                        self._num_flippable_cxs += 2
                return self
            raise ValueError(f"Invalid CX gate {gate} for given topology: another gate "
                             f"{self._gates[coupling]} already exists for this qubit pair.")
        # CX gate gets added to the layer:
        self._gates[coupling] = (ctrl, trgt)
        self._matching.flip(coupling)
        self._num_flippable_cxs -= 1
        for q in self._topology.adjacent(ctrl):
            if q != trgt and self.incident(q) is None:
                self._num_flippable_cxs -= 2
        for q in self._topology.adjacent(trgt):
            if q != ctrl and self.incident(q) is None:
                self._num_flippable_cxs -= 2
        return self

    def clone(self) -> "CXCircuitLayer":
        """
            Returns a copy of this CX layer.
        """
        return CXCircuitLayer(self.topology, self.gates)

    def draw(self, layout: str = "kamada_kawai", *,
             figsize: Optional[Tuple[int, int]] = None,
             zcolor: str = "#CCFFCC",
             xcolor: str = "#FF8888",
             noshow: bool = False,
             **kwargs):
        # pylint: disable = too-many-locals, too-many-branches
        """
            Draws this CX circuit layer using NetworkX and Matplotlib.

            The `layout` keyword argument can be used to select a NetworkX layout
            from the available ones (exposed by `Topology.available_nx_layouts`).
            The `figsize` keyword argument is passed to `matplotlib.pyplot.figure`:
            if specified, it determines the width and height of the figure being drawn.
            The `zcolor` and `xcolor` keyword arguments are used to determine the colour
            of the Z and X dots in a CX gate (analogous to `PhaseCircuit.to_svg`).
            Keyword arguments `kwargs` are those of `networkx.draw_networkx`.
        """
        try:
            # pylint: disable = import-outside-toplevel
            import networkx as nx # type: ignore
        except ModuleNotFoundError as _:
            raise ModuleNotFoundError("You must install the 'networkx' library.")
        try:
            # pylint: disable = import-outside-toplevel
            import matplotlib.pyplot as plt # type: ignore
        except ModuleNotFoundError as _:
            raise ModuleNotFoundError("You must install the 'matplotlib' library.")
        G = self.topology.to_nx
        nodes = sorted(self.topology.qubits)
        edges = sorted(self.topology.couplings, key=lambda c: c.as_pair)
        kwargs = {**kwargs}
        layouts = self.topology.available_nx_layouts
        if "pos" not in kwargs:
            if layout not in layouts:
                raise ValueError(f"Invalid layout found: {layout}. "
                                 f"Valid layouts: {', '.join(repr(l) for l in layouts)}")
            kwargs["pos"] = getattr(nx, layout+"_layout")(G)
        if "node_color" not in kwargs:
            kwargs["node_color"] = ["#dddddd" for _ in nodes]
        for node_idx, node in enumerate(nodes):
            gate = self.incident(node)
            if gate is not None:
                ctrl, trgt = gate
                if node == ctrl:
                    kwargs["node_color"][node_idx] = zcolor
                else:
                    kwargs["node_color"][node_idx] = xcolor
        if "edge_color" not in kwargs:
            kwargs["edge_color"] = ["#dddddd" for _ in edges]
        for ctrl, trgt in self.gates:
            edge_idx = edges.index(Coupling(ctrl, trgt))
            kwargs["edge_color"][edge_idx] = "#000000"
        if not noshow:
            plt.figure(figsize=figsize)
        nx.draw_networkx(G, **kwargs)
        if not noshow:
            plt.show()

    def __irshift__(self, gates: Union[GateLike, Sequence[GateLike]]) -> "CXCircuitLayer":
        if (isinstance(gates, (list, tuple))
                and all(isinstance(x, int) for x in gates) and len(gates) == 2):
            gates = [cast(Union[List[int], Tuple[int, int]], gates)]
        if not isinstance(gates, Sequence):
            raise TypeError(f"Expected sequence of gates, found {gates}")
        for gate in gates:
            if not isinstance(gate, Sequence) or len(gate) != 2:
                raise TypeError(f"Expected ordered pair, found {gate}")
            ctrl, trgt = gate
            self.flip_cx(ctrl, trgt)
        return self

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, CXCircuitLayer):
            return NotImplemented
        if self.topology != other.topology:
            return False
        return self.gates == other.gates

    def _iter_flippable_cxs(self) -> Iterator[Tuple[int, int]]:
        """
            Iterates over all CX gates that can be flipped.
            The layer must not be changed while the gates are being iterated,
            reason why this is a private method.

            The private method `pauliopt.topology.Matching._iter_flippable_couplings`
            can be called safely because `self._matching` is only accessible internally
            to the layer and cannot be accidentally modified (subject to the layer not
            being modified).
        """
        # pylint: disable = protected-access
        for coupling in self._matching._iter_flippable_couplings():
            if coupling in self._gates:
                yield self._gates[coupling]
            else:
                fst, snd = coupling
                yield (fst, snd)
                yield (snd, fst)

CXCircuitLayerLike = Union[CXCircuitLayer, "CXCircuitLayerView", Sequence[GateLike]]
CXCircuitLike = Union["CXCircuit", "CXCircuitView", Sequence[CXCircuitLayerLike]]

class CXCircuit(Sequence[CXCircuitLayer]):
    """
        Container for a circuit of CX gates, consisting of a given number of layers
        and constrained by a given qubit topology.
    """

    _topology: Topology
    _layers: List[CXCircuitLayer]

    def __init__(self, topology: Topology, layers: Sequence[CXCircuitLayer] = tuple()):
        if not isinstance(topology, Topology):
            raise TypeError(f"Expected Topology, found {type(topology)}.")
        if not isinstance(layers, Sequence):
            raise TypeError(f"Expected sequence of CXCircuitLayer, found {layers}")
        for layer in layers:
            if not isinstance(layer, CXCircuitLayer):
                raise TypeError(f"Expected CXCircuitLayer, found {type(layer)}")
            if layer.topology != topology:
                raise ValueError("Layer topology different from circuit topology.")
        self._topology = topology
        self._layers = list(layers)

    @property
    def topology(self) -> Topology:
        """
            Readonly property exposing the qubit topology
            constraining this CX circuit.
        """
        return self._topology

    @property
    def num_gates(self) -> int:
        """
            Readonly property returning the total number of gates in this
            CX circuit.
        """
        return sum((layer.num_gates for layer in self), 0)

    def dag(self) -> "CXCircuit":
        """
            Returns a copy of this CX circuit,
            with the layers in reverse order.
        """
        return CXCircuit(self.topology, list(self))

    def clone(self) -> "CXCircuit":
        """
            Returns a copy of this CX circuit.
        """
        return CXCircuit(self.topology, [l.clone() for l in self])

    def draw(self, layout: str = "kamada_kawai", *,
             figsize: Optional[Tuple[int, int]] = None,
             zcolor: str = "#CCFFCC",
             xcolor: str = "#FF8888",
             **kwargs):
        """
            Draws this CX circuit using NetworkX and Matplotlib.
            Keyword arguments `kwargs` are those of `networkx.draw_networkx`.
        """
        try:
            # pylint: disable = import-outside-toplevel
            import matplotlib.pyplot as plt # type: ignore
        except ModuleNotFoundError as _:
            raise ModuleNotFoundError("You must install the 'matplotlib' library.")
        large_figsize = None
        if figsize is not None:
            w, h = figsize
            large_figsize = (w*len(self), h)
        plt.figure(figsize=large_figsize)
        # plt.tight_layout()
        plt.subplots_adjust(wspace=0)
        for layer_idx, layer in enumerate(self):
            # print(f"Layer {layer_idx}:")
            plt.subplot(1, len(self), layer_idx+1, title=f"Layer {layer_idx}")
            layer.draw(layout=layout, figsize=figsize, noshow=True,
                       zcolor=zcolor, xcolor=xcolor, **kwargs)
        plt.show()

    @overload
    def __getitem__(self, layer_idx: int) -> CXCircuitLayer:
        ...

    @overload
    def __getitem__(self, layer_idx: slice) -> Sequence[CXCircuitLayer]:
        ...

    def __getitem__(self, layer_idx):
        return self._layers[layer_idx]

    def __len__(self) -> int:
        return len(self._layers)

    def __iter__(self) -> Iterator[CXCircuitLayer]:
        return iter(self._layers)

    def __irshift__(self, layers: Union[CXCircuitLayerLike,
                                        CXCircuitLike]) -> "CXCircuit":
        if isinstance(layers, (CXCircuitLayer, CXCircuitLayerView)):
            layers = [layers]
        if isinstance(layers, (CXCircuit, CXCircuitView)):
            layers = [layer.clone() for layer in layers]
        elif (isinstance(layers, Sequence)
              and all(isinstance(g, (list, tuple))
                      and all(isinstance(x, int) for x in g) # pylint: disable = C0330
                      and len(g) == 2 for g in layers)): # pylint: disable = C0330
            layers = [cast(Sequence[GateLike], layers)]
        if not isinstance(layers, Sequence):
            raise TypeError(f"Expected sequence of layers, found {layers}")
        for layer in layers:
            if isinstance(layer, CXCircuitLayerView):
                layer = layer.clone()
            elif not isinstance(layer, CXCircuitLayer):
                if not isinstance(layer, Sequence):
                    raise TypeError(f"Expected a sequence of pairs of ints, found {layer}")
                layer = CXCircuitLayer(self.topology, cast(Sequence[GateLike], layer))
            self._layers.append(layer)
        return self

    def __rshift__(self, layers: Union[CXCircuitLayerLike,
                                       CXCircuitLike]) -> "CXCircuit":
        circ = CXCircuit(self.topology, [])
        circ >>= layers
        return circ

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, CXCircuit):
            return NotImplemented
        if self.topology != other.topology:
            return False
        if len(self) != len(other):
            return False
        return all(sl == ol for sl, ol in zip(self, other))


class CXCircuitLayerView():
    """
        Readonly view on a CX circuit layer.
    """

    _layer: CXCircuitLayer

    def __init__(self, layer: CXCircuitLayer):
        if not isinstance(layer, CXCircuitLayer):
            raise TypeError(f"Expected CXCircuitLayer, found {type(layer)}.")
        self._layer = layer

    @property
    def topology(self) -> Topology:
        """
            Readonly property exposing the qubit topology
            constraining this CX circuit layer.
        """
        return self._layer.topology

    @property
    def gates(self) -> FrozenSet[Tuple[int, int]]:
        """
            Readonly property returning the collection of gates in this
            CX circuit layer.

            This collection is freshly generated at every call.
        """
        return self._layer.gates

    @property
    def num_gates(self) -> int:
        """
            Readonly property returning the number of gates in this
            CX circuit layer.
        """
        return self._layer.num_gates

    @property
    def flippable_cxs(self) -> FrozenSet[Tuple[int, int]]:
        """
            Readonly property returning the collection of CX gates that
            that can be currently flipped in this layer, namely:

            - all gates currently in the layer (will be removed by flip);
            - all gates with both qubits currently not covered by a gate
              already in the layer (will be added by flip).

            This collection is freshly generated at every call.
        """
        return self._layer.flippable_cxs

    def incident(self, qubit: int) -> Optional[Tuple[int, int]]:
        """
            Returns the CX gate incident to the given qubit in this layer,
            or `None` if there is no gate incident to the qubit.
        """
        return self._layer.incident(qubit)

    def has_cx(self, ctrl: int, trgt: int) -> bool:
        """
            Checks whether the given CX gate is in the layer:
        """
        return self._layer.has_cx(ctrl, trgt)

    def is_cx_flippable(self, ctrl: int, trgt: int) -> bool:
        """
            Checks whether the given CX gate can be flipped in this layer.
            This is true if:

            - the gate is present (gate can be removed);
            - the gate is not present, and neither the control nor the
              target are already covered by some other gate (gate can be added).
        """
        return self._layer.is_cx_flippable(ctrl, trgt)

    def clone(self) -> CXCircuitLayer:
        """
            Returns a copy of this CX layer.
        """
        return self._layer.clone()

    def draw(self, layout: str = "kamada_kawai", *,
             figsize: Optional[Tuple[int, int]] = None,
             zcolor: str = "#CCFFCC",
             xcolor: str = "#FF8888",
             **kwargs):
        """
            Draws this CX circuit layer using NetworkX and Matplotlib.
            Keyword arguments `kwargs` are those of `networkx.draw_networkx`.
        """
        return self._layer.draw(layout=layout, figsize=figsize,
                                zcolor=zcolor, xcolor=xcolor, **kwargs)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if isinstance(other, CXCircuitLayer):
            return self._layer == other
        if isinstance(other, CXCircuitLayerView):
            return self._layer == other._layer
        return NotImplemented


class CXCircuitView(Sequence[CXCircuitLayerView]):
    """
        Readonly view on a CX circuit.
    """

    _circuit: CXCircuit

    def __init__(self, circuit: CXCircuit):
        if not isinstance(circuit, CXCircuit):
            raise TypeError(f"Expected CXCircuit, found {type(circuit)}.")
        self._circuit = circuit

    @property
    def topology(self) -> Topology:
        """
            Readonly property exposing the qubit topology
            constraining this CX circuit.
        """
        return self._circuit.topology


    @property
    def num_gates(self) -> int:
        """
            Readonly property returning the number of gates in this
            CX circuit.
        """
        return self._circuit.num_gates

    def dag(self) -> "CXCircuit":
        """
            Returns a copy of this CX circuit,
            with the layers in reverse order.
        """
        return self._circuit.dag()

    def clone(self) -> CXCircuit:
        """
            Returns a copy of this CX circuit.
        """
        return self._circuit.clone()

    def draw(self, layout: str = "kamada_kawai", *,
             figsize: Optional[Tuple[int, int]] = None,
             zcolor: str = "#CCFFCC",
             xcolor: str = "#FF8888",
             **kwargs):
        """
            Draws this CX circuit using NetworkX and Matplotlib.
            Keyword arguments `kwargs` are those of `networkx.draw_networkx`.
        """
        return self._circuit.draw(layout=layout, figsize=figsize,
                                  zcolor=zcolor, xcolor=xcolor, **kwargs)

    @overload
    def __getitem__(self, layer_idx: int) -> CXCircuitLayerView:
        ...

    @overload
    def __getitem__(self, layer_idx: slice) -> Sequence[CXCircuitLayerView]:
        ...

    def __getitem__(self, layer_idx):
        return CXCircuitLayerView(self._circuit[layer_idx])

    def __len__(self) -> int:
        return len(self._circuit)

    def __iter__(self) -> Iterator[CXCircuitLayerView]:
        return (CXCircuitLayerView(l) for l in self._circuit)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if isinstance(other, CXCircuit):
            return self._circuit == other
        if isinstance(other, CXCircuitView):
            return self._circuit == other._circuit
        return NotImplemented
