# vim: set expandtab shiftwidth=4 softtabstop=4:

# === UCSF ChimeraX Copyright ===
# Copyright 2016 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  For details see:
# http://www.rbvi.ucsf.edu/chimerax/docs/licensing.html
# This notice must be embedded in or attached to all copies,
# including partial copies, of the software or any revisions
# or derivations thereof.
# === UCSF ChimeraX Copyright ===

from chimerax.webservices.cxservices_job import CxServicesJob

class BlastProteinJob(CxServicesJob):

    QUERY_FILENAME = "query.fa"
    RESULTS_FILENAME = "results.json"

    def __init__(self, session, seq, atomspec, **kw):
        super().__init__(session)
        self.setup(seq, atomspec, **kw)
        params = {"db": self.database,
                  "evalue": str(self.cutoff),
                  "matrix": self.matrix,
                  "blimit": str(self.max_seqs),
                  "input_seq": self.seq,
                  "output_file": self.RESULTS_FILENAME}
        self.start("blast", params)


    def setup(self, seq, atomspec, database="pdb", cutoff=1.0e-3,
              matrix="BLOSUM62", max_seqs=500, log=None, tool_inst_name=None,
              sequence_name=None):
        from . import tool
        from . import databases
        self.seq = seq.replace('?', 'X')        # string
        self.sequence_name = sequence_name	# string
        self.atomspec = atomspec                # string (atom specifier)
        self.database = database                # string
        self._database = databases.get_database(database) # object
        self.cutoff = cutoff                    # float
        self.matrix = matrix                    # string
        self.max_seqs = max_seqs                # int
        self.log = log
        self.tool_inst_name = tool_inst_name
        self.tool = tool.find(tool_inst_name)

    def _seq_to_fasta(self, seq, title):
        data = ["> %s\n" % title]
        block_size = 60
        for i in range(0, len(seq), block_size):
            data.append("%s\n" % seq[i:i+block_size])
        return ''.join(data)

    def _params(self):
        # Keys must match HTML element ids
        return [
            ( "chain", self.atomspec ),
            ( "database", self.database ),
            ( "cutoff", self.cutoff ),
            ( "maxSeqs", self.max_seqs ),
            ( "matrix", self.matrix ),
        ]

    def on_finish(self):
        logger = self.session.logger
        logger.info("BlastProtein finished.")
        out = self.get_stdout()
        if out:
            logger.error("Standard output:\n" + out)
        if not self.exited_normally():
            err = self.get_stderr()
            if self.tool:
                self.tool.job_failed(self, err)
            else:
                if err:
                    logger.bug("Standard error:\n" + err)
        else:
            results = self.get_file(self.RESULTS_FILENAME)
            try:
                logger.info("Parsing BLAST results.")
                qname = self.sequence_name or 'query'
                self._database.parse(qname, self.seq, results)
            except Exception as e:
                if self.tool:
                    err = self.get_stderr()
                    self.tool.job_failed(self, err + str(e))
                else:
                    logger.bug("BLAST output parsing error: %s" % str(e))
            else:
                if self.tool:
                    self.tool.job_finished(self, self._database, self._params())
                else:
                    if self.session.ui.is_gui:
                        from .tool import ToolUI
                        ToolUI(self.session, "BlastProtein",
                               blast_results=self._database, params=self._params(),
                               instance_name=self.tool_inst_name)
                if self.log or (self.log is None and
                                not self.session.ui.is_gui):
                    msgs = ["BLAST results for:"]
                    for name, value in self._params():
                        msgs.append("  %s: %s" % (name, value))
                    for m in self._database.parser.matches:
                        name = m.match if m.match else m.name
                        msgs.append('\t'.join([name, "%.1e" % m.evalue,
                                               str(m.score),
                                               m.description]))
                    logger.info('\n'.join(msgs))
