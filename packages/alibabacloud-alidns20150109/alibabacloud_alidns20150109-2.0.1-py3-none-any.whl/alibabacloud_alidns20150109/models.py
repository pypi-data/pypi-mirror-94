# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict


class AddCustomLineRequestIpSegment(TeaModel):
    def __init__(
        self,
        end_ip: str = None,
        start_ip: str = None,
    ):
        self.end_ip = end_ip
        self.start_ip = start_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_ip is not None:
            result['EndIp'] = self.end_ip
        if self.start_ip is not None:
            result['StartIp'] = self.start_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndIp') is not None:
            self.end_ip = m.get('EndIp')
        if m.get('StartIp') is not None:
            self.start_ip = m.get('StartIp')
        return self


class AddCustomLineRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        line_name: str = None,
        ip_segment: List[AddCustomLineRequestIpSegment] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.line_name = line_name
        self.ip_segment = ip_segment

    def validate(self):
        if self.ip_segment:
            for k in self.ip_segment:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.line_name is not None:
            result['LineName'] = self.line_name
        result['IpSegment'] = []
        if self.ip_segment is not None:
            for k in self.ip_segment:
                result['IpSegment'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        self.ip_segment = []
        if m.get('IpSegment') is not None:
            for k in m.get('IpSegment'):
                temp_model = AddCustomLineRequestIpSegment()
                self.ip_segment.append(temp_model.from_map(k))
        return self


class AddCustomLineResponseBody(TeaModel):
    def __init__(
        self,
        line_id: int = None,
        request_id: str = None,
        line_code: str = None,
    ):
        self.line_id = line_id
        self.request_id = request_id
        self.line_code = line_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.line_id is not None:
            result['LineId'] = self.line_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LineId') is not None:
            self.line_id = m.get('LineId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        return self


class AddCustomLineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddCustomLineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddCustomLineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDnsCacheDomainRequestSourceDnsServer(TeaModel):
    def __init__(
        self,
        host: str = None,
        port: str = None,
    ):
        self.host = host
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.host is not None:
            result['Host'] = self.host
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Host') is not None:
            self.host = m.get('Host')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class AddDnsCacheDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        instance_id: str = None,
        cache_ttl_min: int = None,
        cache_ttl_max: int = None,
        source_protocol: str = None,
        source_edns: str = None,
        remark: str = None,
        source_dns_server: List[AddDnsCacheDomainRequestSourceDnsServer] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.instance_id = instance_id
        self.cache_ttl_min = cache_ttl_min
        self.cache_ttl_max = cache_ttl_max
        self.source_protocol = source_protocol
        self.source_edns = source_edns
        self.remark = remark
        self.source_dns_server = source_dns_server

    def validate(self):
        if self.source_dns_server:
            for k in self.source_dns_server:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.cache_ttl_min is not None:
            result['CacheTtlMin'] = self.cache_ttl_min
        if self.cache_ttl_max is not None:
            result['CacheTtlMax'] = self.cache_ttl_max
        if self.source_protocol is not None:
            result['SourceProtocol'] = self.source_protocol
        if self.source_edns is not None:
            result['SourceEdns'] = self.source_edns
        if self.remark is not None:
            result['Remark'] = self.remark
        result['SourceDnsServer'] = []
        if self.source_dns_server is not None:
            for k in self.source_dns_server:
                result['SourceDnsServer'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('CacheTtlMin') is not None:
            self.cache_ttl_min = m.get('CacheTtlMin')
        if m.get('CacheTtlMax') is not None:
            self.cache_ttl_max = m.get('CacheTtlMax')
        if m.get('SourceProtocol') is not None:
            self.source_protocol = m.get('SourceProtocol')
        if m.get('SourceEdns') is not None:
            self.source_edns = m.get('SourceEdns')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        self.source_dns_server = []
        if m.get('SourceDnsServer') is not None:
            for k in m.get('SourceDnsServer'):
                temp_model = AddDnsCacheDomainRequestSourceDnsServer()
                self.source_dns_server.append(temp_model.from_map(k))
        return self


class AddDnsCacheDomainResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddDnsCacheDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDnsCacheDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDnsCacheDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDnsGtmAccessStrategyRequestDefaultAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class AddDnsGtmAccessStrategyRequestFailoverAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class AddDnsGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        strategy_name: str = None,
        lines: str = None,
        default_addr_pool_type: str = None,
        default_lba_strategy: str = None,
        default_min_available_addr_num: int = None,
        default_max_return_addr_num: int = None,
        default_latency_optimization: str = None,
        failover_addr_pool_type: str = None,
        failover_lba_strategy: str = None,
        failover_min_available_addr_num: int = None,
        failover_max_return_addr_num: int = None,
        failover_latency_optimization: str = None,
        strategy_mode: str = None,
        default_addr_pool: List[AddDnsGtmAccessStrategyRequestDefaultAddrPool] = None,
        failover_addr_pool: List[AddDnsGtmAccessStrategyRequestFailoverAddrPool] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.strategy_name = strategy_name
        self.lines = lines
        self.default_addr_pool_type = default_addr_pool_type
        self.default_lba_strategy = default_lba_strategy
        self.default_min_available_addr_num = default_min_available_addr_num
        self.default_max_return_addr_num = default_max_return_addr_num
        self.default_latency_optimization = default_latency_optimization
        self.failover_addr_pool_type = failover_addr_pool_type
        self.failover_lba_strategy = failover_lba_strategy
        self.failover_min_available_addr_num = failover_min_available_addr_num
        self.failover_max_return_addr_num = failover_max_return_addr_num
        self.failover_latency_optimization = failover_latency_optimization
        self.strategy_mode = strategy_mode
        self.default_addr_pool = default_addr_pool
        self.failover_addr_pool = failover_addr_pool

    def validate(self):
        if self.default_addr_pool:
            for k in self.default_addr_pool:
                if k:
                    k.validate()
        if self.failover_addr_pool:
            for k in self.failover_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.lines is not None:
            result['Lines'] = self.lines
        if self.default_addr_pool_type is not None:
            result['DefaultAddrPoolType'] = self.default_addr_pool_type
        if self.default_lba_strategy is not None:
            result['DefaultLbaStrategy'] = self.default_lba_strategy
        if self.default_min_available_addr_num is not None:
            result['DefaultMinAvailableAddrNum'] = self.default_min_available_addr_num
        if self.default_max_return_addr_num is not None:
            result['DefaultMaxReturnAddrNum'] = self.default_max_return_addr_num
        if self.default_latency_optimization is not None:
            result['DefaultLatencyOptimization'] = self.default_latency_optimization
        if self.failover_addr_pool_type is not None:
            result['FailoverAddrPoolType'] = self.failover_addr_pool_type
        if self.failover_lba_strategy is not None:
            result['FailoverLbaStrategy'] = self.failover_lba_strategy
        if self.failover_min_available_addr_num is not None:
            result['FailoverMinAvailableAddrNum'] = self.failover_min_available_addr_num
        if self.failover_max_return_addr_num is not None:
            result['FailoverMaxReturnAddrNum'] = self.failover_max_return_addr_num
        if self.failover_latency_optimization is not None:
            result['FailoverLatencyOptimization'] = self.failover_latency_optimization
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        result['DefaultAddrPool'] = []
        if self.default_addr_pool is not None:
            for k in self.default_addr_pool:
                result['DefaultAddrPool'].append(k.to_map() if k else None)
        result['FailoverAddrPool'] = []
        if self.failover_addr_pool is not None:
            for k in self.failover_addr_pool:
                result['FailoverAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('Lines') is not None:
            self.lines = m.get('Lines')
        if m.get('DefaultAddrPoolType') is not None:
            self.default_addr_pool_type = m.get('DefaultAddrPoolType')
        if m.get('DefaultLbaStrategy') is not None:
            self.default_lba_strategy = m.get('DefaultLbaStrategy')
        if m.get('DefaultMinAvailableAddrNum') is not None:
            self.default_min_available_addr_num = m.get('DefaultMinAvailableAddrNum')
        if m.get('DefaultMaxReturnAddrNum') is not None:
            self.default_max_return_addr_num = m.get('DefaultMaxReturnAddrNum')
        if m.get('DefaultLatencyOptimization') is not None:
            self.default_latency_optimization = m.get('DefaultLatencyOptimization')
        if m.get('FailoverAddrPoolType') is not None:
            self.failover_addr_pool_type = m.get('FailoverAddrPoolType')
        if m.get('FailoverLbaStrategy') is not None:
            self.failover_lba_strategy = m.get('FailoverLbaStrategy')
        if m.get('FailoverMinAvailableAddrNum') is not None:
            self.failover_min_available_addr_num = m.get('FailoverMinAvailableAddrNum')
        if m.get('FailoverMaxReturnAddrNum') is not None:
            self.failover_max_return_addr_num = m.get('FailoverMaxReturnAddrNum')
        if m.get('FailoverLatencyOptimization') is not None:
            self.failover_latency_optimization = m.get('FailoverLatencyOptimization')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        self.default_addr_pool = []
        if m.get('DefaultAddrPool') is not None:
            for k in m.get('DefaultAddrPool'):
                temp_model = AddDnsGtmAccessStrategyRequestDefaultAddrPool()
                self.default_addr_pool.append(temp_model.from_map(k))
        self.failover_addr_pool = []
        if m.get('FailoverAddrPool') is not None:
            for k in m.get('FailoverAddrPool'):
                temp_model = AddDnsGtmAccessStrategyRequestFailoverAddrPool()
                self.failover_addr_pool.append(temp_model.from_map(k))
        return self


class AddDnsGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        strategy_id: str = None,
    ):
        self.request_id = request_id
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class AddDnsGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDnsGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDnsGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDnsGtmAddressPoolRequestAddr(TeaModel):
    def __init__(
        self,
        attribute_info: str = None,
        remark: str = None,
        lba_weight: int = None,
        addr: str = None,
        mode: str = None,
    ):
        self.attribute_info = attribute_info
        self.remark = remark
        self.lba_weight = lba_weight
        self.addr = addr
        self.mode = mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.attribute_info is not None:
            result['AttributeInfo'] = self.attribute_info
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.addr is not None:
            result['Addr'] = self.addr
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AttributeInfo') is not None:
            self.attribute_info = m.get('AttributeInfo')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Addr') is not None:
            self.addr = m.get('Addr')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class AddDnsGtmAddressPoolRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class AddDnsGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        name: str = None,
        type: str = None,
        lba_strategy: str = None,
        monitor_status: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        addr: List[AddDnsGtmAddressPoolRequestAddr] = None,
        isp_city_node: List[AddDnsGtmAddressPoolRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.name = name
        self.type = type
        self.lba_strategy = lba_strategy
        self.monitor_status = monitor_status
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.addr = addr
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = AddDnsGtmAddressPoolRequestAddr()
                self.addr.append(temp_model.from_map(k))
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = AddDnsGtmAddressPoolRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class AddDnsGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        addr_pool_id: str = None,
        monitor_config_id: str = None,
    ):
        self.request_id = request_id
        self.addr_pool_id = addr_pool_id
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class AddDnsGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDnsGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDnsGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDnsGtmMonitorRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class AddDnsGtmMonitorRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        isp_city_node: List[AddDnsGtmMonitorRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = AddDnsGtmMonitorRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class AddDnsGtmMonitorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        monitor_config_id: str = None,
    ):
        self.request_id = request_id
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class AddDnsGtmMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDnsGtmMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDnsGtmMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        domain_name: str = None,
        group_id: str = None,
        resource_group_id: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.domain_name = domain_name
        self.group_id = group_id
        self.resource_group_id = resource_group_id
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class AddDomainResponseBodyDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class AddDomainResponseBody(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        domain_id: str = None,
        request_id: str = None,
        domain_name: str = None,
        puny_code: str = None,
        dns_servers: AddDomainResponseBodyDnsServers = None,
        group_id: str = None,
    ):
        self.group_name = group_name
        self.domain_id = domain_id
        self.request_id = request_id
        self.domain_name = domain_name
        self.puny_code = puny_code
        self.dns_servers = dns_servers
        self.group_id = group_id

    def validate(self):
        if self.dns_servers:
            self.dns_servers.validate()

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.domain_id is not None:
            result['DomainId'] = self.domain_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.puny_code is not None:
            result['PunyCode'] = self.puny_code
        if self.dns_servers is not None:
            result['DnsServers'] = self.dns_servers.to_map()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('DomainId') is not None:
            self.domain_id = m.get('DomainId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PunyCode') is not None:
            self.puny_code = m.get('PunyCode')
        if m.get('DnsServers') is not None:
            temp_model = AddDomainResponseBodyDnsServers()
            self.dns_servers = temp_model.from_map(m['DnsServers'])
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class AddDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDomainBackupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        domain_name: str = None,
        period_type: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.domain_name = domain_name
        self.period_type = period_type
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.period_type is not None:
            result['PeriodType'] = self.period_type
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PeriodType') is not None:
            self.period_type = m.get('PeriodType')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class AddDomainBackupResponseBody(TeaModel):
    def __init__(
        self,
        period_type: str = None,
        request_id: str = None,
        domain_name: str = None,
    ):
        self.period_type = period_type
        self.request_id = request_id
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.period_type is not None:
            result['PeriodType'] = self.period_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PeriodType') is not None:
            self.period_type = m.get('PeriodType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class AddDomainBackupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDomainBackupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDomainBackupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDomainGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        group_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.group_name = group_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        return self


class AddDomainGroupResponseBody(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        request_id: str = None,
        group_id: str = None,
    ):
        self.group_name = group_name
        self.request_id = request_id
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class AddDomainGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDomainGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDomainGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddDomainRecordRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        rr: str = None,
        type: str = None,
        value: str = None,
        ttl: int = None,
        priority: int = None,
        line: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.rr = rr
        self.type = type
        self.value = value
        self.ttl = ttl
        self.priority = priority
        self.line = line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.rr is not None:
            result['RR'] = self.rr
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.ttl is not None:
            result['TTL'] = self.ttl
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.line is not None:
            result['Line'] = self.line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('TTL') is not None:
            self.ttl = m.get('TTL')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        return self


class AddDomainRecordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        record_id: str = None,
    ):
        self.request_id = request_id
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class AddDomainRecordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddDomainRecordResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddDomainRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        strategy_name: str = None,
        default_addr_pool_id: str = None,
        failover_addr_pool_id: str = None,
        access_lines: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.strategy_name = strategy_name
        self.default_addr_pool_id = default_addr_pool_id
        self.failover_addr_pool_id = failover_addr_pool_id
        self.access_lines = access_lines

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.default_addr_pool_id is not None:
            result['DefaultAddrPoolId'] = self.default_addr_pool_id
        if self.failover_addr_pool_id is not None:
            result['FailoverAddrPoolId'] = self.failover_addr_pool_id
        if self.access_lines is not None:
            result['AccessLines'] = self.access_lines
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('DefaultAddrPoolId') is not None:
            self.default_addr_pool_id = m.get('DefaultAddrPoolId')
        if m.get('FailoverAddrPoolId') is not None:
            self.failover_addr_pool_id = m.get('FailoverAddrPoolId')
        if m.get('AccessLines') is not None:
            self.access_lines = m.get('AccessLines')
        return self


class AddGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        strategy_id: str = None,
    ):
        self.request_id = request_id
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class AddGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddGtmAddressPoolRequestAddr(TeaModel):
    def __init__(
        self,
        value: str = None,
        lba_weight: int = None,
        mode: str = None,
    ):
        self.value = value
        self.lba_weight = lba_weight
        self.mode = mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class AddGtmAddressPoolRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class AddGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        name: str = None,
        type: str = None,
        min_available_addr_num: int = None,
        monitor_status: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        addr: List[AddGtmAddressPoolRequestAddr] = None,
        isp_city_node: List[AddGtmAddressPoolRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.name = name
        self.type = type
        self.min_available_addr_num = min_available_addr_num
        self.monitor_status = monitor_status
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.addr = addr
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.min_available_addr_num is not None:
            result['MinAvailableAddrNum'] = self.min_available_addr_num
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('MinAvailableAddrNum') is not None:
            self.min_available_addr_num = m.get('MinAvailableAddrNum')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = AddGtmAddressPoolRequestAddr()
                self.addr.append(temp_model.from_map(k))
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = AddGtmAddressPoolRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class AddGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        addr_pool_id: str = None,
        monitor_config_id: str = None,
    ):
        self.request_id = request_id
        self.addr_pool_id = addr_pool_id
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class AddGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddGtmMonitorRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class AddGtmMonitorRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        isp_city_node: List[AddGtmMonitorRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = AddGtmMonitorRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class AddGtmMonitorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        monitor_config_id: str = None,
    ):
        self.request_id = request_id
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class AddGtmMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddGtmMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddGtmMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        name: str = None,
        remark: str = None,
        fault_addr_pool: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.name = name
        self.remark = remark
        self.fault_addr_pool = fault_addr_pool

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.name is not None:
            result['Name'] = self.name
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.fault_addr_pool is not None:
            result['FaultAddrPool'] = self.fault_addr_pool
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('FaultAddrPool') is not None:
            self.fault_addr_pool = m.get('FaultAddrPool')
        return self


class AddGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        recovery_plan_id: str = None,
        request_id: str = None,
    ):
        self.recovery_plan_id = recovery_plan_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BindInstanceDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        domain_names: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.domain_names = domain_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.domain_names is not None:
            result['DomainNames'] = self.domain_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('DomainNames') is not None:
            self.domain_names = m.get('DomainNames')
        return self


class BindInstanceDomainsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        failed_count: int = None,
        success_count: int = None,
    ):
        self.request_id = request_id
        self.failed_count = failed_count
        self.success_count = success_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.failed_count is not None:
            result['FailedCount'] = self.failed_count
        if self.success_count is not None:
            result['SuccessCount'] = self.success_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailedCount') is not None:
            self.failed_count = m.get('FailedCount')
        if m.get('SuccessCount') is not None:
            self.success_count = m.get('SuccessCount')
        return self


class BindInstanceDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: BindInstanceDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = BindInstanceDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ChangeDomainGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        group_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class ChangeDomainGroupResponseBody(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        request_id: str = None,
        group_id: str = None,
    ):
        self.group_name = group_name
        self.request_id = request_id
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class ChangeDomainGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ChangeDomainGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ChangeDomainGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ChangeDomainOfDnsProductRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        new_domain: str = None,
        force: bool = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.new_domain = new_domain
        self.force = force

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.new_domain is not None:
            result['NewDomain'] = self.new_domain
        if self.force is not None:
            result['Force'] = self.force
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('NewDomain') is not None:
            self.new_domain = m.get('NewDomain')
        if m.get('Force') is not None:
            self.force = m.get('Force')
        return self


class ChangeDomainOfDnsProductResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        original_domain: str = None,
    ):
        self.request_id = request_id
        self.original_domain = original_domain

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.original_domain is not None:
            result['OriginalDomain'] = self.original_domain
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OriginalDomain') is not None:
            self.original_domain = m.get('OriginalDomain')
        return self


class ChangeDomainOfDnsProductResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ChangeDomainOfDnsProductResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ChangeDomainOfDnsProductResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CopyGtmConfigRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        source_id: str = None,
        target_id: str = None,
        copy_type: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.source_id = source_id
        self.target_id = target_id
        self.copy_type = copy_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.source_id is not None:
            result['SourceId'] = self.source_id
        if self.target_id is not None:
            result['TargetId'] = self.target_id
        if self.copy_type is not None:
            result['CopyType'] = self.copy_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('SourceId') is not None:
            self.source_id = m.get('SourceId')
        if m.get('TargetId') is not None:
            self.target_id = m.get('TargetId')
        if m.get('CopyType') is not None:
            self.copy_type = m.get('CopyType')
        return self


class CopyGtmConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CopyGtmConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CopyGtmConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CopyGtmConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteCustomLinesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        line_ids: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.line_ids = line_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.line_ids is not None:
            result['LineIds'] = self.line_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('LineIds') is not None:
            self.line_ids = m.get('LineIds')
        return self


class DeleteCustomLinesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteCustomLinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteCustomLinesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteCustomLinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDnsCacheDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DeleteDnsCacheDomainResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteDnsCacheDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDnsCacheDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDnsCacheDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDnsGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class DeleteDnsGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteDnsGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDnsGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDnsGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDnsGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        return self


class DeleteDnsGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteDnsGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDnsGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDnsGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DeleteDomainResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        domain_name: str = None,
    ):
        self.request_id = request_id
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DeleteDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDomainGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        group_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DeleteDomainGroupResponseBody(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        request_id: str = None,
    ):
        self.group_name = group_name
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteDomainGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDomainGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDomainGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDomainRecordRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class DeleteDomainRecordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        record_id: str = None,
    ):
        self.request_id = request_id
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class DeleteDomainRecordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDomainRecordResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDomainRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class DeleteGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        return self


class DeleteGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        recovery_plan_id: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.recovery_plan_id = recovery_plan_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        return self


class DeleteGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSubDomainRecordsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        rr: str = None,
        type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.rr = rr
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.rr is not None:
            result['RR'] = self.rr
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class DeleteSubDomainRecordsResponseBody(TeaModel):
    def __init__(
        self,
        rr: str = None,
        total_count: str = None,
        request_id: str = None,
    ):
        self.rr = rr
        self.total_count = total_count
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rr is not None:
            result['RR'] = self.rr
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteSubDomainRecordsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteSubDomainRecordsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteSubDomainRecordsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBatchResultCountRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        task_id: int = None,
        batch_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.task_id = task_id
        self.batch_type = batch_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.batch_type is not None:
            result['BatchType'] = self.batch_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('BatchType') is not None:
            self.batch_type = m.get('BatchType')
        return self


class DescribeBatchResultCountResponseBody(TeaModel):
    def __init__(
        self,
        status: int = None,
        total_count: int = None,
        task_id: int = None,
        request_id: str = None,
        failed_count: int = None,
        success_count: int = None,
        batch_type: str = None,
        reason: str = None,
    ):
        self.status = status
        self.total_count = total_count
        self.task_id = task_id
        self.request_id = request_id
        self.failed_count = failed_count
        self.success_count = success_count
        self.batch_type = batch_type
        self.reason = reason

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.failed_count is not None:
            result['FailedCount'] = self.failed_count
        if self.success_count is not None:
            result['SuccessCount'] = self.success_count
        if self.batch_type is not None:
            result['BatchType'] = self.batch_type
        if self.reason is not None:
            result['Reason'] = self.reason
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailedCount') is not None:
            self.failed_count = m.get('FailedCount')
        if m.get('SuccessCount') is not None:
            self.success_count = m.get('SuccessCount')
        if m.get('BatchType') is not None:
            self.batch_type = m.get('BatchType')
        if m.get('Reason') is not None:
            self.reason = m.get('Reason')
        return self


class DescribeBatchResultCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBatchResultCountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBatchResultCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBatchResultDetailRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        task_id: int = None,
        batch_type: str = None,
        status: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.task_id = task_id
        self.batch_type = batch_type
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.batch_type is not None:
            result['BatchType'] = self.batch_type
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('BatchType') is not None:
            self.batch_type = m.get('BatchType')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeBatchResultDetailResponseBodyBatchResultDetailsBatchResultDetail(TeaModel):
    def __init__(
        self,
        status: bool = None,
        type: str = None,
        domain: str = None,
        remark: str = None,
        record_id: str = None,
        rr: str = None,
        priority: str = None,
        rr_status: str = None,
        operate_date_str: str = None,
        new_value: str = None,
        value: str = None,
        ttl: str = None,
        batch_type: str = None,
        line: str = None,
        new_rr: str = None,
        reason: str = None,
    ):
        self.status = status
        self.type = type
        self.domain = domain
        self.remark = remark
        self.record_id = record_id
        self.rr = rr
        self.priority = priority
        self.rr_status = rr_status
        self.operate_date_str = operate_date_str
        self.new_value = new_value
        self.value = value
        self.ttl = ttl
        self.batch_type = batch_type
        self.line = line
        self.new_rr = new_rr
        self.reason = reason

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.type is not None:
            result['Type'] = self.type
        if self.domain is not None:
            result['Domain'] = self.domain
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.rr_status is not None:
            result['RrStatus'] = self.rr_status
        if self.operate_date_str is not None:
            result['OperateDateStr'] = self.operate_date_str
        if self.new_value is not None:
            result['NewValue'] = self.new_value
        if self.value is not None:
            result['Value'] = self.value
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.batch_type is not None:
            result['BatchType'] = self.batch_type
        if self.line is not None:
            result['Line'] = self.line
        if self.new_rr is not None:
            result['NewRr'] = self.new_rr
        if self.reason is not None:
            result['Reason'] = self.reason
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Domain') is not None:
            self.domain = m.get('Domain')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RrStatus') is not None:
            self.rr_status = m.get('RrStatus')
        if m.get('OperateDateStr') is not None:
            self.operate_date_str = m.get('OperateDateStr')
        if m.get('NewValue') is not None:
            self.new_value = m.get('NewValue')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('BatchType') is not None:
            self.batch_type = m.get('BatchType')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('NewRr') is not None:
            self.new_rr = m.get('NewRr')
        if m.get('Reason') is not None:
            self.reason = m.get('Reason')
        return self


