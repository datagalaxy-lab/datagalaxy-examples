from pyflink.table import EnvironmentSettings, TableEnvironment
import os
import json
from pyflink.table import EnvironmentSettings, TableEnvironment, DataTypes
from pyflink.table.expressions import col, call
from pyflink.table.udf import udtf
from pyflink.table import expressions as expr
from pyflink.table.window import Tumble
from pyflink.table import DataTypes
from pyflink.table.udf import udf
from pyflink.common import Configuration

import logging

# Set up logging for your PyFlink job
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Create a batch TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# Get the current working directory
CURRENT_DIR = os.getcwd()

# Define a list of JAR file names you want to add
jar_files = [
    "flink-sql-connector-postgres-cdc-3.3.0.jar",
    "flink-sql-connector-kafka-3.4.0-1.20.jar"
]

root_dir_list = __file__.split("/")[:-2]
root_dir = "/".join(root_dir_list)

# Build the list of JAR URLs by prepending 'file:///' to each file name
jar_urls = [f"file://{root_dir}/lib/{jar_file}" for jar_file in jar_files]

table_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    ";".join(jar_urls)
)

config = Configuration()
config.set_string("parallelism.default", "2")
table_env.get_config().add_configuration(config)
# Définition de la table source PostgreSQL via CDC
table_env.execute_sql("""
        CREATE TABLE catalog_item (
            id INT,
            name STRING,
            description STRING,
            category_id INT,
            last_updated TIMESTAMP(3),
            db_name STRING METADATA FROM 'database_name' VIRTUAL,
            schema_name STRING METADATA FROM 'schema_name' VIRTUAL,
            table_name STRING METADATA FROM 'table_name' VIRTUAL,
            op_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
            row_kind STRING METADATA FROM 'row_kind' VIRTUAL,
            PRIMARY KEY (id) NOT ENFORCED
        ) WITH (
            'connector' = 'postgres-cdc',
            'hostname' = 'db.data-catalog-app.svc.cluster.local',
            'port' = '5432',
            'username' = 'postgres',
            'password' = 'postgres',
            'database-name' = 'catalogdb',
            'schema-name' = 'public',
            'table-name' = 'catalog_item',
            'slot.name' = 'data_catalog_to_es_slot',
            'decoding.plugin.name' = 'pgoutput',
            'changelog-mode' = 'upsert'
        );
    """)

table_env.execute_sql("""
        CREATE TABLE category (
            id INT,
            name STRING,
            description STRING,
            db_name STRING METADATA FROM 'database_name' VIRTUAL,
            schema_name STRING METADATA FROM 'schema_name' VIRTUAL,
            table_name STRING METADATA FROM 'table_name' VIRTUAL,
            operation_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
            row_kind STRING METADATA FROM 'row_kind' VIRTUAL,
            PRIMARY KEY (id) NOT ENFORCED
        ) WITH (
            'connector' = 'postgres-cdc',
            'hostname' = 'db.data-catalog-app.svc.cluster.local',
            'port' = '5432',
            'username' = 'postgres',
            'password' = 'postgres',
            'database-name' = 'catalogdb',
            'schema-name' = 'public',
            'table-name' = 'category',
            'slot.name' = 'category_to_es_slot',
            'decoding.plugin.name' = 'pgoutput',
            'changelog-mode' = 'upsert'
        );
    """)


sink_ddl="""
    CREATE TABLE es_sink (
        id INT,
        name STRING,
        description STRING,
        category_id INT,
        category_name STRING,
        category_description STRING,
        db_name STRING,
        schema_name STRING,
        table_name STRING,
        op_ts TIMESTAMP_LTZ(3),
        PRIMARY KEY (id,table_name,schema_name,db_name ) NOT ENFORCED
    ) WITH (
        'connector' = 'upsert-kafka',
        'topic' = 'catalog-enriched',
        'properties.bootstrap.servers' = 'redpanda.default.svc.cluster.local:9093',
        'key.format' = 'json',
        'value.format' = 'json'
    )
"""



# sink_ddl = """
#   CREATE TABLE es_sink (
#     id INT,
#     data MAP<STRING, STRING>,
#     db_name STRING,
#     schema_name STRING,
#     table_name STRING,
#     op_ts TIMESTAMP_LTZ(3),
#     env STRING,
#     PRIMARY KEY (id, db_name, schema_name, table_name) NOT ENFORCED
#   ) WITH (
#       'connector' = 'upsert-kafka',
#       'topic' = 'catalog-enriched',
#       'properties.bootstrap.servers' = 'redpanda.default.svc.cluster.local:9093',
#       'key.format' = 'json',
#       'value.format' = 'json'
#   );
# """

table_env.execute_sql(sink_ddl)

statement_set = table_env.create_statement_set()

insert_statement = """
    INSERT INTO es_sink
    SELECT
        ci.id,
        ci.name,
        ci.description,
        ci.category_id,
        c.name AS category_name,
        c.description AS category_description,
        ci.db_name,
        ci.schema_name,
        ci.table_name,
        ci.op_ts
    FROM catalog_item AS ci
    JOIN category AS c
      ON ci.category_id  = c.id
"""




# statement_set.add_insert_sql("""
#     INSERT INTO es_sink
#     SELECT 
#         id,
#         MAP[
#             'name', name, 
#             'description', description, 
#             'category_id', category_id,
#             'last_updated', CAST(last_updated AS STRING)
#         ] AS data,
#         db_name,
#         schema_name,                                           
#         table_name,
#         op_ts,                   
#         'dev' AS env
#     FROM catalog_item;
# """)
statement_set.add_insert_sql(insert_statement)
statement_set.execute()