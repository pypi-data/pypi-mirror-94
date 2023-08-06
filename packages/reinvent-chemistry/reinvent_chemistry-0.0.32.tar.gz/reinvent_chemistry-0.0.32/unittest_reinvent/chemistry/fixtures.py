from rdkit import Chem

celecoxib = 'Cc1ccc(-c2cc(C(F)(F)F)nn2-c2ccc(S(N)(=O)=O)cc2)cc1'
aspirin = 'CC(=O)Oc1ccccc1C(=O)O'
caffeine = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
dopamine = "C1=CC(=C(C=C1CCN)O)O"
serotonin = "c1cc2c(cc1O)c(c[nH]2)CCN"
invalid = 'INVALID'
stereo_smiles = 'Cc1ccccc1CC[C@H]NC'
non_stereo_smiles = 'CN[CH]CCc1ccccc1C'

smiles_collection = [celecoxib, aspirin, invalid]
mols_collection = [Chem.MolFromSmiles(smile) for smile in [celecoxib, aspirin]]