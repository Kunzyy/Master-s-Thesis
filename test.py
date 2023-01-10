import xmltodict
import json

with open('openvas_scan_report.xml') as xml_file:
    json_data = xmltodict.parse(xml_file.read())

    results = json_data["report"]["report"]["results"]["result"]
    severity_threshold = 5.0

    json_output = {}
    index = 0
    for i in range(len(results)):
        result = results[i]
        if float(result["severity"]) >= severity_threshold:
            if not "NOCVE" == result["nvt"]["cve"]:
                name = result["name"]
                host = result["host"]["#text"]
                port = result["port"]

                print(name, host, port)

                tmp = {
                    "name": name,
                    "host": host,
                    "port": port,
                    "cve": result["nvt"]["cve"]
                }

                print(result['name'])
                json_output[index] = tmp
                index += 1

    print(json.dumps(json_output, indent=4))

    with open('openvas_scan_report.json', 'w') as json_file:
        json.dump(json_output, json_file, indent=4)







