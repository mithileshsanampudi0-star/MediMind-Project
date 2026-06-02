import os
import ssl

import certifi
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError
)

from config import Config


class MongoDB:
    """
    MongoDB Database Manager
    """

    _client = None
    _db = None

    @classmethod
    def initialize(cls):

        mongo_uri = Config.MONGO_URI

        if not mongo_uri:
            raise RuntimeError(
                "MongoDB connection failed: MONGO_URI is not configured."
            )

        tls_required = (
            mongo_uri.startswith("mongodb+srv://") or
            "tls=true" in mongo_uri.lower() or
            "ssl=true" in mongo_uri.lower()
        )

        base_options = {
            "serverSelectionTimeoutMS": 10000,
            "connectTimeoutMS": 10000,
            "socketTimeoutMS": 20000,
        }

        config_override_invalid_certs = (
            os.getenv("MONGO_TLS_ALLOW_INVALID_CERTS", "False").lower() == "true"
        )
        config_override_invalid_hostnames = (
            os.getenv("MONGO_TLS_ALLOW_INVALID_HOSTNAMES", "False").lower() == "true"
        )

        tls_configurations = []

        if config_override_invalid_certs or config_override_invalid_hostnames:
            opts = base_options.copy()
            if tls_required:
                opts["tls"] = True
            if config_override_invalid_certs:
                opts["tlsAllowInvalidCertificates"] = True
            if config_override_invalid_hostnames:
                opts["tlsAllowInvalidHostnames"] = True
            tls_configurations.append(("user-override", opts))
        else:
            if tls_required:
                opts = base_options.copy()
                opts["tls"] = True
                opts["tlsCAFile"] = certifi.where()
                tls_configurations.append(("strict-tls-with-ca", opts))

                opts_relaxed = base_options.copy()
                opts_relaxed["tls"] = True
                opts_relaxed["tlsAllowInvalidCertificates"] = True
                opts_relaxed["tlsAllowInvalidHostnames"] = True
                tls_configurations.append(("relaxed-tls-fallback", opts_relaxed))
            else:
                tls_configurations.append(("no-tls", base_options.copy()))

        last_error = None

        for config_name, client_options in tls_configurations:

            try:

                cls._client = MongoClient(
                    mongo_uri,
                    **client_options
                )

                cls._client.admin.command("ping")

                cls._db = cls._client[
                    Config.DATABASE_NAME
                ]

                if config_name != "strict-tls-with-ca":
                    print(
                        f"[MongoDB] Connected with {config_name} configuration"
                    )
                else:
                    print(
                        f"[MongoDB] Connected with strict TLS"
                    )

                print(
                    f"[MongoDB] Connected successfully to "
                    f"{Config.DATABASE_NAME}"
                )

                return

            except (
                ConnectionFailure,
                ServerSelectionTimeoutError
            ) as error:

                last_error = error

                if config_name == "strict-tls-with-ca":
                    print(
                        f"[MongoDB] Strict TLS failed, attempting fallback: {type(error).__name__}"
                    )

        if last_error:
            raise RuntimeError(
                f"MongoDB connection failed: {last_error}"
            )

    @classmethod
    def get_database(cls):

        if cls._db is None:
            cls.initialize()

        return cls._db

    # ==========================================
    # Compatibility Method
    # Fixes MongoDB.db() errors
    # ==========================================

    @classmethod
    def db(cls):

        return cls.get_database()

    @classmethod
    def close_connection(cls):

        if cls._client:

            cls._client.close()

            print(
                "[MongoDB] Connection closed"
            )

    # ==========================================
    # Collections
    # ==========================================

    @classmethod
    def users_collection(cls):

        return cls.get_database()[
            Config.USERS_COLLECTION
        ]

    @classmethod
    def symptoms_collection(cls):

        return cls.get_database()[
            Config.SYMPTOMS_COLLECTION
        ]

    @classmethod
    def reports_collection(cls):

        return cls.get_database()[
            Config.REPORTS_COLLECTION
        ]

    @classmethod
    def hospitals_collection(cls):

        return cls.get_database()[
            Config.HOSPITALS_COLLECTION
        ]

    @classmethod
    def analysis_collection(cls):

        return cls.get_database()[
            Config.ANALYSIS_COLLECTION
        ]


# ==================================================
# CREATE INDEXES
# ==================================================

def create_indexes():

    db = MongoDB.get_database()

    db[
        Config.SYMPTOMS_COLLECTION
    ].create_index(
        "created_at"
    )

    db[
        Config.REPORTS_COLLECTION
    ].create_index(
        "created_at"
    )

    db[
        Config.ANALYSIS_COLLECTION
    ].create_index(
        "created_at"
    )

    db[
        Config.HOSPITALS_COLLECTION
    ].create_index(
        "searched_at"
    )

    db[
        Config.ANALYSIS_COLLECTION
    ].create_index(
        "risk_level"
    )

    db[
        Config.ANALYSIS_COLLECTION
    ].create_index(
        "specialist"
    )

    db[
        Config.ANALYSIS_COLLECTION
    ].create_index(
        "emergency"
    )


# ==================================================
# HEALTH CHECK
# ==================================================

def database_health():

    try:

        MongoDB.get_database().command(
            "ping"
        )

        return {

            "status":
                "healthy",

            "database":
                Config.DATABASE_NAME

        }

    except Exception as error:

        return {

            "status":
                "unhealthy",

            "error":
                str(error)

        }