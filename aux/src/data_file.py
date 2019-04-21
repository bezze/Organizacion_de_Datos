import pandas as pd
import numpy as np
import pickle
import datetime


common_types_Ev_Ins = {

    'application_id': np.uint16,
    'attributed': np.bool_,
    'device_brand': np.float64,
    'device_countrycode': np.int64,
    'device_language': np.float64,
    'device_model': np.float64,
    'ip_address': np.int64,
    'ref_hash': np.int64,
    'ref_type': np.int64,

    'user_agent': np.object,
    'session_user_agent': np.object,
    'kind': np.object,

 # 'wifi': np.bool_,

}



class DataFile():

    def __init__(self, df=None):
        """docstring for __init__"""
        self.df = df

    def save(self, name="save.pickle"):
        """docstring for save"""
        with open(name, "wb") as fdesc:
            pickle.dump(self.df, fdesc)

    @classmethod
    def load(cls, name=None, **kwargs):
        """docstring for save"""
        if name.endswith(".csv"):
            dataframe = pd.read_csv(name, **kwargs)
        elif name.endswith(".pickle"):
            with open(name, "rb") as fdesc:
                dataframe = pickle.load(fdesc)
        object_= cls()
        object_.df = dataframe
        return object_


class Auctions(DataFile):

    def __init__(self):
        """docstring for __init__"""
        super(Auctions).__init__()

    @classmethod
    def load(cls, name=None, **kwargs):

        DTYPES = {
            "country": np.uint8,
            "device_id": np.uint64,
            "platform": np.uint8,
            "ref_type_id": np.uint16,
            "source_id": np.uint16
        }

        converters = {
            "auction_type_id": lambda x: np.uint8(0) if x == '' else x,
            "date": lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"), }

        kwargs = dict(
            **kwargs,
            dtype=DTYPES,
            converters=converters,
            low_memory=False,
        )

        return super().load(name=name, **kwargs)


class Events(DataFile):
    def __init__(self):
        """docstring for __init__"""
        super().__init__()

    @classmethod
    def load(cls, name=None, **kwargs):

        DTYPES = dict(
            **common_types_Ev_Ins,
            # {'device_os', 'device_city', 'device_os_version', 'carrier', 'event_id', 'date', 'connection_type'}
        )

        converters = {
            "date": lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"),
    # 'event_uuid': str,
    # 'kind': str,
    # 'session_user_agent': str,
    # 'trans_id': str,
    # 'user_agent': str,

        }

        kwargs = dict(
            **kwargs,
            dtype=DTYPES,
            converters=converters,
            low_memory=False,
        )

        return super().load(name=name, **kwargs)


class Installs(DataFile):
    def __init__(self):
        """docstring for __init__"""
        super().__init__()

    @classmethod
    def load(cls, name=None, **kwargs):

        DTYPES = dict(
            **common_types_Ev_Ins,
            implicit=np.bool_,
            # {'implicit', 'created'}
        )

        def strnanparser(x):
            """docstring for strnanparser"""
            return "NaN" if x=='' else str(x)

        converters = {
            "created": lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"),
            # "session_user_agent": strnanparser,
        }

        kwargs = dict(
            **kwargs,
            usecols=lambda x: x not in ["click_hash"],
            dtype=DTYPES,
            converters=converters,
            low_memory=False,
        )

        return super().load(name=name, **kwargs)
