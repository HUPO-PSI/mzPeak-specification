## Use cases

This describes which components are engaged for a particular scan configuration. This includes the inlet and ion source which may be configured independently of the mass analyzer. This is also the place to note the [MS:1000031|instrument model](http://purl.obolibrary.org/obo/MS_1000031), [MS:1000529|serial number](http://purl.obolibrary.org/obo/MS_1000529) and any [MS:1000032|customization](http://purl.obolibrary.org/obo/MS_1000032) done to the hardware.

### Multiple configurations

When handling an instrument with multiple mass analyzers like an [MS:1003971|ion trap fourier transform ion cyclotron resonance instrument](http://purl.obolibrary.org/obo/MS_1003971), there [SHOULD]{class="should-chip"} be multiple [`instrument_configuration`](#instrument_configuration) instances.

??? example "An example with two configurations, one using the ion trap, one using the Fourier transform ion cyclotron resonance mass spectrometer (FT-ICR)"
    ```json
    [
        {
        "components": [
        {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
            {
                "accession": "MS:1000073",
                "name": "electrospray ionization"
            },
            {
                "accession": "MS:1000057",
                "name": "electrospray inlet"
            }
            ]
        },
        {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
            {
                "accession": "MS:1000079",
                "name": "fourier transform ion cyclotron resonance mass spectrometer"
            }
            ]
        },
        {
            "component_type": "detector",
            "order": 3,
            "parameters": [
            {
                "accession": "MS:1000624",
                "name": "inductive detector"
            }
            ]
        }
        ],
        "id": 0,
        "parameters": [
        {
            "accession": "MS:1000448",
            "name": "LTQ FT"
        },
        {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "value": "SN06061F"
        }
        ],
        "software_reference": "Xcalibur"
        },
        {
        "components": [
            {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
                {
                "accession": "MS:1000073",
                "name": "electrospray ionization"
                },
                {
                "accession": "MS:1000057",
                "name": "electrospray inlet"
                }
            ]
            },
            {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
                {
                "accession": "MS:1000083",
                "name": "radial ejection linear ion trap"
                }
            ]
            },
            {
            "component_type": "detector",
            "order": 3,
            "parameters": [
                {
                "accession": "MS:1000253",
                "name": "electron multiplier"
                }
            ]
            }
        ],
        "id": 1,
        "parameters": [
            {
            "accession": "MS:1000448",
            "name": "LTQ FT"
            },
            {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "value": "SN06061F"
            }
        ],
        "software_reference": "Xcalibur"
        }
    ]
    ```

### Repeated component types

Many instruments have multiple analyzers that process ions in tandem like triple-quadrupole instruments, or which
use a quadrupole as a mass filter before another mass analyzer like a time-of-flight mass analyzer. These instruments
have multiple [`component`](#component) entries in the same [`instrument_configuration`](#instrument_configuration)
with the same `component_type` property value(`analyzer`). The `order` property of these distinct analyzers [SHOULD]{class="should-chip"}
reflect the order in which ions are introduced to the component.
