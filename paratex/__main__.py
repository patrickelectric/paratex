from datetime import date
from pathlib import Path

import pandas as pd

from .extractor import extract_attendance, Session, fetch_sessions_from_interval
from .join_parts import PARTITIONED_PATH, JOINED_PATH

def partitioned_process(sessions):
    PARTITIONED_PATH.mkdir(parents=True, exist_ok=True)
    for month in sessions:
        for session in month:
            session_id = session[0]
            session_data = extract_attendance(session_id)
            dataframe = session_as_dataframe(session_data)
            path = PARTITIONED_PATH / f'{dataframe.iloc[1, 3]}.csv'
            print('Saving', path, end='\r')
            dataframe.to_csv(path, index=False)


def joined_process(sessions, interval_begin, interval_end):
    JOINED_PATH.mkdir(parents=True, exist_ok=True)
    all_dfs = pd.DataFrame()

    for month in sessions:
        for session in month:
            session_id = session[0]
            session_data = extract_attendance(session_id)
            dataframe = session_as_dataframe(session_data)
            print(f'Building {dataframe.iloc[1, 3]}.csv', end='\r')
            all_dfs = pd.concat([all_dfs, dataframe])

    dataframe.to_csv(JOINED_PATH / f'{interval_begin}_to_{interval_end}.csv', index=False)


def main(partitioned_mode=False):
    '''partitioned_mode:
            True makes output splitted into a CSV file for each session,
            False joins sessions into a single CSV.'''
    interval_begin = '2011-10-15'
    interval_end = '2011-10-15'

    sessions = fetch_sessions_from_interval(date(2011, 10, 15), date(2019, 10, 15))

    if partitioned_mode:
        partitioned_process(sessions)
    else:
        joined_process(sessions, interval_begin, interval_end)


# Intended to be used later on the code. Will leave this here for utility
# purposes for now.
def session_as_dataframe(session: Session):
    observations = (
        (name, presence, justification, session.date)
        for name, (presence, justification) in session.attendance.items()
    )
    df = pd.DataFrame(observations)
    df = df.rename(
        {0: 'Nome', 1: 'Presenca', 2: 'Justificativa', 3: 'Data'},
        axis=1
    )
    return df


if __name__ == '__main__':
    main()