class DescribeBatchResultDetailResponseBodyBatchResultDetails(TeaModel):
    def __init__(
        self,
        batch_result_detail: List[DescribeBatchResultDetailResponseBodyBatchResultDetailsBatchResultDetail] = None,
    ):
        self.batch_result_detail = batch_result_detail

    def validate(self):
        if self.batch_result_detail:
            for k in self.batch_result_detail:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['BatchResultDetail'] = []
        if self.batch_result_detail is not None:
            for k in self.batch_result_detail:
                result['BatchResultDetail'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.batch_result_detail = []
        if m.get('BatchResultDetail') is not None:
            for k in m.get('BatchResultDetail'):
                temp_model = DescribeBatchResultDetailResponseBodyBatchResultDetailsBatchResultDetail()
                self.batch_result_detail.append(temp_model.from_map(k))
        return self


class DescribeBatchResultDetailResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        batch_result_details: DescribeBatchResultDetailResponseBodyBatchResultDetails = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.batch_result_details = batch_result_details
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.batch_result_details:
            self.batch_result_details.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.batch_result_details is not None:
            result['BatchResultDetails'] = self.batch_result_details.to_map()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('BatchResultDetails') is not None:
            temp_model = DescribeBatchResultDetailResponseBodyBatchResultDetails()
            self.batch_result_details = temp_model.from_map(m['BatchResultDetails'])
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeBatchResultDetailResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBatchResultDetailResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBatchResultDetailResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomLineRequest(TeaModel):
    def __init__(
        self,
        line_id: int = None,
        lang: str = None,
        user_client_ip: str = None,
    ):
        self.line_id = line_id
        self.lang = lang
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.line_id is not None:
            result['LineId'] = self.line_id
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LineId') is not None:
            self.line_id = m.get('LineId')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeCustomLineResponseBodyIpSegmentList(TeaModel):
    def __init__(
        self,
        end_ip: str = None,
        start_ip: str = None,
    ):
        self.end_ip = end_ip
        self.start_ip = start_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_ip is not None:
            result['EndIp'] = self.end_ip
        if self.start_ip is not None:
            result['StartIp'] = self.start_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndIp') is not None:
            self.end_ip = m.get('EndIp')
        if m.get('StartIp') is not None:
            self.start_ip = m.get('StartIp')
        return self


class DescribeCustomLineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        ip_segment_list: List[DescribeCustomLineResponseBodyIpSegmentList] = None,
        domain_name: str = None,
        id: int = None,
        code: str = None,
        name: str = None,
    ):
        self.request_id = request_id
        self.ip_segment_list = ip_segment_list
        self.domain_name = domain_name
        self.id = id
        self.code = code
        self.name = name

    def validate(self):
        if self.ip_segment_list:
            for k in self.ip_segment_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['IpSegmentList'] = []
        if self.ip_segment_list is not None:
            for k in self.ip_segment_list:
                result['IpSegmentList'].append(k.to_map() if k else None)
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.id is not None:
            result['Id'] = self.id
        if self.code is not None:
            result['Code'] = self.code
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.ip_segment_list = []
        if m.get('IpSegmentList') is not None:
            for k in m.get('IpSegmentList'):
                temp_model = DescribeCustomLineResponseBodyIpSegmentList()
                self.ip_segment_list.append(temp_model.from_map(k))
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeCustomLineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomLineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomLineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomLinesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeCustomLinesResponseBodyCustomLines(TeaModel):
    def __init__(
        self,
        code: str = None,
        name: str = None,
        id: int = None,
    ):
        self.code = code
        self.name = name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeCustomLinesResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        custom_lines: List[DescribeCustomLinesResponseBodyCustomLines] = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.custom_lines = custom_lines
        self.total_items = total_items

    def validate(self):
        if self.custom_lines:
            for k in self.custom_lines:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        result['CustomLines'] = []
        if self.custom_lines is not None:
            for k in self.custom_lines:
                result['CustomLines'].append(k.to_map() if k else None)
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        self.custom_lines = []
        if m.get('CustomLines') is not None:
            for k in m.get('CustomLines'):
                temp_model = DescribeCustomLinesResponseBodyCustomLines()
                self.custom_lines.append(temp_model.from_map(k))
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeCustomLinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomLinesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomLinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsCacheDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        keyword: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.keyword = keyword
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDnsCacheDomainsResponseBodyDomainsSourceDnsServers(TeaModel):
    def __init__(
        self,
        host: str = None,
        port: str = None,
    ):
        self.host = host
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.host is not None:
            result['Host'] = self.host
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Host') is not None:
            self.host = m.get('Host')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class DescribeDnsCacheDomainsResponseBodyDomains(TeaModel):
    def __init__(
        self,
        source_protocol: str = None,
        update_time: str = None,
        remark: str = None,
        expire_time: str = None,
        create_time: str = None,
        instance_id: str = None,
        source_edns: str = None,
        domain_name: str = None,
        domain_id: str = None,
        update_timestamp: int = None,
        expire_timestamp: int = None,
        cache_ttl_max: int = None,
        cache_ttl_min: int = None,
        version_code: str = None,
        source_dns_servers: List[DescribeDnsCacheDomainsResponseBodyDomainsSourceDnsServers] = None,
        create_timestamp: int = None,
    ):
        self.source_protocol = source_protocol
        self.update_time = update_time
        self.remark = remark
        self.expire_time = expire_time
        self.create_time = create_time
        self.instance_id = instance_id
        self.source_edns = source_edns
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.update_timestamp = update_timestamp
        self.expire_timestamp = expire_timestamp
        self.cache_ttl_max = cache_ttl_max
        self.cache_ttl_min = cache_ttl_min
        self.version_code = version_code
        self.source_dns_servers = source_dns_servers
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.source_dns_servers:
            for k in self.source_dns_servers:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.source_protocol is not None:
            result['SourceProtocol'] = self.source_protocol
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.source_edns is not None:
            result['SourceEdns'] = self.source_edns
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.domain_id is not None:
            result['DomainId'] = self.domain_id
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.expire_timestamp is not None:
            result['ExpireTimestamp'] = self.expire_timestamp
        if self.cache_ttl_max is not None:
            result['CacheTtlMax'] = self.cache_ttl_max
        if self.cache_ttl_min is not None:
            result['CacheTtlMin'] = self.cache_ttl_min
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        result['SourceDnsServers'] = []
        if self.source_dns_servers is not None:
            for k in self.source_dns_servers:
                result['SourceDnsServers'].append(k.to_map() if k else None)
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SourceProtocol') is not None:
            self.source_protocol = m.get('SourceProtocol')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('SourceEdns') is not None:
            self.source_edns = m.get('SourceEdns')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('DomainId') is not None:
            self.domain_id = m.get('DomainId')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('ExpireTimestamp') is not None:
            self.expire_timestamp = m.get('ExpireTimestamp')
        if m.get('CacheTtlMax') is not None:
            self.cache_ttl_max = m.get('CacheTtlMax')
        if m.get('CacheTtlMin') is not None:
            self.cache_ttl_min = m.get('CacheTtlMin')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        self.source_dns_servers = []
        if m.get('SourceDnsServers') is not None:
            for k in m.get('SourceDnsServers'):
                temp_model = DescribeDnsCacheDomainsResponseBodyDomainsSourceDnsServers()
                self.source_dns_servers.append(temp_model.from_map(k))
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeDnsCacheDomainsResponseBody(TeaModel):
    def __init__(
        self,
        domains: List[DescribeDnsCacheDomainsResponseBodyDomains] = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.domains = domains
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.domains:
            for k in self.domains:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Domains'] = []
        if self.domains is not None:
            for k in self.domains:
                result['Domains'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domains = []
        if m.get('Domains') is not None:
            for k in m.get('Domains'):
                temp_model = DescribeDnsCacheDomainsResponseBodyDomains()
                self.domains.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeDnsCacheDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsCacheDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsCacheDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAccessStrategiesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        strategy_mode: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size
        self.strategy_mode = strategy_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPoolsEffectiveAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPools(TeaModel):
    def __init__(
        self,
        effective_addr_pool: List[DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPoolsEffectiveAddrPool] = None,
    ):
        self.effective_addr_pool = effective_addr_pool

    def validate(self):
        if self.effective_addr_pool:
            for k in self.effective_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['EffectiveAddrPool'] = []
        if self.effective_addr_pool is not None:
            for k in self.effective_addr_pool:
                result['EffectiveAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.effective_addr_pool = []
        if m.get('EffectiveAddrPool') is not None:
            for k in m.get('EffectiveAddrPool'):
                temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPoolsEffectiveAddrPool()
                self.effective_addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategy(TeaModel):
    def __init__(
        self,
        effective_lba_strategy: str = None,
        strategy_id: str = None,
        strategy_name: str = None,
        effective_addr_pool_group_type: str = None,
        create_time: str = None,
        effective_addr_pools: DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPools = None,
        create_timestamp: int = None,
        effective_addr_pool_type: str = None,
        lines: DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLines = None,
    ):
        self.effective_lba_strategy = effective_lba_strategy
        self.strategy_id = strategy_id
        self.strategy_name = strategy_name
        self.effective_addr_pool_group_type = effective_addr_pool_group_type
        self.create_time = create_time
        self.effective_addr_pools = effective_addr_pools
        self.create_timestamp = create_timestamp
        self.effective_addr_pool_type = effective_addr_pool_type
        self.lines = lines

    def validate(self):
        if self.effective_addr_pools:
            self.effective_addr_pools.validate()
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.effective_lba_strategy is not None:
            result['EffectiveLbaStrategy'] = self.effective_lba_strategy
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.effective_addr_pool_group_type is not None:
            result['EffectiveAddrPoolGroupType'] = self.effective_addr_pool_group_type
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.effective_addr_pools is not None:
            result['EffectiveAddrPools'] = self.effective_addr_pools.to_map()
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.effective_addr_pool_type is not None:
            result['EffectiveAddrPoolType'] = self.effective_addr_pool_type
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EffectiveLbaStrategy') is not None:
            self.effective_lba_strategy = m.get('EffectiveLbaStrategy')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('EffectiveAddrPoolGroupType') is not None:
            self.effective_addr_pool_group_type = m.get('EffectiveAddrPoolGroupType')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('EffectiveAddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyEffectiveAddrPools()
            self.effective_addr_pools = temp_model.from_map(m['EffectiveAddrPools'])
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('EffectiveAddrPoolType') is not None:
            self.effective_addr_pool_type = m.get('EffectiveAddrPoolType')
        if m.get('Lines') is not None:
            temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategyLines()
            self.lines = temp_model.from_map(m['Lines'])
        return self


class DescribeDnsGtmAccessStrategiesResponseBodyStrategies(TeaModel):
    def __init__(
        self,
        strategy: List[DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategy] = None,
    ):
        self.strategy = strategy

    def validate(self):
        if self.strategy:
            for k in self.strategy:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Strategy'] = []
        if self.strategy is not None:
            for k in self.strategy:
                result['Strategy'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.strategy = []
        if m.get('Strategy') is not None:
            for k in m.get('Strategy'):
                temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategiesStrategy()
                self.strategy.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategiesResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        strategies: DescribeDnsGtmAccessStrategiesResponseBodyStrategies = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.strategies = strategies
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.strategies:
            self.strategies.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.strategies is not None:
            result['Strategies'] = self.strategies.to_map()
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Strategies') is not None:
            temp_model = DescribeDnsGtmAccessStrategiesResponseBodyStrategies()
            self.strategies = temp_model.from_map(m['Strategies'])
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeDnsGtmAccessStrategiesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAccessStrategiesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAccessStrategiesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPoolsFailoverAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPools(TeaModel):
    def __init__(
        self,
        failover_addr_pool: List[DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPoolsFailoverAddrPool] = None,
    ):
        self.failover_addr_pool = failover_addr_pool

    def validate(self):
        if self.failover_addr_pool:
            for k in self.failover_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['FailoverAddrPool'] = []
        if self.failover_addr_pool is not None:
            for k in self.failover_addr_pool:
                result['FailoverAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.failover_addr_pool = []
        if m.get('FailoverAddrPool') is not None:
            for k in m.get('FailoverAddrPool'):
                temp_model = DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPoolsFailoverAddrPool()
                self.failover_addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPoolsDefaultAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPools(TeaModel):
    def __init__(
        self,
        default_addr_pool: List[DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPoolsDefaultAddrPool] = None,
    ):
        self.default_addr_pool = default_addr_pool

    def validate(self):
        if self.default_addr_pool:
            for k in self.default_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DefaultAddrPool'] = []
        if self.default_addr_pool is not None:
            for k in self.default_addr_pool:
                result['DefaultAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.default_addr_pool = []
        if m.get('DefaultAddrPool') is not None:
            for k in m.get('DefaultAddrPool'):
                temp_model = DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPoolsDefaultAddrPool()
                self.default_addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyResponseBodyLinesLine(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeDnsGtmAccessStrategyResponseBodyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeDnsGtmAccessStrategyResponseBodyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeDnsGtmAccessStrategyResponseBodyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        failover_min_available_addr_num: int = None,
        default_addr_pool_type: str = None,
        default_available_addr_num: int = None,
        strategy_id: str = None,
        failover_addr_pool_group_status: str = None,
        failover_available_addr_num: int = None,
        failover_lba_strategy: str = None,
        default_max_return_addr_num: int = None,
        strategy_mode: str = None,
        create_timestamp: int = None,
        default_lba_strategy: str = None,
        default_addr_pool_group_status: str = None,
        failover_addr_pool_type: str = None,
        request_id: str = None,
        instance_id: str = None,
        failover_addr_pools: DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPools = None,
        default_latency_optimization: str = None,
        effective_addr_pool_group_type: str = None,
        create_time: str = None,
        default_addr_pools: DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPools = None,
        default_min_available_addr_num: int = None,
        failover_latency_optimization: str = None,
        strategy_name: str = None,
        failover_max_return_addr_num: int = None,
        access_mode: str = None,
        lines: DescribeDnsGtmAccessStrategyResponseBodyLines = None,
    ):
        self.failover_min_available_addr_num = failover_min_available_addr_num
        self.default_addr_pool_type = default_addr_pool_type
        self.default_available_addr_num = default_available_addr_num
        self.strategy_id = strategy_id
        self.failover_addr_pool_group_status = failover_addr_pool_group_status
        self.failover_available_addr_num = failover_available_addr_num
        self.failover_lba_strategy = failover_lba_strategy
        self.default_max_return_addr_num = default_max_return_addr_num
        self.strategy_mode = strategy_mode
        self.create_timestamp = create_timestamp
        self.default_lba_strategy = default_lba_strategy
        self.default_addr_pool_group_status = default_addr_pool_group_status
        self.failover_addr_pool_type = failover_addr_pool_type
        self.request_id = request_id
        self.instance_id = instance_id
        self.failover_addr_pools = failover_addr_pools
        self.default_latency_optimization = default_latency_optimization
        self.effective_addr_pool_group_type = effective_addr_pool_group_type
        self.create_time = create_time
        self.default_addr_pools = default_addr_pools
        self.default_min_available_addr_num = default_min_available_addr_num
        self.failover_latency_optimization = failover_latency_optimization
        self.strategy_name = strategy_name
        self.failover_max_return_addr_num = failover_max_return_addr_num
        self.access_mode = access_mode
        self.lines = lines

    def validate(self):
        if self.failover_addr_pools:
            self.failover_addr_pools.validate()
        if self.default_addr_pools:
            self.default_addr_pools.validate()
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.failover_min_available_addr_num is not None:
            result['FailoverMinAvailableAddrNum'] = self.failover_min_available_addr_num
        if self.default_addr_pool_type is not None:
            result['DefaultAddrPoolType'] = self.default_addr_pool_type
        if self.default_available_addr_num is not None:
            result['DefaultAvailableAddrNum'] = self.default_available_addr_num
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.failover_addr_pool_group_status is not None:
            result['FailoverAddrPoolGroupStatus'] = self.failover_addr_pool_group_status
        if self.failover_available_addr_num is not None:
            result['FailoverAvailableAddrNum'] = self.failover_available_addr_num
        if self.failover_lba_strategy is not None:
            result['FailoverLbaStrategy'] = self.failover_lba_strategy
        if self.default_max_return_addr_num is not None:
            result['DefaultMaxReturnAddrNum'] = self.default_max_return_addr_num
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.default_lba_strategy is not None:
            result['DefaultLbaStrategy'] = self.default_lba_strategy
        if self.default_addr_pool_group_status is not None:
            result['DefaultAddrPoolGroupStatus'] = self.default_addr_pool_group_status
        if self.failover_addr_pool_type is not None:
            result['FailoverAddrPoolType'] = self.failover_addr_pool_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.failover_addr_pools is not None:
            result['FailoverAddrPools'] = self.failover_addr_pools.to_map()
        if self.default_latency_optimization is not None:
            result['DefaultLatencyOptimization'] = self.default_latency_optimization
        if self.effective_addr_pool_group_type is not None:
            result['EffectiveAddrPoolGroupType'] = self.effective_addr_pool_group_type
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.default_addr_pools is not None:
            result['DefaultAddrPools'] = self.default_addr_pools.to_map()
        if self.default_min_available_addr_num is not None:
            result['DefaultMinAvailableAddrNum'] = self.default_min_available_addr_num
        if self.failover_latency_optimization is not None:
            result['FailoverLatencyOptimization'] = self.failover_latency_optimization
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.failover_max_return_addr_num is not None:
            result['FailoverMaxReturnAddrNum'] = self.failover_max_return_addr_num
        if self.access_mode is not None:
            result['AccessMode'] = self.access_mode
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FailoverMinAvailableAddrNum') is not None:
            self.failover_min_available_addr_num = m.get('FailoverMinAvailableAddrNum')
        if m.get('DefaultAddrPoolType') is not None:
            self.default_addr_pool_type = m.get('DefaultAddrPoolType')
        if m.get('DefaultAvailableAddrNum') is not None:
            self.default_available_addr_num = m.get('DefaultAvailableAddrNum')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('FailoverAddrPoolGroupStatus') is not None:
            self.failover_addr_pool_group_status = m.get('FailoverAddrPoolGroupStatus')
        if m.get('FailoverAvailableAddrNum') is not None:
            self.failover_available_addr_num = m.get('FailoverAvailableAddrNum')
        if m.get('FailoverLbaStrategy') is not None:
            self.failover_lba_strategy = m.get('FailoverLbaStrategy')
        if m.get('DefaultMaxReturnAddrNum') is not None:
            self.default_max_return_addr_num = m.get('DefaultMaxReturnAddrNum')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('DefaultLbaStrategy') is not None:
            self.default_lba_strategy = m.get('DefaultLbaStrategy')
        if m.get('DefaultAddrPoolGroupStatus') is not None:
            self.default_addr_pool_group_status = m.get('DefaultAddrPoolGroupStatus')
        if m.get('FailoverAddrPoolType') is not None:
            self.failover_addr_pool_type = m.get('FailoverAddrPoolType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('FailoverAddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategyResponseBodyFailoverAddrPools()
            self.failover_addr_pools = temp_model.from_map(m['FailoverAddrPools'])
        if m.get('DefaultLatencyOptimization') is not None:
            self.default_latency_optimization = m.get('DefaultLatencyOptimization')
        if m.get('EffectiveAddrPoolGroupType') is not None:
            self.effective_addr_pool_group_type = m.get('EffectiveAddrPoolGroupType')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DefaultAddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategyResponseBodyDefaultAddrPools()
            self.default_addr_pools = temp_model.from_map(m['DefaultAddrPools'])
        if m.get('DefaultMinAvailableAddrNum') is not None:
            self.default_min_available_addr_num = m.get('DefaultMinAvailableAddrNum')
        if m.get('FailoverLatencyOptimization') is not None:
            self.failover_latency_optimization = m.get('FailoverLatencyOptimization')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('FailoverMaxReturnAddrNum') is not None:
            self.failover_max_return_addr_num = m.get('FailoverMaxReturnAddrNum')
        if m.get('AccessMode') is not None:
            self.access_mode = m.get('AccessMode')
        if m.get('Lines') is not None:
            temp_model = DescribeDnsGtmAccessStrategyResponseBodyLines()
            self.lines = temp_model.from_map(m['Lines'])
        return self


class DescribeDnsGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        strategy_mode: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.strategy_mode = strategy_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedDomainLines(TeaModel):
    def __init__(
        self,
        selected_domain_line: List[str] = None,
    ):
        self.selected_domain_line = selected_domain_line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.selected_domain_line is not None:
            result['SelectedDomainLine'] = self.selected_domain_line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SelectedDomainLine') is not None:
            self.selected_domain_line = m.get('SelectedDomainLine')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPoolsDomainAddrPool(TeaModel):
    def __init__(
        self,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPools(TeaModel):
    def __init__(
        self,
        domain_addr_pool: List[DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPoolsDomainAddrPool] = None,
    ):
        self.domain_addr_pool = domain_addr_pool

    def validate(self):
        if self.domain_addr_pool:
            for k in self.domain_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainAddrPool'] = []
        if self.domain_addr_pool is not None:
            for k in self.domain_addr_pool:
                result['DomainAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_addr_pool = []
        if m.get('DomainAddrPool') is not None:
            for k in m.get('DomainAddrPool'):
                temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPoolsDomainAddrPool()
                self.domain_addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPoolsIpv4AddrPool(TeaModel):
    def __init__(
        self,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPools(TeaModel):
    def __init__(
        self,
        ipv_4addr_pool: List[DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPoolsIpv4AddrPool] = None,
    ):
        self.ipv_4addr_pool = ipv_4addr_pool

    def validate(self):
        if self.ipv_4addr_pool:
            for k in self.ipv_4addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Ipv4AddrPool'] = []
        if self.ipv_4addr_pool is not None:
            for k in self.ipv_4addr_pool:
                result['Ipv4AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.ipv_4addr_pool = []
        if m.get('Ipv4AddrPool') is not None:
            for k in m.get('Ipv4AddrPool'):
                temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPoolsIpv4AddrPool()
                self.ipv_4addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv4Lines(TeaModel):
    def __init__(
        self,
        selected_ipv_4line: List[str] = None,
    ):
        self.selected_ipv_4line = selected_ipv_4line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.selected_ipv_4line is not None:
            result['SelectedIpv4Line'] = self.selected_ipv_4line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SelectedIpv4Line') is not None:
            self.selected_ipv_4line = m.get('SelectedIpv4Line')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPoolsIpv6AddrPool(TeaModel):
    def __init__(
        self,
        name: str = None,
        addr_count: int = None,
        id: str = None,
    ):
        self.name = name
        self.addr_count = addr_count
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPools(TeaModel):
    def __init__(
        self,
        ipv_6addr_pool: List[DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPoolsIpv6AddrPool] = None,
    ):
        self.ipv_6addr_pool = ipv_6addr_pool

    def validate(self):
        if self.ipv_6addr_pool:
            for k in self.ipv_6addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Ipv6AddrPool'] = []
        if self.ipv_6addr_pool is not None:
            for k in self.ipv_6addr_pool:
                result['Ipv6AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.ipv_6addr_pool = []
        if m.get('Ipv6AddrPool') is not None:
            for k in m.get('Ipv6AddrPool'):
                temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPoolsIpv6AddrPool()
                self.ipv_6addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv6Lines(TeaModel):
    def __init__(
        self,
        selected_ipv_6line: List[str] = None,
    ):
        self.selected_ipv_6line = selected_ipv_6line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.selected_ipv_6line is not None:
            result['SelectedIpv6Line'] = self.selected_ipv_6line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SelectedIpv6Line') is not None:
            self.selected_ipv_6line = m.get('SelectedIpv6Line')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLinesLine(TeaModel):
    def __init__(
        self,
        father_code: str = None,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.father_code = father_code
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        selected_domain_lines: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedDomainLines = None,
        domain_addr_pools: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPools = None,
        ipv_4addr_pools: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPools = None,
        request_id: str = None,
        selected_ipv_4lines: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv4Lines = None,
        ipv_6addr_pools: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPools = None,
        suggest_set_default_line: bool = None,
        selected_ipv_6lines: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv6Lines = None,
        lines: DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLines = None,
    ):
        self.selected_domain_lines = selected_domain_lines
        self.domain_addr_pools = domain_addr_pools
        self.ipv_4addr_pools = ipv_4addr_pools
        self.request_id = request_id
        self.selected_ipv_4lines = selected_ipv_4lines
        self.ipv_6addr_pools = ipv_6addr_pools
        self.suggest_set_default_line = suggest_set_default_line
        self.selected_ipv_6lines = selected_ipv_6lines
        self.lines = lines

    def validate(self):
        if self.selected_domain_lines:
            self.selected_domain_lines.validate()
        if self.domain_addr_pools:
            self.domain_addr_pools.validate()
        if self.ipv_4addr_pools:
            self.ipv_4addr_pools.validate()
        if self.selected_ipv_4lines:
            self.selected_ipv_4lines.validate()
        if self.ipv_6addr_pools:
            self.ipv_6addr_pools.validate()
        if self.selected_ipv_6lines:
            self.selected_ipv_6lines.validate()
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.selected_domain_lines is not None:
            result['SelectedDomainLines'] = self.selected_domain_lines.to_map()
        if self.domain_addr_pools is not None:
            result['DomainAddrPools'] = self.domain_addr_pools.to_map()
        if self.ipv_4addr_pools is not None:
            result['Ipv4AddrPools'] = self.ipv_4addr_pools.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.selected_ipv_4lines is not None:
            result['SelectedIpv4Lines'] = self.selected_ipv_4lines.to_map()
        if self.ipv_6addr_pools is not None:
            result['Ipv6AddrPools'] = self.ipv_6addr_pools.to_map()
        if self.suggest_set_default_line is not None:
            result['SuggestSetDefaultLine'] = self.suggest_set_default_line
        if self.selected_ipv_6lines is not None:
            result['SelectedIpv6Lines'] = self.selected_ipv_6lines.to_map()
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SelectedDomainLines') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedDomainLines()
            self.selected_domain_lines = temp_model.from_map(m['SelectedDomainLines'])
        if m.get('DomainAddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyDomainAddrPools()
            self.domain_addr_pools = temp_model.from_map(m['DomainAddrPools'])
        if m.get('Ipv4AddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv4AddrPools()
            self.ipv_4addr_pools = temp_model.from_map(m['Ipv4AddrPools'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SelectedIpv4Lines') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv4Lines()
            self.selected_ipv_4lines = temp_model.from_map(m['SelectedIpv4Lines'])
        if m.get('Ipv6AddrPools') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyIpv6AddrPools()
            self.ipv_6addr_pools = temp_model.from_map(m['Ipv6AddrPools'])
        if m.get('SuggestSetDefaultLine') is not None:
            self.suggest_set_default_line = m.get('SuggestSetDefaultLine')
        if m.get('SelectedIpv6Lines') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodySelectedIpv6Lines()
            self.selected_ipv_6lines = temp_model.from_map(m['SelectedIpv6Lines'])
        if m.get('Lines') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBodyLines()
            self.lines = temp_model.from_map(m['Lines'])
        return self


class DescribeDnsGtmAccessStrategyAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAccessStrategyAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAccessStrategyAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAddrAttributeInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        type: str = None,
        addrs: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.type = type
        self.addrs = addrs

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.type is not None:
            result['Type'] = self.type
        if self.addrs is not None:
            result['Addrs'] = self.addrs
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Addrs') is not None:
            self.addrs = m.get('Addrs')
        return self


class DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddrAttributeInfo(TeaModel):
    def __init__(
        self,
        father_code: str = None,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.father_code = father_code
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddr(TeaModel):
    def __init__(
        self,
        attribute_info: DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddrAttributeInfo = None,
        addr: str = None,
    ):
        self.attribute_info = attribute_info
        self.addr = addr

    def validate(self):
        if self.attribute_info:
            self.attribute_info.validate()

    def to_map(self):
        result = dict()
        if self.attribute_info is not None:
            result['AttributeInfo'] = self.attribute_info.to_map()
        if self.addr is not None:
            result['Addr'] = self.addr
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AttributeInfo') is not None:
            temp_model = DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddrAttributeInfo()
            self.attribute_info = temp_model.from_map(m['AttributeInfo'])
        if m.get('Addr') is not None:
            self.addr = m.get('Addr')
        return self


class DescribeDnsGtmAddrAttributeInfoResponseBodyAddr(TeaModel):
    def __init__(
        self,
        addr: List[DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddr] = None,
    ):
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = DescribeDnsGtmAddrAttributeInfoResponseBodyAddrAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAddrAttributeInfoResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        addr: DescribeDnsGtmAddrAttributeInfoResponseBodyAddr = None,
    ):
        self.request_id = request_id
        self.addr = addr

    def validate(self):
        if self.addr:
            self.addr.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.addr is not None:
            result['Addr'] = self.addr.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Addr') is not None:
            temp_model = DescribeDnsGtmAddrAttributeInfoResponseBodyAddr()
            self.addr = temp_model.from_map(m['Addr'])
        return self


class DescribeDnsGtmAddrAttributeInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAddrAttributeInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAddrAttributeInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAddressPoolAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfosAttributeInfo(TeaModel):
    def __init__(
        self,
        father_code: str = None,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.father_code = father_code
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfos(TeaModel):
    def __init__(
        self,
        attribute_info: List[DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfosAttributeInfo] = None,
    ):
        self.attribute_info = attribute_info

    def validate(self):
        if self.attribute_info:
            for k in self.attribute_info:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AttributeInfo'] = []
        if self.attribute_info is not None:
            for k in self.attribute_info:
                result['AttributeInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.attribute_info = []
        if m.get('AttributeInfo') is not None:
            for k in m.get('AttributeInfo'):
                temp_model = DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfosAttributeInfo()
                self.attribute_info.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmAddressPoolAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        attribute_infos: DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfos = None,
    ):
        self.request_id = request_id
        self.attribute_infos = attribute_infos

    def validate(self):
        if self.attribute_infos:
            self.attribute_infos.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.attribute_infos is not None:
            result['AttributeInfos'] = self.attribute_infos.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AttributeInfos') is not None:
            temp_model = DescribeDnsGtmAddressPoolAvailableConfigResponseBodyAttributeInfos()
            self.attribute_infos = temp_model.from_map(m['AttributeInfos'])
        return self


class DescribeDnsGtmAddressPoolAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAddressPoolAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAddressPoolAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmAvailableAlertGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeDnsGtmAvailableAlertGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        available_alert_group: str = None,
    ):
        self.request_id = request_id
        self.available_alert_group = available_alert_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.available_alert_group is not None:
            result['AvailableAlertGroup'] = self.available_alert_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AvailableAlertGroup') is not None:
            self.available_alert_group = m.get('AvailableAlertGroup')
        return self


class DescribeDnsGtmAvailableAlertGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmAvailableAlertGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmAvailableAlertGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstanceRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeDnsGtmInstanceResponseBodyConfigAlertConfigAlertConfig(TeaModel):
    def __init__(
        self,
        sms_notice: bool = None,
        notice_type: str = None,
        email_notice: bool = None,
    ):
        self.sms_notice = sms_notice
        self.notice_type = notice_type
        self.email_notice = email_notice

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.sms_notice is not None:
            result['SmsNotice'] = self.sms_notice
        if self.notice_type is not None:
            result['NoticeType'] = self.notice_type
        if self.email_notice is not None:
            result['EmailNotice'] = self.email_notice
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SmsNotice') is not None:
            self.sms_notice = m.get('SmsNotice')
        if m.get('NoticeType') is not None:
            self.notice_type = m.get('NoticeType')
        if m.get('EmailNotice') is not None:
            self.email_notice = m.get('EmailNotice')
        return self


class DescribeDnsGtmInstanceResponseBodyConfigAlertConfig(TeaModel):
    def __init__(
        self,
        alert_config: List[DescribeDnsGtmInstanceResponseBodyConfigAlertConfigAlertConfig] = None,
    ):
        self.alert_config = alert_config

    def validate(self):
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = DescribeDnsGtmInstanceResponseBodyConfigAlertConfigAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmInstanceResponseBodyConfig(TeaModel):
    def __init__(
        self,
        ttl: int = None,
        alert_group: str = None,
        cname_type: str = None,
        strategy_mode: str = None,
        instance_name: str = None,
        public_cname_mode: str = None,
        alert_config: DescribeDnsGtmInstanceResponseBodyConfigAlertConfig = None,
        public_user_domain_name: str = None,
        pubic_zone_name: str = None,
    ):
        self.ttl = ttl
        self.alert_group = alert_group
        self.cname_type = cname_type
        self.strategy_mode = strategy_mode
        self.instance_name = instance_name
        self.public_cname_mode = public_cname_mode
        self.alert_config = alert_config
        self.public_user_domain_name = public_user_domain_name
        self.pubic_zone_name = pubic_zone_name

    def validate(self):
        if self.alert_config:
            self.alert_config.validate()

    def to_map(self):
        result = dict()
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.cname_type is not None:
            result['CnameType'] = self.cname_type
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.public_cname_mode is not None:
            result['PublicCnameMode'] = self.public_cname_mode
        if self.alert_config is not None:
            result['AlertConfig'] = self.alert_config.to_map()
        if self.public_user_domain_name is not None:
            result['PublicUserDomainName'] = self.public_user_domain_name
        if self.pubic_zone_name is not None:
            result['PubicZoneName'] = self.pubic_zone_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('CnameType') is not None:
            self.cname_type = m.get('CnameType')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('PublicCnameMode') is not None:
            self.public_cname_mode = m.get('PublicCnameMode')
        if m.get('AlertConfig') is not None:
            temp_model = DescribeDnsGtmInstanceResponseBodyConfigAlertConfig()
            self.alert_config = temp_model.from_map(m['AlertConfig'])
        if m.get('PublicUserDomainName') is not None:
            self.public_user_domain_name = m.get('PublicUserDomainName')
        if m.get('PubicZoneName') is not None:
            self.pubic_zone_name = m.get('PubicZoneName')
        return self


class DescribeDnsGtmInstanceResponseBodyUsedQuota(TeaModel):
    def __init__(
        self,
        email_used_count: int = None,
        task_used_count: int = None,
        sms_used_count: int = None,
    ):
        self.email_used_count = email_used_count
        self.task_used_count = task_used_count
        self.sms_used_count = sms_used_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.email_used_count is not None:
            result['EmailUsedCount'] = self.email_used_count
        if self.task_used_count is not None:
            result['TaskUsedCount'] = self.task_used_count
        if self.sms_used_count is not None:
            result['SmsUsedCount'] = self.sms_used_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EmailUsedCount') is not None:
            self.email_used_count = m.get('EmailUsedCount')
        if m.get('TaskUsedCount') is not None:
            self.task_used_count = m.get('TaskUsedCount')
        if m.get('SmsUsedCount') is not None:
            self.sms_used_count = m.get('SmsUsedCount')
        return self


class DescribeDnsGtmInstanceResponseBody(TeaModel):
    def __init__(
        self,
        expire_timestamp: int = None,
        request_id: str = None,
        resource_group_id: str = None,
        instance_id: str = None,
        task_quota: int = None,
        config: DescribeDnsGtmInstanceResponseBodyConfig = None,
        create_time: str = None,
        sms_quota: int = None,
        version_code: str = None,
        payment_type: str = None,
        expire_time: str = None,
        create_timestamp: int = None,
        used_quota: DescribeDnsGtmInstanceResponseBodyUsedQuota = None,
    ):
        self.expire_timestamp = expire_timestamp
        self.request_id = request_id
        self.resource_group_id = resource_group_id
        self.instance_id = instance_id
        self.task_quota = task_quota
        self.config = config
        self.create_time = create_time
        self.sms_quota = sms_quota
        self.version_code = version_code
        self.payment_type = payment_type
        self.expire_time = expire_time
        self.create_timestamp = create_timestamp
        self.used_quota = used_quota

    def validate(self):
        if self.config:
            self.config.validate()
        if self.used_quota:
            self.used_quota.validate()

    def to_map(self):
        result = dict()
        if self.expire_timestamp is not None:
            result['ExpireTimestamp'] = self.expire_timestamp
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.task_quota is not None:
            result['TaskQuota'] = self.task_quota
        if self.config is not None:
            result['Config'] = self.config.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.sms_quota is not None:
            result['SmsQuota'] = self.sms_quota
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.used_quota is not None:
            result['UsedQuota'] = self.used_quota.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpireTimestamp') is not None:
            self.expire_timestamp = m.get('ExpireTimestamp')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('TaskQuota') is not None:
            self.task_quota = m.get('TaskQuota')
        if m.get('Config') is not None:
            temp_model = DescribeDnsGtmInstanceResponseBodyConfig()
            self.config = temp_model.from_map(m['Config'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('SmsQuota') is not None:
            self.sms_quota = m.get('SmsQuota')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('UsedQuota') is not None:
            temp_model = DescribeDnsGtmInstanceResponseBodyUsedQuota()
            self.used_quota = temp_model.from_map(m['UsedQuota'])
        return self


class DescribeDnsGtmInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstanceAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        return self


class DescribeDnsGtmInstanceAddressPoolResponseBodyAddrsAddr(TeaModel):
    def __init__(
        self,
        update_timestamp: int = None,
        attribute_info: str = None,
        update_time: str = None,
        alert_status: str = None,
        remark: str = None,
        lba_weight: int = None,
        addr: str = None,
        create_time: str = None,
        mode: str = None,
        create_timestamp: int = None,
    ):
        self.update_timestamp = update_timestamp
        self.attribute_info = attribute_info
        self.update_time = update_time
        self.alert_status = alert_status
        self.remark = remark
        self.lba_weight = lba_weight
        self.addr = addr
        self.create_time = create_time
        self.mode = mode
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.attribute_info is not None:
            result['AttributeInfo'] = self.attribute_info
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.alert_status is not None:
            result['AlertStatus'] = self.alert_status
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.addr is not None:
            result['Addr'] = self.addr
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('AttributeInfo') is not None:
            self.attribute_info = m.get('AttributeInfo')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('AlertStatus') is not None:
            self.alert_status = m.get('AlertStatus')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Addr') is not None:
            self.addr = m.get('Addr')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeDnsGtmInstanceAddressPoolResponseBodyAddrs(TeaModel):
    def __init__(
        self,
        addr: List[DescribeDnsGtmInstanceAddressPoolResponseBodyAddrsAddr] = None,
    ):
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = DescribeDnsGtmInstanceAddressPoolResponseBodyAddrsAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmInstanceAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        addrs: DescribeDnsGtmInstanceAddressPoolResponseBodyAddrs = None,
        request_id: str = None,
        lba_strategy: str = None,
        create_time: str = None,
        addr_count: int = None,
        name: str = None,
        type: str = None,
        update_time: str = None,
        addr_pool_id: str = None,
        update_timestamp: int = None,
        monitor_config_id: str = None,
        monitor_status: str = None,
        create_timestamp: int = None,
    ):
        self.addrs = addrs
        self.request_id = request_id
        self.lba_strategy = lba_strategy
        self.create_time = create_time
        self.addr_count = addr_count
        self.name = name
        self.type = type
        self.update_time = update_time
        self.addr_pool_id = addr_pool_id
        self.update_timestamp = update_timestamp
        self.monitor_config_id = monitor_config_id
        self.monitor_status = monitor_status
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.addrs:
            self.addrs.validate()

    def to_map(self):
        result = dict()
        if self.addrs is not None:
            result['Addrs'] = self.addrs.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Addrs') is not None:
            temp_model = DescribeDnsGtmInstanceAddressPoolResponseBodyAddrs()
            self.addrs = temp_model.from_map(m['Addrs'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeDnsGtmInstanceAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstanceAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstanceAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstanceAddressPoolsRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool(TeaModel):
    def __init__(
        self,
        type: str = None,
        update_timestamp: int = None,
        monitor_status: str = None,
        update_time: str = None,
        create_time: str = None,
        addr_pool_id: str = None,
        lba_strategy: str = None,
        name: str = None,
        addr_count: int = None,
        monitor_config_id: str = None,
        create_timestamp: int = None,
    ):
        self.type = type
        self.update_timestamp = update_timestamp
        self.monitor_status = monitor_status
        self.update_time = update_time
        self.create_time = create_time
        self.addr_pool_id = addr_pool_id
        self.lba_strategy = lba_strategy
        self.name = name
        self.addr_count = addr_count
        self.monitor_config_id = monitor_config_id
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPools(TeaModel):
    def __init__(
        self,
        addr_pool: List[DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool] = None,
    ):
        self.addr_pool = addr_pool

    def validate(self):
        if self.addr_pool:
            for k in self.addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AddrPool'] = []
        if self.addr_pool is not None:
            for k in self.addr_pool:
                result['AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr_pool = []
        if m.get('AddrPool') is not None:
            for k in m.get('AddrPool'):
                temp_model = DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool()
                self.addr_pool.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmInstanceAddressPoolsResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        addr_pools: DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPools = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.addr_pools = addr_pools

    def validate(self):
        if self.addr_pools:
            self.addr_pools.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.addr_pools is not None:
            result['AddrPools'] = self.addr_pools.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('AddrPools') is not None:
            temp_model = DescribeDnsGtmInstanceAddressPoolsResponseBodyAddrPools()
            self.addr_pools = temp_model.from_map(m['AddrPools'])
        return self


class DescribeDnsGtmInstanceAddressPoolsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstanceAddressPoolsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstanceAddressPoolsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstancesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        keyword: str = None,
        resource_group_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.keyword = keyword
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class DescribeDnsGtmInstancesResponseBodyGtmInstancesConfigAlertConfig(TeaModel):
    def __init__(
        self,
        sms_notice: str = None,
        notice_type: str = None,
        email_notice: str = None,
    ):
        self.sms_notice = sms_notice
        self.notice_type = notice_type
        self.email_notice = email_notice

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.sms_notice is not None:
            result['SmsNotice'] = self.sms_notice
        if self.notice_type is not None:
            result['NoticeType'] = self.notice_type
        if self.email_notice is not None:
            result['EmailNotice'] = self.email_notice
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SmsNotice') is not None:
            self.sms_notice = m.get('SmsNotice')
        if m.get('NoticeType') is not None:
            self.notice_type = m.get('NoticeType')
        if m.get('EmailNotice') is not None:
            self.email_notice = m.get('EmailNotice')
        return self


class DescribeDnsGtmInstancesResponseBodyGtmInstancesConfig(TeaModel):
    def __init__(
        self,
        ttl: int = None,
        alert_group: str = None,
        public_zone_name: str = None,
        cname_type: str = None,
        strategy_mode: str = None,
        instance_name: str = None,
        public_cname_mode: str = None,
        alert_config: List[DescribeDnsGtmInstancesResponseBodyGtmInstancesConfigAlertConfig] = None,
        public_user_domain_name: str = None,
    ):
        self.ttl = ttl
        self.alert_group = alert_group
        self.public_zone_name = public_zone_name
        self.cname_type = cname_type
        self.strategy_mode = strategy_mode
        self.instance_name = instance_name
        self.public_cname_mode = public_cname_mode
        self.alert_config = alert_config
        self.public_user_domain_name = public_user_domain_name

    def validate(self):
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.public_zone_name is not None:
            result['PublicZoneName'] = self.public_zone_name
        if self.cname_type is not None:
            result['CnameType'] = self.cname_type
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.public_cname_mode is not None:
            result['PublicCnameMode'] = self.public_cname_mode
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        if self.public_user_domain_name is not None:
            result['PublicUserDomainName'] = self.public_user_domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('PublicZoneName') is not None:
            self.public_zone_name = m.get('PublicZoneName')
        if m.get('CnameType') is not None:
            self.cname_type = m.get('CnameType')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('PublicCnameMode') is not None:
            self.public_cname_mode = m.get('PublicCnameMode')
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = DescribeDnsGtmInstancesResponseBodyGtmInstancesConfigAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        if m.get('PublicUserDomainName') is not None:
            self.public_user_domain_name = m.get('PublicUserDomainName')
        return self


class DescribeDnsGtmInstancesResponseBodyGtmInstancesUsedQuota(TeaModel):
    def __init__(
        self,
        email_used_count: int = None,
        task_used_count: int = None,
        sms_used_count: int = None,
    ):
        self.email_used_count = email_used_count
        self.task_used_count = task_used_count
        self.sms_used_count = sms_used_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.email_used_count is not None:
            result['EmailUsedCount'] = self.email_used_count
        if self.task_used_count is not None:
            result['TaskUsedCount'] = self.task_used_count
        if self.sms_used_count is not None:
            result['SmsUsedCount'] = self.sms_used_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EmailUsedCount') is not None:
            self.email_used_count = m.get('EmailUsedCount')
        if m.get('TaskUsedCount') is not None:
            self.task_used_count = m.get('TaskUsedCount')
        if m.get('SmsUsedCount') is not None:
            self.sms_used_count = m.get('SmsUsedCount')
        return self


class DescribeDnsGtmInstancesResponseBodyGtmInstances(TeaModel):
    def __init__(
        self,
        payment_type: str = None,
        expire_time: str = None,
        create_time: str = None,
        sms_quota: int = None,
        instance_id: str = None,
        config: DescribeDnsGtmInstancesResponseBodyGtmInstancesConfig = None,
        expire_timestamp: int = None,
        resource_group_id: str = None,
        version_code: str = None,
        used_quota: DescribeDnsGtmInstancesResponseBodyGtmInstancesUsedQuota = None,
        task_quota: int = None,
        create_timestamp: int = None,
    ):
        self.payment_type = payment_type
        self.expire_time = expire_time
        self.create_time = create_time
        self.sms_quota = sms_quota
        self.instance_id = instance_id
        self.config = config
        self.expire_timestamp = expire_timestamp
        self.resource_group_id = resource_group_id
        self.version_code = version_code
        self.used_quota = used_quota
        self.task_quota = task_quota
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.config:
            self.config.validate()
        if self.used_quota:
            self.used_quota.validate()

    def to_map(self):
        result = dict()
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.sms_quota is not None:
            result['SmsQuota'] = self.sms_quota
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.config is not None:
            result['Config'] = self.config.to_map()
        if self.expire_timestamp is not None:
            result['ExpireTimestamp'] = self.expire_timestamp
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.used_quota is not None:
            result['UsedQuota'] = self.used_quota.to_map()
        if self.task_quota is not None:
            result['TaskQuota'] = self.task_quota
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('SmsQuota') is not None:
            self.sms_quota = m.get('SmsQuota')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Config') is not None:
            temp_model = DescribeDnsGtmInstancesResponseBodyGtmInstancesConfig()
            self.config = temp_model.from_map(m['Config'])
        if m.get('ExpireTimestamp') is not None:
            self.expire_timestamp = m.get('ExpireTimestamp')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('UsedQuota') is not None:
            temp_model = DescribeDnsGtmInstancesResponseBodyGtmInstancesUsedQuota()
            self.used_quota = temp_model.from_map(m['UsedQuota'])
        if m.get('TaskQuota') is not None:
            self.task_quota = m.get('TaskQuota')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeDnsGtmInstancesResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        gtm_instances: List[DescribeDnsGtmInstancesResponseBodyGtmInstances] = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.gtm_instances = gtm_instances
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.gtm_instances:
            for k in self.gtm_instances:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['GtmInstances'] = []
        if self.gtm_instances is not None:
            for k in self.gtm_instances:
                result['GtmInstances'].append(k.to_map() if k else None)
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.gtm_instances = []
        if m.get('GtmInstances') is not None:
            for k in m.get('GtmInstances'):
                temp_model = DescribeDnsGtmInstancesResponseBodyGtmInstances()
                self.gtm_instances.append(temp_model.from_map(k))
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeDnsGtmInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstanceStatusRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeDnsGtmInstanceStatusResponseBody(TeaModel):
    def __init__(
        self,
        strategy_not_available_num: int = None,
        addr_available_num: int = None,
        request_id: str = None,
        switch_to_failover_strategy_num: int = None,
        addr_not_available_num: int = None,
        addr_pool_group_not_available_num: int = None,
    ):
        self.strategy_not_available_num = strategy_not_available_num
        self.addr_available_num = addr_available_num
        self.request_id = request_id
        self.switch_to_failover_strategy_num = switch_to_failover_strategy_num
        self.addr_not_available_num = addr_not_available_num
        self.addr_pool_group_not_available_num = addr_pool_group_not_available_num

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.strategy_not_available_num is not None:
            result['StrategyNotAvailableNum'] = self.strategy_not_available_num
        if self.addr_available_num is not None:
            result['AddrAvailableNum'] = self.addr_available_num
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.switch_to_failover_strategy_num is not None:
            result['SwitchToFailoverStrategyNum'] = self.switch_to_failover_strategy_num
        if self.addr_not_available_num is not None:
            result['AddrNotAvailableNum'] = self.addr_not_available_num
        if self.addr_pool_group_not_available_num is not None:
            result['AddrPoolGroupNotAvailableNum'] = self.addr_pool_group_not_available_num
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StrategyNotAvailableNum') is not None:
            self.strategy_not_available_num = m.get('StrategyNotAvailableNum')
        if m.get('AddrAvailableNum') is not None:
            self.addr_available_num = m.get('AddrAvailableNum')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SwitchToFailoverStrategyNum') is not None:
            self.switch_to_failover_strategy_num = m.get('SwitchToFailoverStrategyNum')
        if m.get('AddrNotAvailableNum') is not None:
            self.addr_not_available_num = m.get('AddrNotAvailableNum')
        if m.get('AddrPoolGroupNotAvailableNum') is not None:
            self.addr_pool_group_not_available_num = m.get('AddrPoolGroupNotAvailableNum')
        return self


class DescribeDnsGtmInstanceStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstanceStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstanceStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmInstanceSystemCnameRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeDnsGtmInstanceSystemCnameResponseBody(TeaModel):
    def __init__(
        self,
        system_cname: str = None,
        request_id: str = None,
    ):
        self.system_cname = system_cname
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.system_cname is not None:
            result['SystemCname'] = self.system_cname
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SystemCname') is not None:
            self.system_cname = m.get('SystemCname')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeDnsGtmInstanceSystemCnameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmInstanceSystemCnameResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmInstanceSystemCnameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmLogsRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        keyword: str = None,
        page_number: int = None,
        page_size: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.keyword = keyword
        self.page_number = page_number
        self.page_size = page_size
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        return self


class DescribeDnsGtmLogsResponseBodyLogsLog(TeaModel):
    def __init__(
        self,
        oper_timestamp: int = None,
        entity_id: str = None,
        entity_type: str = None,
        oper_time: str = None,
        oper_action: str = None,
        content: str = None,
        entity_name: str = None,
        id: int = None,
    ):
        self.oper_timestamp = oper_timestamp
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.oper_time = oper_time
        self.oper_action = oper_action
        self.content = content
        self.entity_name = entity_name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.oper_timestamp is not None:
            result['OperTimestamp'] = self.oper_timestamp
        if self.entity_id is not None:
            result['EntityId'] = self.entity_id
        if self.entity_type is not None:
            result['EntityType'] = self.entity_type
        if self.oper_time is not None:
            result['OperTime'] = self.oper_time
        if self.oper_action is not None:
            result['OperAction'] = self.oper_action
        if self.content is not None:
            result['Content'] = self.content
        if self.entity_name is not None:
            result['EntityName'] = self.entity_name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperTimestamp') is not None:
            self.oper_timestamp = m.get('OperTimestamp')
        if m.get('EntityId') is not None:
            self.entity_id = m.get('EntityId')
        if m.get('EntityType') is not None:
            self.entity_type = m.get('EntityType')
        if m.get('OperTime') is not None:
            self.oper_time = m.get('OperTime')
        if m.get('OperAction') is not None:
            self.oper_action = m.get('OperAction')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('EntityName') is not None:
            self.entity_name = m.get('EntityName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeDnsGtmLogsResponseBodyLogs(TeaModel):
    def __init__(
        self,
        log: List[DescribeDnsGtmLogsResponseBodyLogsLog] = None,
    ):
        self.log = log

    def validate(self):
        if self.log:
            for k in self.log:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Log'] = []
        if self.log is not None:
            for k in self.log:
                result['Log'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.log = []
        if m.get('Log') is not None:
            for k in m.get('Log'):
                temp_model = DescribeDnsGtmLogsResponseBodyLogsLog()
                self.log.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmLogsResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        logs: DescribeDnsGtmLogsResponseBodyLogs = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.logs = logs
        self.total_items = total_items

    def validate(self):
        if self.logs:
            self.logs.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.logs is not None:
            result['Logs'] = self.logs.to_map()
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('Logs') is not None:
            temp_model = DescribeDnsGtmLogsResponseBodyLogs()
            self.logs = temp_model.from_map(m['Logs'])
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeDnsGtmLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmMonitorAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodesIpv4IspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        group_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        isp_name: str = None,
        group_type: str = None,
        default_selected: bool = None,
    ):
        self.city_code = city_code
        self.group_name = group_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.isp_name = isp_name
        self.group_type = group_type
        self.default_selected = default_selected

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.group_type is not None:
            result['GroupType'] = self.group_type
        if self.default_selected is not None:
            result['DefaultSelected'] = self.default_selected
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('GroupType') is not None:
            self.group_type = m.get('GroupType')
        if m.get('DefaultSelected') is not None:
            self.default_selected = m.get('DefaultSelected')
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodes(TeaModel):
    def __init__(
        self,
        ipv_4isp_city_node: List[DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodesIpv4IspCityNode] = None,
    ):
        self.ipv_4isp_city_node = ipv_4isp_city_node

    def validate(self):
        if self.ipv_4isp_city_node:
            for k in self.ipv_4isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Ipv4IspCityNode'] = []
        if self.ipv_4isp_city_node is not None:
            for k in self.ipv_4isp_city_node:
                result['Ipv4IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.ipv_4isp_city_node = []
        if m.get('Ipv4IspCityNode') is not None:
            for k in m.get('Ipv4IspCityNode'):
                temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodesIpv4IspCityNode()
                self.ipv_4isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodesDomainIpv4IspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        group_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        isp_name: str = None,
        group_type: str = None,
        default_selected: bool = None,
    ):
        self.city_code = city_code
        self.group_name = group_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.isp_name = isp_name
        self.group_type = group_type
        self.default_selected = default_selected

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.group_type is not None:
            result['GroupType'] = self.group_type
        if self.default_selected is not None:
            result['DefaultSelected'] = self.default_selected
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('GroupType') is not None:
            self.group_type = m.get('GroupType')
        if m.get('DefaultSelected') is not None:
            self.default_selected = m.get('DefaultSelected')
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodes(TeaModel):
    def __init__(
        self,
        domain_ipv_4isp_city_node: List[DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodesDomainIpv4IspCityNode] = None,
    ):
        self.domain_ipv_4isp_city_node = domain_ipv_4isp_city_node

    def validate(self):
        if self.domain_ipv_4isp_city_node:
            for k in self.domain_ipv_4isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainIpv4IspCityNode'] = []
        if self.domain_ipv_4isp_city_node is not None:
            for k in self.domain_ipv_4isp_city_node:
                result['DomainIpv4IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_ipv_4isp_city_node = []
        if m.get('DomainIpv4IspCityNode') is not None:
            for k in m.get('DomainIpv4IspCityNode'):
                temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodesDomainIpv4IspCityNode()
                self.domain_ipv_4isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodesDomainIpv6IspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        group_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        isp_name: str = None,
        group_type: str = None,
        default_selected: bool = None,
    ):
        self.city_code = city_code
        self.group_name = group_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.isp_name = isp_name
        self.group_type = group_type
        self.default_selected = default_selected

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.group_type is not None:
            result['GroupType'] = self.group_type
        if self.default_selected is not None:
            result['DefaultSelected'] = self.default_selected
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('GroupType') is not None:
            self.group_type = m.get('GroupType')
        if m.get('DefaultSelected') is not None:
            self.default_selected = m.get('DefaultSelected')
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodes(TeaModel):
    def __init__(
        self,
        domain_ipv_6isp_city_node: List[DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodesDomainIpv6IspCityNode] = None,
    ):
        self.domain_ipv_6isp_city_node = domain_ipv_6isp_city_node

    def validate(self):
        if self.domain_ipv_6isp_city_node:
            for k in self.domain_ipv_6isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainIpv6IspCityNode'] = []
        if self.domain_ipv_6isp_city_node is not None:
            for k in self.domain_ipv_6isp_city_node:
                result['DomainIpv6IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_ipv_6isp_city_node = []
        if m.get('DomainIpv6IspCityNode') is not None:
            for k in m.get('DomainIpv6IspCityNode'):
                temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodesDomainIpv6IspCityNode()
                self.domain_ipv_6isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodesIpv6IspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        group_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        isp_name: str = None,
        group_type: str = None,
        default_selected: bool = None,
    ):
        self.city_code = city_code
        self.group_name = group_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.isp_name = isp_name
        self.group_type = group_type
        self.default_selected = default_selected

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.group_type is not None:
            result['GroupType'] = self.group_type
        if self.default_selected is not None:
            result['DefaultSelected'] = self.default_selected
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('GroupType') is not None:
            self.group_type = m.get('GroupType')
        if m.get('DefaultSelected') is not None:
            self.default_selected = m.get('DefaultSelected')
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodes(TeaModel):
    def __init__(
        self,
        ipv_6isp_city_node: List[DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodesIpv6IspCityNode] = None,
    ):
        self.ipv_6isp_city_node = ipv_6isp_city_node

    def validate(self):
        if self.ipv_6isp_city_node:
            for k in self.ipv_6isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Ipv6IspCityNode'] = []
        if self.ipv_6isp_city_node is not None:
            for k in self.ipv_6isp_city_node:
                result['Ipv6IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.ipv_6isp_city_node = []
        if m.get('Ipv6IspCityNode') is not None:
            for k in m.get('Ipv6IspCityNode'):
                temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodesIpv6IspCityNode()
                self.ipv_6isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmMonitorAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        ipv_4isp_city_nodes: DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodes = None,
        domain_ipv_4isp_city_nodes: DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodes = None,
        request_id: str = None,
        domain_ipv_6isp_city_nodes: DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodes = None,
        ipv_6isp_city_nodes: DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodes = None,
    ):
        self.ipv_4isp_city_nodes = ipv_4isp_city_nodes
        self.domain_ipv_4isp_city_nodes = domain_ipv_4isp_city_nodes
        self.request_id = request_id
        self.domain_ipv_6isp_city_nodes = domain_ipv_6isp_city_nodes
        self.ipv_6isp_city_nodes = ipv_6isp_city_nodes

    def validate(self):
        if self.ipv_4isp_city_nodes:
            self.ipv_4isp_city_nodes.validate()
        if self.domain_ipv_4isp_city_nodes:
            self.domain_ipv_4isp_city_nodes.validate()
        if self.domain_ipv_6isp_city_nodes:
            self.domain_ipv_6isp_city_nodes.validate()
        if self.ipv_6isp_city_nodes:
            self.ipv_6isp_city_nodes.validate()

    def to_map(self):
        result = dict()
        if self.ipv_4isp_city_nodes is not None:
            result['Ipv4IspCityNodes'] = self.ipv_4isp_city_nodes.to_map()
        if self.domain_ipv_4isp_city_nodes is not None:
            result['DomainIpv4IspCityNodes'] = self.domain_ipv_4isp_city_nodes.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_ipv_6isp_city_nodes is not None:
            result['DomainIpv6IspCityNodes'] = self.domain_ipv_6isp_city_nodes.to_map()
        if self.ipv_6isp_city_nodes is not None:
            result['Ipv6IspCityNodes'] = self.ipv_6isp_city_nodes.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ipv4IspCityNodes') is not None:
            temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv4IspCityNodes()
            self.ipv_4isp_city_nodes = temp_model.from_map(m['Ipv4IspCityNodes'])
        if m.get('DomainIpv4IspCityNodes') is not None:
            temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv4IspCityNodes()
            self.domain_ipv_4isp_city_nodes = temp_model.from_map(m['DomainIpv4IspCityNodes'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainIpv6IspCityNodes') is not None:
            temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyDomainIpv6IspCityNodes()
            self.domain_ipv_6isp_city_nodes = temp_model.from_map(m['DomainIpv6IspCityNodes'])
        if m.get('Ipv6IspCityNodes') is not None:
            temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBodyIpv6IspCityNodes()
            self.ipv_6isp_city_nodes = temp_model.from_map(m['Ipv6IspCityNodes'])
        return self


class DescribeDnsGtmMonitorAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmMonitorAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmMonitorAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsGtmMonitorConfigRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class DescribeDnsGtmMonitorConfigResponseBodyIspCityNodesIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        country_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        country_code: str = None,
        isp_name: str = None,
    ):
        self.city_code = city_code
        self.country_name = country_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.country_code = country_code
        self.isp_name = isp_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.country_name is not None:
            result['CountryName'] = self.country_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.country_code is not None:
            result['CountryCode'] = self.country_code
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('CountryName') is not None:
            self.country_name = m.get('CountryName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('CountryCode') is not None:
            self.country_code = m.get('CountryCode')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        return self


class DescribeDnsGtmMonitorConfigResponseBodyIspCityNodes(TeaModel):
    def __init__(
        self,
        isp_city_node: List[DescribeDnsGtmMonitorConfigResponseBodyIspCityNodesIspCityNode] = None,
    ):
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = DescribeDnsGtmMonitorConfigResponseBodyIspCityNodesIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeDnsGtmMonitorConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        timeout: int = None,
        protocol_type: str = None,
        isp_city_nodes: DescribeDnsGtmMonitorConfigResponseBodyIspCityNodes = None,
        create_time: str = None,
        update_time: str = None,
        evaluation_count: int = None,
        update_timestamp: int = None,
        monitor_extend_info: str = None,
        monitor_config_id: str = None,
        create_timestamp: int = None,
        interval: int = None,
    ):
        self.request_id = request_id
        self.timeout = timeout
        self.protocol_type = protocol_type
        self.isp_city_nodes = isp_city_nodes
        self.create_time = create_time
        self.update_time = update_time
        self.evaluation_count = evaluation_count
        self.update_timestamp = update_timestamp
        self.monitor_extend_info = monitor_extend_info
        self.monitor_config_id = monitor_config_id
        self.create_timestamp = create_timestamp
        self.interval = interval

    def validate(self):
        if self.isp_city_nodes:
            self.isp_city_nodes.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.isp_city_nodes is not None:
            result['IspCityNodes'] = self.isp_city_nodes.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.interval is not None:
            result['Interval'] = self.interval
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('IspCityNodes') is not None:
            temp_model = DescribeDnsGtmMonitorConfigResponseBodyIspCityNodes()
            self.isp_city_nodes = temp_model.from_map(m['IspCityNodes'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        return self


class DescribeDnsGtmMonitorConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsGtmMonitorConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsGtmMonitorConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsProductInstanceRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeDnsProductInstanceResponseBodyDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class DescribeDnsProductInstanceResponseBody(TeaModel):
    def __init__(
        self,
        monitor_node_count: int = None,
        in_black_hole: bool = None,
        bind_domain_count: int = None,
        region_lines: bool = None,
        bind_count: int = None,
        end_time: str = None,
        start_timestamp: int = None,
        isplines: str = None,
        end_timestamp: int = None,
        dns_servers: DescribeDnsProductInstanceResponseBodyDnsServers = None,
        ddos_defend_query: int = None,
        dns_security: str = None,
        domain_type: str = None,
        urlforward_count: int = None,
        ttlmin_value: int = None,
        payment_type: str = None,
        version_name: str = None,
        oversea_line: str = None,
        ispregion_lines: str = None,
        gslb: bool = None,
        bind_used_count: int = None,
        request_id: str = None,
        dns_slbcount: int = None,
        instance_id: str = None,
        monitor_task_count: int = None,
        start_time: str = None,
        ddos_defend_flow: int = None,
        monitor_frequency: int = None,
        search_engine_lines: str = None,
        bind_domain_used_count: int = None,
        version_code: str = None,
        oversea_ddos_defend_flow: int = None,
        in_clean: bool = None,
        sub_domain_level: int = None,
        domain: str = None,
    ):
        self.monitor_node_count = monitor_node_count
        self.in_black_hole = in_black_hole
        self.bind_domain_count = bind_domain_count
        self.region_lines = region_lines
        self.bind_count = bind_count
        self.end_time = end_time
        self.start_timestamp = start_timestamp
        self.isplines = isplines
        self.end_timestamp = end_timestamp
        self.dns_servers = dns_servers
        self.ddos_defend_query = ddos_defend_query
        self.dns_security = dns_security
        self.domain_type = domain_type
        self.urlforward_count = urlforward_count
        self.ttlmin_value = ttlmin_value
        self.payment_type = payment_type
        self.version_name = version_name
        self.oversea_line = oversea_line
        self.ispregion_lines = ispregion_lines
        self.gslb = gslb
        self.bind_used_count = bind_used_count
        self.request_id = request_id
        self.dns_slbcount = dns_slbcount
        self.instance_id = instance_id
        self.monitor_task_count = monitor_task_count
        self.start_time = start_time
        self.ddos_defend_flow = ddos_defend_flow
        self.monitor_frequency = monitor_frequency
        self.search_engine_lines = search_engine_lines
        self.bind_domain_used_count = bind_domain_used_count
        self.version_code = version_code
        self.oversea_ddos_defend_flow = oversea_ddos_defend_flow
        self.in_clean = in_clean
        self.sub_domain_level = sub_domain_level
        self.domain = domain

    def validate(self):
        if self.dns_servers:
            self.dns_servers.validate()

    def to_map(self):
        result = dict()
        if self.monitor_node_count is not None:
            result['MonitorNodeCount'] = self.monitor_node_count
        if self.in_black_hole is not None:
            result['InBlackHole'] = self.in_black_hole
        if self.bind_domain_count is not None:
            result['BindDomainCount'] = self.bind_domain_count
        if self.region_lines is not None:
            result['RegionLines'] = self.region_lines
        if self.bind_count is not None:
            result['BindCount'] = self.bind_count
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.isplines is not None:
            result['ISPLines'] = self.isplines
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        if self.dns_servers is not None:
            result['DnsServers'] = self.dns_servers.to_map()
        if self.ddos_defend_query is not None:
            result['DDosDefendQuery'] = self.ddos_defend_query
        if self.dns_security is not None:
            result['DnsSecurity'] = self.dns_security
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        if self.urlforward_count is not None:
            result['URLForwardCount'] = self.urlforward_count
        if self.ttlmin_value is not None:
            result['TTLMinValue'] = self.ttlmin_value
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.oversea_line is not None:
            result['OverseaLine'] = self.oversea_line
        if self.ispregion_lines is not None:
            result['ISPRegionLines'] = self.ispregion_lines
        if self.gslb is not None:
            result['Gslb'] = self.gslb
        if self.bind_used_count is not None:
            result['BindUsedCount'] = self.bind_used_count
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.dns_slbcount is not None:
            result['DnsSLBCount'] = self.dns_slbcount
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.monitor_task_count is not None:
            result['MonitorTaskCount'] = self.monitor_task_count
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.ddos_defend_flow is not None:
            result['DDosDefendFlow'] = self.ddos_defend_flow
        if self.monitor_frequency is not None:
            result['MonitorFrequency'] = self.monitor_frequency
        if self.search_engine_lines is not None:
            result['SearchEngineLines'] = self.search_engine_lines
        if self.bind_domain_used_count is not None:
            result['BindDomainUsedCount'] = self.bind_domain_used_count
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.oversea_ddos_defend_flow is not None:
            result['OverseaDDosDefendFlow'] = self.oversea_ddos_defend_flow
        if self.in_clean is not None:
            result['InClean'] = self.in_clean
        if self.sub_domain_level is not None:
            result['SubDomainLevel'] = self.sub_domain_level
        if self.domain is not None:
            result['Domain'] = self.domain
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MonitorNodeCount') is not None:
            self.monitor_node_count = m.get('MonitorNodeCount')
        if m.get('InBlackHole') is not None:
            self.in_black_hole = m.get('InBlackHole')
        if m.get('BindDomainCount') is not None:
            self.bind_domain_count = m.get('BindDomainCount')
        if m.get('RegionLines') is not None:
            self.region_lines = m.get('RegionLines')
        if m.get('BindCount') is not None:
            self.bind_count = m.get('BindCount')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('ISPLines') is not None:
            self.isplines = m.get('ISPLines')
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        if m.get('DnsServers') is not None:
            temp_model = DescribeDnsProductInstanceResponseBodyDnsServers()
            self.dns_servers = temp_model.from_map(m['DnsServers'])
        if m.get('DDosDefendQuery') is not None:
            self.ddos_defend_query = m.get('DDosDefendQuery')
        if m.get('DnsSecurity') is not None:
            self.dns_security = m.get('DnsSecurity')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        if m.get('URLForwardCount') is not None:
            self.urlforward_count = m.get('URLForwardCount')
        if m.get('TTLMinValue') is not None:
            self.ttlmin_value = m.get('TTLMinValue')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('OverseaLine') is not None:
            self.oversea_line = m.get('OverseaLine')
        if m.get('ISPRegionLines') is not None:
            self.ispregion_lines = m.get('ISPRegionLines')
        if m.get('Gslb') is not None:
            self.gslb = m.get('Gslb')
        if m.get('BindUsedCount') is not None:
            self.bind_used_count = m.get('BindUsedCount')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DnsSLBCount') is not None:
            self.dns_slbcount = m.get('DnsSLBCount')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MonitorTaskCount') is not None:
            self.monitor_task_count = m.get('MonitorTaskCount')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('DDosDefendFlow') is not None:
            self.ddos_defend_flow = m.get('DDosDefendFlow')
        if m.get('MonitorFrequency') is not None:
            self.monitor_frequency = m.get('MonitorFrequency')
        if m.get('SearchEngineLines') is not None:
            self.search_engine_lines = m.get('SearchEngineLines')
        if m.get('BindDomainUsedCount') is not None:
            self.bind_domain_used_count = m.get('BindDomainUsedCount')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('OverseaDDosDefendFlow') is not None:
            self.oversea_ddos_defend_flow = m.get('OverseaDDosDefendFlow')
        if m.get('InClean') is not None:
            self.in_clean = m.get('InClean')
        if m.get('SubDomainLevel') is not None:
            self.sub_domain_level = m.get('SubDomainLevel')
        if m.get('Domain') is not None:
            self.domain = m.get('Domain')
        return self


class DescribeDnsProductInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsProductInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsProductInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDnsProductInstancesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        version_code: str = None,
        domain_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.version_code = version_code
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeDnsProductInstancesResponseBodyDnsProductsDnsProduct(TeaModel):
    def __init__(
        self,
        oversea_line: str = None,
        payment_type: str = None,
        monitor_node_count: int = None,
        in_black_hole: bool = None,
        bind_domain_used_count: int = None,
        ispregion_lines: str = None,
        ttlmin_value: int = None,
        isplines: str = None,
        search_engine_lines: str = None,
        end_timestamp: int = None,
        version_name: str = None,
        version_code: str = None,
        monitor_task_count: int = None,
        bind_used_count: int = None,
        domain: str = None,
        monitor_frequency: int = None,
        in_clean: bool = None,
        urlforward_count: int = None,
        start_timestamp: int = None,
        ddos_defend_query: int = None,
        instance_id: str = None,
        ddos_defend_flow: int = None,
        bind_count: int = None,
        sub_domain_level: int = None,
        bind_domain_count: int = None,
        end_time: str = None,
        start_time: str = None,
        oversea_ddos_defend_flow: int = None,
        region_lines: bool = None,
        gslb: bool = None,
        dns_security: str = None,
        dns_slbcount: int = None,
    ):
        self.oversea_line = oversea_line
        self.payment_type = payment_type
        self.monitor_node_count = monitor_node_count
        self.in_black_hole = in_black_hole
        self.bind_domain_used_count = bind_domain_used_count
        self.ispregion_lines = ispregion_lines
        self.ttlmin_value = ttlmin_value
        self.isplines = isplines
        self.search_engine_lines = search_engine_lines
        self.end_timestamp = end_timestamp
        self.version_name = version_name
        self.version_code = version_code
        self.monitor_task_count = monitor_task_count
        self.bind_used_count = bind_used_count
        self.domain = domain
        self.monitor_frequency = monitor_frequency
        self.in_clean = in_clean
        self.urlforward_count = urlforward_count
        self.start_timestamp = start_timestamp
        self.ddos_defend_query = ddos_defend_query
        self.instance_id = instance_id
        self.ddos_defend_flow = ddos_defend_flow
        self.bind_count = bind_count
        self.sub_domain_level = sub_domain_level
        self.bind_domain_count = bind_domain_count
        self.end_time = end_time
        self.start_time = start_time
        self.oversea_ddos_defend_flow = oversea_ddos_defend_flow
        self.region_lines = region_lines
        self.gslb = gslb
        self.dns_security = dns_security
        self.dns_slbcount = dns_slbcount

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.oversea_line is not None:
            result['OverseaLine'] = self.oversea_line
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.monitor_node_count is not None:
            result['MonitorNodeCount'] = self.monitor_node_count
        if self.in_black_hole is not None:
            result['InBlackHole'] = self.in_black_hole
        if self.bind_domain_used_count is not None:
            result['BindDomainUsedCount'] = self.bind_domain_used_count
        if self.ispregion_lines is not None:
            result['ISPRegionLines'] = self.ispregion_lines
        if self.ttlmin_value is not None:
            result['TTLMinValue'] = self.ttlmin_value
        if self.isplines is not None:
            result['ISPLines'] = self.isplines
        if self.search_engine_lines is not None:
            result['SearchEngineLines'] = self.search_engine_lines
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.monitor_task_count is not None:
            result['MonitorTaskCount'] = self.monitor_task_count
        if self.bind_used_count is not None:
            result['BindUsedCount'] = self.bind_used_count
        if self.domain is not None:
            result['Domain'] = self.domain
        if self.monitor_frequency is not None:
            result['MonitorFrequency'] = self.monitor_frequency
        if self.in_clean is not None:
            result['InClean'] = self.in_clean
        if self.urlforward_count is not None:
            result['URLForwardCount'] = self.urlforward_count
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.ddos_defend_query is not None:
            result['DDosDefendQuery'] = self.ddos_defend_query
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.ddos_defend_flow is not None:
            result['DDosDefendFlow'] = self.ddos_defend_flow
        if self.bind_count is not None:
            result['BindCount'] = self.bind_count
        if self.sub_domain_level is not None:
            result['SubDomainLevel'] = self.sub_domain_level
        if self.bind_domain_count is not None:
            result['BindDomainCount'] = self.bind_domain_count
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.oversea_ddos_defend_flow is not None:
            result['OverseaDDosDefendFlow'] = self.oversea_ddos_defend_flow
        if self.region_lines is not None:
            result['RegionLines'] = self.region_lines
        if self.gslb is not None:
            result['Gslb'] = self.gslb
        if self.dns_security is not None:
            result['DnsSecurity'] = self.dns_security
        if self.dns_slbcount is not None:
            result['DnsSLBCount'] = self.dns_slbcount
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OverseaLine') is not None:
            self.oversea_line = m.get('OverseaLine')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('MonitorNodeCount') is not None:
            self.monitor_node_count = m.get('MonitorNodeCount')
        if m.get('InBlackHole') is not None:
            self.in_black_hole = m.get('InBlackHole')
        if m.get('BindDomainUsedCount') is not None:
            self.bind_domain_used_count = m.get('BindDomainUsedCount')
        if m.get('ISPRegionLines') is not None:
            self.ispregion_lines = m.get('ISPRegionLines')
        if m.get('TTLMinValue') is not None:
            self.ttlmin_value = m.get('TTLMinValue')
        if m.get('ISPLines') is not None:
            self.isplines = m.get('ISPLines')
        if m.get('SearchEngineLines') is not None:
            self.search_engine_lines = m.get('SearchEngineLines')
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('MonitorTaskCount') is not None:
            self.monitor_task_count = m.get('MonitorTaskCount')
        if m.get('BindUsedCount') is not None:
            self.bind_used_count = m.get('BindUsedCount')
        if m.get('Domain') is not None:
            self.domain = m.get('Domain')
        if m.get('MonitorFrequency') is not None:
            self.monitor_frequency = m.get('MonitorFrequency')
        if m.get('InClean') is not None:
            self.in_clean = m.get('InClean')
        if m.get('URLForwardCount') is not None:
            self.urlforward_count = m.get('URLForwardCount')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('DDosDefendQuery') is not None:
            self.ddos_defend_query = m.get('DDosDefendQuery')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('DDosDefendFlow') is not None:
            self.ddos_defend_flow = m.get('DDosDefendFlow')
        if m.get('BindCount') is not None:
            self.bind_count = m.get('BindCount')
        if m.get('SubDomainLevel') is not None:
            self.sub_domain_level = m.get('SubDomainLevel')
        if m.get('BindDomainCount') is not None:
            self.bind_domain_count = m.get('BindDomainCount')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('OverseaDDosDefendFlow') is not None:
            self.oversea_ddos_defend_flow = m.get('OverseaDDosDefendFlow')
        if m.get('RegionLines') is not None:
            self.region_lines = m.get('RegionLines')
        if m.get('Gslb') is not None:
            self.gslb = m.get('Gslb')
        if m.get('DnsSecurity') is not None:
            self.dns_security = m.get('DnsSecurity')
        if m.get('DnsSLBCount') is not None:
            self.dns_slbcount = m.get('DnsSLBCount')
        return self


class DescribeDnsProductInstancesResponseBodyDnsProducts(TeaModel):
    def __init__(
        self,
        dns_product: List[DescribeDnsProductInstancesResponseBodyDnsProductsDnsProduct] = None,
    ):
        self.dns_product = dns_product

    def validate(self):
        if self.dns_product:
            for k in self.dns_product:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DnsProduct'] = []
        if self.dns_product is not None:
            for k in self.dns_product:
                result['DnsProduct'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.dns_product = []
        if m.get('DnsProduct') is not None:
            for k in m.get('DnsProduct'):
                temp_model = DescribeDnsProductInstancesResponseBodyDnsProductsDnsProduct()
                self.dns_product.append(temp_model.from_map(k))
        return self


class DescribeDnsProductInstancesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        domain_type: str = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        dns_products: DescribeDnsProductInstancesResponseBodyDnsProducts = None,
    ):
        self.total_count = total_count
        self.domain_type = domain_type
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.dns_products = dns_products

    def validate(self):
        if self.dns_products:
            self.dns_products.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.dns_products is not None:
            result['DnsProducts'] = self.dns_products.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('DnsProducts') is not None:
            temp_model = DescribeDnsProductInstancesResponseBodyDnsProducts()
            self.dns_products = temp_model.from_map(m['DnsProducts'])
        return self


class DescribeDnsProductInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDnsProductInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDnsProductInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDNSSLBSubDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        page_number: int = None,
        page_size: int = None,
        rr: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.page_number = page_number
        self.page_size = page_size
        self.rr = rr

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.rr is not None:
            result['Rr'] = self.rr
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        return self


class DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithmsLineAlgorithm(TeaModel):
    def __init__(
        self,
        line: str = None,
        open: bool = None,
    ):
        self.line = line
        self.open = open

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.line is not None:
            result['Line'] = self.line
        if self.open is not None:
            result['Open'] = self.open
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Open') is not None:
            self.open = m.get('Open')
        return self


class DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithms(TeaModel):
    def __init__(
        self,
        line_algorithm: List[DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithmsLineAlgorithm] = None,
    ):
        self.line_algorithm = line_algorithm

    def validate(self):
        if self.line_algorithm:
            for k in self.line_algorithm:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['LineAlgorithm'] = []
        if self.line_algorithm is not None:
            for k in self.line_algorithm:
                result['LineAlgorithm'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line_algorithm = []
        if m.get('LineAlgorithm') is not None:
            for k in m.get('LineAlgorithm'):
                temp_model = DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithmsLineAlgorithm()
                self.line_algorithm.append(temp_model.from_map(k))
        return self


class DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomain(TeaModel):
    def __init__(
        self,
        type: str = None,
        record_count: int = None,
        open: bool = None,
        sub_domain: str = None,
        line_algorithms: DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithms = None,
    ):
        self.type = type
        self.record_count = record_count
        self.open = open
        self.sub_domain = sub_domain
        self.line_algorithms = line_algorithms

    def validate(self):
        if self.line_algorithms:
            self.line_algorithms.validate()

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.open is not None:
            result['Open'] = self.open
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.line_algorithms is not None:
            result['LineAlgorithms'] = self.line_algorithms.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Open') is not None:
            self.open = m.get('Open')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('LineAlgorithms') is not None:
            temp_model = DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomainLineAlgorithms()
            self.line_algorithms = temp_model.from_map(m['LineAlgorithms'])
        return self


class DescribeDNSSLBSubDomainsResponseBodySlbSubDomains(TeaModel):
    def __init__(
        self,
        slb_sub_domain: List[DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomain] = None,
    ):
        self.slb_sub_domain = slb_sub_domain

    def validate(self):
        if self.slb_sub_domain:
            for k in self.slb_sub_domain:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SlbSubDomain'] = []
        if self.slb_sub_domain is not None:
            for k in self.slb_sub_domain:
                result['SlbSubDomain'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.slb_sub_domain = []
        if m.get('SlbSubDomain') is not None:
            for k in m.get('SlbSubDomain'):
                temp_model = DescribeDNSSLBSubDomainsResponseBodySlbSubDomainsSlbSubDomain()
                self.slb_sub_domain.append(temp_model.from_map(k))
        return self


class DescribeDNSSLBSubDomainsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        slb_sub_domains: DescribeDNSSLBSubDomainsResponseBodySlbSubDomains = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.slb_sub_domains = slb_sub_domains

    def validate(self):
        if self.slb_sub_domains:
            self.slb_sub_domains.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.slb_sub_domains is not None:
            result['SlbSubDomains'] = self.slb_sub_domains.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('SlbSubDomains') is not None:
            temp_model = DescribeDNSSLBSubDomainsResponseBodySlbSubDomains()
            self.slb_sub_domains = temp_model.from_map(m['SlbSubDomains'])
        return self


class DescribeDNSSLBSubDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDNSSLBSubDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDNSSLBSubDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohAccountStatisticsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self.lang = lang
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        return self


class DescribeDohAccountStatisticsResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        v_6http_count: int = None,
        v_4https_count: int = None,
        timestamp: int = None,
        total_count: int = None,
        v_4http_count: int = None,
        v_6https_count: int = None,
    ):
        self.v_6http_count = v_6http_count
        self.v_4https_count = v_4https_count
        self.timestamp = timestamp
        self.total_count = total_count
        self.v_4http_count = v_4http_count
        self.v_6https_count = v_6https_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_6http_count is not None:
            result['V6HttpCount'] = self.v_6http_count
        if self.v_4https_count is not None:
            result['V4HttpsCount'] = self.v_4https_count
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.v_4http_count is not None:
            result['V4HttpCount'] = self.v_4http_count
        if self.v_6https_count is not None:
            result['V6HttpsCount'] = self.v_6https_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('V6HttpCount') is not None:
            self.v_6http_count = m.get('V6HttpCount')
        if m.get('V4HttpsCount') is not None:
            self.v_4https_count = m.get('V4HttpsCount')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('V4HttpCount') is not None:
            self.v_4http_count = m.get('V4HttpCount')
        if m.get('V6HttpsCount') is not None:
            self.v_6https_count = m.get('V6HttpsCount')
        return self


class DescribeDohAccountStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: List[DescribeDohAccountStatisticsResponseBodyStatistics] = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = DescribeDohAccountStatisticsResponseBodyStatistics()
                self.statistics.append(temp_model.from_map(k))
        return self


class DescribeDohAccountStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohAccountStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohAccountStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohDomainStatisticsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        domain_name: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self.lang = lang
        self.domain_name = domain_name
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        return self


class DescribeDohDomainStatisticsResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        v_6http_count: int = None,
        v_4https_count: int = None,
        timestamp: int = None,
        total_count: int = None,
        v_4http_count: int = None,
        v_6https_count: int = None,
    ):
        self.v_6http_count = v_6http_count
        self.v_4https_count = v_4https_count
        self.timestamp = timestamp
        self.total_count = total_count
        self.v_4http_count = v_4http_count
        self.v_6https_count = v_6https_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_6http_count is not None:
            result['V6HttpCount'] = self.v_6http_count
        if self.v_4https_count is not None:
            result['V4HttpsCount'] = self.v_4https_count
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.v_4http_count is not None:
            result['V4HttpCount'] = self.v_4http_count
        if self.v_6https_count is not None:
            result['V6HttpsCount'] = self.v_6https_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('V6HttpCount') is not None:
            self.v_6http_count = m.get('V6HttpCount')
        if m.get('V4HttpsCount') is not None:
            self.v_4https_count = m.get('V4HttpsCount')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('V4HttpCount') is not None:
            self.v_4http_count = m.get('V4HttpCount')
        if m.get('V6HttpsCount') is not None:
            self.v_6https_count = m.get('V6HttpsCount')
        return self


class DescribeDohDomainStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: List[DescribeDohDomainStatisticsResponseBodyStatistics] = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = DescribeDohDomainStatisticsResponseBodyStatistics()
                self.statistics.append(temp_model.from_map(k))
        return self


class DescribeDohDomainStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohDomainStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohDomainStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohDomainStatisticsSummaryRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        page_number: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        order_by: str = None,
        direction: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.page_number = page_number
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.order_by = order_by
        self.direction = direction
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeDohDomainStatisticsSummaryResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        v_6http_count: int = None,
        v_4https_count: int = None,
        ip_count: int = None,
        total_count: int = None,
        http_count: int = None,
        domain_name: str = None,
        https_count: int = None,
        v_4http_count: int = None,
        v_6https_count: int = None,
    ):
        self.v_6http_count = v_6http_count
        self.v_4https_count = v_4https_count
        self.ip_count = ip_count
        self.total_count = total_count
        self.http_count = http_count
        self.domain_name = domain_name
        self.https_count = https_count
        self.v_4http_count = v_4http_count
        self.v_6https_count = v_6https_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_6http_count is not None:
            result['V6HttpCount'] = self.v_6http_count
        if self.v_4https_count is not None:
            result['V4HttpsCount'] = self.v_4https_count
        if self.ip_count is not None:
            result['IpCount'] = self.ip_count
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.http_count is not None:
            result['HttpCount'] = self.http_count
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.https_count is not None:
            result['HttpsCount'] = self.https_count
        if self.v_4http_count is not None:
            result['V4HttpCount'] = self.v_4http_count
        if self.v_6https_count is not None:
            result['V6HttpsCount'] = self.v_6https_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('V6HttpCount') is not None:
            self.v_6http_count = m.get('V6HttpCount')
        if m.get('V4HttpsCount') is not None:
            self.v_4https_count = m.get('V4HttpsCount')
        if m.get('IpCount') is not None:
            self.ip_count = m.get('IpCount')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('HttpCount') is not None:
            self.http_count = m.get('HttpCount')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('HttpsCount') is not None:
            self.https_count = m.get('HttpsCount')
        if m.get('V4HttpCount') is not None:
            self.v_4http_count = m.get('V4HttpCount')
        if m.get('V6HttpsCount') is not None:
            self.v_6https_count = m.get('V6HttpsCount')
        return self


class DescribeDohDomainStatisticsSummaryResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        statistics: List[DescribeDohDomainStatisticsSummaryResponseBodyStatistics] = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = DescribeDohDomainStatisticsSummaryResponseBodyStatistics()
                self.statistics.append(temp_model.from_map(k))
        return self


class DescribeDohDomainStatisticsSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohDomainStatisticsSummaryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohDomainStatisticsSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohSubDomainStatisticsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        sub_domain: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self.lang = lang
        self.sub_domain = sub_domain
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        return self


class DescribeDohSubDomainStatisticsResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        v_6http_count: int = None,
        v_4https_count: int = None,
        timestamp: int = None,
        total_count: int = None,
        v_4http_count: int = None,
        v_6https_count: int = None,
    ):
        self.v_6http_count = v_6http_count
        self.v_4https_count = v_4https_count
        self.timestamp = timestamp
        self.total_count = total_count
        self.v_4http_count = v_4http_count
        self.v_6https_count = v_6https_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_6http_count is not None:
            result['V6HttpCount'] = self.v_6http_count
        if self.v_4https_count is not None:
            result['V4HttpsCount'] = self.v_4https_count
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.v_4http_count is not None:
            result['V4HttpCount'] = self.v_4http_count
        if self.v_6https_count is not None:
            result['V6HttpsCount'] = self.v_6https_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('V6HttpCount') is not None:
            self.v_6http_count = m.get('V6HttpCount')
        if m.get('V4HttpsCount') is not None:
            self.v_4https_count = m.get('V4HttpsCount')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('V4HttpCount') is not None:
            self.v_4http_count = m.get('V4HttpCount')
        if m.get('V6HttpsCount') is not None:
            self.v_6https_count = m.get('V6HttpsCount')
        return self


class DescribeDohSubDomainStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: List[DescribeDohSubDomainStatisticsResponseBodyStatistics] = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = DescribeDohSubDomainStatisticsResponseBodyStatistics()
                self.statistics.append(temp_model.from_map(k))
        return self


class DescribeDohSubDomainStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohSubDomainStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohSubDomainStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohSubDomainStatisticsSummaryRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        page_number: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        order_by: str = None,
        direction: str = None,
        sub_domain: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.page_number = page_number
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.order_by = order_by
        self.direction = direction
        self.sub_domain = sub_domain
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeDohSubDomainStatisticsSummaryResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        v_6http_count: int = None,
        v_4https_count: int = None,
        ip_count: int = None,
        sub_domain: str = None,
        total_count: int = None,
        http_count: int = None,
        https_count: int = None,
        v_4http_count: int = None,
        v_6https_count: int = None,
    ):
        self.v_6http_count = v_6http_count
        self.v_4https_count = v_4https_count
        self.ip_count = ip_count
        self.sub_domain = sub_domain
        self.total_count = total_count
        self.http_count = http_count
        self.https_count = https_count
        self.v_4http_count = v_4http_count
        self.v_6https_count = v_6https_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_6http_count is not None:
            result['V6HttpCount'] = self.v_6http_count
        if self.v_4https_count is not None:
            result['V4HttpsCount'] = self.v_4https_count
        if self.ip_count is not None:
            result['IpCount'] = self.ip_count
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.http_count is not None:
            result['HttpCount'] = self.http_count
        if self.https_count is not None:
            result['HttpsCount'] = self.https_count
        if self.v_4http_count is not None:
            result['V4HttpCount'] = self.v_4http_count
        if self.v_6https_count is not None:
            result['V6HttpsCount'] = self.v_6https_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('V6HttpCount') is not None:
            self.v_6http_count = m.get('V6HttpCount')
        if m.get('V4HttpsCount') is not None:
            self.v_4https_count = m.get('V4HttpsCount')
        if m.get('IpCount') is not None:
            self.ip_count = m.get('IpCount')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('HttpCount') is not None:
            self.http_count = m.get('HttpCount')
        if m.get('HttpsCount') is not None:
            self.https_count = m.get('HttpsCount')
        if m.get('V4HttpCount') is not None:
            self.v_4http_count = m.get('V4HttpCount')
        if m.get('V6HttpsCount') is not None:
            self.v_6https_count = m.get('V6HttpsCount')
        return self


class DescribeDohSubDomainStatisticsSummaryResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        statistics: List[DescribeDohSubDomainStatisticsSummaryResponseBodyStatistics] = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = DescribeDohSubDomainStatisticsSummaryResponseBodyStatistics()
                self.statistics.append(temp_model.from_map(k))
        return self


class DescribeDohSubDomainStatisticsSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohSubDomainStatisticsSummaryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohSubDomainStatisticsSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDohUserInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self.lang = lang
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        return self


class DescribeDohUserInfoResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        sub_domain_count: int = None,
        pdns_id: int = None,
        domain_count: int = None,
    ):
        self.request_id = request_id
        self.sub_domain_count = sub_domain_count
        self.pdns_id = pdns_id
        self.domain_count = domain_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.sub_domain_count is not None:
            result['SubDomainCount'] = self.sub_domain_count
        if self.pdns_id is not None:
            result['PdnsId'] = self.pdns_id
        if self.domain_count is not None:
            result['DomainCount'] = self.domain_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SubDomainCount') is not None:
            self.sub_domain_count = m.get('SubDomainCount')
        if m.get('PdnsId') is not None:
            self.pdns_id = m.get('PdnsId')
        if m.get('DomainCount') is not None:
            self.domain_count = m.get('DomainCount')
        return self


class DescribeDohUserInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDohUserInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDohUserInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainDnssecInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeDomainDnssecInfoResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        request_id: str = None,
        digest: str = None,
        domain_name: str = None,
        public_key: str = None,
        digest_type: str = None,
        ds_record: str = None,
        key_tag: str = None,
        flags: str = None,
        algorithm: str = None,
    ):
        self.status = status
        self.request_id = request_id
        self.digest = digest
        self.domain_name = domain_name
        self.public_key = public_key
        self.digest_type = digest_type
        self.ds_record = ds_record
        self.key_tag = key_tag
        self.flags = flags
        self.algorithm = algorithm

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.digest is not None:
            result['Digest'] = self.digest
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.public_key is not None:
            result['PublicKey'] = self.public_key
        if self.digest_type is not None:
            result['DigestType'] = self.digest_type
        if self.ds_record is not None:
            result['DsRecord'] = self.ds_record
        if self.key_tag is not None:
            result['KeyTag'] = self.key_tag
        if self.flags is not None:
            result['Flags'] = self.flags
        if self.algorithm is not None:
            result['Algorithm'] = self.algorithm
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Digest') is not None:
            self.digest = m.get('Digest')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PublicKey') is not None:
            self.public_key = m.get('PublicKey')
        if m.get('DigestType') is not None:
            self.digest_type = m.get('DigestType')
        if m.get('DsRecord') is not None:
            self.ds_record = m.get('DsRecord')
        if m.get('KeyTag') is not None:
            self.key_tag = m.get('KeyTag')
        if m.get('Flags') is not None:
            self.flags = m.get('Flags')
        if m.get('Algorithm') is not None:
            self.algorithm = m.get('Algorithm')
        return self


class DescribeDomainDnssecInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainDnssecInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainDnssecInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainGroupsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        key_word: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.key_word = key_word
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDomainGroupsResponseBodyDomainGroupsDomainGroup(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        group_name: str = None,
        domain_count: int = None,
    ):
        self.group_id = group_id
        self.group_name = group_name
        self.domain_count = domain_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.domain_count is not None:
            result['DomainCount'] = self.domain_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('DomainCount') is not None:
            self.domain_count = m.get('DomainCount')
        return self


class DescribeDomainGroupsResponseBodyDomainGroups(TeaModel):
    def __init__(
        self,
        domain_group: List[DescribeDomainGroupsResponseBodyDomainGroupsDomainGroup] = None,
    ):
        self.domain_group = domain_group

    def validate(self):
        if self.domain_group:
            for k in self.domain_group:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainGroup'] = []
        if self.domain_group is not None:
            for k in self.domain_group:
                result['DomainGroup'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_group = []
        if m.get('DomainGroup') is not None:
            for k in m.get('DomainGroup'):
                temp_model = DescribeDomainGroupsResponseBodyDomainGroupsDomainGroup()
                self.domain_group.append(temp_model.from_map(k))
        return self


class DescribeDomainGroupsResponseBody(TeaModel):
    def __init__(
        self,
        domain_groups: DescribeDomainGroupsResponseBodyDomainGroups = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.domain_groups = domain_groups
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.domain_groups:
            self.domain_groups.validate()

    def to_map(self):
        result = dict()
        if self.domain_groups is not None:
            result['DomainGroups'] = self.domain_groups.to_map()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DomainGroups') is not None:
            temp_model = DescribeDomainGroupsResponseBodyDomainGroups()
            self.domain_groups = temp_model.from_map(m['DomainGroups'])
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeDomainGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        need_detail_attributes: bool = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.need_detail_attributes = need_detail_attributes

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.need_detail_attributes is not None:
            result['NeedDetailAttributes'] = self.need_detail_attributes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('NeedDetailAttributes') is not None:
            self.need_detail_attributes = m.get('NeedDetailAttributes')
        return self


class DescribeDomainInfoResponseBodyDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class DescribeDomainInfoResponseBodyRecordLinesRecordLine(TeaModel):
    def __init__(
        self,
        father_code: str = None,
        line_display_name: str = None,
        line_code: str = None,
        line_name: str = None,
    ):
        self.father_code = father_code
        self.line_display_name = line_display_name
        self.line_code = line_code
        self.line_name = line_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.line_display_name is not None:
            result['LineDisplayName'] = self.line_display_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('LineDisplayName') is not None:
            self.line_display_name = m.get('LineDisplayName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        return self


class DescribeDomainInfoResponseBodyRecordLines(TeaModel):
    def __init__(
        self,
        record_line: List[DescribeDomainInfoResponseBodyRecordLinesRecordLine] = None,
    ):
        self.record_line = record_line

    def validate(self):
        if self.record_line:
            for k in self.record_line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RecordLine'] = []
        if self.record_line is not None:
            for k in self.record_line:
                result['RecordLine'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record_line = []
        if m.get('RecordLine') is not None:
            for k in m.get('RecordLine'):
                temp_model = DescribeDomainInfoResponseBodyRecordLinesRecordLine()
                self.record_line.append(temp_model.from_map(k))
        return self


class DescribeDomainInfoResponseBodyAvailableTtls(TeaModel):
    def __init__(
        self,
        available_ttl: List[str] = None,
    ):
        self.available_ttl = available_ttl

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.available_ttl is not None:
            result['AvailableTtl'] = self.available_ttl
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AvailableTtl') is not None:
            self.available_ttl = m.get('AvailableTtl')
        return self


class DescribeDomainInfoResponseBody(TeaModel):
    def __init__(
        self,
        record_line_tree_json: str = None,
        group_name: str = None,
        in_black_hole: bool = None,
        region_lines: bool = None,
        slave_dns: bool = None,
        ali_domain: bool = None,
        request_id: str = None,
        resource_group_id: str = None,
        instance_id: str = None,
        domain_name: str = None,
        create_time: str = None,
        puny_code: str = None,
        dns_servers: DescribeDomainInfoResponseBodyDnsServers = None,
        remark: str = None,
        group_id: str = None,
        version_code: str = None,
        record_lines: DescribeDomainInfoResponseBodyRecordLines = None,
        domain_id: str = None,
        available_ttls: DescribeDomainInfoResponseBodyAvailableTtls = None,
        min_ttl: int = None,
        in_clean: bool = None,
        version_name: str = None,
        line_type: str = None,
    ):
        self.record_line_tree_json = record_line_tree_json
        self.group_name = group_name
        self.in_black_hole = in_black_hole
        self.region_lines = region_lines
        self.slave_dns = slave_dns
        self.ali_domain = ali_domain
        self.request_id = request_id
        self.resource_group_id = resource_group_id
        self.instance_id = instance_id
        self.domain_name = domain_name
        self.create_time = create_time
        self.puny_code = puny_code
        self.dns_servers = dns_servers
        self.remark = remark
        self.group_id = group_id
        self.version_code = version_code
        self.record_lines = record_lines
        self.domain_id = domain_id
        self.available_ttls = available_ttls
        self.min_ttl = min_ttl
        self.in_clean = in_clean
        self.version_name = version_name
        self.line_type = line_type

    def validate(self):
        if self.dns_servers:
            self.dns_servers.validate()
        if self.record_lines:
            self.record_lines.validate()
        if self.available_ttls:
            self.available_ttls.validate()

    def to_map(self):
        result = dict()
        if self.record_line_tree_json is not None:
            result['RecordLineTreeJson'] = self.record_line_tree_json
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.in_black_hole is not None:
            result['InBlackHole'] = self.in_black_hole
        if self.region_lines is not None:
            result['RegionLines'] = self.region_lines
        if self.slave_dns is not None:
            result['SlaveDns'] = self.slave_dns
        if self.ali_domain is not None:
            result['AliDomain'] = self.ali_domain
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.puny_code is not None:
            result['PunyCode'] = self.puny_code
        if self.dns_servers is not None:
            result['DnsServers'] = self.dns_servers.to_map()
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.record_lines is not None:
            result['RecordLines'] = self.record_lines.to_map()
        if self.domain_id is not None:
            result['DomainId'] = self.domain_id
        if self.available_ttls is not None:
            result['AvailableTtls'] = self.available_ttls.to_map()
        if self.min_ttl is not None:
            result['MinTtl'] = self.min_ttl
        if self.in_clean is not None:
            result['InClean'] = self.in_clean
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.line_type is not None:
            result['LineType'] = self.line_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RecordLineTreeJson') is not None:
            self.record_line_tree_json = m.get('RecordLineTreeJson')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('InBlackHole') is not None:
            self.in_black_hole = m.get('InBlackHole')
        if m.get('RegionLines') is not None:
            self.region_lines = m.get('RegionLines')
        if m.get('SlaveDns') is not None:
            self.slave_dns = m.get('SlaveDns')
        if m.get('AliDomain') is not None:
            self.ali_domain = m.get('AliDomain')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('PunyCode') is not None:
            self.puny_code = m.get('PunyCode')
        if m.get('DnsServers') is not None:
            temp_model = DescribeDomainInfoResponseBodyDnsServers()
            self.dns_servers = temp_model.from_map(m['DnsServers'])
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('RecordLines') is not None:
            temp_model = DescribeDomainInfoResponseBodyRecordLines()
            self.record_lines = temp_model.from_map(m['RecordLines'])
        if m.get('DomainId') is not None:
            self.domain_id = m.get('DomainId')
        if m.get('AvailableTtls') is not None:
            temp_model = DescribeDomainInfoResponseBodyAvailableTtls()
            self.available_ttls = temp_model.from_map(m['AvailableTtls'])
        if m.get('MinTtl') is not None:
            self.min_ttl = m.get('MinTtl')
        if m.get('InClean') is not None:
            self.in_clean = m.get('InClean')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('LineType') is not None:
            self.line_type = m.get('LineType')
        return self


class DescribeDomainInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainLogsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        key_word: str = None,
        group_id: str = None,
        page_number: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.key_word = key_word
        self.group_id = group_id
        self.page_number = page_number
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['endDate'] = self.end_date
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('endDate') is not None:
            self.end_date = m.get('endDate')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class DescribeDomainLogsResponseBodyDomainLogsDomainLog(TeaModel):
    def __init__(
        self,
        action: str = None,
        action_timestamp: int = None,
        zone_id: str = None,
        client_ip: str = None,
        message: str = None,
        action_time: str = None,
        domain_name: str = None,
    ):
        self.action = action
        self.action_timestamp = action_timestamp
        self.zone_id = zone_id
        self.client_ip = client_ip
        self.message = message
        self.action_time = action_time
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.action_timestamp is not None:
            result['ActionTimestamp'] = self.action_timestamp
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.client_ip is not None:
            result['ClientIp'] = self.client_ip
        if self.message is not None:
            result['Message'] = self.message
        if self.action_time is not None:
            result['ActionTime'] = self.action_time
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('ActionTimestamp') is not None:
            self.action_timestamp = m.get('ActionTimestamp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ClientIp') is not None:
            self.client_ip = m.get('ClientIp')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('ActionTime') is not None:
            self.action_time = m.get('ActionTime')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeDomainLogsResponseBodyDomainLogs(TeaModel):
    def __init__(
        self,
        domain_log: List[DescribeDomainLogsResponseBodyDomainLogsDomainLog] = None,
    ):
        self.domain_log = domain_log

    def validate(self):
        if self.domain_log:
            for k in self.domain_log:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainLog'] = []
        if self.domain_log is not None:
            for k in self.domain_log:
                result['DomainLog'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_log = []
        if m.get('DomainLog') is not None:
            for k in m.get('DomainLog'):
                temp_model = DescribeDomainLogsResponseBodyDomainLogsDomainLog()
                self.domain_log.append(temp_model.from_map(k))
        return self


class DescribeDomainLogsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        domain_logs: DescribeDomainLogsResponseBodyDomainLogs = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.domain_logs = domain_logs

    def validate(self):
        if self.domain_logs:
            self.domain_logs.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.domain_logs is not None:
            result['DomainLogs'] = self.domain_logs.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('DomainLogs') is not None:
            temp_model = DescribeDomainLogsResponseBodyDomainLogs()
            self.domain_logs = temp_model.from_map(m['DomainLogs'])
        return self


class DescribeDomainLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainNsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        domain_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeDomainNsResponseBodyExpectDnsServers(TeaModel):
    def __init__(
        self,
        expect_dns_server: List[str] = None,
    ):
        self.expect_dns_server = expect_dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.expect_dns_server is not None:
            result['ExpectDnsServer'] = self.expect_dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpectDnsServer') is not None:
            self.expect_dns_server = m.get('ExpectDnsServer')
        return self


class DescribeDomainNsResponseBodyDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class DescribeDomainNsResponseBody(TeaModel):
    def __init__(
        self,
        all_ali_dns: bool = None,
        request_id: str = None,
        expect_dns_servers: DescribeDomainNsResponseBodyExpectDnsServers = None,
        dns_servers: DescribeDomainNsResponseBodyDnsServers = None,
        include_ali_dns: bool = None,
    ):
        self.all_ali_dns = all_ali_dns
        self.request_id = request_id
        self.expect_dns_servers = expect_dns_servers
        self.dns_servers = dns_servers
        self.include_ali_dns = include_ali_dns

    def validate(self):
        if self.expect_dns_servers:
            self.expect_dns_servers.validate()
        if self.dns_servers:
            self.dns_servers.validate()

    def to_map(self):
        result = dict()
        if self.all_ali_dns is not None:
            result['AllAliDns'] = self.all_ali_dns
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.expect_dns_servers is not None:
            result['ExpectDnsServers'] = self.expect_dns_servers.to_map()
        if self.dns_servers is not None:
            result['DnsServers'] = self.dns_servers.to_map()
        if self.include_ali_dns is not None:
            result['IncludeAliDns'] = self.include_ali_dns
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllAliDns') is not None:
            self.all_ali_dns = m.get('AllAliDns')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ExpectDnsServers') is not None:
            temp_model = DescribeDomainNsResponseBodyExpectDnsServers()
            self.expect_dns_servers = temp_model.from_map(m['ExpectDnsServers'])
        if m.get('DnsServers') is not None:
            temp_model = DescribeDomainNsResponseBodyDnsServers()
            self.dns_servers = temp_model.from_map(m['DnsServers'])
        if m.get('IncludeAliDns') is not None:
            self.include_ali_dns = m.get('IncludeAliDns')
        return self


class DescribeDomainNsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainNsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainNsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainRecordInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class DescribeDomainRecordInfoResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        rr: str = None,
        group_name: str = None,
        request_id: str = None,
        domain_name: str = None,
        priority: int = None,
        puny_code: str = None,
        ttl: int = None,
        group_id: str = None,
        line: str = None,
        locked: bool = None,
        type: str = None,
        domain_id: str = None,
        value: str = None,
        record_id: str = None,
    ):
        self.status = status
        self.rr = rr
        self.group_name = group_name
        self.request_id = request_id
        self.domain_name = domain_name
        self.priority = priority
        self.puny_code = puny_code
        self.ttl = ttl
        self.group_id = group_id
        self.line = line
        self.locked = locked
        self.type = type
        self.domain_id = domain_id
        self.value = value
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.rr is not None:
            result['RR'] = self.rr
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.puny_code is not None:
            result['PunyCode'] = self.puny_code
        if self.ttl is not None:
            result['TTL'] = self.ttl
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.line is not None:
            result['Line'] = self.line
        if self.locked is not None:
            result['Locked'] = self.locked
        if self.type is not None:
            result['Type'] = self.type
        if self.domain_id is not None:
            result['DomainId'] = self.domain_id
        if self.value is not None:
            result['Value'] = self.value
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('PunyCode') is not None:
            self.puny_code = m.get('PunyCode')
        if m.get('TTL') is not None:
            self.ttl = m.get('TTL')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Locked') is not None:
            self.locked = m.get('Locked')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('DomainId') is not None:
            self.domain_id = m.get('DomainId')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class DescribeDomainRecordInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainRecordInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainRecordInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainRecordsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        page_number: int = None,
        page_size: int = None,
        key_word: str = None,
        rrkey_word: str = None,
        type_key_word: str = None,
        value_key_word: str = None,
        order_by: str = None,
        direction: str = None,
        search_mode: str = None,
        group_id: int = None,
        type: str = None,
        line: str = None,
        status: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.page_number = page_number
        self.page_size = page_size
        self.key_word = key_word
        self.rrkey_word = rrkey_word
        self.type_key_word = type_key_word
        self.value_key_word = value_key_word
        self.order_by = order_by
        self.direction = direction
        self.search_mode = search_mode
        self.group_id = group_id
        self.type = type
        self.line = line
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.rrkey_word is not None:
            result['RRKeyWord'] = self.rrkey_word
        if self.type_key_word is not None:
            result['TypeKeyWord'] = self.type_key_word
        if self.value_key_word is not None:
            result['ValueKeyWord'] = self.value_key_word
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.type is not None:
            result['Type'] = self.type
        if self.line is not None:
            result['Line'] = self.line
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('RRKeyWord') is not None:
            self.rrkey_word = m.get('RRKeyWord')
        if m.get('TypeKeyWord') is not None:
            self.type_key_word = m.get('TypeKeyWord')
        if m.get('ValueKeyWord') is not None:
            self.value_key_word = m.get('ValueKeyWord')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeDomainRecordsResponseBodyDomainRecordsRecord(TeaModel):
    def __init__(
        self,
        status: str = None,
        type: str = None,
        remark: str = None,
        ttl: int = None,
        record_id: str = None,
        priority: int = None,
        rr: str = None,
        domain_name: str = None,
        weight: int = None,
        value: str = None,
        line: str = None,
        locked: bool = None,
    ):
        self.status = status
        self.type = type
        self.remark = remark
        self.ttl = ttl
        self.record_id = record_id
        self.priority = priority
        self.rr = rr
        self.domain_name = domain_name
        self.weight = weight
        self.value = value
        self.line = line
        self.locked = locked

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.type is not None:
            result['Type'] = self.type
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.ttl is not None:
            result['TTL'] = self.ttl
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.rr is not None:
            result['RR'] = self.rr
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.value is not None:
            result['Value'] = self.value
        if self.line is not None:
            result['Line'] = self.line
        if self.locked is not None:
            result['Locked'] = self.locked
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('TTL') is not None:
            self.ttl = m.get('TTL')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Locked') is not None:
            self.locked = m.get('Locked')
        return self


class DescribeDomainRecordsResponseBodyDomainRecords(TeaModel):
    def __init__(
        self,
        record: List[DescribeDomainRecordsResponseBodyDomainRecordsRecord] = None,
    ):
        self.record = record

    def validate(self):
        if self.record:
            for k in self.record:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Record'] = []
        if self.record is not None:
            for k in self.record:
                result['Record'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record = []
        if m.get('Record') is not None:
            for k in m.get('Record'):
                temp_model = DescribeDomainRecordsResponseBodyDomainRecordsRecord()
                self.record.append(temp_model.from_map(k))
        return self


class DescribeDomainRecordsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        domain_records: DescribeDomainRecordsResponseBodyDomainRecords = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.domain_records = domain_records
        self.page_number = page_number

    def validate(self):
        if self.domain_records:
            self.domain_records.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_records is not None:
            result['DomainRecords'] = self.domain_records.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainRecords') is not None:
            temp_model = DescribeDomainRecordsResponseBodyDomainRecords()
            self.domain_records = temp_model.from_map(m['DomainRecords'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeDomainRecordsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainRecordsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainRecordsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainsRequestTag(TeaModel):
    def __init__(self):
        pass

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        return self


class DescribeDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        key_word: str = None,
        group_id: str = None,
        page_number: int = None,
        page_size: int = None,
        search_mode: str = None,
        resource_group_id: str = None,
        order_by: str = None,
        direction: str = None,
        starmark: bool = None,
        start_date: str = None,
        end_date: str = None,
        tag: List[DescribeDomainsRequestTag] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.key_word = key_word
        self.group_id = group_id
        self.page_number = page_number
        self.page_size = page_size
        self.search_mode = search_mode
        self.resource_group_id = resource_group_id
        self.order_by = order_by
        self.direction = direction
        self.starmark = starmark
        self.start_date = start_date
        self.end_date = end_date
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.starmark is not None:
            result['Starmark'] = self.starmark
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('Starmark') is not None:
            self.starmark = m.get('Starmark')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeDomainsRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class DescribeDomainsResponseBodyDomainsDomainTagsTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeDomainsResponseBodyDomainsDomainTags(TeaModel):
    def __init__(
        self,
        tag: List[DescribeDomainsResponseBodyDomainsDomainTagsTag] = None,
    ):
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeDomainsResponseBodyDomainsDomainTagsTag()
                self.tag.append(temp_model.from_map(k))
        return self


class DescribeDomainsResponseBodyDomainsDomainDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class DescribeDomainsResponseBodyDomainsDomain(TeaModel):
    def __init__(
        self,
        remark: str = None,
        create_time: str = None,
        record_count: int = None,
        tags: DescribeDomainsResponseBodyDomainsDomainTags = None,
        instance_id: str = None,
        domain_name: str = None,
        domain_id: str = None,
        ali_domain: bool = None,
        group_id: str = None,
        group_name: str = None,
        resource_group_id: str = None,
        instance_end_time: str = None,
        instance_expired: bool = None,
        version_name: str = None,
        dns_servers: DescribeDomainsResponseBodyDomainsDomainDnsServers = None,
        version_code: str = None,
        puny_code: str = None,
        registrant_email: str = None,
        create_timestamp: int = None,
        starmark: bool = None,
    ):
        self.remark = remark
        self.create_time = create_time
        self.record_count = record_count
        self.tags = tags
        self.instance_id = instance_id
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.ali_domain = ali_domain
        self.group_id = group_id
        self.group_name = group_name
        self.resource_group_id = resource_group_id
        self.instance_end_time = instance_end_time
        self.instance_expired = instance_expired
        self.version_name = version_name
        self.dns_servers = dns_servers
        self.version_code = version_code
        self.puny_code = puny_code
        self.registrant_email = registrant_email
        self.create_timestamp = create_timestamp
        self.starmark = starmark

    def validate(self):
        if self.tags:
            self.tags.validate()
        if self.dns_servers:
            self.dns_servers.validate()

    def to_map(self):
        result = dict()
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.tags is not None:
            result['Tags'] = self.tags.to_map()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.domain_id is not None:
            result['DomainId'] = self.domain_id
        if self.ali_domain is not None:
            result['AliDomain'] = self.ali_domain
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.instance_end_time is not None:
            result['InstanceEndTime'] = self.instance_end_time
        if self.instance_expired is not None:
            result['InstanceExpired'] = self.instance_expired
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.dns_servers is not None:
            result['DnsServers'] = self.dns_servers.to_map()
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.puny_code is not None:
            result['PunyCode'] = self.puny_code
        if self.registrant_email is not None:
            result['RegistrantEmail'] = self.registrant_email
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.starmark is not None:
            result['Starmark'] = self.starmark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Tags') is not None:
            temp_model = DescribeDomainsResponseBodyDomainsDomainTags()
            self.tags = temp_model.from_map(m['Tags'])
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('DomainId') is not None:
            self.domain_id = m.get('DomainId')
        if m.get('AliDomain') is not None:
            self.ali_domain = m.get('AliDomain')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('InstanceEndTime') is not None:
            self.instance_end_time = m.get('InstanceEndTime')
        if m.get('InstanceExpired') is not None:
            self.instance_expired = m.get('InstanceExpired')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('DnsServers') is not None:
            temp_model = DescribeDomainsResponseBodyDomainsDomainDnsServers()
            self.dns_servers = temp_model.from_map(m['DnsServers'])
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('PunyCode') is not None:
            self.puny_code = m.get('PunyCode')
        if m.get('RegistrantEmail') is not None:
            self.registrant_email = m.get('RegistrantEmail')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Starmark') is not None:
            self.starmark = m.get('Starmark')
        return self


class DescribeDomainsResponseBodyDomains(TeaModel):
    def __init__(
        self,
        domain: List[DescribeDomainsResponseBodyDomainsDomain] = None,
    ):
        self.domain = domain

    def validate(self):
        if self.domain:
            for k in self.domain:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Domain'] = []
        if self.domain is not None:
            for k in self.domain:
                result['Domain'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain = []
        if m.get('Domain') is not None:
            for k in m.get('Domain'):
                temp_model = DescribeDomainsResponseBodyDomainsDomain()
                self.domain.append(temp_model.from_map(k))
        return self


class DescribeDomainsResponseBody(TeaModel):
    def __init__(
        self,
        domains: DescribeDomainsResponseBodyDomains = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.domains = domains
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.domains:
            self.domains.validate()

    def to_map(self):
        result = dict()
        if self.domains is not None:
            result['Domains'] = self.domains.to_map()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Domains') is not None:
            temp_model = DescribeDomainsResponseBodyDomains()
            self.domains = temp_model.from_map(m['Domains'])
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainStatisticsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        start_date: str = None,
        end_date: str = None,
        domain_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.start_date = start_date
        self.end_date = end_date
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeDomainStatisticsResponseBodyStatisticsStatistic(TeaModel):
    def __init__(
        self,
        timestamp: int = None,
        count: int = None,
    ):
        self.timestamp = timestamp
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeDomainStatisticsResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        statistic: List[DescribeDomainStatisticsResponseBodyStatisticsStatistic] = None,
    ):
        self.statistic = statistic

    def validate(self):
        if self.statistic:
            for k in self.statistic:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Statistic'] = []
        if self.statistic is not None:
            for k in self.statistic:
                result['Statistic'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.statistic = []
        if m.get('Statistic') is not None:
            for k in m.get('Statistic'):
                temp_model = DescribeDomainStatisticsResponseBodyStatisticsStatistic()
                self.statistic.append(temp_model.from_map(k))
        return self


class DescribeDomainStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: DescribeDomainStatisticsResponseBodyStatistics = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            self.statistics.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            temp_model = DescribeDomainStatisticsResponseBodyStatistics()
            self.statistics = temp_model.from_map(m['Statistics'])
        return self


class DescribeDomainStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDomainStatisticsSummaryRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        order_by: str = None,
        direction: str = None,
        search_mode: str = None,
        keyword: str = None,
        threshold: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.order_by = order_by
        self.direction = direction
        self.search_mode = search_mode
        self.keyword = keyword
        self.threshold = threshold

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        return self


class DescribeDomainStatisticsSummaryResponseBodyStatisticsStatistic(TeaModel):
    def __init__(
        self,
        domain_name: str = None,
        count: int = None,
        domain_type: str = None,
    ):
        self.domain_name = domain_name
        self.count = count
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.count is not None:
            result['Count'] = self.count
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeDomainStatisticsSummaryResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        statistic: List[DescribeDomainStatisticsSummaryResponseBodyStatisticsStatistic] = None,
    ):
        self.statistic = statistic

    def validate(self):
        if self.statistic:
            for k in self.statistic:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Statistic'] = []
        if self.statistic is not None:
            for k in self.statistic:
                result['Statistic'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.statistic = []
        if m.get('Statistic') is not None:
            for k in m.get('Statistic'):
                temp_model = DescribeDomainStatisticsSummaryResponseBodyStatisticsStatistic()
                self.statistic.append(temp_model.from_map(k))
        return self


class DescribeDomainStatisticsSummaryResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        statistics: DescribeDomainStatisticsSummaryResponseBodyStatistics = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            self.statistics.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.statistics is not None:
            result['Statistics'] = self.statistics.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('Statistics') is not None:
            temp_model = DescribeDomainStatisticsSummaryResponseBodyStatistics()
            self.statistics = temp_model.from_map(m['Statistics'])
        return self


class DescribeDomainStatisticsSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDomainStatisticsSummaryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDomainStatisticsSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmAccessStrategiesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeGtmAccessStrategiesResponseBodyStrategiesStrategy(TeaModel):
    def __init__(
        self,
        access_mode: str = None,
        strategy_name: str = None,
        default_addr_pool_monitor_status: str = None,
        strategy_mode: str = None,
        create_time: str = None,
        default_addr_pool_status: str = None,
        instance_id: str = None,
        lines: DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLines = None,
        failover_addr_pool_id: str = None,
        default_addr_pool_id: str = None,
        strategy_id: str = None,
        failover_addr_pool_status: str = None,
        access_status: str = None,
        failover_addr_pool_monitor_status: str = None,
        default_addr_pool_name: str = None,
        failover_addr_pool_name: str = None,
        create_timestamp: int = None,
    ):
        self.access_mode = access_mode
        self.strategy_name = strategy_name
        self.default_addr_pool_monitor_status = default_addr_pool_monitor_status
        self.strategy_mode = strategy_mode
        self.create_time = create_time
        self.default_addr_pool_status = default_addr_pool_status
        self.instance_id = instance_id
        self.lines = lines
        self.failover_addr_pool_id = failover_addr_pool_id
        self.default_addr_pool_id = default_addr_pool_id
        self.strategy_id = strategy_id
        self.failover_addr_pool_status = failover_addr_pool_status
        self.access_status = access_status
        self.failover_addr_pool_monitor_status = failover_addr_pool_monitor_status
        self.default_addr_pool_name = default_addr_pool_name
        self.failover_addr_pool_name = failover_addr_pool_name
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.access_mode is not None:
            result['AccessMode'] = self.access_mode
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.default_addr_pool_monitor_status is not None:
            result['DefaultAddrPoolMonitorStatus'] = self.default_addr_pool_monitor_status
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.default_addr_pool_status is not None:
            result['DefaultAddrPoolStatus'] = self.default_addr_pool_status
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        if self.failover_addr_pool_id is not None:
            result['FailoverAddrPoolId'] = self.failover_addr_pool_id
        if self.default_addr_pool_id is not None:
            result['DefaultAddrPoolId'] = self.default_addr_pool_id
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.failover_addr_pool_status is not None:
            result['FailoverAddrPoolStatus'] = self.failover_addr_pool_status
        if self.access_status is not None:
            result['AccessStatus'] = self.access_status
        if self.failover_addr_pool_monitor_status is not None:
            result['FailoverAddrPoolMonitorStatus'] = self.failover_addr_pool_monitor_status
        if self.default_addr_pool_name is not None:
            result['DefaultAddrPoolName'] = self.default_addr_pool_name
        if self.failover_addr_pool_name is not None:
            result['FailoverAddrPoolName'] = self.failover_addr_pool_name
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccessMode') is not None:
            self.access_mode = m.get('AccessMode')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('DefaultAddrPoolMonitorStatus') is not None:
            self.default_addr_pool_monitor_status = m.get('DefaultAddrPoolMonitorStatus')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DefaultAddrPoolStatus') is not None:
            self.default_addr_pool_status = m.get('DefaultAddrPoolStatus')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Lines') is not None:
            temp_model = DescribeGtmAccessStrategiesResponseBodyStrategiesStrategyLines()
            self.lines = temp_model.from_map(m['Lines'])
        if m.get('FailoverAddrPoolId') is not None:
            self.failover_addr_pool_id = m.get('FailoverAddrPoolId')
        if m.get('DefaultAddrPoolId') is not None:
            self.default_addr_pool_id = m.get('DefaultAddrPoolId')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('FailoverAddrPoolStatus') is not None:
            self.failover_addr_pool_status = m.get('FailoverAddrPoolStatus')
        if m.get('AccessStatus') is not None:
            self.access_status = m.get('AccessStatus')
        if m.get('FailoverAddrPoolMonitorStatus') is not None:
            self.failover_addr_pool_monitor_status = m.get('FailoverAddrPoolMonitorStatus')
        if m.get('DefaultAddrPoolName') is not None:
            self.default_addr_pool_name = m.get('DefaultAddrPoolName')
        if m.get('FailoverAddrPoolName') is not None:
            self.failover_addr_pool_name = m.get('FailoverAddrPoolName')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmAccessStrategiesResponseBodyStrategies(TeaModel):
    def __init__(
        self,
        strategy: List[DescribeGtmAccessStrategiesResponseBodyStrategiesStrategy] = None,
    ):
        self.strategy = strategy

    def validate(self):
        if self.strategy:
            for k in self.strategy:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Strategy'] = []
        if self.strategy is not None:
            for k in self.strategy:
                result['Strategy'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.strategy = []
        if m.get('Strategy') is not None:
            for k in m.get('Strategy'):
                temp_model = DescribeGtmAccessStrategiesResponseBodyStrategiesStrategy()
                self.strategy.append(temp_model.from_map(k))
        return self


class DescribeGtmAccessStrategiesResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        strategies: DescribeGtmAccessStrategiesResponseBodyStrategies = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.strategies = strategies
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.strategies:
            self.strategies.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.strategies is not None:
            result['Strategies'] = self.strategies.to_map()
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Strategies') is not None:
            temp_model = DescribeGtmAccessStrategiesResponseBodyStrategies()
            self.strategies = temp_model.from_map(m['Strategies'])
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeGtmAccessStrategiesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmAccessStrategiesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmAccessStrategiesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class DescribeGtmAccessStrategyResponseBodyLinesLine(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        line_code: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.group_name = group_name
        self.line_code = line_code
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeGtmAccessStrategyResponseBodyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeGtmAccessStrategyResponseBodyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeGtmAccessStrategyResponseBodyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        instance_id: str = None,
        strategy_id: str = None,
        default_addr_pool_status: str = None,
        failover_addr_pool_id: str = None,
        access_status: str = None,
        default_addr_pool_monitor_status: str = None,
        default_addr_pool_name: str = None,
        defult_addr_pool_id: str = None,
        strategy_name: str = None,
        failover_addr_pool_status: str = None,
        access_mode: str = None,
        strategy_mode: str = None,
        failover_addr_pool_monitor_status: str = None,
        failover_addr_pool_name: str = None,
        lines: DescribeGtmAccessStrategyResponseBodyLines = None,
    ):
        self.request_id = request_id
        self.instance_id = instance_id
        self.strategy_id = strategy_id
        self.default_addr_pool_status = default_addr_pool_status
        self.failover_addr_pool_id = failover_addr_pool_id
        self.access_status = access_status
        self.default_addr_pool_monitor_status = default_addr_pool_monitor_status
        self.default_addr_pool_name = default_addr_pool_name
        self.defult_addr_pool_id = defult_addr_pool_id
        self.strategy_name = strategy_name
        self.failover_addr_pool_status = failover_addr_pool_status
        self.access_mode = access_mode
        self.strategy_mode = strategy_mode
        self.failover_addr_pool_monitor_status = failover_addr_pool_monitor_status
        self.failover_addr_pool_name = failover_addr_pool_name
        self.lines = lines

    def validate(self):
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.default_addr_pool_status is not None:
            result['DefaultAddrPoolStatus'] = self.default_addr_pool_status
        if self.failover_addr_pool_id is not None:
            result['FailoverAddrPoolId'] = self.failover_addr_pool_id
        if self.access_status is not None:
            result['AccessStatus'] = self.access_status
        if self.default_addr_pool_monitor_status is not None:
            result['DefaultAddrPoolMonitorStatus'] = self.default_addr_pool_monitor_status
        if self.default_addr_pool_name is not None:
            result['DefaultAddrPoolName'] = self.default_addr_pool_name
        if self.defult_addr_pool_id is not None:
            result['DefultAddrPoolId'] = self.defult_addr_pool_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.failover_addr_pool_status is not None:
            result['FailoverAddrPoolStatus'] = self.failover_addr_pool_status
        if self.access_mode is not None:
            result['AccessMode'] = self.access_mode
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        if self.failover_addr_pool_monitor_status is not None:
            result['FailoverAddrPoolMonitorStatus'] = self.failover_addr_pool_monitor_status
        if self.failover_addr_pool_name is not None:
            result['FailoverAddrPoolName'] = self.failover_addr_pool_name
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('DefaultAddrPoolStatus') is not None:
            self.default_addr_pool_status = m.get('DefaultAddrPoolStatus')
        if m.get('FailoverAddrPoolId') is not None:
            self.failover_addr_pool_id = m.get('FailoverAddrPoolId')
        if m.get('AccessStatus') is not None:
            self.access_status = m.get('AccessStatus')
        if m.get('DefaultAddrPoolMonitorStatus') is not None:
            self.default_addr_pool_monitor_status = m.get('DefaultAddrPoolMonitorStatus')
        if m.get('DefaultAddrPoolName') is not None:
            self.default_addr_pool_name = m.get('DefaultAddrPoolName')
        if m.get('DefultAddrPoolId') is not None:
            self.defult_addr_pool_id = m.get('DefultAddrPoolId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('FailoverAddrPoolStatus') is not None:
            self.failover_addr_pool_status = m.get('FailoverAddrPoolStatus')
        if m.get('AccessMode') is not None:
            self.access_mode = m.get('AccessMode')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        if m.get('FailoverAddrPoolMonitorStatus') is not None:
            self.failover_addr_pool_monitor_status = m.get('FailoverAddrPoolMonitorStatus')
        if m.get('FailoverAddrPoolName') is not None:
            self.failover_addr_pool_name = m.get('FailoverAddrPoolName')
        if m.get('Lines') is not None:
            temp_model = DescribeGtmAccessStrategyResponseBodyLines()
            self.lines = temp_model.from_map(m['Lines'])
        return self


class DescribeGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmAccessStrategyAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPoolsAddrPool(TeaModel):
    def __init__(
        self,
        addr_pool_id: str = None,
        addr_pool_name: str = None,
    ):
        self.addr_pool_id = addr_pool_id
        self.addr_pool_name = addr_pool_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.addr_pool_name is not None:
            result['AddrPoolName'] = self.addr_pool_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('AddrPoolName') is not None:
            self.addr_pool_name = m.get('AddrPoolName')
        return self


class DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPools(TeaModel):
    def __init__(
        self,
        addr_pool: List[DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPoolsAddrPool] = None,
    ):
        self.addr_pool = addr_pool

    def validate(self):
        if self.addr_pool:
            for k in self.addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AddrPool'] = []
        if self.addr_pool is not None:
            for k in self.addr_pool:
                result['AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr_pool = []
        if m.get('AddrPool') is not None:
            for k in m.get('AddrPool'):
                temp_model = DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPoolsAddrPool()
                self.addr_pool.append(temp_model.from_map(k))
        return self


class DescribeGtmAccessStrategyAvailableConfigResponseBodyLinesLine(TeaModel):
    def __init__(
        self,
        status: str = None,
        father_code: str = None,
        line_code: str = None,
        group_name: str = None,
        line_name: str = None,
        group_code: str = None,
    ):
        self.status = status
        self.father_code = father_code
        self.line_code = line_code
        self.group_name = group_name
        self.line_name = line_name
        self.group_code = group_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.group_code is not None:
            result['GroupCode'] = self.group_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('GroupCode') is not None:
            self.group_code = m.get('GroupCode')
        return self


class DescribeGtmAccessStrategyAvailableConfigResponseBodyLines(TeaModel):
    def __init__(
        self,
        line: List[DescribeGtmAccessStrategyAvailableConfigResponseBodyLinesLine] = None,
    ):
        self.line = line

    def validate(self):
        if self.line:
            for k in self.line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Line'] = []
        if self.line is not None:
            for k in self.line:
                result['Line'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.line = []
        if m.get('Line') is not None:
            for k in m.get('Line'):
                temp_model = DescribeGtmAccessStrategyAvailableConfigResponseBodyLinesLine()
                self.line.append(temp_model.from_map(k))
        return self


class DescribeGtmAccessStrategyAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        addr_pools: DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPools = None,
        lines: DescribeGtmAccessStrategyAvailableConfigResponseBodyLines = None,
    ):
        self.request_id = request_id
        self.addr_pools = addr_pools
        self.lines = lines

    def validate(self):
        if self.addr_pools:
            self.addr_pools.validate()
        if self.lines:
            self.lines.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.addr_pools is not None:
            result['AddrPools'] = self.addr_pools.to_map()
        if self.lines is not None:
            result['Lines'] = self.lines.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AddrPools') is not None:
            temp_model = DescribeGtmAccessStrategyAvailableConfigResponseBodyAddrPools()
            self.addr_pools = temp_model.from_map(m['AddrPools'])
        if m.get('Lines') is not None:
            temp_model = DescribeGtmAccessStrategyAvailableConfigResponseBodyLines()
            self.lines = temp_model.from_map(m['Lines'])
        return self


class DescribeGtmAccessStrategyAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmAccessStrategyAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmAccessStrategyAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmAvailableAlertGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeGtmAvailableAlertGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        available_alert_group: str = None,
    ):
        self.request_id = request_id
        self.available_alert_group = available_alert_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.available_alert_group is not None:
            result['AvailableAlertGroup'] = self.available_alert_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AvailableAlertGroup') is not None:
            self.available_alert_group = m.get('AvailableAlertGroup')
        return self


class DescribeGtmAvailableAlertGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmAvailableAlertGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmAvailableAlertGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstanceRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        need_detail_attributes: bool = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.need_detail_attributes = need_detail_attributes

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.need_detail_attributes is not None:
            result['NeedDetailAttributes'] = self.need_detail_attributes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('NeedDetailAttributes') is not None:
            self.need_detail_attributes = m.get('NeedDetailAttributes')
        return self


class DescribeGtmInstanceResponseBody(TeaModel):
    def __init__(
        self,
        expire_timestamp: int = None,
        user_domain_name: str = None,
        request_id: str = None,
        lba_strategy: str = None,
        instance_id: str = None,
        create_time: str = None,
        cname_mode: str = None,
        ttl: int = None,
        cname: str = None,
        instance_name: str = None,
        version_code: str = None,
        alert_group: str = None,
        address_pool_num: int = None,
        access_strategy_num: int = None,
        expire_time: str = None,
        create_timestamp: int = None,
    ):
        self.expire_timestamp = expire_timestamp
        self.user_domain_name = user_domain_name
        self.request_id = request_id
        self.lba_strategy = lba_strategy
        self.instance_id = instance_id
        self.create_time = create_time
        self.cname_mode = cname_mode
        self.ttl = ttl
        self.cname = cname
        self.instance_name = instance_name
        self.version_code = version_code
        self.alert_group = alert_group
        self.address_pool_num = address_pool_num
        self.access_strategy_num = access_strategy_num
        self.expire_time = expire_time
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.expire_timestamp is not None:
            result['ExpireTimestamp'] = self.expire_timestamp
        if self.user_domain_name is not None:
            result['UserDomainName'] = self.user_domain_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.cname_mode is not None:
            result['CnameMode'] = self.cname_mode
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.cname is not None:
            result['Cname'] = self.cname
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.address_pool_num is not None:
            result['AddressPoolNum'] = self.address_pool_num
        if self.access_strategy_num is not None:
            result['AccessStrategyNum'] = self.access_strategy_num
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpireTimestamp') is not None:
            self.expire_timestamp = m.get('ExpireTimestamp')
        if m.get('UserDomainName') is not None:
            self.user_domain_name = m.get('UserDomainName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CnameMode') is not None:
            self.cname_mode = m.get('CnameMode')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Cname') is not None:
            self.cname = m.get('Cname')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('AddressPoolNum') is not None:
            self.address_pool_num = m.get('AddressPoolNum')
        if m.get('AccessStrategyNum') is not None:
            self.access_strategy_num = m.get('AccessStrategyNum')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstanceAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        return self


class DescribeGtmInstanceAddressPoolResponseBodyAddrsAddr(TeaModel):
    def __init__(
        self,
        value: str = None,
        update_timestamp: int = None,
        update_time: str = None,
        alert_status: str = None,
        lba_weight: int = None,
        create_time: str = None,
        addr_id: int = None,
        mode: str = None,
        create_timestamp: int = None,
    ):
        self.value = value
        self.update_timestamp = update_timestamp
        self.update_time = update_time
        self.alert_status = alert_status
        self.lba_weight = lba_weight
        self.create_time = create_time
        self.addr_id = addr_id
        self.mode = mode
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.alert_status is not None:
            result['AlertStatus'] = self.alert_status
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.addr_id is not None:
            result['AddrId'] = self.addr_id
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('AlertStatus') is not None:
            self.alert_status = m.get('AlertStatus')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('AddrId') is not None:
            self.addr_id = m.get('AddrId')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmInstanceAddressPoolResponseBodyAddrs(TeaModel):
    def __init__(
        self,
        addr: List[DescribeGtmInstanceAddressPoolResponseBodyAddrsAddr] = None,
    ):
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = DescribeGtmInstanceAddressPoolResponseBodyAddrsAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class DescribeGtmInstanceAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        addrs: DescribeGtmInstanceAddressPoolResponseBodyAddrs = None,
        request_id: str = None,
        create_time: str = None,
        addr_count: int = None,
        name: str = None,
        type: str = None,
        update_time: str = None,
        addr_pool_id: str = None,
        update_timestamp: int = None,
        monitor_config_id: str = None,
        min_available_addr_num: int = None,
        monitor_status: str = None,
        create_timestamp: int = None,
    ):
        self.status = status
        self.addrs = addrs
        self.request_id = request_id
        self.create_time = create_time
        self.addr_count = addr_count
        self.name = name
        self.type = type
        self.update_time = update_time
        self.addr_pool_id = addr_pool_id
        self.update_timestamp = update_timestamp
        self.monitor_config_id = monitor_config_id
        self.min_available_addr_num = min_available_addr_num
        self.monitor_status = monitor_status
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.addrs:
            self.addrs.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.addrs is not None:
            result['Addrs'] = self.addrs.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.min_available_addr_num is not None:
            result['MinAvailableAddrNum'] = self.min_available_addr_num
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Addrs') is not None:
            temp_model = DescribeGtmInstanceAddressPoolResponseBodyAddrs()
            self.addrs = temp_model.from_map(m['Addrs'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('MinAvailableAddrNum') is not None:
            self.min_available_addr_num = m.get('MinAvailableAddrNum')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmInstanceAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstanceAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstanceAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstanceAddressPoolsRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool(TeaModel):
    def __init__(
        self,
        type: str = None,
        status: str = None,
        update_time: str = None,
        create_time: str = None,
        monitor_config_id: str = None,
        min_available_addr_num: int = None,
        update_timestamp: int = None,
        monitor_status: str = None,
        addr_pool_id: str = None,
        name: str = None,
        addr_count: int = None,
        create_timestamp: int = None,
    ):
        self.type = type
        self.status = status
        self.update_time = update_time
        self.create_time = create_time
        self.monitor_config_id = monitor_config_id
        self.min_available_addr_num = min_available_addr_num
        self.update_timestamp = update_timestamp
        self.monitor_status = monitor_status
        self.addr_pool_id = addr_pool_id
        self.name = name
        self.addr_count = addr_count
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.status is not None:
            result['Status'] = self.status
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.min_available_addr_num is not None:
            result['MinAvailableAddrNum'] = self.min_available_addr_num
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_status is not None:
            result['MonitorStatus'] = self.monitor_status
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.name is not None:
            result['Name'] = self.name
        if self.addr_count is not None:
            result['AddrCount'] = self.addr_count
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('MinAvailableAddrNum') is not None:
            self.min_available_addr_num = m.get('MinAvailableAddrNum')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorStatus') is not None:
            self.monitor_status = m.get('MonitorStatus')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddrCount') is not None:
            self.addr_count = m.get('AddrCount')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmInstanceAddressPoolsResponseBodyAddrPools(TeaModel):
    def __init__(
        self,
        addr_pool: List[DescribeGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool] = None,
    ):
        self.addr_pool = addr_pool

    def validate(self):
        if self.addr_pool:
            for k in self.addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AddrPool'] = []
        if self.addr_pool is not None:
            for k in self.addr_pool:
                result['AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr_pool = []
        if m.get('AddrPool') is not None:
            for k in m.get('AddrPool'):
                temp_model = DescribeGtmInstanceAddressPoolsResponseBodyAddrPoolsAddrPool()
                self.addr_pool.append(temp_model.from_map(k))
        return self


class DescribeGtmInstanceAddressPoolsResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        addr_pools: DescribeGtmInstanceAddressPoolsResponseBodyAddrPools = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.addr_pools = addr_pools

    def validate(self):
        if self.addr_pools:
            self.addr_pools.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.addr_pools is not None:
            result['AddrPools'] = self.addr_pools.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('AddrPools') is not None:
            temp_model = DescribeGtmInstanceAddressPoolsResponseBodyAddrPools()
            self.addr_pools = temp_model.from_map(m['AddrPools'])
        return self


class DescribeGtmInstanceAddressPoolsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstanceAddressPoolsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstanceAddressPoolsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstancesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        keyword: str = None,
        resource_group_id: str = None,
        need_detail_attributes: bool = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.keyword = keyword
        self.resource_group_id = resource_group_id
        self.need_detail_attributes = need_detail_attributes

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.need_detail_attributes is not None:
            result['NeedDetailAttributes'] = self.need_detail_attributes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('NeedDetailAttributes') is not None:
            self.need_detail_attributes = m.get('NeedDetailAttributes')
        return self


class DescribeGtmInstancesResponseBodyGtmInstancesGtmInstance(TeaModel):
    def __init__(
        self,
        expire_time: str = None,
        access_strategy_num: int = None,
        create_time: str = None,
        cname_mode: str = None,
        instance_id: str = None,
        expire_timestamp: int = None,
        ttl: int = None,
        alert_group: str = None,
        address_pool_num: int = None,
        instance_name: str = None,
        lba_strategy: str = None,
        cname: str = None,
        version_code: str = None,
        user_domain_name: str = None,
        create_timestamp: int = None,
    ):
        self.expire_time = expire_time
        self.access_strategy_num = access_strategy_num
        self.create_time = create_time
        self.cname_mode = cname_mode
        self.instance_id = instance_id
        self.expire_timestamp = expire_timestamp
        self.ttl = ttl
        self.alert_group = alert_group
        self.address_pool_num = address_pool_num
        self.instance_name = instance_name
        self.lba_strategy = lba_strategy
        self.cname = cname
        self.version_code = version_code
        self.user_domain_name = user_domain_name
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.access_strategy_num is not None:
            result['AccessStrategyNum'] = self.access_strategy_num
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.cname_mode is not None:
            result['CnameMode'] = self.cname_mode
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.expire_timestamp is not None:
            result['ExpireTimestamp'] = self.expire_timestamp
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.address_pool_num is not None:
            result['AddressPoolNum'] = self.address_pool_num
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.cname is not None:
            result['Cname'] = self.cname
        if self.version_code is not None:
            result['VersionCode'] = self.version_code
        if self.user_domain_name is not None:
            result['UserDomainName'] = self.user_domain_name
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('AccessStrategyNum') is not None:
            self.access_strategy_num = m.get('AccessStrategyNum')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CnameMode') is not None:
            self.cname_mode = m.get('CnameMode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ExpireTimestamp') is not None:
            self.expire_timestamp = m.get('ExpireTimestamp')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('AddressPoolNum') is not None:
            self.address_pool_num = m.get('AddressPoolNum')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('Cname') is not None:
            self.cname = m.get('Cname')
        if m.get('VersionCode') is not None:
            self.version_code = m.get('VersionCode')
        if m.get('UserDomainName') is not None:
            self.user_domain_name = m.get('UserDomainName')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmInstancesResponseBodyGtmInstances(TeaModel):
    def __init__(
        self,
        gtm_instance: List[DescribeGtmInstancesResponseBodyGtmInstancesGtmInstance] = None,
    ):
        self.gtm_instance = gtm_instance

    def validate(self):
        if self.gtm_instance:
            for k in self.gtm_instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['GtmInstance'] = []
        if self.gtm_instance is not None:
            for k in self.gtm_instance:
                result['GtmInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.gtm_instance = []
        if m.get('GtmInstance') is not None:
            for k in m.get('GtmInstance'):
                temp_model = DescribeGtmInstancesResponseBodyGtmInstancesGtmInstance()
                self.gtm_instance.append(temp_model.from_map(k))
        return self


class DescribeGtmInstancesResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        gtm_instances: DescribeGtmInstancesResponseBodyGtmInstances = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.gtm_instances = gtm_instances
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.gtm_instances:
            self.gtm_instances.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.gtm_instances is not None:
            result['GtmInstances'] = self.gtm_instances.to_map()
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('GtmInstances') is not None:
            temp_model = DescribeGtmInstancesResponseBodyGtmInstances()
            self.gtm_instances = temp_model.from_map(m['GtmInstances'])
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeGtmInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstanceStatusRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeGtmInstanceStatusResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        strategy_not_available_num: int = None,
        request_id: str = None,
        switch_to_failover_strategy_num: int = None,
        status_reason: str = None,
        addr_not_available_num: int = None,
        addr_pool_not_available_num: int = None,
    ):
        self.status = status
        self.strategy_not_available_num = strategy_not_available_num
        self.request_id = request_id
        self.switch_to_failover_strategy_num = switch_to_failover_strategy_num
        self.status_reason = status_reason
        self.addr_not_available_num = addr_not_available_num
        self.addr_pool_not_available_num = addr_pool_not_available_num

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.strategy_not_available_num is not None:
            result['StrategyNotAvailableNum'] = self.strategy_not_available_num
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.switch_to_failover_strategy_num is not None:
            result['SwitchToFailoverStrategyNum'] = self.switch_to_failover_strategy_num
        if self.status_reason is not None:
            result['StatusReason'] = self.status_reason
        if self.addr_not_available_num is not None:
            result['AddrNotAvailableNum'] = self.addr_not_available_num
        if self.addr_pool_not_available_num is not None:
            result['AddrPoolNotAvailableNum'] = self.addr_pool_not_available_num
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('StrategyNotAvailableNum') is not None:
            self.strategy_not_available_num = m.get('StrategyNotAvailableNum')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SwitchToFailoverStrategyNum') is not None:
            self.switch_to_failover_strategy_num = m.get('SwitchToFailoverStrategyNum')
        if m.get('StatusReason') is not None:
            self.status_reason = m.get('StatusReason')
        if m.get('AddrNotAvailableNum') is not None:
            self.addr_not_available_num = m.get('AddrNotAvailableNum')
        if m.get('AddrPoolNotAvailableNum') is not None:
            self.addr_pool_not_available_num = m.get('AddrPoolNotAvailableNum')
        return self


class DescribeGtmInstanceStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstanceStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstanceStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmInstanceSystemCnameRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeGtmInstanceSystemCnameResponseBody(TeaModel):
    def __init__(
        self,
        system_cname: str = None,
        request_id: str = None,
    ):
        self.system_cname = system_cname
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.system_cname is not None:
            result['SystemCname'] = self.system_cname
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SystemCname') is not None:
            self.system_cname = m.get('SystemCname')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeGtmInstanceSystemCnameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmInstanceSystemCnameResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmInstanceSystemCnameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmLogsRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        instance_id: str = None,
        keyword: str = None,
        page_number: int = None,
        page_size: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.instance_id = instance_id
        self.keyword = keyword
        self.page_number = page_number
        self.page_size = page_size
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        return self


class DescribeGtmLogsResponseBodyLogsLog(TeaModel):
    def __init__(
        self,
        oper_timestamp: int = None,
        entity_id: str = None,
        entity_type: str = None,
        oper_time: str = None,
        oper_ip: str = None,
        oper_action: str = None,
        content: str = None,
        entity_name: str = None,
        id: int = None,
    ):
        self.oper_timestamp = oper_timestamp
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.oper_time = oper_time
        self.oper_ip = oper_ip
        self.oper_action = oper_action
        self.content = content
        self.entity_name = entity_name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.oper_timestamp is not None:
            result['OperTimestamp'] = self.oper_timestamp
        if self.entity_id is not None:
            result['EntityId'] = self.entity_id
        if self.entity_type is not None:
            result['EntityType'] = self.entity_type
        if self.oper_time is not None:
            result['OperTime'] = self.oper_time
        if self.oper_ip is not None:
            result['OperIp'] = self.oper_ip
        if self.oper_action is not None:
            result['OperAction'] = self.oper_action
        if self.content is not None:
            result['Content'] = self.content
        if self.entity_name is not None:
            result['EntityName'] = self.entity_name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperTimestamp') is not None:
            self.oper_timestamp = m.get('OperTimestamp')
        if m.get('EntityId') is not None:
            self.entity_id = m.get('EntityId')
        if m.get('EntityType') is not None:
            self.entity_type = m.get('EntityType')
        if m.get('OperTime') is not None:
            self.oper_time = m.get('OperTime')
        if m.get('OperIp') is not None:
            self.oper_ip = m.get('OperIp')
        if m.get('OperAction') is not None:
            self.oper_action = m.get('OperAction')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('EntityName') is not None:
            self.entity_name = m.get('EntityName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeGtmLogsResponseBodyLogs(TeaModel):
    def __init__(
        self,
        log: List[DescribeGtmLogsResponseBodyLogsLog] = None,
    ):
        self.log = log

    def validate(self):
        if self.log:
            for k in self.log:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Log'] = []
        if self.log is not None:
            for k in self.log:
                result['Log'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.log = []
        if m.get('Log') is not None:
            for k in m.get('Log'):
                temp_model = DescribeGtmLogsResponseBodyLogsLog()
                self.log.append(temp_model.from_map(k))
        return self


class DescribeGtmLogsResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        logs: DescribeGtmLogsResponseBodyLogs = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.logs = logs
        self.total_items = total_items

    def validate(self):
        if self.logs:
            self.logs.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.logs is not None:
            result['Logs'] = self.logs.to_map()
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('Logs') is not None:
            temp_model = DescribeGtmLogsResponseBodyLogs()
            self.logs = temp_model.from_map(m['Logs'])
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeGtmLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmMonitorAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        return self


class DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodesIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        mainland: bool = None,
        group_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        isp_name: str = None,
        group_type: str = None,
        default_selected: bool = None,
    ):
        self.city_code = city_code
        self.mainland = mainland
        self.group_name = group_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.isp_name = isp_name
        self.group_type = group_type
        self.default_selected = default_selected

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.mainland is not None:
            result['Mainland'] = self.mainland
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.group_type is not None:
            result['GroupType'] = self.group_type
        if self.default_selected is not None:
            result['DefaultSelected'] = self.default_selected
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('Mainland') is not None:
            self.mainland = m.get('Mainland')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('GroupType') is not None:
            self.group_type = m.get('GroupType')
        if m.get('DefaultSelected') is not None:
            self.default_selected = m.get('DefaultSelected')
        return self


class DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodes(TeaModel):
    def __init__(
        self,
        isp_city_node: List[DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodesIspCityNode] = None,
    ):
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodesIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeGtmMonitorAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        isp_city_nodes: DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodes = None,
    ):
        self.request_id = request_id
        self.isp_city_nodes = isp_city_nodes

    def validate(self):
        if self.isp_city_nodes:
            self.isp_city_nodes.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.isp_city_nodes is not None:
            result['IspCityNodes'] = self.isp_city_nodes.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('IspCityNodes') is not None:
            temp_model = DescribeGtmMonitorAvailableConfigResponseBodyIspCityNodes()
            self.isp_city_nodes = temp_model.from_map(m['IspCityNodes'])
        return self


class DescribeGtmMonitorAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmMonitorAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmMonitorAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmMonitorConfigRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        return self


class DescribeGtmMonitorConfigResponseBodyIspCityNodesIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        country_name: str = None,
        isp_code: str = None,
        city_name: str = None,
        country_code: str = None,
        isp_name: str = None,
    ):
        self.city_code = city_code
        self.country_name = country_name
        self.isp_code = isp_code
        self.city_name = city_name
        self.country_code = country_code
        self.isp_name = isp_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.country_name is not None:
            result['CountryName'] = self.country_name
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.country_code is not None:
            result['CountryCode'] = self.country_code
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('CountryName') is not None:
            self.country_name = m.get('CountryName')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('CountryCode') is not None:
            self.country_code = m.get('CountryCode')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        return self


class DescribeGtmMonitorConfigResponseBodyIspCityNodes(TeaModel):
    def __init__(
        self,
        isp_city_node: List[DescribeGtmMonitorConfigResponseBodyIspCityNodesIspCityNode] = None,
    ):
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = DescribeGtmMonitorConfigResponseBodyIspCityNodesIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class DescribeGtmMonitorConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        timeout: int = None,
        protocol_type: str = None,
        isp_city_nodes: DescribeGtmMonitorConfigResponseBodyIspCityNodes = None,
        create_time: str = None,
        update_time: str = None,
        evaluation_count: int = None,
        update_timestamp: int = None,
        monitor_extend_info: str = None,
        monitor_config_id: str = None,
        create_timestamp: int = None,
        interval: int = None,
    ):
        self.request_id = request_id
        self.timeout = timeout
        self.protocol_type = protocol_type
        self.isp_city_nodes = isp_city_nodes
        self.create_time = create_time
        self.update_time = update_time
        self.evaluation_count = evaluation_count
        self.update_timestamp = update_timestamp
        self.monitor_extend_info = monitor_extend_info
        self.monitor_config_id = monitor_config_id
        self.create_timestamp = create_timestamp
        self.interval = interval

    def validate(self):
        if self.isp_city_nodes:
            self.isp_city_nodes.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.isp_city_nodes is not None:
            result['IspCityNodes'] = self.isp_city_nodes.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.interval is not None:
            result['Interval'] = self.interval
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('IspCityNodes') is not None:
            temp_model = DescribeGtmMonitorConfigResponseBodyIspCityNodes()
            self.isp_city_nodes = temp_model.from_map(m['IspCityNodes'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        return self


class DescribeGtmMonitorConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmMonitorConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmMonitorConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        recovery_plan_id: int = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.recovery_plan_id = recovery_plan_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        return self


class DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrsAddr(TeaModel):
    def __init__(
        self,
        value: str = None,
        mode: str = None,
        id: int = None,
    ):
        self.value = value
        self.mode = mode
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrs(TeaModel):
    def __init__(
        self,
        addr: List[DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrsAddr] = None,
    ):
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrsAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPool(TeaModel):
    def __init__(
        self,
        addrs: DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrs = None,
        addr_pool_id: str = None,
        instance_id: str = None,
        addr_pool_name: str = None,
    ):
        self.addrs = addrs
        self.addr_pool_id = addr_pool_id
        self.instance_id = instance_id
        self.addr_pool_name = addr_pool_name

    def validate(self):
        if self.addrs:
            self.addrs.validate()

    def to_map(self):
        result = dict()
        if self.addrs is not None:
            result['Addrs'] = self.addrs.to_map()
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.addr_pool_name is not None:
            result['AddrPoolName'] = self.addr_pool_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Addrs') is not None:
            temp_model = DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPoolAddrs()
            self.addrs = temp_model.from_map(m['Addrs'])
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('AddrPoolName') is not None:
            self.addr_pool_name = m.get('AddrPoolName')
        return self


class DescribeGtmRecoveryPlanResponseBodyFaultAddrPools(TeaModel):
    def __init__(
        self,
        fault_addr_pool: List[DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPool] = None,
    ):
        self.fault_addr_pool = fault_addr_pool

    def validate(self):
        if self.fault_addr_pool:
            for k in self.fault_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['FaultAddrPool'] = []
        if self.fault_addr_pool is not None:
            for k in self.fault_addr_pool:
                result['FaultAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.fault_addr_pool = []
        if m.get('FaultAddrPool') is not None:
            for k in m.get('FaultAddrPool'):
                temp_model = DescribeGtmRecoveryPlanResponseBodyFaultAddrPoolsFaultAddrPool()
                self.fault_addr_pool.append(temp_model.from_map(k))
        return self


class DescribeGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        last_rollback_time: str = None,
        fault_addr_pool_num: int = None,
        fault_addr_pools: DescribeGtmRecoveryPlanResponseBodyFaultAddrPools = None,
        last_execute_time: str = None,
        request_id: str = None,
        create_time: str = None,
        last_execute_timestamp: int = None,
        remark: str = None,
        name: str = None,
        recovery_plan_id: int = None,
        update_time: str = None,
        update_timestamp: int = None,
        last_rollback_timestamp: int = None,
        create_timestamp: int = None,
    ):
        self.status = status
        self.last_rollback_time = last_rollback_time
        self.fault_addr_pool_num = fault_addr_pool_num
        self.fault_addr_pools = fault_addr_pools
        self.last_execute_time = last_execute_time
        self.request_id = request_id
        self.create_time = create_time
        self.last_execute_timestamp = last_execute_timestamp
        self.remark = remark
        self.name = name
        self.recovery_plan_id = recovery_plan_id
        self.update_time = update_time
        self.update_timestamp = update_timestamp
        self.last_rollback_timestamp = last_rollback_timestamp
        self.create_timestamp = create_timestamp

    def validate(self):
        if self.fault_addr_pools:
            self.fault_addr_pools.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.last_rollback_time is not None:
            result['LastRollbackTime'] = self.last_rollback_time
        if self.fault_addr_pool_num is not None:
            result['FaultAddrPoolNum'] = self.fault_addr_pool_num
        if self.fault_addr_pools is not None:
            result['FaultAddrPools'] = self.fault_addr_pools.to_map()
        if self.last_execute_time is not None:
            result['LastExecuteTime'] = self.last_execute_time
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.last_execute_timestamp is not None:
            result['LastExecuteTimestamp'] = self.last_execute_timestamp
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.name is not None:
            result['Name'] = self.name
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.last_rollback_timestamp is not None:
            result['LastRollbackTimestamp'] = self.last_rollback_timestamp
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('LastRollbackTime') is not None:
            self.last_rollback_time = m.get('LastRollbackTime')
        if m.get('FaultAddrPoolNum') is not None:
            self.fault_addr_pool_num = m.get('FaultAddrPoolNum')
        if m.get('FaultAddrPools') is not None:
            temp_model = DescribeGtmRecoveryPlanResponseBodyFaultAddrPools()
            self.fault_addr_pools = temp_model.from_map(m['FaultAddrPools'])
        if m.get('LastExecuteTime') is not None:
            self.last_execute_time = m.get('LastExecuteTime')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('LastExecuteTimestamp') is not None:
            self.last_execute_timestamp = m.get('LastExecuteTimestamp')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('LastRollbackTimestamp') is not None:
            self.last_rollback_timestamp = m.get('LastRollbackTimestamp')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmRecoveryPlanAvailableConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPoolsAddrPool(TeaModel):
    def __init__(
        self,
        addr_pool_id: str = None,
        name: str = None,
    ):
        self.addr_pool_id = addr_pool_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPools(TeaModel):
    def __init__(
        self,
        addr_pool: List[DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPoolsAddrPool] = None,
    ):
        self.addr_pool = addr_pool

    def validate(self):
        if self.addr_pool:
            for k in self.addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AddrPool'] = []
        if self.addr_pool is not None:
            for k in self.addr_pool:
                result['AddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.addr_pool = []
        if m.get('AddrPool') is not None:
            for k in m.get('AddrPool'):
                temp_model = DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPoolsAddrPool()
                self.addr_pool.append(temp_model.from_map(k))
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstance(TeaModel):
    def __init__(
        self,
        addr_pools: DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPools = None,
        instance_name: str = None,
        instance_id: str = None,
    ):
        self.addr_pools = addr_pools
        self.instance_name = instance_name
        self.instance_id = instance_id

    def validate(self):
        if self.addr_pools:
            self.addr_pools.validate()

    def to_map(self):
        result = dict()
        if self.addr_pools is not None:
            result['AddrPools'] = self.addr_pools.to_map()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AddrPools') is not None:
            temp_model = DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstanceAddrPools()
            self.addr_pools = temp_model.from_map(m['AddrPools'])
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstances(TeaModel):
    def __init__(
        self,
        instance: List[DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstance] = None,
    ):
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstancesInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponseBody(TeaModel):
    def __init__(
        self,
        instances: DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstances = None,
        request_id: str = None,
    ):
        self.instances = instances
        self.request_id = request_id

    def validate(self):
        if self.instances:
            self.instances.validate()

    def to_map(self):
        result = dict()
        if self.instances is not None:
            result['Instances'] = self.instances.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Instances') is not None:
            temp_model = DescribeGtmRecoveryPlanAvailableConfigResponseBodyInstances()
            self.instances = temp_model.from_map(m['Instances'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeGtmRecoveryPlanAvailableConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmRecoveryPlanAvailableConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmRecoveryPlanAvailableConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGtmRecoveryPlansRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        keyword: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.keyword = keyword
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGtmRecoveryPlansResponseBodyRecoveryPlansRecoveryPlan(TeaModel):
    def __init__(
        self,
        status: str = None,
        last_rollback_timestamp: int = None,
        update_time: str = None,
        remark: str = None,
        create_time: str = None,
        recovery_plan_id: int = None,
        update_timestamp: int = None,
        last_execute_timestamp: int = None,
        last_execute_time: str = None,
        last_rollback_time: str = None,
        name: str = None,
        fault_addr_pool_num: int = None,
        create_timestamp: int = None,
    ):
        self.status = status
        self.last_rollback_timestamp = last_rollback_timestamp
        self.update_time = update_time
        self.remark = remark
        self.create_time = create_time
        self.recovery_plan_id = recovery_plan_id
        self.update_timestamp = update_timestamp
        self.last_execute_timestamp = last_execute_timestamp
        self.last_execute_time = last_execute_time
        self.last_rollback_time = last_rollback_time
        self.name = name
        self.fault_addr_pool_num = fault_addr_pool_num
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.last_rollback_timestamp is not None:
            result['LastRollbackTimestamp'] = self.last_rollback_timestamp
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.last_execute_timestamp is not None:
            result['LastExecuteTimestamp'] = self.last_execute_timestamp
        if self.last_execute_time is not None:
            result['LastExecuteTime'] = self.last_execute_time
        if self.last_rollback_time is not None:
            result['LastRollbackTime'] = self.last_rollback_time
        if self.name is not None:
            result['Name'] = self.name
        if self.fault_addr_pool_num is not None:
            result['FaultAddrPoolNum'] = self.fault_addr_pool_num
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('LastRollbackTimestamp') is not None:
            self.last_rollback_timestamp = m.get('LastRollbackTimestamp')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('LastExecuteTimestamp') is not None:
            self.last_execute_timestamp = m.get('LastExecuteTimestamp')
        if m.get('LastExecuteTime') is not None:
            self.last_execute_time = m.get('LastExecuteTime')
        if m.get('LastRollbackTime') is not None:
            self.last_rollback_time = m.get('LastRollbackTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('FaultAddrPoolNum') is not None:
            self.fault_addr_pool_num = m.get('FaultAddrPoolNum')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeGtmRecoveryPlansResponseBodyRecoveryPlans(TeaModel):
    def __init__(
        self,
        recovery_plan: List[DescribeGtmRecoveryPlansResponseBodyRecoveryPlansRecoveryPlan] = None,
    ):
        self.recovery_plan = recovery_plan

    def validate(self):
        if self.recovery_plan:
            for k in self.recovery_plan:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RecoveryPlan'] = []
        if self.recovery_plan is not None:
            for k in self.recovery_plan:
                result['RecoveryPlan'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.recovery_plan = []
        if m.get('RecoveryPlan') is not None:
            for k in m.get('RecoveryPlan'):
                temp_model = DescribeGtmRecoveryPlansResponseBodyRecoveryPlansRecoveryPlan()
                self.recovery_plan.append(temp_model.from_map(k))
        return self


class DescribeGtmRecoveryPlansResponseBody(TeaModel):
    def __init__(
        self,
        recovery_plans: DescribeGtmRecoveryPlansResponseBodyRecoveryPlans = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.recovery_plans = recovery_plans
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.recovery_plans:
            self.recovery_plans.validate()

    def to_map(self):
        result = dict()
        if self.recovery_plans is not None:
            result['RecoveryPlans'] = self.recovery_plans.to_map()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RecoveryPlans') is not None:
            temp_model = DescribeGtmRecoveryPlansResponseBodyRecoveryPlans()
            self.recovery_plans = temp_model.from_map(m['RecoveryPlans'])
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeGtmRecoveryPlansResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGtmRecoveryPlansResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGtmRecoveryPlansResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstanceDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeInstanceDomainsResponseBodyInstanceDomains(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        domain_name: str = None,
        create_timestamp: int = None,
    ):
        self.create_time = create_time
        self.domain_name = domain_name
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeInstanceDomainsResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        instance_domains: List[DescribeInstanceDomainsResponseBodyInstanceDomains] = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.instance_domains = instance_domains
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.instance_domains:
            for k in self.instance_domains:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['InstanceDomains'] = []
        if self.instance_domains is not None:
            for k in self.instance_domains:
                result['InstanceDomains'].append(k.to_map() if k else None)
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.instance_domains = []
        if m.get('InstanceDomains') is not None:
            for k in m.get('InstanceDomains'):
                temp_model = DescribeInstanceDomainsResponseBodyInstanceDomains()
                self.instance_domains.append(temp_model.from_map(k))
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class DescribeInstanceDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstanceDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstanceDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecordLogsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        page_number: int = None,
        page_size: int = None,
        key_word: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.page_number = page_number
        self.page_size = page_size
        self.key_word = key_word
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['endDate'] = self.end_date
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('endDate') is not None:
            self.end_date = m.get('endDate')
        return self


class DescribeRecordLogsResponseBodyRecordLogsRecordLog(TeaModel):
    def __init__(
        self,
        action: str = None,
        action_timestamp: int = None,
        client_ip: str = None,
        message: str = None,
        action_time: str = None,
    ):
        self.action = action
        self.action_timestamp = action_timestamp
        self.client_ip = client_ip
        self.message = message
        self.action_time = action_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.action_timestamp is not None:
            result['ActionTimestamp'] = self.action_timestamp
        if self.client_ip is not None:
            result['ClientIp'] = self.client_ip
        if self.message is not None:
            result['Message'] = self.message
        if self.action_time is not None:
            result['ActionTime'] = self.action_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('ActionTimestamp') is not None:
            self.action_timestamp = m.get('ActionTimestamp')
        if m.get('ClientIp') is not None:
            self.client_ip = m.get('ClientIp')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('ActionTime') is not None:
            self.action_time = m.get('ActionTime')
        return self


class DescribeRecordLogsResponseBodyRecordLogs(TeaModel):
    def __init__(
        self,
        record_log: List[DescribeRecordLogsResponseBodyRecordLogsRecordLog] = None,
    ):
        self.record_log = record_log

    def validate(self):
        if self.record_log:
            for k in self.record_log:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RecordLog'] = []
        if self.record_log is not None:
            for k in self.record_log:
                result['RecordLog'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record_log = []
        if m.get('RecordLog') is not None:
            for k in m.get('RecordLog'):
                temp_model = DescribeRecordLogsResponseBodyRecordLogsRecordLog()
                self.record_log.append(temp_model.from_map(k))
        return self


class DescribeRecordLogsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        record_logs: DescribeRecordLogsResponseBodyRecordLogs = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.record_logs = record_logs

    def validate(self):
        if self.record_logs:
            self.record_logs.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.record_logs is not None:
            result['RecordLogs'] = self.record_logs.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('RecordLogs') is not None:
            temp_model = DescribeRecordLogsResponseBodyRecordLogs()
            self.record_logs = temp_model.from_map(m['RecordLogs'])
        return self


class DescribeRecordLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRecordLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRecordLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecordStatisticsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        start_date: str = None,
        end_date: str = None,
        domain_name: str = None,
        rr: str = None,
        domain_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.start_date = start_date
        self.end_date = end_date
        self.domain_name = domain_name
        self.rr = rr
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeRecordStatisticsResponseBodyStatisticsStatistic(TeaModel):
    def __init__(
        self,
        timestamp: int = None,
        count: int = None,
    ):
        self.timestamp = timestamp
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeRecordStatisticsResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        statistic: List[DescribeRecordStatisticsResponseBodyStatisticsStatistic] = None,
    ):
        self.statistic = statistic

    def validate(self):
        if self.statistic:
            for k in self.statistic:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Statistic'] = []
        if self.statistic is not None:
            for k in self.statistic:
                result['Statistic'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.statistic = []
        if m.get('Statistic') is not None:
            for k in m.get('Statistic'):
                temp_model = DescribeRecordStatisticsResponseBodyStatisticsStatistic()
                self.statistic.append(temp_model.from_map(k))
        return self


class DescribeRecordStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: DescribeRecordStatisticsResponseBodyStatistics = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            self.statistics.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            temp_model = DescribeRecordStatisticsResponseBodyStatistics()
            self.statistics = temp_model.from_map(m['Statistics'])
        return self


class DescribeRecordStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRecordStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRecordStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecordStatisticsSummaryRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        order_by: str = None,
        direction: str = None,
        domain_name: str = None,
        search_mode: str = None,
        keyword: str = None,
        threshold: int = None,
        domain_type: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.order_by = order_by
        self.direction = direction
        self.domain_name = domain_name
        self.search_mode = search_mode
        self.keyword = keyword
        self.threshold = threshold
        self.domain_type = domain_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.domain_type is not None:
            result['DomainType'] = self.domain_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('DomainType') is not None:
            self.domain_type = m.get('DomainType')
        return self


class DescribeRecordStatisticsSummaryResponseBodyStatisticsStatistic(TeaModel):
    def __init__(
        self,
        sub_domain: str = None,
        count: int = None,
    ):
        self.sub_domain = sub_domain
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeRecordStatisticsSummaryResponseBodyStatistics(TeaModel):
    def __init__(
        self,
        statistic: List[DescribeRecordStatisticsSummaryResponseBodyStatisticsStatistic] = None,
    ):
        self.statistic = statistic

    def validate(self):
        if self.statistic:
            for k in self.statistic:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Statistic'] = []
        if self.statistic is not None:
            for k in self.statistic:
                result['Statistic'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.statistic = []
        if m.get('Statistic') is not None:
            for k in m.get('Statistic'):
                temp_model = DescribeRecordStatisticsSummaryResponseBodyStatisticsStatistic()
                self.statistic.append(temp_model.from_map(k))
        return self


class DescribeRecordStatisticsSummaryResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        total_pages: int = None,
        total_items: int = None,
        statistics: DescribeRecordStatisticsSummaryResponseBodyStatistics = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.total_pages = total_pages
        self.total_items = total_items
        self.statistics = statistics

    def validate(self):
        if self.statistics:
            self.statistics.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.statistics is not None:
            result['Statistics'] = self.statistics.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('Statistics') is not None:
            temp_model = DescribeRecordStatisticsSummaryResponseBodyStatistics()
            self.statistics = temp_model.from_map(m['Statistics'])
        return self


class DescribeRecordStatisticsSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRecordStatisticsSummaryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRecordStatisticsSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSubDomainRecordsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        sub_domain: str = None,
        page_number: int = None,
        page_size: int = None,
        type: str = None,
        line: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.sub_domain = sub_domain
        self.page_number = page_number
        self.page_size = page_size
        self.type = type
        self.line = line
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.type is not None:
            result['Type'] = self.type
        if self.line is not None:
            result['Line'] = self.line
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeSubDomainRecordsResponseBodyDomainRecordsRecord(TeaModel):
    def __init__(
        self,
        status: str = None,
        type: str = None,
        weight: int = None,
        value: str = None,
        ttl: int = None,
        line: str = None,
        record_id: str = None,
        priority: int = None,
        rr: str = None,
        domain_name: str = None,
        locked: bool = None,
    ):
        self.status = status
        self.type = type
        self.weight = weight
        self.value = value
        self.ttl = ttl
        self.line = line
        self.record_id = record_id
        self.priority = priority
        self.rr = rr
        self.domain_name = domain_name
        self.locked = locked

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.type is not None:
            result['Type'] = self.type
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.value is not None:
            result['Value'] = self.value
        if self.ttl is not None:
            result['TTL'] = self.ttl
        if self.line is not None:
            result['Line'] = self.line
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.rr is not None:
            result['RR'] = self.rr
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.locked is not None:
            result['Locked'] = self.locked
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('TTL') is not None:
            self.ttl = m.get('TTL')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Locked') is not None:
            self.locked = m.get('Locked')
        return self


class DescribeSubDomainRecordsResponseBodyDomainRecords(TeaModel):
    def __init__(
        self,
        record: List[DescribeSubDomainRecordsResponseBodyDomainRecordsRecord] = None,
    ):
        self.record = record

    def validate(self):
        if self.record:
            for k in self.record:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Record'] = []
        if self.record is not None:
            for k in self.record:
                result['Record'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record = []
        if m.get('Record') is not None:
            for k in m.get('Record'):
                temp_model = DescribeSubDomainRecordsResponseBodyDomainRecordsRecord()
                self.record.append(temp_model.from_map(k))
        return self


class DescribeSubDomainRecordsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        domain_records: DescribeSubDomainRecordsResponseBodyDomainRecords = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.domain_records = domain_records
        self.page_number = page_number

    def validate(self):
        if self.domain_records:
            self.domain_records.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_records is not None:
            result['DomainRecords'] = self.domain_records.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainRecords') is not None:
            temp_model = DescribeSubDomainRecordsResponseBodyDomainRecords()
            self.domain_records = temp_model.from_map(m['DomainRecords'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeSubDomainRecordsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSubDomainRecordsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSubDomainRecordsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSupportLinesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class DescribeSupportLinesResponseBodyRecordLinesRecordLine(TeaModel):
    def __init__(
        self,
        father_code: str = None,
        line_display_name: str = None,
        line_code: str = None,
        line_name: str = None,
    ):
        self.father_code = father_code
        self.line_display_name = line_display_name
        self.line_code = line_code
        self.line_name = line_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.father_code is not None:
            result['FatherCode'] = self.father_code
        if self.line_display_name is not None:
            result['LineDisplayName'] = self.line_display_name
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        if self.line_name is not None:
            result['LineName'] = self.line_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatherCode') is not None:
            self.father_code = m.get('FatherCode')
        if m.get('LineDisplayName') is not None:
            self.line_display_name = m.get('LineDisplayName')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        return self


class DescribeSupportLinesResponseBodyRecordLines(TeaModel):
    def __init__(
        self,
        record_line: List[DescribeSupportLinesResponseBodyRecordLinesRecordLine] = None,
    ):
        self.record_line = record_line

    def validate(self):
        if self.record_line:
            for k in self.record_line:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RecordLine'] = []
        if self.record_line is not None:
            for k in self.record_line:
                result['RecordLine'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record_line = []
        if m.get('RecordLine') is not None:
            for k in m.get('RecordLine'):
                temp_model = DescribeSupportLinesResponseBodyRecordLinesRecordLine()
                self.record_line.append(temp_model.from_map(k))
        return self


class DescribeSupportLinesResponseBody(TeaModel):
    def __init__(
        self,
        record_lines: DescribeSupportLinesResponseBodyRecordLines = None,
        request_id: str = None,
    ):
        self.record_lines = record_lines
        self.request_id = request_id

    def validate(self):
        if self.record_lines:
            self.record_lines.validate()

    def to_map(self):
        result = dict()
        if self.record_lines is not None:
            result['RecordLines'] = self.record_lines.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RecordLines') is not None:
            temp_model = DescribeSupportLinesResponseBodyRecordLines()
            self.record_lines = temp_model.from_map(m['RecordLines'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeSupportLinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSupportLinesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSupportLinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTagsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        resource_type: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.resource_type = resource_type
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeTagsResponseBodyTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        values: List[str] = None,
    ):
        self.key = key
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class DescribeTagsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        tags: List[DescribeTagsResponseBodyTags] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.tags = tags

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = DescribeTagsResponseBodyTags()
                self.tags.append(temp_model.from_map(k))
        return self


class DescribeTagsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTagsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTagsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTransferDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        page_number: int = None,
        page_size: int = None,
        transfer_type: str = None,
        domain_name: str = None,
        from_user_id: int = None,
        target_user_id: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.page_number = page_number
        self.page_size = page_size
        self.transfer_type = transfer_type
        self.domain_name = domain_name
        self.from_user_id = from_user_id
        self.target_user_id = target_user_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.transfer_type is not None:
            result['TransferType'] = self.transfer_type
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.from_user_id is not None:
            result['FromUserId'] = self.from_user_id
        if self.target_user_id is not None:
            result['TargetUserId'] = self.target_user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TransferType') is not None:
            self.transfer_type = m.get('TransferType')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('FromUserId') is not None:
            self.from_user_id = m.get('FromUserId')
        if m.get('TargetUserId') is not None:
            self.target_user_id = m.get('TargetUserId')
        return self


class DescribeTransferDomainsResponseBodyDomainTransfersDomainTransfer(TeaModel):
    def __init__(
        self,
        from_user_id: int = None,
        create_time: str = None,
        target_user_id: int = None,
        domain_name: str = None,
        id: int = None,
        create_timestamp: int = None,
    ):
        self.from_user_id = from_user_id
        self.create_time = create_time
        self.target_user_id = target_user_id
        self.domain_name = domain_name
        self.id = id
        self.create_timestamp = create_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_user_id is not None:
            result['FromUserId'] = self.from_user_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.target_user_id is not None:
            result['TargetUserId'] = self.target_user_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.id is not None:
            result['Id'] = self.id
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromUserId') is not None:
            self.from_user_id = m.get('FromUserId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('TargetUserId') is not None:
            self.target_user_id = m.get('TargetUserId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeTransferDomainsResponseBodyDomainTransfers(TeaModel):
    def __init__(
        self,
        domain_transfer: List[DescribeTransferDomainsResponseBodyDomainTransfersDomainTransfer] = None,
    ):
        self.domain_transfer = domain_transfer

    def validate(self):
        if self.domain_transfer:
            for k in self.domain_transfer:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DomainTransfer'] = []
        if self.domain_transfer is not None:
            for k in self.domain_transfer:
                result['DomainTransfer'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.domain_transfer = []
        if m.get('DomainTransfer') is not None:
            for k in m.get('DomainTransfer'):
                temp_model = DescribeTransferDomainsResponseBodyDomainTransfersDomainTransfer()
                self.domain_transfer.append(temp_model.from_map(k))
        return self


class DescribeTransferDomainsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        domain_transfers: DescribeTransferDomainsResponseBodyDomainTransfers = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.domain_transfers = domain_transfers

    def validate(self):
        if self.domain_transfers:
            self.domain_transfers.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.domain_transfers is not None:
            result['DomainTransfers'] = self.domain_transfers.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('DomainTransfers') is not None:
            temp_model = DescribeTransferDomainsResponseBodyDomainTransfers()
            self.domain_transfers = temp_model.from_map(m['DomainTransfers'])
        return self


class DescribeTransferDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTransferDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTransferDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ExecuteGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        recovery_plan_id: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.recovery_plan_id = recovery_plan_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        return self


class ExecuteGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ExecuteGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ExecuteGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ExecuteGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMainDomainNameRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        input_string: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.input_string = input_string

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.input_string is not None:
            result['InputString'] = self.input_string
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InputString') is not None:
            self.input_string = m.get('InputString')
        return self


class GetMainDomainNameResponseBody(TeaModel):
    def __init__(
        self,
        rr: str = None,
        request_id: str = None,
        domain_name: str = None,
        domain_level: int = None,
    ):
        self.rr = rr
        self.request_id = request_id
        self.domain_name = domain_name
        self.domain_level = domain_level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rr is not None:
            result['RR'] = self.rr
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.domain_level is not None:
            result['DomainLevel'] = self.domain_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('DomainLevel') is not None:
            self.domain_level = m.get('DomainLevel')
        return self


class GetMainDomainNameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetMainDomainNameResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetMainDomainNameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTxtRecordForVerifyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        domain_name: str = None,
        type: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.domain_name = domain_name
        self.type = type
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.type is not None:
            result['Type'] = self.type
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class GetTxtRecordForVerifyResponseBody(TeaModel):
    def __init__(
        self,
        rr: str = None,
        request_id: str = None,
        domain_name: str = None,
        value: str = None,
    ):
        self.rr = rr
        self.request_id = request_id
        self.domain_name = domain_name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rr is not None:
            result['RR'] = self.rr
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTxtRecordForVerifyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetTxtRecordForVerifyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetTxtRecordForVerifyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTagResourcesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        resource_type: str = None,
        next_token: str = None,
        size: int = None,
        tag: List[ListTagResourcesRequestTag] = None,
        resource_id: List[str] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.resource_type = resource_type
        self.next_token = next_token
        self.size = size
        self.tag = tag
        self.resource_id = resource_id

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.size is not None:
            result['Size'] = self.size
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Size') is not None:
            self.size = m.get('Size')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = ListTagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(
        self,
        resource_type: str = None,
        tag_value: str = None,
        resource_id: str = None,
        tag_key: str = None,
    ):
        self.resource_type = resource_type
        self.tag_value = tag_value
        self.resource_id = resource_id
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        tag_resources: List[ListTagResourcesResponseBodyTagResources] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.tag_resources = tag_resources

    def validate(self):
        if self.tag_resources:
            for k in self.tag_resources:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['TagResources'] = []
        if self.tag_resources is not None:
            for k in self.tag_resources:
                result['TagResources'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.tag_resources = []
        if m.get('TagResources') is not None:
            for k in m.get('TagResources'):
                temp_model = ListTagResourcesResponseBodyTagResources()
                self.tag_resources.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyHichinaDomainDNSRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class ModifyHichinaDomainDNSResponseBodyNewDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class ModifyHichinaDomainDNSResponseBodyOriginalDnsServers(TeaModel):
    def __init__(
        self,
        dns_server: List[str] = None,
    ):
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dns_server is not None:
            result['DnsServer'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsServer') is not None:
            self.dns_server = m.get('DnsServer')
        return self


class ModifyHichinaDomainDNSResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        new_dns_servers: ModifyHichinaDomainDNSResponseBodyNewDnsServers = None,
        original_dns_servers: ModifyHichinaDomainDNSResponseBodyOriginalDnsServers = None,
    ):
        self.request_id = request_id
        self.new_dns_servers = new_dns_servers
        self.original_dns_servers = original_dns_servers

    def validate(self):
        if self.new_dns_servers:
            self.new_dns_servers.validate()
        if self.original_dns_servers:
            self.original_dns_servers.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.new_dns_servers is not None:
            result['NewDnsServers'] = self.new_dns_servers.to_map()
        if self.original_dns_servers is not None:
            result['OriginalDnsServers'] = self.original_dns_servers.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('NewDnsServers') is not None:
            temp_model = ModifyHichinaDomainDNSResponseBodyNewDnsServers()
            self.new_dns_servers = temp_model.from_map(m['NewDnsServers'])
        if m.get('OriginalDnsServers') is not None:
            temp_model = ModifyHichinaDomainDNSResponseBodyOriginalDnsServers()
            self.original_dns_servers = temp_model.from_map(m['OriginalDnsServers'])
        return self


class ModifyHichinaDomainDNSResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyHichinaDomainDNSResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyHichinaDomainDNSResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class MoveDomainResourceGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        resource_id: str = None,
        new_resource_group_id: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.resource_id = resource_id
        self.new_resource_group_id = new_resource_group_id
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.new_resource_group_id is not None:
            result['NewResourceGroupId'] = self.new_resource_group_id
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('NewResourceGroupId') is not None:
            self.new_resource_group_id = m.get('NewResourceGroupId')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class MoveDomainResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class MoveDomainResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: MoveDomainResourceGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = MoveDomainResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class MoveGtmResourceGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        resource_id: str = None,
        new_resource_group_id: str = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.resource_id = resource_id
        self.new_resource_group_id = new_resource_group_id
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.new_resource_group_id is not None:
            result['NewResourceGroupId'] = self.new_resource_group_id
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('NewResourceGroupId') is not None:
            self.new_resource_group_id = m.get('NewResourceGroupId')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class MoveGtmResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class MoveGtmResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: MoveGtmResourceGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = MoveGtmResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class OperateBatchDomainRequestDomainRecordInfo(TeaModel):
    def __init__(
        self,
        type: str = None,
        value: str = None,
        ttl: int = None,
        domain: str = None,
        line: str = None,
        new_rr: str = None,
        rr: str = None,
        priority: int = None,
        new_type: str = None,
        new_value: str = None,
    ):
        self.type = type
        self.value = value
        self.ttl = ttl
        self.domain = domain
        self.line = line
        self.new_rr = new_rr
        self.rr = rr
        self.priority = priority
        self.new_type = new_type
        self.new_value = new_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.domain is not None:
            result['Domain'] = self.domain
        if self.line is not None:
            result['Line'] = self.line
        if self.new_rr is not None:
            result['NewRr'] = self.new_rr
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.new_type is not None:
            result['NewType'] = self.new_type
        if self.new_value is not None:
            result['NewValue'] = self.new_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Domain') is not None:
            self.domain = m.get('Domain')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('NewRr') is not None:
            self.new_rr = m.get('NewRr')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('NewType') is not None:
            self.new_type = m.get('NewType')
        if m.get('NewValue') is not None:
            self.new_value = m.get('NewValue')
        return self


class OperateBatchDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        type: str = None,
        domain_record_info: List[OperateBatchDomainRequestDomainRecordInfo] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.type = type
        self.domain_record_info = domain_record_info

    def validate(self):
        if self.domain_record_info:
            for k in self.domain_record_info:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.type is not None:
            result['Type'] = self.type
        result['DomainRecordInfo'] = []
        if self.domain_record_info is not None:
            for k in self.domain_record_info:
                result['DomainRecordInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        self.domain_record_info = []
        if m.get('DomainRecordInfo') is not None:
            for k in m.get('DomainRecordInfo'):
                temp_model = OperateBatchDomainRequestDomainRecordInfo()
                self.domain_record_info.append(temp_model.from_map(k))
        return self


class OperateBatchDomainResponseBody(TeaModel):
    def __init__(
        self,
        task_id: int = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class OperateBatchDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: OperateBatchDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = OperateBatchDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PreviewGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        recovery_plan_id: int = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.recovery_plan_id = recovery_plan_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfosSwitchInfo(TeaModel):
    def __init__(
        self,
        strategy_name: str = None,
        content: str = None,
    ):
        self.strategy_name = strategy_name
        self.content = content

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.content is not None:
            result['Content'] = self.content
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        return self


class PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfos(TeaModel):
    def __init__(
        self,
        switch_info: List[PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfosSwitchInfo] = None,
    ):
        self.switch_info = switch_info

    def validate(self):
        if self.switch_info:
            for k in self.switch_info:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SwitchInfo'] = []
        if self.switch_info is not None:
            for k in self.switch_info:
                result['SwitchInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.switch_info = []
        if m.get('SwitchInfo') is not None:
            for k in m.get('SwitchInfo'):
                temp_model = PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfosSwitchInfo()
                self.switch_info.append(temp_model.from_map(k))
        return self


class PreviewGtmRecoveryPlanResponseBodyPreviewsPreview(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        switch_infos: PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfos = None,
        name: str = None,
        user_domain_name: str = None,
    ):
        self.instance_id = instance_id
        self.switch_infos = switch_infos
        self.name = name
        self.user_domain_name = user_domain_name

    def validate(self):
        if self.switch_infos:
            self.switch_infos.validate()

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.switch_infos is not None:
            result['SwitchInfos'] = self.switch_infos.to_map()
        if self.name is not None:
            result['Name'] = self.name
        if self.user_domain_name is not None:
            result['UserDomainName'] = self.user_domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('SwitchInfos') is not None:
            temp_model = PreviewGtmRecoveryPlanResponseBodyPreviewsPreviewSwitchInfos()
            self.switch_infos = temp_model.from_map(m['SwitchInfos'])
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('UserDomainName') is not None:
            self.user_domain_name = m.get('UserDomainName')
        return self


class PreviewGtmRecoveryPlanResponseBodyPreviews(TeaModel):
    def __init__(
        self,
        preview: List[PreviewGtmRecoveryPlanResponseBodyPreviewsPreview] = None,
    ):
        self.preview = preview

    def validate(self):
        if self.preview:
            for k in self.preview:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Preview'] = []
        if self.preview is not None:
            for k in self.preview:
                result['Preview'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.preview = []
        if m.get('Preview') is not None:
            for k in m.get('Preview'):
                temp_model = PreviewGtmRecoveryPlanResponseBodyPreviewsPreview()
                self.preview.append(temp_model.from_map(k))
        return self


class PreviewGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        previews: PreviewGtmRecoveryPlanResponseBodyPreviews = None,
        total_pages: int = None,
        total_items: int = None,
    ):
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.previews = previews
        self.total_pages = total_pages
        self.total_items = total_items

    def validate(self):
        if self.previews:
            self.previews.validate()

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.previews is not None:
            result['Previews'] = self.previews.to_map()
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Previews') is not None:
            temp_model = PreviewGtmRecoveryPlanResponseBodyPreviews()
            self.previews = temp_model.from_map(m['Previews'])
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        return self


class PreviewGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PreviewGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PreviewGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RetrieveDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        return self


class RetrieveDomainResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RetrieveDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RetrieveDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RetrieveDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RollbackGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        recovery_plan_id: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.recovery_plan_id = recovery_plan_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        return self


class RollbackGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RollbackGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RollbackGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RollbackGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetDnsGtmAccessModeRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
        access_mode: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id
        self.access_mode = access_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.access_mode is not None:
            result['AccessMode'] = self.access_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('AccessMode') is not None:
            self.access_mode = m.get('AccessMode')
        return self


class SetDnsGtmAccessModeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetDnsGtmAccessModeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetDnsGtmAccessModeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetDnsGtmAccessModeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetDnsGtmMonitorStatusRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
        status: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SetDnsGtmMonitorStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetDnsGtmMonitorStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetDnsGtmMonitorStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetDnsGtmMonitorStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetDNSSLBStatusRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        sub_domain: str = None,
        open: bool = None,
        domain_name: str = None,
        type: str = None,
        line: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.sub_domain = sub_domain
        self.open = open
        self.domain_name = domain_name
        self.type = type
        self.line = line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.sub_domain is not None:
            result['SubDomain'] = self.sub_domain
        if self.open is not None:
            result['Open'] = self.open
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.type is not None:
            result['Type'] = self.type
        if self.line is not None:
            result['Line'] = self.line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('SubDomain') is not None:
            self.sub_domain = m.get('SubDomain')
        if m.get('Open') is not None:
            self.open = m.get('Open')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        return self


class SetDNSSLBStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        record_count: int = None,
        open: bool = None,
    ):
        self.request_id = request_id
        self.record_count = record_count
        self.open = open

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.open is not None:
            result['Open'] = self.open
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Open') is not None:
            self.open = m.get('Open')
        return self


class SetDNSSLBStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetDNSSLBStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetDNSSLBStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetDomainDnssecStatusRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        domain_name: str = None,
        status: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.domain_name = domain_name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SetDomainDnssecStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetDomainDnssecStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetDomainDnssecStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetDomainDnssecStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetDomainRecordStatusRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
        status: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SetDomainRecordStatusResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        request_id: str = None,
        record_id: str = None,
    ):
        self.status = status
        self.request_id = request_id
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class SetDomainRecordStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetDomainRecordStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetDomainRecordStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetGtmAccessModeRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
        access_mode: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id
        self.access_mode = access_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.access_mode is not None:
            result['AccessMode'] = self.access_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('AccessMode') is not None:
            self.access_mode = m.get('AccessMode')
        return self


class SetGtmAccessModeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetGtmAccessModeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetGtmAccessModeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetGtmAccessModeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetGtmMonitorStatusRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
        status: str = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SetGtmMonitorStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetGtmMonitorStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetGtmMonitorStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetGtmMonitorStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SwitchDnsGtmInstanceStrategyModeRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        strategy_mode: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.strategy_mode = strategy_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.strategy_mode is not None:
            result['StrategyMode'] = self.strategy_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StrategyMode') is not None:
            self.strategy_mode = m.get('StrategyMode')
        return self


class SwitchDnsGtmInstanceStrategyModeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SwitchDnsGtmInstanceStrategyModeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SwitchDnsGtmInstanceStrategyModeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SwitchDnsGtmInstanceStrategyModeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class TagResourcesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        resource_type: str = None,
        over_write: bool = None,
        tag: List[TagResourcesRequestTag] = None,
        resource_id: List[str] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.resource_type = resource_type
        self.over_write = over_write
        self.tag = tag
        self.resource_id = resource_id

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.over_write is not None:
            result['OverWrite'] = self.over_write
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('OverWrite') is not None:
            self.over_write = m.get('OverWrite')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = TagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        return self


class TagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TransferDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        domain_names: str = None,
        remark: str = None,
        target_user_id: int = None,
        user_client_ip: str = None,
    ):
        self.lang = lang
        self.domain_names = domain_names
        self.remark = remark
        self.target_user_id = target_user_id
        self.user_client_ip = user_client_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.domain_names is not None:
            result['DomainNames'] = self.domain_names
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.target_user_id is not None:
            result['TargetUserId'] = self.target_user_id
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('DomainNames') is not None:
            self.domain_names = m.get('DomainNames')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('TargetUserId') is not None:
            self.target_user_id = m.get('TargetUserId')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class TransferDomainResponseBody(TeaModel):
    def __init__(
        self,
        task_id: int = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TransferDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TransferDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = TransferDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UnbindInstanceDomainsRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_names: str = None,
        instance_id: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_names = domain_names
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_names is not None:
            result['DomainNames'] = self.domain_names
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainNames') is not None:
            self.domain_names = m.get('DomainNames')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class UnbindInstanceDomainsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        failed_count: int = None,
        success_count: int = None,
    ):
        self.request_id = request_id
        self.failed_count = failed_count
        self.success_count = success_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.failed_count is not None:
            result['FailedCount'] = self.failed_count
        if self.success_count is not None:
            result['SuccessCount'] = self.success_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailedCount') is not None:
            self.failed_count = m.get('FailedCount')
        if m.get('SuccessCount') is not None:
            self.success_count = m.get('SuccessCount')
        return self


class UnbindInstanceDomainsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UnbindInstanceDomainsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UnbindInstanceDomainsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        resource_type: str = None,
        all: bool = None,
        resource_id: List[str] = None,
        tag_key: List[str] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.resource_type = resource_type
        self.all = all
        self.resource_id = resource_id
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.all is not None:
            result['All'] = self.all
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class UntagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UntagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UntagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateCustomLineRequestIpSegment(TeaModel):
    def __init__(
        self,
        end_ip: str = None,
        start_ip: str = None,
    ):
        self.end_ip = end_ip
        self.start_ip = start_ip

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_ip is not None:
            result['EndIp'] = self.end_ip
        if self.start_ip is not None:
            result['StartIp'] = self.start_ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndIp') is not None:
            self.end_ip = m.get('EndIp')
        if m.get('StartIp') is not None:
            self.start_ip = m.get('StartIp')
        return self


class UpdateCustomLineRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        line_name: str = None,
        line_id: int = None,
        ip_segment: List[UpdateCustomLineRequestIpSegment] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.line_name = line_name
        self.line_id = line_id
        self.ip_segment = ip_segment

    def validate(self):
        if self.ip_segment:
            for k in self.ip_segment:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.line_name is not None:
            result['LineName'] = self.line_name
        if self.line_id is not None:
            result['LineId'] = self.line_id
        result['IpSegment'] = []
        if self.ip_segment is not None:
            for k in self.ip_segment:
                result['IpSegment'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('LineName') is not None:
            self.line_name = m.get('LineName')
        if m.get('LineId') is not None:
            self.line_id = m.get('LineId')
        self.ip_segment = []
        if m.get('IpSegment') is not None:
            for k in m.get('IpSegment'):
                temp_model = UpdateCustomLineRequestIpSegment()
                self.ip_segment.append(temp_model.from_map(k))
        return self


class UpdateCustomLineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateCustomLineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateCustomLineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateCustomLineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsCacheDomainRequestSourceDnsServer(TeaModel):
    def __init__(
        self,
        host: str = None,
        port: str = None,
    ):
        self.host = host
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.host is not None:
            result['Host'] = self.host
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Host') is not None:
            self.host = m.get('Host')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class UpdateDnsCacheDomainRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        instance_id: str = None,
        cache_ttl_min: int = None,
        cache_ttl_max: int = None,
        source_protocol: str = None,
        source_edns: str = None,
        source_dns_server: List[UpdateDnsCacheDomainRequestSourceDnsServer] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.instance_id = instance_id
        self.cache_ttl_min = cache_ttl_min
        self.cache_ttl_max = cache_ttl_max
        self.source_protocol = source_protocol
        self.source_edns = source_edns
        self.source_dns_server = source_dns_server

    def validate(self):
        if self.source_dns_server:
            for k in self.source_dns_server:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.cache_ttl_min is not None:
            result['CacheTtlMin'] = self.cache_ttl_min
        if self.cache_ttl_max is not None:
            result['CacheTtlMax'] = self.cache_ttl_max
        if self.source_protocol is not None:
            result['SourceProtocol'] = self.source_protocol
        if self.source_edns is not None:
            result['SourceEdns'] = self.source_edns
        result['SourceDnsServer'] = []
        if self.source_dns_server is not None:
            for k in self.source_dns_server:
                result['SourceDnsServer'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('CacheTtlMin') is not None:
            self.cache_ttl_min = m.get('CacheTtlMin')
        if m.get('CacheTtlMax') is not None:
            self.cache_ttl_max = m.get('CacheTtlMax')
        if m.get('SourceProtocol') is not None:
            self.source_protocol = m.get('SourceProtocol')
        if m.get('SourceEdns') is not None:
            self.source_edns = m.get('SourceEdns')
        self.source_dns_server = []
        if m.get('SourceDnsServer') is not None:
            for k in m.get('SourceDnsServer'):
                temp_model = UpdateDnsCacheDomainRequestSourceDnsServer()
                self.source_dns_server.append(temp_model.from_map(k))
        return self


class UpdateDnsCacheDomainResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDnsCacheDomainResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsCacheDomainResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsCacheDomainResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsCacheDomainRemarkRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        remark: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.remark = remark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class UpdateDnsCacheDomainRemarkResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDnsCacheDomainRemarkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsCacheDomainRemarkResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsCacheDomainRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsGtmAccessStrategyRequestDefaultAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class UpdateDnsGtmAccessStrategyRequestFailoverAddrPool(TeaModel):
    def __init__(
        self,
        lba_weight: int = None,
        id: str = None,
    ):
        self.lba_weight = lba_weight
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class UpdateDnsGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
        strategy_name: str = None,
        lines: str = None,
        default_addr_pool_type: str = None,
        default_lba_strategy: str = None,
        default_min_available_addr_num: int = None,
        default_max_return_addr_num: int = None,
        default_latency_optimization: str = None,
        failover_addr_pool_type: str = None,
        failover_lba_strategy: str = None,
        failover_min_available_addr_num: int = None,
        failover_max_return_addr_num: int = None,
        failover_latency_optimization: str = None,
        default_addr_pool: List[UpdateDnsGtmAccessStrategyRequestDefaultAddrPool] = None,
        failover_addr_pool: List[UpdateDnsGtmAccessStrategyRequestFailoverAddrPool] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id
        self.strategy_name = strategy_name
        self.lines = lines
        self.default_addr_pool_type = default_addr_pool_type
        self.default_lba_strategy = default_lba_strategy
        self.default_min_available_addr_num = default_min_available_addr_num
        self.default_max_return_addr_num = default_max_return_addr_num
        self.default_latency_optimization = default_latency_optimization
        self.failover_addr_pool_type = failover_addr_pool_type
        self.failover_lba_strategy = failover_lba_strategy
        self.failover_min_available_addr_num = failover_min_available_addr_num
        self.failover_max_return_addr_num = failover_max_return_addr_num
        self.failover_latency_optimization = failover_latency_optimization
        self.default_addr_pool = default_addr_pool
        self.failover_addr_pool = failover_addr_pool

    def validate(self):
        if self.default_addr_pool:
            for k in self.default_addr_pool:
                if k:
                    k.validate()
        if self.failover_addr_pool:
            for k in self.failover_addr_pool:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.lines is not None:
            result['Lines'] = self.lines
        if self.default_addr_pool_type is not None:
            result['DefaultAddrPoolType'] = self.default_addr_pool_type
        if self.default_lba_strategy is not None:
            result['DefaultLbaStrategy'] = self.default_lba_strategy
        if self.default_min_available_addr_num is not None:
            result['DefaultMinAvailableAddrNum'] = self.default_min_available_addr_num
        if self.default_max_return_addr_num is not None:
            result['DefaultMaxReturnAddrNum'] = self.default_max_return_addr_num
        if self.default_latency_optimization is not None:
            result['DefaultLatencyOptimization'] = self.default_latency_optimization
        if self.failover_addr_pool_type is not None:
            result['FailoverAddrPoolType'] = self.failover_addr_pool_type
        if self.failover_lba_strategy is not None:
            result['FailoverLbaStrategy'] = self.failover_lba_strategy
        if self.failover_min_available_addr_num is not None:
            result['FailoverMinAvailableAddrNum'] = self.failover_min_available_addr_num
        if self.failover_max_return_addr_num is not None:
            result['FailoverMaxReturnAddrNum'] = self.failover_max_return_addr_num
        if self.failover_latency_optimization is not None:
            result['FailoverLatencyOptimization'] = self.failover_latency_optimization
        result['DefaultAddrPool'] = []
        if self.default_addr_pool is not None:
            for k in self.default_addr_pool:
                result['DefaultAddrPool'].append(k.to_map() if k else None)
        result['FailoverAddrPool'] = []
        if self.failover_addr_pool is not None:
            for k in self.failover_addr_pool:
                result['FailoverAddrPool'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('Lines') is not None:
            self.lines = m.get('Lines')
        if m.get('DefaultAddrPoolType') is not None:
            self.default_addr_pool_type = m.get('DefaultAddrPoolType')
        if m.get('DefaultLbaStrategy') is not None:
            self.default_lba_strategy = m.get('DefaultLbaStrategy')
        if m.get('DefaultMinAvailableAddrNum') is not None:
            self.default_min_available_addr_num = m.get('DefaultMinAvailableAddrNum')
        if m.get('DefaultMaxReturnAddrNum') is not None:
            self.default_max_return_addr_num = m.get('DefaultMaxReturnAddrNum')
        if m.get('DefaultLatencyOptimization') is not None:
            self.default_latency_optimization = m.get('DefaultLatencyOptimization')
        if m.get('FailoverAddrPoolType') is not None:
            self.failover_addr_pool_type = m.get('FailoverAddrPoolType')
        if m.get('FailoverLbaStrategy') is not None:
            self.failover_lba_strategy = m.get('FailoverLbaStrategy')
        if m.get('FailoverMinAvailableAddrNum') is not None:
            self.failover_min_available_addr_num = m.get('FailoverMinAvailableAddrNum')
        if m.get('FailoverMaxReturnAddrNum') is not None:
            self.failover_max_return_addr_num = m.get('FailoverMaxReturnAddrNum')
        if m.get('FailoverLatencyOptimization') is not None:
            self.failover_latency_optimization = m.get('FailoverLatencyOptimization')
        self.default_addr_pool = []
        if m.get('DefaultAddrPool') is not None:
            for k in m.get('DefaultAddrPool'):
                temp_model = UpdateDnsGtmAccessStrategyRequestDefaultAddrPool()
                self.default_addr_pool.append(temp_model.from_map(k))
        self.failover_addr_pool = []
        if m.get('FailoverAddrPool') is not None:
            for k in m.get('FailoverAddrPool'):
                temp_model = UpdateDnsGtmAccessStrategyRequestFailoverAddrPool()
                self.failover_addr_pool.append(temp_model.from_map(k))
        return self


class UpdateDnsGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        strategy_id: str = None,
    ):
        self.request_id = request_id
        self.strategy_id = strategy_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        return self


class UpdateDnsGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsGtmAddressPoolRequestAddr(TeaModel):
    def __init__(
        self,
        attribute_info: str = None,
        remark: str = None,
        lba_weight: int = None,
        addr: str = None,
        mode: str = None,
    ):
        self.attribute_info = attribute_info
        self.remark = remark
        self.lba_weight = lba_weight
        self.addr = addr
        self.mode = mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.attribute_info is not None:
            result['AttributeInfo'] = self.attribute_info
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.addr is not None:
            result['Addr'] = self.addr
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AttributeInfo') is not None:
            self.attribute_info = m.get('AttributeInfo')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Addr') is not None:
            self.addr = m.get('Addr')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class UpdateDnsGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
        name: str = None,
        lba_strategy: str = None,
        addr: List[UpdateDnsGtmAddressPoolRequestAddr] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id
        self.name = name
        self.lba_strategy = lba_strategy
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.name is not None:
            result['Name'] = self.name
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = UpdateDnsGtmAddressPoolRequestAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class UpdateDnsGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDnsGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsGtmInstanceGlobalConfigRequestAlertConfig(TeaModel):
    def __init__(
        self,
        sms_notice: bool = None,
        notice_type: str = None,
        email_notice: bool = None,
    ):
        self.sms_notice = sms_notice
        self.notice_type = notice_type
        self.email_notice = email_notice

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.sms_notice is not None:
            result['SmsNotice'] = self.sms_notice
        if self.notice_type is not None:
            result['NoticeType'] = self.notice_type
        if self.email_notice is not None:
            result['EmailNotice'] = self.email_notice
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SmsNotice') is not None:
            self.sms_notice = m.get('SmsNotice')
        if m.get('NoticeType') is not None:
            self.notice_type = m.get('NoticeType')
        if m.get('EmailNotice') is not None:
            self.email_notice = m.get('EmailNotice')
        return self


class UpdateDnsGtmInstanceGlobalConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        instance_name: str = None,
        ttl: int = None,
        public_cname_mode: str = None,
        public_user_domain_name: str = None,
        public_zone_name: str = None,
        alert_group: str = None,
        cname_type: str = None,
        alert_config: List[UpdateDnsGtmInstanceGlobalConfigRequestAlertConfig] = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.ttl = ttl
        self.public_cname_mode = public_cname_mode
        self.public_user_domain_name = public_user_domain_name
        self.public_zone_name = public_zone_name
        self.alert_group = alert_group
        self.cname_type = cname_type
        self.alert_config = alert_config

    def validate(self):
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.public_cname_mode is not None:
            result['PublicCnameMode'] = self.public_cname_mode
        if self.public_user_domain_name is not None:
            result['PublicUserDomainName'] = self.public_user_domain_name
        if self.public_zone_name is not None:
            result['PublicZoneName'] = self.public_zone_name
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.cname_type is not None:
            result['CnameType'] = self.cname_type
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('PublicCnameMode') is not None:
            self.public_cname_mode = m.get('PublicCnameMode')
        if m.get('PublicUserDomainName') is not None:
            self.public_user_domain_name = m.get('PublicUserDomainName')
        if m.get('PublicZoneName') is not None:
            self.public_zone_name = m.get('PublicZoneName')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('CnameType') is not None:
            self.cname_type = m.get('CnameType')
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = UpdateDnsGtmInstanceGlobalConfigRequestAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        return self


class UpdateDnsGtmInstanceGlobalConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDnsGtmInstanceGlobalConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsGtmInstanceGlobalConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsGtmInstanceGlobalConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDnsGtmMonitorRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class UpdateDnsGtmMonitorRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        isp_city_node: List[UpdateDnsGtmMonitorRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = UpdateDnsGtmMonitorRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class UpdateDnsGtmMonitorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDnsGtmMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDnsGtmMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDnsGtmMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDNSSLBWeightRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
        weight: int = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id
        self.weight = weight

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.weight is not None:
            result['Weight'] = self.weight
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        return self


class UpdateDNSSLBWeightResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        record_id: str = None,
        weight: int = None,
    ):
        self.request_id = request_id
        self.record_id = record_id
        self.weight = weight

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.weight is not None:
            result['Weight'] = self.weight
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        return self


class UpdateDNSSLBWeightResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDNSSLBWeightResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDNSSLBWeightResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDomainGroupRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        group_id: str = None,
        group_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.group_id = group_id
        self.group_name = group_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        return self


class UpdateDomainGroupResponseBody(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        request_id: str = None,
        group_id: str = None,
    ):
        self.group_name = group_name
        self.request_id = request_id
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class UpdateDomainGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDomainGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDomainGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDomainRecordRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
        rr: str = None,
        type: str = None,
        value: str = None,
        ttl: int = None,
        priority: int = None,
        line: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id
        self.rr = rr
        self.type = type
        self.value = value
        self.ttl = ttl
        self.priority = priority
        self.line = line

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.rr is not None:
            result['RR'] = self.rr
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.ttl is not None:
            result['TTL'] = self.ttl
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.line is not None:
            result['Line'] = self.line
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RR') is not None:
            self.rr = m.get('RR')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('TTL') is not None:
            self.ttl = m.get('TTL')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        return self


class UpdateDomainRecordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        record_id: str = None,
    ):
        self.request_id = request_id
        self.record_id = record_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        return self


class UpdateDomainRecordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDomainRecordResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDomainRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDomainRecordRemarkRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        record_id: str = None,
        remark: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.record_id = record_id
        self.remark = remark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class UpdateDomainRecordRemarkResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDomainRecordRemarkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDomainRecordRemarkResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDomainRecordRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateDomainRemarkRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        domain_name: str = None,
        remark: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.domain_name = domain_name
        self.remark = remark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.domain_name is not None:
            result['DomainName'] = self.domain_name
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('DomainName') is not None:
            self.domain_name = m.get('DomainName')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class UpdateDomainRemarkResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateDomainRemarkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateDomainRemarkResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateDomainRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateGtmAccessStrategyRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        strategy_id: str = None,
        strategy_name: str = None,
        default_addr_pool_id: str = None,
        failover_addr_pool_id: str = None,
        access_lines: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.strategy_id = strategy_id
        self.strategy_name = strategy_name
        self.default_addr_pool_id = default_addr_pool_id
        self.failover_addr_pool_id = failover_addr_pool_id
        self.access_lines = access_lines

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.strategy_id is not None:
            result['StrategyId'] = self.strategy_id
        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name
        if self.default_addr_pool_id is not None:
            result['DefaultAddrPoolId'] = self.default_addr_pool_id
        if self.failover_addr_pool_id is not None:
            result['FailoverAddrPoolId'] = self.failover_addr_pool_id
        if self.access_lines is not None:
            result['AccessLines'] = self.access_lines
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('StrategyId') is not None:
            self.strategy_id = m.get('StrategyId')
        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')
        if m.get('DefaultAddrPoolId') is not None:
            self.default_addr_pool_id = m.get('DefaultAddrPoolId')
        if m.get('FailoverAddrPoolId') is not None:
            self.failover_addr_pool_id = m.get('FailoverAddrPoolId')
        if m.get('AccessLines') is not None:
            self.access_lines = m.get('AccessLines')
        return self


class UpdateGtmAccessStrategyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateGtmAccessStrategyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateGtmAccessStrategyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateGtmAccessStrategyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateGtmAddressPoolRequestAddr(TeaModel):
    def __init__(
        self,
        value: str = None,
        lba_weight: int = None,
        mode: str = None,
    ):
        self.value = value
        self.lba_weight = lba_weight
        self.mode = mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.lba_weight is not None:
            result['LbaWeight'] = self.lba_weight
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('LbaWeight') is not None:
            self.lba_weight = m.get('LbaWeight')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class UpdateGtmAddressPoolRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        addr_pool_id: str = None,
        name: str = None,
        type: str = None,
        min_available_addr_num: int = None,
        addr: List[UpdateGtmAddressPoolRequestAddr] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.addr_pool_id = addr_pool_id
        self.name = name
        self.type = type
        self.min_available_addr_num = min_available_addr_num
        self.addr = addr

    def validate(self):
        if self.addr:
            for k in self.addr:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.addr_pool_id is not None:
            result['AddrPoolId'] = self.addr_pool_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.min_available_addr_num is not None:
            result['MinAvailableAddrNum'] = self.min_available_addr_num
        result['Addr'] = []
        if self.addr is not None:
            for k in self.addr:
                result['Addr'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('AddrPoolId') is not None:
            self.addr_pool_id = m.get('AddrPoolId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('MinAvailableAddrNum') is not None:
            self.min_available_addr_num = m.get('MinAvailableAddrNum')
        self.addr = []
        if m.get('Addr') is not None:
            for k in m.get('Addr'):
                temp_model = UpdateGtmAddressPoolRequestAddr()
                self.addr.append(temp_model.from_map(k))
        return self


class UpdateGtmAddressPoolResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateGtmAddressPoolResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateGtmAddressPoolResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateGtmAddressPoolResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateGtmInstanceGlobalConfigRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        instance_id: str = None,
        instance_name: str = None,
        ttl: int = None,
        user_domain_name: str = None,
        lba_strategy: str = None,
        alert_group: str = None,
        cname_mode: str = None,
        cname_custom_domain_name: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.ttl = ttl
        self.user_domain_name = user_domain_name
        self.lba_strategy = lba_strategy
        self.alert_group = alert_group
        self.cname_mode = cname_mode
        self.cname_custom_domain_name = cname_custom_domain_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.user_domain_name is not None:
            result['UserDomainName'] = self.user_domain_name
        if self.lba_strategy is not None:
            result['LbaStrategy'] = self.lba_strategy
        if self.alert_group is not None:
            result['AlertGroup'] = self.alert_group
        if self.cname_mode is not None:
            result['CnameMode'] = self.cname_mode
        if self.cname_custom_domain_name is not None:
            result['CnameCustomDomainName'] = self.cname_custom_domain_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('UserDomainName') is not None:
            self.user_domain_name = m.get('UserDomainName')
        if m.get('LbaStrategy') is not None:
            self.lba_strategy = m.get('LbaStrategy')
        if m.get('AlertGroup') is not None:
            self.alert_group = m.get('AlertGroup')
        if m.get('CnameMode') is not None:
            self.cname_mode = m.get('CnameMode')
        if m.get('CnameCustomDomainName') is not None:
            self.cname_custom_domain_name = m.get('CnameCustomDomainName')
        return self


class UpdateGtmInstanceGlobalConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateGtmInstanceGlobalConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateGtmInstanceGlobalConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateGtmInstanceGlobalConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateGtmMonitorRequestIspCityNode(TeaModel):
    def __init__(
        self,
        city_code: str = None,
        isp_code: str = None,
    ):
        self.city_code = city_code
        self.isp_code = isp_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_code is not None:
            result['CityCode'] = self.city_code
        if self.isp_code is not None:
            result['IspCode'] = self.isp_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityCode') is not None:
            self.city_code = m.get('CityCode')
        if m.get('IspCode') is not None:
            self.isp_code = m.get('IspCode')
        return self


class UpdateGtmMonitorRequest(TeaModel):
    def __init__(
        self,
        user_client_ip: str = None,
        lang: str = None,
        monitor_config_id: str = None,
        protocol_type: str = None,
        interval: int = None,
        evaluation_count: int = None,
        timeout: int = None,
        monitor_extend_info: str = None,
        isp_city_node: List[UpdateGtmMonitorRequestIspCityNode] = None,
    ):
        self.user_client_ip = user_client_ip
        self.lang = lang
        self.monitor_config_id = monitor_config_id
        self.protocol_type = protocol_type
        self.interval = interval
        self.evaluation_count = evaluation_count
        self.timeout = timeout
        self.monitor_extend_info = monitor_extend_info
        self.isp_city_node = isp_city_node

    def validate(self):
        if self.isp_city_node:
            for k in self.isp_city_node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.monitor_config_id is not None:
            result['MonitorConfigId'] = self.monitor_config_id
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.monitor_extend_info is not None:
            result['MonitorExtendInfo'] = self.monitor_extend_info
        result['IspCityNode'] = []
        if self.isp_city_node is not None:
            for k in self.isp_city_node:
                result['IspCityNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('MonitorConfigId') is not None:
            self.monitor_config_id = m.get('MonitorConfigId')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('MonitorExtendInfo') is not None:
            self.monitor_extend_info = m.get('MonitorExtendInfo')
        self.isp_city_node = []
        if m.get('IspCityNode') is not None:
            for k in m.get('IspCityNode'):
                temp_model = UpdateGtmMonitorRequestIspCityNode()
                self.isp_city_node.append(temp_model.from_map(k))
        return self


class UpdateGtmMonitorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateGtmMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateGtmMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateGtmMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateGtmRecoveryPlanRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        recovery_plan_id: int = None,
        name: str = None,
        remark: str = None,
        fault_addr_pool: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.recovery_plan_id = recovery_plan_id
        self.name = name
        self.remark = remark
        self.fault_addr_pool = fault_addr_pool

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.recovery_plan_id is not None:
            result['RecoveryPlanId'] = self.recovery_plan_id
        if self.name is not None:
            result['Name'] = self.name
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.fault_addr_pool is not None:
            result['FaultAddrPool'] = self.fault_addr_pool
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('RecoveryPlanId') is not None:
            self.recovery_plan_id = m.get('RecoveryPlanId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('FaultAddrPool') is not None:
            self.fault_addr_pool = m.get('FaultAddrPool')
        return self


class UpdateGtmRecoveryPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateGtmRecoveryPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateGtmRecoveryPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateGtmRecoveryPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ValidateDnsGtmAttributeInfoRequest(TeaModel):
    def __init__(
        self,
        lang: str = None,
        user_client_ip: str = None,
        line_code: str = None,
    ):
        self.lang = lang
        self.user_client_ip = user_client_ip
        self.line_code = line_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.line_code is not None:
            result['LineCode'] = self.line_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('LineCode') is not None:
            self.line_code = m.get('LineCode')
        return self


class ValidateDnsGtmAttributeInfoResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ValidateDnsGtmAttributeInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ValidateDnsGtmAttributeInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ValidateDnsGtmAttributeInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


