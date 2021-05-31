"""A CephFS configurable cluster.

This profile creates a minimum Ceph cluster and configurable CephFS clients.
"""

# Import the Portal object.
import geni.portal as portal

# Import the ProtoGENI library.
import geni.rspec.pg as pg

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
monitor = request.RawPC("monitor")

# Create three object storage daemons
osd1 = request.RawPC("osd1")
osd2 = request.RawPC("osd2")
osd3 = request.RawPC("osd3")

# Create a single metadata daemon
mds = request.RawPC("mds")

clients = [request.RawPC("client" + str(i)) for i in range(params.c)]

# Create a link between them
link1 = request.Link(members=[monitor, osd1, osd2, osd3, mds] + clients)

# Abort execution if there are any errors, and report them.
pc.verifyParameters()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
