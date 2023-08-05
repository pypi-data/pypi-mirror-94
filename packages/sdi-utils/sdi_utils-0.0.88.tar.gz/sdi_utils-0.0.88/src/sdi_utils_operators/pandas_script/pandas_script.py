

import pandas as pd
import subprocess
import io
import os

try:
    api
except NameError:

    class api:

        queue = list()
        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            if port == outports[0]['name']:
                api.queue.append(msg)

        class config:
            ## Meta data
            config_params = dict()
            version = "0.0.17"
            tags = {'pandas': ''}
            operator_name = 'pandas_script'
            operator_description = "Pandas Script"
            operator_description_long = "Creating a DataFrame with csv-data passed through inport."
            add_readme = dict()
            add_readme[
                "References"] = "[pandas doc: read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)"


def process(msg):

    attributes = dict(msg.attributes)
    csv_io = io.BytesIO(msg.body)
    df = pd.read_csv(csv_io)
    data_str = df.to_csv(sep=',', index=False)
    msg = api.Message(attributes=attributes,body=data_str)
    api.send(outports[0]['name'],msg)


inports = [{'name': 'csv', 'type': 'message.file',"description":"Input csv (byte)"}]
outports = [{'name': 'csv', 'type': 'message.file',"description":"Output csv (string)"}]


#api.set_port_callback(inports[0]['name'], process)

def test_operator():

    fname = '/Users/Shared/data/TechEd2020/input_product_ranks/product_ranks.csv'
    attributes = {'format': 'csv', "storage.filename": fname}
    csv = open(fname, mode='rb').read()
    msg = api.Message(attributes=attributes, body=csv)

    process(msg)

    for q in api.queue:
        print(msg.body)

if __name__ == '__main__':
    test_operator()

    if True :
        subprocess.run(["rm", '-r',
                        '/Users/d051079/OneDrive - SAP SE/GitHub/sdi_utils/solution/operators/sdi_utils_operators_' + api.config.version])
        gs.gensolution(os.path.realpath(__file__), api.config, inports, outports)
        solution_name = api.config.operator_name + '_' + api.config.version
        subprocess.run(["vctl", "solution", "bundle",
                        '/Users/d051079/OneDrive - SAP SE/GitHub/sdi_utils/solution/operators/sdi_utils_operators_' + api.config.version, \
                        "-t", solution_name])
        subprocess.run(["mv", solution_name + '.zip', '../../../solution/operators'])

