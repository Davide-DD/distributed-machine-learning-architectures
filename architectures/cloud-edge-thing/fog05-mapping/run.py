from fog05 import FIMAPI
import json
import uuid
import sys
import os
import time

def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip,cloudfile,edgefile,thingfile,netfile1,netfile2):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    cloud_d = json.loads(read_file(cloudfile))
    edge_d = json.loads(read_file(edgefile))
    thing_d = json.loads(read_file(thingfile))
    net1_d = json.loads(read_file(netfile1))
    net2_d = json.loads(read_file(netfile2))

    cloud_uuid = cloud_d.get('uuid')
    edge_uuid = edge_d.get('uuid')
    thing_uuid = thing_d.get('uuid')
    net1_uuid = net1_d.get('uuid')
    net2_uuid = net2_d.get('uuid')

    input("Press enter to create network")
    a.network.add_network(net1_d)
    a.network.add_network(net2_d)

    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    #n1 = '16892ae12009411ab76998fdb7ccaf91'
    n1 = a.node.list()[0]
    #n1 = 'a2d358aaaf2b42cb8d23a89e88b97e5c'

    input('press enter to onboard edge descriptor')
    a.fdu.onboard(edge_d)

    input('Press enter to define edge')
    edgesid = a.fdu.define(edge_uuid, n1)

    input('Press enter to configure edge')
    a.fdu.configure(edgesid)

    input('Press enter to run edge')
    a.fdu.start(edgesid)

    time.sleep(15) # 15 seconds to be sure monitoring has updated network information
    edge4cloud_address = a.fdu.instance_info(edgesid)['hypervisor_info']['network']['eth0']['addresses'][0]['address']
    print(edge4cloud_address)
    edge4thing_address = a.fdu.instance_info(edgesid)['hypervisor_info']['network']['eth1']['addresses'][0]['address']
    print(edge4thing_address)

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))

    cloud_d['configuration']['script'] = "#cloud-config\nruncmd:\n  - [ sh, -xc, 'python3 -u /home/ubuntu/code/server.py http://" + edge4cloud_address + ":5000 > /home/ubuntu/log.txt' ]"
    thing_d['configuration']['script'] = "#cloud-config\nruncmd:\n  - [ sh, -xc, 'python3 -u /home/ubuntu/code/client.py http://" + edge4thing_address + ":5000 > /home/ubuntu/log.txt' ]"

    input('press enter to onboard cloud descriptor')
    a.fdu.onboard(cloud_d)

    input('Press enter to define cloud')
    cloudsid = a.fdu.define(cloud_uuid, n1)

    input('Press enter to configure cloud')
    a.fdu.configure(cloudsid)

    input('Press enter to run cloud')
    a.fdu.start(cloudsid)

    input('press enter to onboard thing descriptor')
    a.fdu.onboard(thing_d)

    input('Press enter to define thing')
    thingsid = a.fdu.define(thing_uuid, n1)

    input('Press enter to configure thing')
    a.fdu.configure(thingsid)

    input('Press enter to run thing')
    a.fdu.start(thingsid)

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))
    input('Press enter to stop')
    a.fdu.stop(cloudsid)
    a.fdu.stop(edgesid)
    a.fdu.stop(thingsid)

    input('Press enter to clean')
    a.fdu.clean(cloudsid)
    a.fdu.clean(edgesid)
    a.fdu.clean(thingsid)

    input('Press enter to undefine')
    a.fdu.undefine(cloudsid)
    a.fdu.undefine(edgesid)
    a.fdu.undefine(thingsid)

    input('Press enter to offload')
    a.fdu.offload(cloud_uuid)
    a.fdu.offload(edge_uuid)
    a.fdu.offload(thing_uuid)

    input("Press enter to remove network")
    a.network.remove_network(net1_uuid)
    a.network.remove_network(net2_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <path to net descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
