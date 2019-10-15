# Architectures

For my master thesis, I created 4 different architectures:
- **Cloud-centric**: it is based on a node resembling the cloud that contains a neural network and all the data for training it and a sensor (thing) that sends current reads to cloud and get predictions about the current status of a machine
- **Cloud-edge-thing**: it is the same of before, but here we also have an edge node that we exploit in order to lower the latency, as now the cloud trains the neural network and then pass it to the edge node, that is then asked from the thing about the current status of the machine like above
- **Federated-learning**: defines the Federated Learning architecture described by Google in [this paper](https://arxiv.org/pdf/1902.01046.pdf)
- **Gossip-learning**: defines the Gossip Learning architecture following the concepts presented in [this paper](https://arxiv.org/pdf/1109.1396.pdf)

Each architecture, except for the last two, are packed with a folder **nodes**, where you can find the actual implementation of each node composing the architecture, and a folder **fog05-mapping**, where you have a descriptor for each node of the architecture (to be used with fogØ5). The last two architectures provide only the first folder, while the second (for each one of them) can be found [here](https://github.com/Davide-DD/fog05-orchestrator/tree/master/example/architectures). Images are missing from this repository due to their size, but they can be found [here](https://drive.google.com/drive/u/1/folders/1JGM00qZzfJq8ertImiCVeU4gt7Kugxb_).
Concluding, in the last two architectures can be found a folder named **tests** that contains 3 important files:
- **test_generator.py**: it permits to easily create a test architecture composed by many nodes
- **test_executor.py**: it permits to easily instantiate all the nodes by which a test architecture is composed
- **test_killer.sh**: it permits to stop a test execution through sending signals to the running nodes

The federated learning architecture also offers a **test_plan.py**, that permits to send a sequence of task to the coordinator in order to execute them one after the other.

If you are interested in more details about the aforementioned architectures, check out my master thesis [here](https://amslaurea.unibo.it/19021/1/Tesi_Davide_Di_Donato.pdf).
