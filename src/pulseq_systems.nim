import std/json
import std/paths
import std/sequtils
import std/tables
import std/math

type 
    SystemSpec* = object
        B0*: float64
        maxSlew*: float64
        maxGrad*: float64
        slewUnit*: string
        gradUnit*: string

const jsonPath = Path("pulseq_systems") / Path("json") / Path("MRSystems.json")
const jsonData = slurp(string(jsonPath))

let systems* = parseJson(jsonData)

let metadata* = systems["_metadata"]

systems.delete("_metadata")

proc listManufacturers*(): seq[string] =
    toSeq(systems.getFields().keys)

proc listModels*(manufacturer: string): seq[string] =
    toSeq(systems[manufacturer].getFields().keys)

proc listGradients*(manufacturer: string, model: string): seq[string] =
    toSeq(systems[manufacturer][model]["gradient_configurations"].keys)

proc getPulseqSpecs*(manufacturer: string, model: string, gradient: string = "", scaleGradients: float64 = 1.0, scaleSlewRate: float64 = 1.0): SystemSpec =
    var gradName: string
    if gradient == "":
        gradName = toSeq(systems[manufacturer][model]["gradient_configurations"].getFields().keys)[0]
    else:
        gradName = gradient
    
    let selectedSystem = systems[manufacturer][model]
    let gradientProperties = selectedSystem["gradient_configurations"][gradName]

    var scaleGradients = scaleGradients
    var scaleSlewRate = scaleSlewRate
    if gradientProperties["is_gradient_strength_per_axis"].kind != JNull and gradientProperties["is_gradient_strength_per_axis"].getBool == false:
        scaleGradients /= sqrt(3.0)
    
    if gradientProperties["is_slew_rate_per_axis"].kind != JNull and gradientProperties["is_slew_rate_per_axis"].getBool == false:
        scaleSlewRate /= sqrt(3.0)

    result = SystemSpec(
        B0: float64(selectedSystem["B0_field_strength_T"].getFloat()),
        maxSlew: float64(gradientProperties["max_slew_rate_T_per_m_per_s"].getFloat()) * scaleSlewRate,
        maxGrad: float64(gradientProperties["max_gradient_strength_mT_per_m"].getFloat() * scaleGradients),
        slewUnit: "T/m/s", 
        gradUnit: "mT/m")
