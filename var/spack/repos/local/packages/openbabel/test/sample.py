from openbabel import openbabel

mol = openbabel.OBMol()
print(mol.NumAtoms())

a = mol.NewAtom()
a.SetAtomicNum(6)
a.SetVector(0.0, 1.0, 2.0)

b = mol.NewAtom()
mol.AddBond(1, 2, 1)
print(mol.NumBonds())
print(mol.NumAtoms())

mol.Clear();
