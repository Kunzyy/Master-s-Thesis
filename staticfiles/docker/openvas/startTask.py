import json
import sys
import os

import gvm.xml
from gvm.connections import TLSConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform

task_name = sys.argv[1]
target_name = sys.argv[2]
target_hosts = sys.argv[3]

username = 'admin'
password = 'cyber2023'
hostname = '0.0.0.0'


def get_scanner(gmp, name_scanner):
    res = gmp.get_scanners()

    for i, scanner in enumerate(res.xpath("scanner")):
        scanner_id = scanner.xpath("@id")[0]
        name = scanner.xpath("name/text()")[0]

        if name == name_scanner:
            # print(f"Scanner = {name} (id: {scanner_id})")
            return scanner_id


def get_scan_config(gmp, name_scan_config):
    res = gmp.get_scan_configs()

    for i, conf in enumerate(res.xpath("config")):
        config_id = conf.xpath("@id")[0]
        # #print(gvm.xml.pretty_print(conf))
        name = conf.xpath("name/text()")[0]

        if name == name_scan_config:
            # print(f"Scan config = {name} (id: {config_id})")
            return config_id


def get_format_report(gmp, name_format):
    res = gmp.get_report_formats()

    for i, conf in enumerate(res.xpath("report_format")):
        config_id = conf.xpath("@id")[0]
        name = conf.xpath("name/text()")[0]

        if name == name_format:
            # print(f"Report format = {name} (id: {config_id})")
            return config_id


def getOpenvasTaskStatus(task_id, gmp):
    task = gmp.get_task(task_id).xpath("task")
    task_status = task[0].xpath("status/text()")[0]
    return task_status


try:
    connection = TLSConnection(hostname=hostname)
    transform = EtreeCheckCommandTransform()

    with Gmp(connection, transform=transform) as gmp:
        gmp.authenticate(username, password)
        # print(gvm.xml.pretty_print(gmp.get_version()))
        # print(target_hosts)

        # Create a new target
        target_xml = gmp.create_target(
            name=target_name,
            hosts=[target_hosts],
            port_list_id='4a4717fe-57d2-11e1-9a26-406186ea4fc5',  # All IANA assigned TCP and UDP
        )

        target_id = target_xml.xpath("@id")[0]
        # print(f"Target id = {target_id}")

        # Create a new task
        task_xml = gmp.create_task(
            name=task_name,
            target_id=target_id,
            config_id=get_scan_config(gmp, 'Full and fast'),
            scanner_id=get_scanner(gmp, 'OpenVAS Default'),
        )

        # print(gvm.xml.pretty_print(target_xml))
        # print(gvm.xml.pretty_print(task_xml))
        task_id = task_xml.xpath("@id")[0]
        res = gmp.start_task(task_id)
        # print("Task started")
        report_id = res.xpath("report_id/text()")[0]

        os.mkdir('openvas/reports/' + report_id)

        json_output = {
            "task_name": task_name,
            "task_id": task_id,
            "target_id": target_id,
            "target_name": target_name,
            "target_hosts": target_hosts,
            "report_id": report_id,
        }

        with open(f'openvas/reports/{report_id}/{report_id}.json', 'w') as json_file:
            json.dump(json_output, json_file, indent=4)

        print(f"Report id: {report_id}")
        # print(get_format_report(gmp, 'XML'))

        while getOpenvasTaskStatus(task_id, gmp) != 'Done':
            pass

        rep = gmp.get_report(report_id, report_format_id=get_format_report(gmp, 'XML'))
        with open(f'openvas/reports/{report_id}/{report_id}.xml', 'w') as xml_file:
            xml_file.write(gvm.xml.pretty_print(rep))


except GvmError as e:
    print('An error occurred: {}'.format(e), file=sys.stderr)
