# Validate SHCD

CANU can be used to validate that an SHCD (SHasta Cabling Diagram) passes basic validation checks.

- The `--architecture / -a` flag is used to set the architecture of the system, either **TDS**, or **Full**.
- Use the `--tabs` flag to select which tabs on the spreadsheet will be included.
- The `--corners` flag is used to input the upper left and lower right corners of the table on each tab of the worksheet. The table should contain the 11 headers: **Source, Rack, Location, Slot, (Blank), Port, Destination, Rack, Location, (Blank), Port**. If the corners are not specified, you will be prompted to enter them for each tab.

## Example

### Validate SHCD

To check an SHCD run: `canu -s 1.4 validate shcd -a tds --shcd FILENAME.xlsx --tabs 25G_10G,NMN,HMN --corners I14,S25,I16,S22,J20,T39`

```bash
$ canu -s 1.4 validate shcd -a tds --shcd FILENAME.xlsx --tabs 25G_10G,NMN,HMN --corners I14,S25,I16,S22,J20,T39

SHCD Node Connections
------------------------------------------------------------
0: sw-spine-001 connects to 6 nodes: [1, 2, 3, 4, 5, 6]
1: sw-spine-002 connects to 6 nodes: [0, 2, 3, 4, 5, 6]
2: sw-leaf-bmc-001 connects to 2 nodes: [0, 1]
3: uan001 connects to 2 nodes: [0, 1]
4: ncn-s001 connects to 2 nodes: [0, 1]
5: ncn-w001 connects to 2 nodes: [0, 1]
6: ncn-m001 connects to 2 nodes: [0, 1]

Warnings

Node type could not be determined for the following
------------------------------------------------------------
CAN switch
```

## Flags

| Option                | Description                                                                |
| --------------------- | -------------------------------------------------------------------------- |
| `-a / --architecture` | Shasta architecture ("Full", or "TDS")                                     |
| `--shcd`              | SHCD File                                                                  |
| `--tabs`              | The tabs on the SHCD file to check, e.g. 10G_25G_40G_100G,NMN,HMN.         |
| `--corners`           | The corners on each tab, comma separated e.g. 'J37,U227,J15,T47,J20,U167'. |
| `--log`               | Level of logging. ("DEBUG", "INFO", "WARNING", "ERROR")                    |

---

**[Back To Readme](/readme.md)**<br>