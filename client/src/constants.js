const API_ENDPOINT = "http://127.0.0.1:8000/api/v1/";

//Enter your token authorization for your account to access api
const TOKEN_AUTH = "";

export default {
  API_ENDPOINT: API_ENDPOINT,
  TOKEN_AUTH: TOKEN_AUTH,
  CHOICE_FIELDS: {
    AHJ: {
      BuildingCode: [
        {value: "", text: getBFormPlaceholder("BuildingCode", "select")},
        {value: "2021IBC", text: "2021 IBC"},
        {value: "2018IBC", text: "2018 IBC"},
        {value: "2015IBC", text: "2015 IBC"},
        {value: "2012IBC", text: "2012 IBC"},
        {value: "2009IBC", text: "2009 IBC"},
        {value: "NoSolarRegulations", text: "No Solar Regulations"}
      ],
      ElectricCode: [
        {value: "", text: getBFormPlaceholder("ElectricCode", "select")},
        {value: "2020NEC", text: "2020 NEC"},
        {value: "2017NEC", text: "2017 NEC"},
        {value: "2014NEC", text: "2014 NEC"},
        {value: "2011NEC", text: "2011 NEC"},
        {value: "NoSolarRegulations", text: "No Solar Regulations"}
      ],
      FireCode: [
        {value: "", text: getBFormPlaceholder("FireCode", "select")},
        {value: "2021IFC", text: "2021 IFC"},
        {value: "2018IFC", text: "2018 IFC"},
        {value: "2015IFC", text: "2015 IFC"},
        {value: "2012IFC", text: "2012 IFC"},
        {value: "2009IFC", text: "2009 IFC"},
        {value: "NoSolarRegulations", text: "No Solar Regulations"}
      ],
      ResidentialCode: [
        {value: "", text: getBFormPlaceholder("ResidentialCode", "select")},
        {value: "2021IRC", text: "2021 IRC"},
        {value: "2018IRC", text: "2018 IRC"},
        {value: "2015IRC", text: "2015 IRC"},
        {value: "2012IRC", text: "2012 IRC"},
        {value: "2009IRC", text: "2009 IRC"},
        {value: "NoSolarRegulations", text: "No Solar Regulations"}
      ],
      WindCode: [
        {value: "", text: getBFormPlaceholder("WindCode", "select")},
        {value: "ASCE7716", text: "ASCE7-16"},
        {value: "ASCE7710", text: "ASCE7-10"},
        {value: "ASCE7705", text: "ASCE7-05"},
        {value: "SpecialWindZone", text: "Special Wind Zone"},
      ]
    },
    Contact: {
      ContactType: [
        {value: "", text: getBFormPlaceholder("ContactType", "select")},
        {value: "Homeowner", text: "Homeowner"},
        {value: "OffTaker", text: "Off Taker"},
        {value: "Inspector", text: "Inspector"},
        {value: "Engineer", text: "Engineer"},
        {value: "Originator", text: "Originator"},
        {value: "Installer", text: "Installer"},
        {value: "Investor", text: "Investor"},
        {value: "PermittingOfficial", text: "Permitting Official"},
        {value: "FireMarshal", text: "Fire Marshal"},
        {value: "ProjectManager", text: "Project Manager"},
        {value: "Salesperson", text: "Salesperson"}
      ],
      PreferredContactMethod: [
        {value: "", text: getBFormPlaceholder("PreferredContactMethod", "select")},
        {value: "Email", text: "Email"},
        {value: "WorkPhone", text: "Work Phone"},
        {value: "CellPhone", text: "Cell Phone"},
        {value: "HomePhone", text: "Home Phone"},
        {value: "CellTextMessage", text: "Cell Text Message"}
      ]
    },
    Address: {
      AddressType: [
        {value: "", text: getBFormPlaceholder("AddressType", "select")},
        {value: "Mailing", text: "Mailing"},
        {value: "Billing", text: "Billing"},
        {value: "Installation", text: "Installation"},
        {value: "Shipping", text: "Shipping"}
      ]
    },
    Location: {
      LocationDeterminationMethod: [
        {value: "", text: getBFormPlaceholder("LocationDeterminationMethod", "select")},
        {value: "GPS", text: "GPS"},
        {value: "Survey", text: "Survey"},
        {value: "AerialImage", text: "Aerial Image"},
        {value: "EngineeringReport", text: "Engineering Report"},
        {value: "AddressGeocoding", text: "Address Geocoding"},
        {value: "Unknown", text: "Unknown"}
      ],
      LocationType: [
        {value: "", text: getBFormPlaceholder("LocationType", "select")},
        {value: "DeviceSpecific", text: "Device Specific"},
        {value: "SiteEntrance", text: "Site Entrance"},
        {value: "GeneralProximity", text: "General Proximity"},
        {value: "Warehouse", text: "Warehouse"}
      ]
    },
    EngineeringReviewRequirement: {
      EngineeringReviewType: [
        {value: "", text: getBFormPlaceholder("EngineeringReviewType", "select")},
        {value: "StructuralEngineer", text: "Structural Engineer"},
        {value: "ElectricalEngineer", text: "Electrical Engineer"},
        {value: "PVEngineer", text: "PV Engineer"},
        {value: "MasterElectrician", text: "Master Electrician"},
        {value: "FireMarshal", text: "Fire Marshal"},
        {value: "EnvironmentalEngineer", text: "Environmental Engineer"}
      ],
      RequirementLevel: [
        {value: "", text: getBFormPlaceholder("RequirementLevel", "select")},
        {value: "Required", text: "Required"},
        {value: "Optional", text: "Optional"},
        {value: "ConditionallyRequired", text: "Conditionally Required"}
      ],
      StampType: [
        {value: "Wet", text: "Wet"},
        {value: "Digital", text: "Digital"},
        {value: "Notary", text: "Notary"},
        {value: "None", text: "None"}
      ]
    }
  }
};


function getBFormPlaceholder(fieldName, type) {
  if (type === "input") {
    return "Enter a " + fieldName + "...";
  } else if (type === "select") {
    return "Select a " + fieldName + "...";
  }
}
