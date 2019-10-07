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


def main(ip,cloudfile,thingfile,netfile):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    cloud_d = json.loads(read_file(cloudfile))
    net_d = json.loads(read_file(netfile))

    cloud_uuid = cloud_d.get('uuid')
    net_uuid = net_d.get('uuid')

    input("Press enter to create network")
    a.network.add_network(net_d)

    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    #n1 = '16892ae12009411ab76998fdb7ccaf91'
    n1 = a.node.list()[0]
    #n1 = 'a2d358aaaf2b42cb8d23a89e88b97e5c'

    input('press enter to onboard descriptor')
    a.fdu.onboard(cloud_d)

    input('Press enter to define')
    cloudsid = a.fdu.define(cloud_uuid, n1)

    input('Press enter to configure')
    a.fdu.configure(cloudsid)

    input('Press enter to run')
    a.fdu.start(cloudsid)

    time.sleep(10) # 10 seconds to be sure monitoring has updated network information
    cloud_address = a.fdu.instance_info(cloudsid)['hypervisor_info']['network']['eth0']['addresses'][0]['address']

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))

    thing_d = json.loads(read_file(thingfile))
    thing_d['configuration']['script'] = "#cloud-config\nruncmd:\n  - [ sh, -xc, 'python3 -u /home/ubuntu/code/client.py http://" + cloud_address + ":5000 > /home/ubuntu/log.txt' ]"
    thing_uuid = thing_d.get('uuid')

    input('press enter to onboard descriptor')
    a.fdu.onboard(thing_d)

    input('Press enter to define')
    thingsid = a.fdu.define(thing_uuid, n1)

    input('Press enter to configure')
    a.fdu.configure(thingsid)

    input('Press enter to run')
    a.fdu.start(thingsid)

    input('Press enter to stop')
    a.fdu.stop(cloudsid)
    a.fdu.stop(thingsid)

    input('Press enter to clean')
    a.fdu.clean(cloudsid)
    a.fdu.clean(thingsid)

    input('Press enter to undefine')
    a.fdu.undefine(cloudsid)
    a.fdu.undefine(thingsid)

    input('Press enter to offload')
    a.fdu.offload(cloud_uuid)
    a.fdu.offload(thing_uuid)

    input("Press enter to remove network")
    a.network.remove_network(net_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('[Usage] {} <yaks ip:port> <path to fdu descriptor> <path to net descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
