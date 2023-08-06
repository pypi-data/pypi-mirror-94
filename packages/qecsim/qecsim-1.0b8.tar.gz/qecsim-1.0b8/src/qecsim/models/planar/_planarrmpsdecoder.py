import functools
import itertools
import json
import logging
import operator

import numpy as np
from mpmath import mp

from qecsim import paulitools as pt, tensortools as tt
from qecsim.model import Decoder, cli_description
from qecsim.models.generic import DepolarizingErrorModel

logger = logging.getLogger(__name__)


@cli_description('Rotated MPS ([chi] INT >=0, [mode] CHAR, ...)')
class PlanarRMPSDecoder(Decoder):
    r"""
    Implements a planar Rotated Matrix Product State (RMPS) decoder.

    Decoding algorithm:

    * A sample recovery operation :math:`f` is found by resolving the syndrome to plaquettes
      (:meth:`qecsim.models.planar.PlanarCode.syndrome_to_plaquette_indices`), finding the nearest boundary of the same
      type for each plaquette (:meth:`qecsim.models.planar.PlanarCode.virtual_plaquette_index`), constructing a recovery
      operation by applying the path between each plaquette and its corresponding boundary
      (:meth:`qecsim.models.planar.PlanarPauli.path`).
    * The probability of the left coset :math:`fG` of the stabilizer group :math:`G` of the planar code with respect
      to :math:`f` is found by contracting an appropriately defined MPS-based tensor network (see
      https://arxiv.org/abs/1405.4883).
    * Since this is a rotated MPS decoder, the links of the network are rotated 45 degrees by splitting each stabilizer
      node into 4 delta nodes that are absorbed into the neighbouring qubit nodes.
    * The complexity of the algorithm can managed by defining a bond dimension :math:`\chi` to which the MPS bond
      dimension is truncated after each row/column of the tensor network is contracted into the MPS.
    * The probability of cosets :math:`f\bar{X}G`, :math:`f\bar{Y}G` and :math:`f\bar{Z}G` are calculated similarly.
    * The default contraction is column-by-column but can be set using the mode parameter to row-by-row or the average
      of both contractions.
    * A sample recovery operation from the most probable coset is returned.

    Notes:

    * Specifying chi=None gives an exact contract (up to rounding errors) but is exponentially slow in the size of
      the lattice.
    * Modes:

        * mode='c': contract by columns
        * mode='r': contract by rows
        * mode='a': contract by columns and by rows and, for each coset, take the average of the probabilities.

    * Contracting by columns (i.e. truncating vertical links) may give different coset probabilities to contracting by
      rows (i.e. truncating horizontal links). However, the effect is symmetric in that transposing the sample_pauli on
      the lattice and exchanging X and Z single Paulis reverses the difference between X and Z cosets probabilities.
    * Specifying stp (skip truncate probability) gives the probability that a tensor is not truncated in the approximate
      contraction controlled by chi. This can be used to break the symmetry of the contraction approximation.

    Tensor network example:

    3x4 planar code (H=qubit on horizontal edge, V=qubit on vertical edge):
    ::

        H---H---H---H
          |   |   |
          V   V   V
          |   |   |
        H---H---H---H
          |   |   |
          V   V   V
          |   |   |
        H---H---H---H

    MPS tensor network as per https://arxiv.org/abs/1405.4883 (s=stabilizer):
    ::

         0 1 2 3 4 5 6
        0H-s-H-s-H-s-H
         | | | | | | |
        1s-V-s-V-s-V-s
         | | | | | | |
        2H-s-H-s-H-s-H
         | | | | | | |
        3s-V-s-V-s-V-s
         | | | | | | |
        4H-s-H-s-H-s-H

    Links are rotated by splitting stabilizers and summing them into neighbouring qubits:
    ::

          H            H            H
          |            |           / \
        V-s-V  =>      s      =>  V   V
          |           / \          \ /
          H        V-s   s-V        H
                      \ /
                       s
                       |
                       H

    Resultant MPS tensor network (rotated 45 degree clockwise for contraction by column/row):
    ::

         0 1 2 3 4 5
        0    H
             |
        1  H-V-H
           | | |
        2H-V-H-V-H
           | | | |
        3  H-V-H-V-H
             | | |
        4    H-V-H
               |
        5      H
    """

    def __init__(self, chi=None, mode='c', stp=None, tol=None):
        """
        Initialise new planar RMPS decoder.

        :param chi: Truncated bond dimension. (default=None, unrestricted=falsy)
        :type chi: int or None
        :param mode: Contraction mode. (default='c', 'c'=columns, 'r'=rows, 'a'=average)
        :type mode: str
        :param stp: Skip truncate probability. (default=None, disabled=falsy)
        :type stp: float or None
        :param tol: Tolerance for treating normalised singular values as zero. (default=None, unrestricted=falsy)
        :type tol: float or None
        :raises ValueError: if chi is not falsy or > 0.
        :raises ValueError: if mode not in ('c', 'r', 'a').
        :raises ValueError: if stp is not falsy or 1.0 >= stp > 0.0.
        :raises ValueError: if tol is not falsy or > 0.0.
        :raises TypeError: if any parameter is of an invalid type.
        """
        try:  # paranoid checking for CLI. (operator.index ensures the parameter can be treated as an int)
            if not (not chi or operator.index(chi) > 0):
                raise ValueError('{} valid chi values are falsy or integer > 0'.format(type(self).__name__))
            if mode not in ('c', 'r', 'a'):
                raise ValueError("{} valid mode values are ('c', 'r', 'a')".format(type(self).__name__))
            if not (not stp or 1.0 >= stp > 0.0):
                raise ValueError('{} valid stp values are falsy or 1.0 >= number > 0.0'.format(type(self).__name__))
            if not (not tol or tol > 0.0):
                raise ValueError('{} valid tol values are falsy or number > 0.0'.format(type(self).__name__))
        except TypeError as ex:
            raise TypeError('{} invalid parameter type'.format(type(self).__name__)) from ex
        self._chi = chi
        self._mode = mode
        self._stp = stp
        self._tol = tol
        self._tnc = self.TNC()

    @classmethod
    def sample_recovery(cls, code, syndrome):
        """
        Return a sample Pauli consistent with the syndrome, created by applying a path between each plaquette identified
        by the syndrome and the nearest boundary of the same type as the plaquette.

        :param code: Planar code.
        :type code: PlanarCode
        :param syndrome: Syndrome as binary vector.
        :type syndrome: numpy.array (1d)
        :return: Sample recovery operation as planar pauli.
        :rtype: PlanarPauli
        """
        # prepare sample
        sample_recovery = code.new_pauli()
        # ask code for syndrome plaquette_indices
        plaquette_indices = code.syndrome_to_plaquette_indices(syndrome)
        # for each plaquette
        for index in plaquette_indices:
            # find nearest off-boundary plaquette
            virtual_index = code.virtual_plaquette_index(index)
            # add path to boundary
            sample_recovery.path(index, virtual_index)
        # return sample
        return sample_recovery

    def _coset_probabilities(self, prob_dist, sample_pauli):
        r"""
        Return the (approximate) probability and sample Pauli for the left coset :math:`fG` of the stabilizer group
        :math:`G` of the planar code with respect to the given sample Pauli :math:`f`, as well as for the cosets
        :math:`f\bar{X}G`, :math:`f\bar{Y}G` and :math:`f\bar{Z}G`.

        :param prob_dist: Tuple of probability distribution in the format (P(I), P(X), P(Y), P(Z)).
        :type prob_dist: 4-tuple of float
        :param sample_pauli: Sample planar Pauli.
        :type sample_pauli: PlanarPauli
        :return: Coset probabilities, Sample Paulis (both in order I, X, Y, Z)
            E.g. (0.20, 0.10, 0.05, 0.10), (PlanarPauli(...), PlanarPauli(...), PlanarPauli(...), PlanarPauli(...))
        :rtype: 4-tuple of mp.mpf, 4-tuple of PlanarPauli
        """

        # NOTE: OPTIMIZED CONTRACTION BY COLUMN
        #
        # * Partial contraction of coset-I tensor network by _column_
        #
        # pauli          create         contract       contract
        #                rotated TN     0-1 as bra_i   5-4 as ket_i
        #                               (left_stop=2)  (right_stop=3)
        #
        #  0123456        012345         012345         012345
        # 0. . . .       0  .           0  .           0  .
        # 1 . . .        1 ...          1 *..          1 *..
        # 2. . . .  -->  2.....   -->   2 *...   -->   2 *..*
        # 3 . . .        3 .....        3 *....        3 *..*
        # 4. . . .       4  ...         4  ...         4  ..*
        #                5   .          5   .          5   .
        #
        # * Optimized contraction of coset-Z tensor network (for example) by _column_
        #   using partial contraction of coset-I tensor network
        #
        # pauli with     create         combine and contract
        # logical        rotated TN     (bra_i + 2-3 + ket_i)
        #
        #  0123456        012345         012345
        # 0z . . .       0  z           0  z
        # 1 z . .        1 .z.          1 *z.
        # 2. z . .  -->  2..z..   -->   2 *z.*   -->   \pi
        # 3 . z .        3 .z...        3 *z.*
        # 4. . z z       4  z..         4  z.*
        #                5   z          5   z
        #

        # NOTE: OPTIMIZED CONTRACTION BY ROW
        #
        # * Partial contraction of coset-I tensor network by _row_
        #
        # pauli          create         transpose      contract       contract
        #                rotated TN                    0-1 as bra_i   5-4 as ket_i
        #                                              (left_stop=2)  (right_stop=3)
        #
        #  0123456        012345         012345         012345         012345
        # 0. . . .       0  .           0  .           0  .           0  .
        # 1 . . .        1 ...          1 ...          1 *..          1 *..
        # 2. . . .  -->  2.....   -->   2.....   -->   2 *...   -->   2 *..*
        # 3 . . .        3 .....        3 .....        3 *....        3 *..*
        # 4. . . .       4  ...         4  ...         4  ...         4  ..*
        #                5   .          5   .          5   .          5   .
        #
        # * Optimized contraction of coset-Z tensor network (for example) by _row_
        #   using partial contraction of coset-I tensor network
        #
        # pauli with     create         transpose      combine and contract
        # logical        rotated TN                    (bra_i + 2-3 + ket_i)
        #
        #  0123456        012345         012345         012345
        # 0. . z z       0  .           0  z           0  z
        # 1 . z .        1 ...          1 .z.          1 *z.
        # 2. z . .  -->  2zzzzz   -->   2..z..   -->   2 *z.*   -->   \pi
        # 3 z . .        3 ....z        3 .z...        3 *z.*
        # 4z . . .       4  ...         4  z..         4  z.*
        #                5   .          5   z          5   z
        #

        # NOTE: logicals along major diagonal for various shape codes
        #
        # logical I     logical X     logical Y     logical Z
        #
        #  01234         01234         01234         01234
        # 0. . .        0x . .        0y . .        0z . .
        # 1 . .         1 x .         1 y .         1 z .
        # 2. . .        2. x .        2. y .        2. z .
        # 3 . .         3 . x         3 . y         3 . z
        # 4. . .        4. . x        4. . y        4. . z
        #
        #  0123456       0123456       0123456       0123456
        # 0. . . .      0x . . .      0y . . .      0z . . .
        # 1 . . .       1 x . .       1 y . .       1 z . .
        # 2. . . .      2. x . .      2. y . .      2. z . .
        # 3 . . .       3 . x .       3 . y .       3 . z .
        # 4. . . .      4. . x .      4. . y z      4. . z z
        #
        #  01234         01234         01234         01234
        # 0. . .        0x . .        0y . .        0z . .
        # 1 . .         1 x .         1 y .         1 z .
        # 2. . .        2. x .        2. y .        2. z .
        # 3 . .         3 . x         3 . y         3 . z
        # 4. . .        4. . x        4. . y        4. . z
        # 5 . .         5 . .         5 . .         5 . .
        # 6. . .        6. . x        6. . x        4. . .
        #

        def _logical_x(pauli, major=True):
            """return pauli after applying X along the major/minor diagonal"""
            max_row, max_col = pauli.code.bounds
            # define site indices
            site_indices = itertools.chain(
                zip(range(max_row + 1), range(max_col + 1)),  # along major diagonal
                ((r, max_col) for r in range(max_col + 2, max_row + 1, 2)),  # down rightmost column
            )
            # if not major, switch to minor diagonal
            if not major:
                site_indices = ((max_row - r, c) for r, c in site_indices)
            # apply X on sites
            return pauli.site('X', *site_indices)

        def _logical_z(pauli, major=True):
            """return pauli after applying Z along the major/minor diagonal"""
            max_row, max_col = pauli.code.bounds
            # define site indices
            site_indices = itertools.chain(
                zip(range(max_row + 1), range(max_col + 1)),  # along major diagonal
                ((max_row, c) for c in range(max_row + 2, max_col + 1, 2)),  # across bottom row
            )
            # if not major, switch to minor diagonal
            if not major:
                site_indices = ((max_row - r, c) for r, c in site_indices)
            # apply X on sites
            return pauli.site('Z', *site_indices)

        def _tn_contract_optimized(code, coset_ps, tns, mask):
            """update coset_ps with optimized contraction of tns"""
            # left_stop
            left_stop = min(code.size) - 1
            # note: for optimization we contract tn_i from left to left_stop as bra common to all cosets
            bra_i, bra_i_mult = tt.mps2d.contract(tns[0], chi=self._chi, tol=self._tol, mask=mask, stop=left_stop)
            # right_stop
            right_stop = tns[0].shape[1] - min(code.size)
            # note: for optimization we contract tn_i from right to right_stop as ket common to all cosets
            ket_i, ket_i_mult = tt.mps2d.contract(tns[0], chi=self._chi, tol=self._tol, mask=mask,
                                                  start=-1, stop=right_stop, step=-1)
            # for each tn, combine and contract to coset probability
            for j in range(len(tns)):
                # combine bra_i, tn_j[:, left_stop:right_stop + 1], ket_i as partially contracted tn
                partial_tn = np.column_stack((bra_i, tns[j][:, left_stop:right_stop + 1], ket_i))
                # slice mask to match partially contracted tn
                partial_mask = None if mask is None else mask[:, left_stop - 1:right_stop + 2]
                # contract
                result = tt.mps2d.contract(partial_tn, chi=self._chi, tol=self._tol, mask=partial_mask, step=-1)
                # multiply by multipliers
                coset_ps[j] = result * bra_i_mult * ket_i_mult

        # NOTE: all list/tuples in this method are ordered (i, x, y, z)
        # empty log warnings
        log_warnings = []
        # tensor networks: tn_i is common to both contraction by column and by row (after transposition)
        tn_i = self._tnc.create_tn(prob_dist, sample_pauli)
        mask = self._tnc.create_mask(self._stp, tn_i.shape)  # same mask for all tns
        # probabilities
        coset_ps = (0.0, 0.0, 0.0, 0.0)  # default coset probabilities
        coset_ps_col = coset_ps_row = None  # undefined coset probabilities by column and row
        # N.B. After multiplication by mult, coset_ps will be of type mp.mpf so don't process with numpy!
        if self._mode in ('c', 'a'):
            # note: for optimization we choose cosets to differ only on the major diagonal
            sample_x = _logical_x(sample_pauli.copy())
            tns = [tn_i,
                   self._tnc.create_tn(prob_dist, sample_x),
                   self._tnc.create_tn(prob_dist, _logical_z(sample_x.copy())),
                   self._tnc.create_tn(prob_dist, _logical_z(sample_pauli.copy()))]
            # evaluate coset probabilities by column
            coset_ps_col = [0.0, 0.0, 0.0, 0.0]  # default coset probabilities
            try:
                _tn_contract_optimized(sample_pauli.code, coset_ps_col, tns, mask)
            except (ValueError, np.linalg.LinAlgError) as ex:
                log_warnings.append('CONTRACTION BY COL FAILED: {!r}'.format(ex))
            # treat nan as inf so it doesn't get lost
            coset_ps_col = [mp.inf if mp.isnan(coset_p) else coset_p for coset_p in coset_ps_col]
        if self._mode in ('r', 'a'):
            # note: for optimization we choose cosets to differ only on the minor diagonal
            sample_x = _logical_x(sample_pauli.copy(), major=False)
            tns = [tn_i,
                   self._tnc.create_tn(prob_dist, sample_x),
                   self._tnc.create_tn(prob_dist, _logical_z(sample_x.copy(), major=False)),
                   self._tnc.create_tn(prob_dist, _logical_z(sample_pauli.copy(), major=False))]
            # evaluate coset probabilities by row
            coset_ps_row = [0.0, 0.0, 0.0, 0.0]  # default coset probabilities
            # transpose tensor networks
            tns = [tt.mps2d.transpose(tn) for tn in tns]
            mask = None if mask is None else mask.transpose()
            try:
                _tn_contract_optimized(sample_pauli.code, coset_ps_row, tns, mask)
            except (ValueError, np.linalg.LinAlgError) as ex:
                log_warnings.append('CONTRACTION BY ROW FAILED: {!r}'.format(ex))
            # treat nan as inf so it doesn't get lost
            coset_ps_row = [mp.inf if mp.isnan(coset_p) else coset_p for coset_p in coset_ps_row]
        if self._mode == 'c':
            coset_ps = coset_ps_col
        elif self._mode == 'r':
            coset_ps = coset_ps_row
        elif self._mode == 'a':
            # average coset probabilities
            coset_ps = [sum(coset_p) / len(coset_p) for coset_p in zip(coset_ps_col, coset_ps_row)]
        # logging
        if log_warnings:
            log_data = {
                # instance
                'decoder': repr(self),
                # method parameters
                'prob_dist': prob_dist,
                'sample_pauli': pt.pack(sample_pauli.to_bsf()),
                # variables (convert to string because mp.mpf)
                'coset_ps_col': [repr(p) for p in coset_ps_col] if coset_ps_col else None,
                'coset_ps_row': [repr(p) for p in coset_ps_row] if coset_ps_row else None,
                'coset_ps': [repr(p) for p in coset_ps],
            }
            logger.warning('{}: {}'.format(' | '.join(log_warnings), json.dumps(log_data, sort_keys=True)))
        # results
        sample_paulis = (
            sample_pauli,
            sample_pauli.copy().logical_x(),
            sample_pauli.copy().logical_x().logical_z(),
            sample_pauli.copy().logical_z()
        )
        return tuple(coset_ps), sample_paulis

    def decode(self, code, syndrome,
               error_model=DepolarizingErrorModel(),  # noqa: B008
               error_probability=0.1, **kwargs):
        """
        See :meth:`qecsim.model.Decoder.decode`

        Note: The optional keyword parameters ``error_model`` and ``error_probability`` are used to determine the prior
        probability distribution for use in the decoding algorithm. Any provided error model must implement
        :meth:`~qecsim.model.ErrorModel.probability_distribution`.

        :param code: Planar code.
        :type code: PlanarCode
        :param syndrome: Syndrome as binary vector.
        :type syndrome: numpy.array (1d)
        :param error_model: Error model. (default=DepolarizingErrorModel())
        :type error_model: ErrorModel
        :param error_probability: Overall probability of an error on a single qubit. (default=0.1)
        :type error_probability: float
        :return: Recovery operation as binary symplectic vector.
        :rtype: numpy.array (1d)
        """
        # any recovery
        any_recovery = self.sample_recovery(code, syndrome)
        # probability distribution
        prob_dist = error_model.probability_distribution(error_probability)
        # coset probabilities, recovery operations
        coset_ps, recoveries = self._coset_probabilities(prob_dist, any_recovery)
        # most likely recovery operation
        max_coset_p, max_recovery = max(zip(coset_ps, recoveries), key=lambda coset_p_recovery: coset_p_recovery[0])
        # logging
        if not (mp.isfinite(max_coset_p) and max_coset_p > 0):
            log_data = {
                # instance
                'decoder': repr(self),
                # method parameters
                'code': repr(code),
                'syndrome': pt.pack(syndrome),
                'error_model': repr(error_model),
                'error_probability': error_probability,
                # variables
                'prob_dist': prob_dist,
                'coset_ps': [repr(p) for p in coset_ps],  # convert to string because mp.mpf
                # context
                'error': pt.pack(kwargs['error']) if 'error' in kwargs else None,
            }
            logger.warning('NON-POSITIVE-FINITE MAX COSET PROBABILITY: {}'.format(json.dumps(log_data, sort_keys=True)))
        # return most likely recovery operation as bsf
        return max_recovery.to_bsf()

    @property
    def label(self):
        """See :meth:`qecsim.model.Decoder.label`"""
        params = [('chi', self._chi), ('mode', self._mode), ('stp', self._stp), ('tol', self._tol), ]
        return 'Planar RMPS ({})'.format(', '.join('{}={}'.format(k, v) for k, v in params if v))

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(type(self).__name__, self._chi, self._mode, self._stp, self._tol)

    class TNC:
        """Tensor network creator"""

        @functools.lru_cache()
        def h_node_value(self, prob_dist, f, n, e, s, w):
            """Return horizontal edge tensor element value."""
            paulis = ('I', 'X', 'Y', 'Z')
            op_to_pr = dict(zip(paulis, prob_dist))
            f = pt.pauli_to_bsf(f)
            I, X, Y, Z = pt.pauli_to_bsf(paulis)
            # n, e, s, w are in {0, 1} so multiply op to turn on or off
            op = (f + (n * Z) + (e * X) + (s * Z) + (w * X)) % 2
            return op_to_pr[pt.bsf_to_pauli(op)]

        @functools.lru_cache()
        def v_node_value(self, prob_dist, f, n, e, s, w):
            """Return vertical edge tensor element value."""
            # N.B. for v_node order of nesw is rotated relative to h_node
            return self.h_node_value(prob_dist, f, e, s, w, n)

        @functools.lru_cache()
        def create_h_node(self, prob_dist, f, compass_direction=None):
            """Return horizontal edge tensor."""

            def _shape(compass_direction=None):
                """Return shape of tensor including dummy indices."""
                return {
                    'n': (1, 2, 2, 2),
                    'ne': (1, 1, 2, 2),
                    'e': (2, 1, 2, 2),
                    'se': (2, 1, 1, 2),
                    's': (2, 2, 1, 2),
                    'sw': (2, 2, 1, 1),
                    'w': (2, 2, 2, 1),
                    'nw': (1, 2, 2, 1),
                }.get(compass_direction, (2, 2, 2, 2))

            # create bare h_node
            node = np.empty(_shape(compass_direction), dtype=np.float64)
            # fill values
            for n, e, s, w in np.ndindex(node.shape):
                node[(n, e, s, w)] = self.h_node_value(prob_dist, f, n, e, s, w)
            # multiply in deltas to link directly with surrounding v_nodes
            delta = tt.tsr.delta((2, 2, 2))
            if compass_direction == 'n':  # nesw -> (.n)(..)(eK)(lw)
                node = np.einsum('nesw,sKl->neKlw', node, delta).reshape((1, 1, 4, 4))
            elif compass_direction == 'ne':  # nesw -> (.n)(.e)(..)(sw)
                node = node.reshape((1, 1, 1, 4))
            elif compass_direction == 'e':  # nesw -> (in)(.e)(..)(sL)
                node = np.einsum('nesw,wLi->inesL', node, delta).reshape((4, 1, 1, 4))
            elif compass_direction == 'se':  # nesw -> (wn)(.e)(.s)(..)
                node = np.einsum('nesw->wnes', node).reshape((4, 1, 1, 1))
            elif compass_direction == 's':  # nesw -> (wI)(je)(.s)(..)
                node = np.einsum('nesw,nIj->wIjes', node, delta).reshape((4, 4, 1, 1))
            elif compass_direction == 'sw':  # nesw -> (..)(ne)(.s)(.w)
                node = node.reshape((1, 4, 1, 1))
            elif compass_direction == 'w':  # nesw -> (..)(nJ)(ks)(.w)
                node = np.einsum('nesw,eJk->nJksw', node, delta).reshape((1, 4, 4, 1))
            elif compass_direction == 'nw':  # nesw -> (.n)(..)(es)(.w)
                node = node.reshape((1, 1, 4, 1))
            else:  # nesw -> (iI)(jJ)(kK)(lL)
                node = np.einsum('nesw,nIj,eJk,sKl,wLi->iIjJkKlL',
                                 node, delta, delta, delta, delta).reshape((4, 4, 4, 4))
            return node

        @functools.lru_cache()
        def create_v_node(self, prob_dist, f):
            """Return vertical edge tensor."""
            # create bare v_node
            node = np.empty((2, 2, 2, 2), dtype=np.float64)
            # fill values
            for n, e, s, w in np.ndindex(node.shape):
                node[(n, e, s, w)] = self.v_node_value(prob_dist, f, n, e, s, w)
            # multiply in deltas to link directly with surrounding h_nodes
            delta = tt.tsr.delta((2, 2, 2))
            # nesw -> (Ii)(Jj)(Kk)(Ll)  N.B. order within each leg is reversed relative to h_node
            node = np.einsum('nesw,nIj,eJk,sKl,wLi->IiJjKkLl', node, delta, delta, delta, delta).reshape((4, 4, 4, 4))
            return node

        def create_tn(self, prob_dist, sample_pauli):
            """Return a network (numpy.array 2d) of tensors (numpy.array 4d).
            Note: The network contracts to the coset probability of the given sample_pauli.
            """

            def _rotate_q_index(index, code):
                """rotate q-node code index to tensor network index"""
                r, c = index  # qubit index
                return int(r / 2 + c / 2), int(code.size[0] - 1 - r / 2 + c / 2)

            def _compass_q_direction(index, code):
                """if q-node code index lies on border of give compass direction of that border, or blank otherwise"""
                direction = {0: 'n', code.bounds[0]: 's'}.get(index[0], '')
                direction += {0: 'w', code.bounds[1]: 'e'}.get(index[1], '')
                return direction

            # extract code
            code = sample_pauli.code
            # initialise empty tn
            tn_max_r, _ = _rotate_q_index(code.bounds, code)
            _, tn_max_c = _rotate_q_index((0, code.bounds[1]), code)
            tn = np.empty((tn_max_r + 1, tn_max_c + 1), dtype=object)
            # add h_nodes: iterate horizontal edges only
            for index in itertools.product(range(0, code.bounds[0] + 1, 2), range(0, code.bounds[1] + 1, 2)):
                tn[_rotate_q_index(index, code)] = self.create_h_node(
                    prob_dist, sample_pauli.operator(index), _compass_q_direction(index, code))
            # add v_nodes: iterate vertical edges only
            for index in itertools.product(range(1, code.bounds[0], 2), range(1, code.bounds[1], 2)):
                tn[_rotate_q_index(index, code)] = self.create_v_node(prob_dist, sample_pauli.operator(index))
            return tn

        def create_mask(self, stp, shape):
            """Return truncate mask (numpy.array 2d) of elements True with probability 1-stp and False with probability
            stp. Note: None is returned if stp (skip truncate probability) is falsy."""
            rng = np.random.default_rng()
            return rng.choice((True, False), size=shape, p=(1 - stp, stp)) if stp else None
