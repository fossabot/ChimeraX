// vim: set expandtab ts=4 sw=4:
#ifndef atomstruct_AtomicStructure
#define atomstruct_AtomicStructure

#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <set>

// can't use forward declarations for classes that we will
// use unique pointers for, since template expansion checks
// that they have default delete functions
#include "Atom.h"
#include "Bond.h"
#include "Chain.h"
#include "CoordSet.h"
#include "imex.h"
#include "Pseudobond.h"
#include "Residue.h"
#include "Ring.h"
#include "basegeom/Graph.h"

namespace atomstruct {

class Element;

class ATOMSTRUCT_IMEX AtomicStructure: public basegeom::Graph<Atom, Bond> {
public:
    typedef Vertices  Atoms;
    typedef Edges  Bonds;
    typedef std::vector<std::unique_ptr<Chain>> Chains;
    typedef std::vector<std::unique_ptr<CoordSet>>  CoordSets;
    static const char*  PBG_METAL_COORDINATION;
    static const char*  PBG_MISSING_STRUCTURE;
    typedef std::vector<std::unique_ptr<Residue>>  Residues;
    typedef std::set<Ring>  Rings;
private:
    CoordSet *  _active_coord_set;
    bool  _being_destroyed;
    mutable Chains *  _chains;
    CoordSets  _coord_sets;
    AS_PBManager  _pb_mgr;
    Residues  _residues;
public:
    AtomicStructure();
    virtual  ~AtomicStructure() { _being_destroyed = true; }
    const Atoms &    atoms() const { return vertices(); }
    CoordSet *  active_coord_set() const { return _active_coord_set; };
    bool  asterisks_translated;
    bool  being_destroyed() const { return _being_destroyed; }
    std::unordered_map<Residue *, char>  best_alt_locs() const;
    const Bonds &    bonds() const { return edges(); }
    const Chains &  chains() const { if (_chains == nullptr) make_chains(); return *_chains; }
    const CoordSets &  coord_sets() const { return _coord_sets; }
    void  delete_atom(Atom* a) {
        for (auto b: a->bonds()) delete_bond(b);
        delete_vertex(a);
    }
    void  delete_bond(Bond* b) {
        for (auto a: b->atoms()) a->remove_bond(b);
        delete_edge(b);
    }
    CoordSet *  find_coord_set(int) const;
    Residue *  find_residue(std::string &chain_id, int pos, char insert) const;
    Residue *  find_residue(std::string &chain_id, int pos, char insert,
        std::string &name) const;
    bool  is_traj;
    bool  lower_case_chains;
    typedef std::pair<Chain::Residues, Sequence::Contents*> CI_Chain_Pairing;
    typedef std::map<std::string, CI_Chain_Pairing> ChainInfo;
    void  make_chains(const ChainInfo *ci = nullptr) const;
    Atom *  new_atom(const std::string &name, Element e);
    Bond *  new_bond(Atom *, Atom *);
    CoordSet *  new_coord_set();
    CoordSet *  new_coord_set(int index);
    CoordSet *  new_coord_set(int index, int size);
    Residue *  new_residue(const std::string &name, const std::string &chain,
        int pos, char insert, Residue *neighbor=NULL, bool after=true);
    int  num_atoms() const { return atoms().size(); }
    int  num_bonds() const { return bonds().size(); }
    AS_PBManager&  pb_mgr() { return _pb_mgr; }
    std::unordered_map<std::string, std::vector<std::string>> pdb_headers;
    int  pdb_version;
    std::vector<Chain::Residues>  polymers() const;
    const Residues &  residues() const { return _residues; }
    void  set_active_coord_set(CoordSet *cs);
    void  use_best_alt_locs();
};

}  // namespace atomstruct

#endif  // atomstruct_AtomicStructure
