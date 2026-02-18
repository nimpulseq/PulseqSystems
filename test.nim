import src/pulseq_systems

echo listManufacturers()
echo listModels("Siemens Healthineers")
echo listGradients("Siemens Healthineers", "MAGNETOM Free Max")

echo "Canon Galan"
echo $getPulseqSpecs("Canon Medical Systems", "Vantage Galan 3T Supreme Edition")

echo "Siemens Free.Max"
echo $getPulseqSpecs("Siemens Healthineers", "MAGNETOM Free Max")