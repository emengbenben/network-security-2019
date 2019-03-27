##====================================================================
# Assignment: Lab 1 Milestone 1 - Handshake - init file
# Team: GoldenNugget
# Date: 03-25-2019
#====================================================================

import playground
from .protocol import PassthroughFactory
from .ServerProtocol import PIMPServerProtocol
from .ClientProtocol import PIMPClientProtocol
from playground.network.common import StackingProtocol, StackingProtocolFactory, StackingTransport

f_client = StackingProtocolFactory(lambda: ClientProtocol())

f_server = StackingProtocolFactory(lambda: ServerProtocol())

ptConnector = playground.Connector(protocolStack=(f_client, f_server))

playground.setConnector("lab1protocol", ptConnector)


#passthroughConnector = playground.Connector(protocolStack=(PassthroughFactory(),PassthroughFactory()))
#playground.setConnector("passthrough", passthroughConnector)
#playground.setConnector("any_other_name", passthroughConnector)