"""A CephFS configurable cluster.

This profile creates a minimum Ceph cluster and configurable CephFS clients.
"""

# Import the Portal object.
import geni.portal as portal

# Import the ProtoGENI library.
import geni.rspec.pg as pg


def create_node(name):
    node = request.RawPC(name)
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS8-64-STD"
    bs = node.Blockstore(name + "-data-bs", "/data")
    bs.size = "100GB"
    return node


# Create a portal context.
pc = portal.Context()

# Describe the parameter(s) this profile script can accept.
pc.defineParameter("c", "Number of clients", portal.ParameterType.INTEGER, 1)

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()

# Check parameter validity.
if params.c < 1:
    pc.reportError(
        portal.ParameterError("You must choose at least 1 client.", ["c"]))

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Create a single monitor daemon
monitor = create_node("monitor")

# Create three object storage daemons
osd1 = create_node("osd1")
osd2 = create_node("osd2")
osd3 = create_node("osd3")

# Create a single metadata daemon
mds = create_node("mds")

clients = [create_node("client" + str(i)) for i in range(params.c)]

# Create a link between them
# Note: is this needed? Looks like that a default link is always already created.
link1 = request.Link(members=[monitor, osd1, osd2, osd3, mds] + clients)

# Abort execution if there are any errors, and report them.
pc.verifyParameters()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
