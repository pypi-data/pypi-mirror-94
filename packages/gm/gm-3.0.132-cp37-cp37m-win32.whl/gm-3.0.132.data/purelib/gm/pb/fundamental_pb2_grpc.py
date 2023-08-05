# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from gm.pb import data_pb2 as gm_dot_pb_dot_data__pb2
from gm.pb import fundamental_pb2 as gm_dot_pb_dot_fundamental__pb2


class FundamentalServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFundamentals = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetFundamentals',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.FromString,
                )
        self.GetFundamentalsN = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetFundamentalsN',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsNReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.FromString,
                )
        self.GetInstrumentInfos = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetInstrumentInfos',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetInstrumentInfosReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.InstrumentInfos.FromString,
                )
        self.GetFuzzyMatchInstrumentInfos = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetFuzzyMatchInstrumentInfos',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetFuzzyMatchInstrumentInfosReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.InstrumentInfos.FromString,
                )
        self.GetInstruments = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetInstruments',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetInstrumentsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Instruments.FromString,
                )
        self.GetHistoryInstruments = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetHistoryInstruments',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetHistoryInstrumentsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Instruments.FromString,
                )
        self.GetConstituents = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetConstituents',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetConstituentsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Constituents.FromString,
                )
        self.GetSector = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetSector',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetSectorReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetSectorRsp.FromString,
                )
        self.GetIndustry = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetIndustry',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetIndustryReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetIndustryRsp.FromString,
                )
        self.GetConcept = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetConcept',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetConceptReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetConceptRsp.FromString,
                )
        self.GetTradingDates = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetTradingDates',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetTradingDatesReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetTradingDatesRsp.FromString,
                )
        self.GetPreviousTradingDate = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetPreviousTradingDate',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateRsp.FromString,
                )
        self.GetNextTradingDate = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetNextTradingDate',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateRsp.FromString,
                )
        self.GetTradingTimes = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetTradingTimes',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetTradingTimesReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetTradingTimesRsp.FromString,
                )
        self.GetDividends = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetDividends',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetDividendsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Dividends.FromString,
                )
        self.GetDividendsSnapshot = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetDividendsSnapshot',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetDividendsSnapshotReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Dividends.FromString,
                )
        self.GetContinuousContracts = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetContinuousContracts',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetContinuousContractsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.ContinuousContracts.FromString,
                )
        self.GetOptionsByUnderlying = channel.unary_unary(
                '/fundamental.api.FundamentalService/GetOptionsByUnderlying',
                request_serializer=gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingRsp.FromString,
                )


class FundamentalServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetFundamentals(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFundamentalsN(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInstrumentInfos(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFuzzyMatchInstrumentInfos(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInstruments(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryInstruments(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConstituents(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSector(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIndustry(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConcept(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTradingDates(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPreviousTradingDate(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNextTradingDate(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTradingTimes(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDividends(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDividendsSnapshot(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetContinuousContracts(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOptionsByUnderlying(self, request, context):
        """根据期权标的(如ETF50)查询其期权合约
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FundamentalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFundamentals': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFundamentals,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.SerializeToString,
            ),
            'GetFundamentalsN': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFundamentalsN,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsNReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.SerializeToString,
            ),
            'GetInstrumentInfos': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInstrumentInfos,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetInstrumentInfosReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.InstrumentInfos.SerializeToString,
            ),
            'GetFuzzyMatchInstrumentInfos': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFuzzyMatchInstrumentInfos,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetFuzzyMatchInstrumentInfosReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.InstrumentInfos.SerializeToString,
            ),
            'GetInstruments': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInstruments,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetInstrumentsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Instruments.SerializeToString,
            ),
            'GetHistoryInstruments': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryInstruments,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetHistoryInstrumentsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Instruments.SerializeToString,
            ),
            'GetConstituents': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConstituents,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetConstituentsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Constituents.SerializeToString,
            ),
            'GetSector': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSector,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetSectorReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetSectorRsp.SerializeToString,
            ),
            'GetIndustry': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIndustry,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetIndustryReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetIndustryRsp.SerializeToString,
            ),
            'GetConcept': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConcept,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetConceptReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetConceptRsp.SerializeToString,
            ),
            'GetTradingDates': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTradingDates,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetTradingDatesReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetTradingDatesRsp.SerializeToString,
            ),
            'GetPreviousTradingDate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPreviousTradingDate,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateRsp.SerializeToString,
            ),
            'GetNextTradingDate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNextTradingDate,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateRsp.SerializeToString,
            ),
            'GetTradingTimes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTradingTimes,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetTradingTimesReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetTradingTimesRsp.SerializeToString,
            ),
            'GetDividends': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDividends,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetDividendsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Dividends.SerializeToString,
            ),
            'GetDividendsSnapshot': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDividendsSnapshot,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetDividendsSnapshotReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Dividends.SerializeToString,
            ),
            'GetContinuousContracts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetContinuousContracts,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetContinuousContractsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.ContinuousContracts.SerializeToString,
            ),
            'GetOptionsByUnderlying': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOptionsByUnderlying,
                    request_deserializer=gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingReq.FromString,
                    response_serializer=gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fundamental.api.FundamentalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FundamentalService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetFundamentals(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetFundamentals',
            gm_dot_pb_dot_fundamental__pb2.GetFundamentalsReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFundamentalsN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetFundamentalsN',
            gm_dot_pb_dot_fundamental__pb2.GetFundamentalsNReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetFundamentalsRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetInstrumentInfos(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetInstrumentInfos',
            gm_dot_pb_dot_fundamental__pb2.GetInstrumentInfosReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.InstrumentInfos.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFuzzyMatchInstrumentInfos(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetFuzzyMatchInstrumentInfos',
            gm_dot_pb_dot_fundamental__pb2.GetFuzzyMatchInstrumentInfosReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.InstrumentInfos.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetInstruments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetInstruments',
            gm_dot_pb_dot_fundamental__pb2.GetInstrumentsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Instruments.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryInstruments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetHistoryInstruments',
            gm_dot_pb_dot_fundamental__pb2.GetHistoryInstrumentsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Instruments.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetConstituents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetConstituents',
            gm_dot_pb_dot_fundamental__pb2.GetConstituentsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Constituents.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetSector',
            gm_dot_pb_dot_fundamental__pb2.GetSectorReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetSectorRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIndustry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetIndustry',
            gm_dot_pb_dot_fundamental__pb2.GetIndustryReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetIndustryRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetConcept(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetConcept',
            gm_dot_pb_dot_fundamental__pb2.GetConceptReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetConceptRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTradingDates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetTradingDates',
            gm_dot_pb_dot_fundamental__pb2.GetTradingDatesReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetTradingDatesRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPreviousTradingDate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetPreviousTradingDate',
            gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetPreviousTradingDateRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNextTradingDate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetNextTradingDate',
            gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetNextTradingDateRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTradingTimes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetTradingTimes',
            gm_dot_pb_dot_fundamental__pb2.GetTradingTimesReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetTradingTimesRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDividends(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetDividends',
            gm_dot_pb_dot_fundamental__pb2.GetDividendsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Dividends.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDividendsSnapshot(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetDividendsSnapshot',
            gm_dot_pb_dot_fundamental__pb2.GetDividendsSnapshotReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Dividends.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetContinuousContracts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetContinuousContracts',
            gm_dot_pb_dot_fundamental__pb2.GetContinuousContractsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.ContinuousContracts.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOptionsByUnderlying(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fundamental.api.FundamentalService/GetOptionsByUnderlying',
            gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingReq.SerializeToString,
            gm_dot_pb_dot_fundamental__pb2.GetOptionsByUnderlyingRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
