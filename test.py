import pulseq_systems

print(pulseq_systems.list_manufacturers())
print(pulseq_systems.get_metadata())
print(pulseq_systems.list_models("Siemens Healthineers"))
print(pulseq_systems.list_gradients("Siemens Healthineers", "MAGNETOM Skyra"))
print(pulseq_systems.get_pulseq_specs("Siemens Healthineers", "MAGNETOM Skyra"))