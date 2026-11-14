from cobra import Model, Reaction, Metabolite

# 1. Make an empty model (an empty recipe book)
model = Model("toy_cell")

# 2. The ingredients (metabolites)
glucose = Metabolite("glucose")
oxygen  = Metabolite("oxygen")
energy  = Metabolite("energy")

# 3. The jobs (reactions)
take_glucose = Reaction("take_glucose")          # glucose comes in from the medium
take_glucose.add_metabolites({glucose: 1})
take_glucose.bounds = (0, 10)                    # at most 10 units per hour

take_oxygen = Reaction("take_oxygen")            # oxygen comes in from the medium
take_oxygen.add_metabolites({oxygen: 1})
take_oxygen.bounds = (0, 1000)                   # plenty of oxygen

route_A = Reaction("route_A_respiration")        # glucose + oxygen -> lots of energy
route_A.add_metabolites({glucose: -1, oxygen: -1, energy: 10})
route_A.gene_reaction_rule = "geneA"

route_B = Reaction("route_B_fermentation")       # glucose -> a little energy
route_B.add_metabolites({glucose: -1, energy: 2})
route_B.gene_reaction_rule = "geneB"

growth = Reaction("growth")                      # energy is used to make new cells
growth.add_metabolites({energy: -1})

model.add_reactions([take_glucose, take_oxygen, route_A, route_B, growth])

# 4. The goal: grow as fast as possible
model.objective = "growth"

# 5. Ask the questions
print("Normal (with oxygen):        growth =", model.slim_optimize())

with model:
    model.reactions.take_oxygen.bounds = (0, 0)
    print("No oxygen:                   growth =", model.slim_optimize())

with model:
    model.reactions.take_oxygen.bounds = (0, 0)
    model.genes.geneB.knock_out()
    print("No oxygen + geneB deleted:   growth =", model.slim_optimize(error_value=0))
