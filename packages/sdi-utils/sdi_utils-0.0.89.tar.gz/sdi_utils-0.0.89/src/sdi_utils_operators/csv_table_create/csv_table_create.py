import io
import subprocess
import os
import pandas as pd

import sdi_utils.gensolution as gs
import deprecated.set_logging as slog
import sdi_utils.textfield_parser as tfp

try:
    api
except NameError:
    class api:
        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            if port == outports[1]['name']:
                print(msg.attributes)
                print(msg.body)

        class config:
            ## Meta data
            config_params = dict()
            tags = {'sdi_utils': '', 'pandas':'','numpy36':''}
            version = "0.0.1"
            operator_description = "csv to table create"
            operator_name = 'csv_table_create'
            operator_description_long = "csv to table create"
            add_readme = dict()
            debug_mode = True
            config_params['debug_mode'] = {'title': 'Debug mode',
                                           'description': 'Sending debug level information to log port',
                                           'type': 'boolean'}

            table_name = 'table_name'
            config_params['table_name'] = {'title': 'Table Name',
                                           'description': 'Table name.',
                                           'type': 'string'}



def process(msg):
    att = dict(msg.attributes)

    att['operator'] = 'csv_table_create'
    logger, log_stream = slog.set_logging(att['operator'], loglevel=api.config.debug_mode)

    logger.debug('Attributes: {}'.format(str(att)))

    csv_io = io.BytesIO(msg.body)

    df = pd.read_csv(csv_io)

    table_name = api.config.table_name
    if not tfp.read_value(table_name) :
        table_name = os.path.basename(att['file']['path']).split('.')[0]

    att["table"] = {"name": table_name, "version": 1, "columns": list()}

    for col in df.columns :
        col_dtype = str(df[col].dtype)
        if "int" in col_dtype:
            att["table"]["columns"].append({"name": col, "type":{"hana":"BIGINT"}})
        elif "float" in  col_dtype :
            att["table"]["columns"].append({"name": col, "type": {"hana": "DOUBLE"}})
        elif 'object' in col_dtype  :
            max = df[col].str.len().max()
            att["table"]["columns"].append({"name": col, "size": max + 1,"type": {"hana": "NVARCHAR"}})
        else:
            raise ValueError('Unknown data type: {}'.format(col_dtype))

    sql = "CREATE COLUMN TABLE {table} (".format(table=table_name)
    for col in att['table']['columns'] :
        if col['type']['hana'] == 'NVARCHAR' :
            sql += "\n\t{col_name} {col_type} ({size}),".format(col_name=col['name'], col_type=col['type']['hana'],size =col['size'])
        else :
            sql += "\n\t{col_name} {col_type},".format(col_name = col['name'],col_type = col['type']['hana'])
    sql = sql[:-1] + "\n)"

    api.send(outports[1]['name'], api.Message(attributes=att,body=sql))
    api.send(outports[0]['name'], log_stream.getvalue())


inports = [{'name': 'stream', 'type': 'message.file', "description": "Input csv byte or string"}]
outports = [{'name': 'log', 'type': 'string', "description": "Logging data"}, \
            {'name': 'sql', 'type': 'message.table', "description": "Output data as table"}]

#api.set_port_callback(inports[0]['name'], process)


def test_operator():

    csv = b'id,name,height,birthday\n0,"Albert",1.75,"1960-01-31"\n1,"Berta",1.68,"1965-03-22"\n2,"Claire",1.65,"1970-05-11"'

    csv = pd.read_csv('/Users/d051079/Downloads/car_sales.csv').to_csv(index=False).encode('utf-8')


    attributes = {'format': 'csv', "file": {'path': "/usr/data/friends.csv"}, 'message.lastBatch': True, \
                  'storage.fileIndex': 0, 'storage.fileCount': 1, 'process_list': []}
    msg = api.Message(attributes=attributes, body=csv)
    process(msg)


if __name__ == '__main__':
    test_operator()
    if True :
        gs.gensolution(os.path.realpath(__file__), api.config, inports, outports)
        solution_name = api.config.operator_name+'_'+api.config.version
        print('Solution name: {}'.format(solution_name))
        print('Current directory: {}'.format(os.getcwd()))
        subprocess.run(["vctl", "solution", "bundle", '/Users/d051079/OneDrive - SAP SE/GitHub/sdi_utils/solution/operators/sdi_utils_operators_0.0.1',\
                                  "-t", solution_name])
        subprocess.run(["mv", solution_name+'.zip', '../../../solution/operators'])
