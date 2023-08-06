# tdt

Tucker-Davis Technologies (TDT) Python APIs for reading data into Python and interacting with Synapse software

Usage
```python
import tdt

# download example data from https://www.tdt.com/files/examples/TDTExampleData.zip
tdt.download_demo_data()

# import data block into Python structure
data = tdt.read_block('data/Algernon-180308-130351')
print(data)
print(data.streams)
print(data.epocs)
```

See [SynapseAPI Manual PDF](https://www.tdt.com/files/manuals/SynapseAPIManual.pdf) for full SynapseAPI usage
```python
# connect to Synapse through SynapseAPI
import tdt
syn = tdt.SynapseAPI()
print(syn.getModeStr())
print(syn.getGizmoNames())
syn.setParameterValue('gizmo', 'parameter', new_value)
```