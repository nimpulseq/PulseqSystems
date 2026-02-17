import src/pulseq_systems

echo listManufacturers()
echo listModels("Siemens Healthineers")
echo listGradients("Siemens Healthineers", "MAGNETOM Free Max")
echo getPulseqSpecs("Siemens Healthineers", "MAGNETOM Free Max", scaleGradients=1.0).repr()