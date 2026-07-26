import os
import sys

import fastf1
import pandas as pd
from tableauhyperapi import Connection, CreateMode, HyperProcess, Inserter, SqlType, Telemetry, TableDefinition, TableName, TableDefinition, TableName
import tableauserverclient as TSC


CACHE_DIR = './data/cache'
DB_PATH = './data/f1_database.db'
HYPER_PATH = './data/f1_extract.hyper'


def ensure_dirs():
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs('./data', exist_ok=True)


def phase1_extract():
    fastf1.Cache.enable_cache(CACHE_DIR)
    schedule = fastf1.get_event_schedule(2026, include_testing=False)
    now = pd.Timestamp.now(tz='UTC').date()
    completed = schedule[schedule['EventDate'].dt.date <= now]
    if completed.empty:
        print('No completed rounds found for 2026.')
        sys.exit(0)
    rounds = sorted(completed['RoundNumber'].unique(), reverse=True)
    for round_number in rounds:
        print(f'Trying round {round_number}...')
        session = fastf1.get_session(2026, round_number, 'R')
        try:
            session.load(laps=True, telemetry=False, weather=False, messages=False)
            df = session.laps
        except Exception as exc:
            print(f'Failed to load round {round_number}: {exc}')
            continue
        if df is None or df.empty:
            print(f'No lap data available for round {round_number}.')
            continue
        print(f'Using round {round_number} ({session.event["EventName"]}).')
        return df
    print('No usable lap data found for any completed 2026 round.')
    sys.exit(0)


def phase2_sqlite(df):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('LapTimes', conn, if_exists='replace', index=False)
    conn.close()


def dtype_to_sqltype(dtype):
    if pd.api.types.is_float_dtype(dtype):
        return SqlType.double()
    if pd.api.types.is_integer_dtype(dtype):
        return SqlType.big_int()
    if pd.api.types.is_bool_dtype(dtype):
        return SqlType.bool()
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return SqlType.timestamp()
    return SqlType.text()


def phase3_hyper(df):
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_timedelta64_dtype(df[col].dtype):
            df[col] = df[col].astype(object).apply(lambda x: str(x) if pd.notna(x) else None)
        elif pd.api.types.is_datetime64_dtype(df[col].dtype):
            df[col] = df[col].dt.tz_localize(None) if getattr(df[col].dt, 'tz', None) is not None else df[col]
            df[col] = df[col].astype(object).apply(lambda x: x if pd.notna(x) else None)
        elif pd.api.types.is_float_dtype(df[col].dtype) or pd.api.types.is_integer_dtype(df[col].dtype):
            df[col] = df[col].astype(object).apply(lambda x: x if pd.notna(x) else None)
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, create_mode=CreateMode.CREATE_AND_REPLACE, database=HYPER_PATH) as connection:
            schema = 'Extract'
            table = TableName(schema, 'LapTimes')
            table_def = TableDefinition(table)
            for col in df.columns:
                table_def.add_column(str(col), dtype_to_sqltype(df[col].dtype))
            connection.catalog.create_schema(schema)
            connection.catalog.create_table(table_def)
            with Inserter(connection, table) as inserter:
                for row in df.itertuples(index=False, name=None):
                    inserter.add_row(row)
                inserter.execute()


def phase4_publish():
    server_url = os.environ.get('TABLEAU_SERVER_URL')
    site_id = os.environ.get('TABLEAU_SITE_ID')
    token_name = os.environ.get('TABLEAU_TOKEN_NAME')
    token_value = os.environ.get('TABLEAU_TOKEN_VALUE')

    if not all([server_url, site_id, token_name, token_value]):
        print('Missing Tableau environment variables.')
        sys.exit(1)

    auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id)
    with TSC.Server(server_url, use_server_version=True) as server:
        server.auth.sign_in(auth)
        try:
            project = next(p for p in TSC.Pager(server.projects) if p.name == 'Default')
            with open(HYPER_PATH, 'rb') as f:
                item = TSC.DatasourceItem(project.id, 'F1-Telemetry-Data')
                item = server.datasources.publish(item, f, TSC.PublishMode.Overwrite)
                print(f'Published datasource: {item.id}')
        finally:
            server.auth.sign_out()


def main():
    ensure_dirs()
    df = phase1_extract()
    phase2_sqlite(df)
    phase3_hyper(df)
    phase4_publish()
    print('Pipeline completed successfully.')


if __name__ == '__main__':
    main()