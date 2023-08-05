import json

from grebble_flow.grpc.generated.internal.v1.app_pb2 import (
    AppInfoExternalResponse,
    ProcessorExternalInfo,
)
from grebble_flow.grpc.generated.internal.v1.app_pb2_grpc import ExternalAppServicer
from grebble_flow.managment.info import generate_package_info


class AppService(ExternalAppServicer):
    def __init__(self, *args, **kwargs):
        pass

    def AppInfo(self, request, context):
        info = generate_package_info()

        result = AppInfoExternalResponse()
        result.processors.extend(
            [
                ProcessorExternalInfo(
                    name=processor["name"],
                    attributeSchema=json.dumps(processor["attributes_schema"])
                    if processor.get("attributes_schema")
                    else "",
                )
                for processor in info["processors"]
            ]
        )
        return result
