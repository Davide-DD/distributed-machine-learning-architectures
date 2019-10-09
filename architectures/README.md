# Architectures

For my master thesis, I created 4 different architectures:
- **Cloud-centric**: it is based on a node resembling the cloud that contains a neural network and all the data for training it and a sensor (thing) that sends current reads to cloud and get predictions about the current status of a machine
- **Cloud-edge-thing**: it is the same of before, but here we also have an edge node that we exploit in order to lower the latency, as now the cloud trains the neural network and then pass it to the edge node, that is then asked from the thing about the current status of the machine like above
- **Federated-learning**: defines the Federated Learning architecture described by Google in [this paper](https://arxiv.org/pdf/1902.01046.pdf)
- **Gossip-learning**: defines the Gossip Learning architecture following the concepts presented in [this paper](https://arxiv.org/pdf/1109.1396.pdf)
